import asyncio
from logging.config import fileConfig

from alembic import context
from alembic.autogenerate import rewriter
from alembic.operations import ops

# 1. 우리가 이미 안전하게 정돈해 둔 비동기 engine과 Base를 가져옵니다.
from module_core.common.config.database import engine, Base
from module_core.domain.test.models.test import Test  # 마이그레이션 대상 모델 감지용

# [핵심 교정] Alembic 환경 설정을 조율하는 전역 config 객체는 반드시 아래와 같이 가져와야 합니다.
config = context.config

# alembic.ini 파일에 정의된 로깅 설정을 반영합니다.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic 타겟 스키마 명세서 지정
target_metadata = Base.metadata
timestamp_rewriter = rewriter.Rewriter()

@timestamp_rewriter.rewrites(ops.AddColumnOp)
def rewrite_timestamp_column(context, revision, operation):
    column = operation.column

    # 공통 타임스탬프 컬럼에만 적용
    if (
        column.name not in {"created_at", "updated_at"}
        or column.server_default is None
    ):
        return operation

    server_default = column.server_default

    # 기본값이 없는 컬럼을 먼저 추가해 기존 행을 NULL로 유지
    new_column = column._copy()
    new_column.server_default = None

    add_column = ops.AddColumnOp(
        operation.table_name,
        new_column,
        schema=operation.schema,
    )

    # 컬럼 추가 후 신규 INSERT를 위한 DB 기본값 설정
    alter_column = ops.AlterColumnOp(
        operation.table_name,
        column.name,
        schema=operation.schema,
        existing_type=column.type,
        existing_nullable=column.nullable,
        existing_server_default=None,
        modify_server_default=server_default,
    )

    return [add_column, alter_column]


def run_migrations_offline() -> None:
    """Offline 모드 설정"""
    # 이제 config 객체가 올바르게 살아있으므로 주소를 안전하게 추출합니다.
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# 비동기 엔진 내에서 실제 DDL 쿼리를 동기식으로 안전하게 수행하기 위한 헬퍼 함수
def do_run_migrations(connection):
    context.configure(
        connection=connection, 
        target_metadata=target_metadata, 
        process_revision_directives=timestamp_rewriter
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Online 모드로 마이그레이션을 수행합니다."""
    # 기존 프로젝트에 장착된 비동기 engine을 그대로 연결 통로로 지목합니다.
    connectable = engine

    # async with 구문을 통해 안전하게 비동기 커넥션을 확보합니다.
    async with connectable.connect() as connection:
        # 비동기 스레드 점유를 보장하기 위해 run_sync 메서드로 헬퍼 함수를 매핑합니다.
        await connection.run_sync(do_run_migrations)


# 오프라인 / 온라인 기동 분기 처리
if context.is_offline_mode():
    run_migrations_offline()
else:
    # asyncio 비동기 루프로 온라인 마이그레이션을 강제 점화합니다.
    asyncio.run(run_migrations_online())
