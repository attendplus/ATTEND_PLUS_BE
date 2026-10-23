
import asyncio
import importlib
import pkgutil
from pathlib import Path

from logging.config import fileConfig

from alembic import context
from alembic.autogenerate import rewriter
from alembic.operations import ops

# 1. 우리가 이미 안전하게 정돈해 둔 비동기 engine과 Base를 가져옵니다.
from module_core.common.config.database import engine, Base


MODEL_PACKAGES = (
    "module_core.common.entities",
    "module_core.entities",
    "module_core.domain.test.models",
)


def import_all_models() -> None:
    """모든 모델 모듈을 import하여 Base.metadata에 등록합니다."""

    imported_modules: set[str] = set()

    for package_name in MODEL_PACKAGES:
        try:
            package = importlib.import_module(package_name)
        except ModuleNotFoundError as exc:
            # 지정한 패키지 자체가 존재하지 않는 경우에만 건너뜁니다.
            # 패키지 내부 의존성 누락은 숨기지 않습니다.
            if exc.name == package_name:
                print(
                    f"[Alembic] Model package not found: {package_name}"
                )
                continue
            raise

        # 이미 import된 패키지 자체도 기록합니다.
        imported_modules.add(package.__name__)

        # 기존 pkgutil 탐색을 유지합니다.
        package_paths = getattr(package, "__path__", None)

        if package_paths:
            for module_info in pkgutil.walk_packages(
                package_paths,
                prefix=f"{package.__name__}.",
            ):
                if module_info.name in imported_modules:
                    continue

                importlib.import_module(module_info.name)
                imported_modules.add(module_info.name)

        # 네임스페이스 패키지 및 일반 패키지 아래의
        # 실제 Python 파일도 재귀적으로 확인합니다.
        package_paths = getattr(package, "__path__", None)

        if not package_paths:
            continue

        for package_path in package_paths:
            root = Path(package_path)

            if not root.is_dir():
                continue

            for file_path in sorted(root.rglob("*.py")):
                if file_path.name == "__init__.py":
                    relative_path = file_path.parent.relative_to(root)
                    module_parts = relative_path.parts
                else:
                    relative_path = file_path.relative_to(root)
                    module_parts = (
                        *relative_path.parent.parts,
                        relative_path.stem,
                    )

                if module_parts:
                    module_name = (
                        f"{package.__name__}."
                        + ".".join(module_parts)
                    )
                else:
                    module_name = package.__name__

                if module_name in imported_modules:
                    continue

                importlib.import_module(module_name)
                imported_modules.add(module_name)

    print("\n=== Imported entity modules ===")

    for module_name in sorted(imported_modules):
        print(module_name)

    print("\n=== Registered metadata tables ===")

    for table_name in sorted(Base.metadata.tables):
        print(table_name)

    print(f"=== Total tables: {len(Base.metadata.tables)} ===")

    if not Base.metadata.tables:
        raise RuntimeError(
            "No tables registered in Base.metadata. "
            "Check entity imports and Base inheritance."
        )


# 모델을 먼저 import해야 SQLAlchemy가 테이블을 등록할 수 있습니다.
import_all_models()


# [핵심 교정] Alembic 환경 설정을 조율하는 전역 config 객체
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

    # 컬럼을 추가할 때 기본값을 지정하지 않아
    # 기존 행의 값이 NULL로 유지되도록 합니다.
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

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=timestamp_rewriter,
    )

    with context.begin_transaction():
        context.run_migrations()


# 비동기 엔진 내에서 실제 DDL 쿼리를
# 동기식으로 안전하게 수행하기 위한 헬퍼 함수
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=timestamp_rewriter,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Online 모드로 마이그레이션을 수행합니다."""

    # 기존 프로젝트에 장착된 비동기 engine을 그대로 사용합니다.
    connectable = engine

    # async with 구문으로 비동기 커넥션을 확보합니다.
    async with connectable.connect() as connection:
        # run_sync를 사용해 Alembic의 동기 API를 실행합니다.
        await connection.run_sync(do_run_migrations)


# 오프라인 / 온라인 기동 분기 처리
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
