# Database Config
import os
import time
import logging
import click

from zoneinfo import ZoneInfo
from datetime import datetime
from typing import Any, Final, TypeVar, Generic, Type, Dict
from functools import wraps
from pathlib import Path
from contextvars import ContextVar, Token

from sqlalchemy import DateTime, event, func
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.future import select

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

# 현재 환경 변수 감지 (없으면 local -> .env.local 로드)
PROFILE: Final[str] = os.getenv("PROFILE", "local")
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
ENV_FILE_PATH: Path = PROJECT_ROOT / f".env.{PROFILE}"


class Settings(BaseSettings):
    db_username: str | None = os.getenv("DB_USERNAME")
    db_password: str | None = os.getenv("DB_PASSWORD")
    db_host: str | None = os.getenv("DB_HOST")
    db_port: str | None = os.getenv("DB_PORT")
    db_name: str | None = os.getenv("DB_NAME")

    model_config = SettingsConfigDict(
        env_file = ENV_FILE_PATH,
        env_file_encoding = "utf-8",
        extra = "ignore",
        case_sensitive = False
    )

settings: Settings = Settings()

DB_URL: str = f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine: AsyncEngine = create_async_engine(DB_URL)
AsyncSessionLocal: Any = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base: Any = declarative_base()

# 컨텍스트
PersistenceContext: ContextVar[AsyncSession] = ContextVar("persistence_context")
QueryLogContext: ContextVar[Dict[str, Any]] = ContextVar("query_log_context", default={})

# 현재 비동기 세션 가져오기
def current_async_session() -> AsyncSession:
    try:
        logger.debug("Retrieving active database session from context.")
        return PersistenceContext.get()
    except LookupError:
        raise RuntimeError("Failed to locate database session in current async context.")

# @transactional 데코레이터
def transactional(read_only: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with AsyncSessionLocal() as session:
                token: Token[AsyncSession] = PersistenceContext.set(session)

                ctx: Dict[str, Any] = QueryLogContext.get().copy()
                ctx["service"] = func.__name__
                QueryLogContext.set(ctx)
                
                try:
                    if read_only:
                        logger.debug("Initiating read-only service data retrieval.")
                        return await func(*args, **kwargs)
                    
                    logger.debug("Beginning write-transaction block.")
                    result = await func(*args, **kwargs)
                    
                    await session.flush()
                    await session.commit()

                    logger.debug("Transaction committed successfully.")

                    return result
                except Exception as e:
                    if not read_only:
                        await session.rollback()
                        logger.error(f"Transaction aborted due to error. Rolling back changes. Error: {e}")

                    raise e
                finally:
                    PersistenceContext.reset(token)
                    logger.debug("Persistence context cleared and session closed.")
                    
        return wrapper
    return decorator

# 쿼리 로그 출력 함수
def dynamic_query_logger(conn, cursor, statement, parameters, context, executemany):
    try:
        kst_time: str = datetime.fromtimestamp(time.time(), tz=ZoneInfo("Asia/Seoul")).strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            ctx: Dict[str, Any] = QueryLogContext.get()
        except Exception:
            ctx: Dict[str, Any] = {}

        ctx_id: str = ctx.get("ctx_id", "UNKNOWN_ID")
        ip: str = ctx.get("ip", "UNKNOWN_IP")
        service: str = ctx.get("service", "UNKNOWN_SERVICE")
        router: str = ctx.get("router", "UNKNOWN_ROUTER")
        
        logger.info(f"[{click.style(kst_time, fg='bright_green')}] [{click.style(ctx_id, fg='bright_green')}] [{click.style(ip, fg='bright_green')}] [{click.style(service, fg='bright_green')}] [{click.style(router, fg='bright_green')}] {click.style(statement, fg='black')}")
    except Exception as e:
        logger.error(f"Logging Error: {e}")
        logger.info(f"Backup SQL: {statement}")

# @event.listens_for 대신 동적 컨텍스트 전파를 위해 엔진에 직접 주입합니다.
# before와 after 둘 다 걸어두면 중복될 수 있으므로, 실제 드라이버가 실행을 마친 'after' 시점에만 확실하게 가로챕니다.
event.listen(engine.sync_engine, "after_cursor_execute", dynamic_query_logger)


T = TypeVar('T')

# *
# BaseRepository는 Spring Boot의 JpaRepository 인터페이스 형식을 그대로 따라갑니다.
# *
class BaseRepository(Generic[T]):
    def __init__(self, entity: Type[T]):
        self.entity = entity

    @property
    def em(self) -> AsyncSession:
        return current_async_session()

    async def save(self, entity: T) -> T:
        if hasattr(entity, 'id') and getattr(entity, 'id') is not None:
            entity = await self.em.merge(entity)
        else:
            self.em.add(entity)

        return entity

    async def find_by_id(self, id: int) -> T | None:
        query = select(self.entity).where(self.entity.id == id)
        result = await self.em.execute(query)

        return result.scalar_one_or_none()

    async def find_all(self) -> list[T]:
        query = select(self.entity)
        result = await self.em.execute(query)

        return list(result.scalars().all())

    async def delete(self, entity: T) -> None:
        await self.em.delete(entity)


class BaseTimeEntity:
    # 생성일시
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
        comment="생성일"
    )

    # 수정일시
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
        comment="수정일"
    )

