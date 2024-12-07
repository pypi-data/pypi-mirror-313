import os
import random
import string
import tempfile
from collections.abc import Generator
from collections.abc import Iterator
from contextlib import contextmanager
from contextlib import suppress
from pathlib import Path
from typing import Any

import yaml
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.enums import SchemaTypes

from amsdal.configs.constants import CORE_MIGRATIONS_PATH
from amsdal.configs.main import settings
from amsdal.manager import AmsdalManager
from amsdal.migration import migrations
from amsdal.migration.data_classes import ModuleTypes
from amsdal.migration.executors.default_executor import DefaultMigrationExecutor
from amsdal.migration.file_migration_executor import FileMigrationExecutorManager
from amsdal.migration.file_migration_generator import FileMigrationGenerator
from amsdal.migration.file_migration_writer import FileMigrationWriter
from amsdal.migration.migrations import MigrateData
from amsdal.migration.migrations import MigrationSchemas
from amsdal.migration.migrations_loader import MigrationsLoader
from amsdal.migration.schemas_loaders import JsonClassSchemaLoader
from amsdal.migration.utils import contrib_to_module_root_path
from amsdal.utils.tests.enums import DbExecutionType
from amsdal.utils.tests.enums import LakehouseOption
from amsdal.utils.tests.enums import StateOption

TESTS_DIR = Path(os.getcwd())


def create_postgres_database(database: str) -> tuple[str, str, str, str]:
    import psycopg

    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASSWORD', 'example')

    conn = psycopg.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        autocommit=True,
    )
    cur = conn.cursor()

    with suppress(psycopg.errors.DuplicateDatabase):
        cur.execute(f'CREATE DATABASE "{database}"')

    cur.close()
    conn.close()

    return (
        db_host,
        db_port,
        db_user,
        db_password,
    )


@contextmanager
def override_settings(**kwargs: Any) -> Iterator[None]:
    """
    A context manager that temporarily overrides settings.

    This is a copy of django.test.utils.override_settings, but with the
    ability to override settings with None.
    """
    from amsdal.configs.main import settings

    original_settings = settings.model_dump()

    settings.override(**kwargs)

    try:
        yield
    finally:
        settings.override(**original_settings)


def _get_config_template(
    db_execution_type: DbExecutionType,
    lakehouse_option: LakehouseOption,
    state_option: StateOption,
) -> str:
    config_object: dict[str, Any] = {
        'application_name': 'test_client_app',
        'connections': [
            {'name': 'lock', 'backend': 'amsdal_data.lock.implementations.thread_lock.ThreadLock'},
        ],
        'resources_config': {'lakehouse': 'lakehouse', 'lock': 'lock', 'repository': {'default': 'state'}},
    }
    if lakehouse_option in [LakehouseOption.postgres, LakehouseOption.postgres_immutable]:
        config_object['connections'].append(
            {
                'name': 'lakehouse',
                'backend': 'postgres-historical',
                'credentials': [
                    {
                        'db_host': '{{ db_host }}',
                        'db_port': '{{ db_port }}',
                        'db_user': '{{ db_user }}',
                        'db_password': '{{ db_password }}',
                        'db_name': '{{ lakehouse_postgres_db }}',
                    }
                ],
            }
        )
    elif lakehouse_option in [LakehouseOption.sqlite, LakehouseOption.sqlite_immutable]:
        config_object['connections'].append(
            {
                'name': 'lakehouse',
                'backend': 'sqlite-historical',
                'credentials': [{'db_path': '{{ db_dir }}/sqlite_lakehouse.sqlite3'}],
            }
        )

    if db_execution_type == DbExecutionType.lakehouse_only:
        config_object['resources_config']['repository']['default'] = 'lakehouse'

        return yaml.dump(config_object)

    if state_option == StateOption.postgres:
        config_object['connections'].append(
            {
                'name': 'state',
                'backend': 'postgres',
                'credentials': [
                    {
                        'db_host': '{{ db_host }}',
                        'db_port': '{{ db_port }}',
                        'db_user': '{{ db_user }}',
                        'db_password': '{{ db_password }}',
                        'db_name': '{{ state_postgres_db }}',
                    }
                ],
            }
        )

    elif state_option == StateOption.sqlite:
        config_object['connections'].append(
            {
                'name': 'state',
                'backend': 'sqlite',
                'credentials': [{'db_path': '{{ db_dir }}/sqlite_state.sqlite3'}],
            }
        )

    return yaml.dump(config_object)


@contextmanager
def init_manager(
    db_execution_type: DbExecutionType,
    lakehouse_option: LakehouseOption,
    state_option: StateOption,
) -> Generator[AmsdalManager, Any, None]:
    Path('.tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir='.tmp') as temp_dir:
        db_dir = Path(temp_dir) / 'db_dir'
        (db_dir / 'warehouse').mkdir(exist_ok=True, parents=True)

        lakehouse_database = ''.join(random.sample(string.ascii_letters, 16))
        state_database = ''.join(random.sample(string.ascii_letters, 16))
        config_text = _get_config_template(db_execution_type, lakehouse_option, state_option)

        if lakehouse_option in [LakehouseOption.postgres, LakehouseOption.postgres_immutable]:
            (
                db_host,
                db_port,
                db_user,
                db_password,
            ) = create_postgres_database(lakehouse_database)

            config_text = (
                config_text.replace('{{ db_host }}', db_host)
                .replace('{{ db_port }}', db_port)
                .replace('{{ db_user }}', db_user)
                .replace('{{ db_password }}', db_password)
                .replace('{{ lakehouse_postgres_db }}', lakehouse_database)
            )
        elif lakehouse_option in [LakehouseOption.sqlite, LakehouseOption.sqlite_immutable]:
            config_text = config_text.replace('{{ db_dir }}', db_dir.absolute().as_posix())

        if state_option == StateOption.postgres:
            create_postgres_database(state_database)
            config_text = (
                config_text.replace('{{ db_host }}', db_host)
                .replace('{{ db_port }}', db_port)
                .replace('{{ db_user }}', db_user)
                .replace('{{ db_password }}', db_password)
                .replace('{{ state_postgres_db }}', state_database)
            )
        elif state_option == StateOption.sqlite:
            config_text = config_text.replace('{{ db_dir }}', db_dir.absolute().as_posix())

        config_path = Path(temp_dir) / 'config.yml'
        config_path.write_text(config_text)

        with override_settings(APP_PATH=db_dir, CONFIG_PATH=config_path):
            config_manager = AmsdalConfigManager()
            config_manager.load_config(config_path)
            manager = AmsdalManager()
            manager.setup()
            manager.post_setup()  # type: ignore[call-arg]

            try:
                yield manager
            finally:
                manager.teardown()
                AmsdalManager.invalidate()
                AmsdalConfigManager.invalidate()


def _migrate_per_loader(executor: DefaultMigrationExecutor, loader: MigrationsLoader) -> None:
    for _migration in loader:
        migration_class = FileMigrationExecutorManager.get_migration_class(_migration)
        migration_class_instance = migration_class()

        for _operation in migration_class_instance.operations:
            if isinstance(_operation, MigrateData):
                executor.flush_buffer()

            _operation.forward(executor)

        executor.flush_buffer()


def migrate(app_schemas_path: Path) -> None:
    schemas = MigrationSchemas()
    executor = DefaultMigrationExecutor(schemas)
    _migrate_per_loader(
        executor,
        MigrationsLoader(
            migrations_dir=CORE_MIGRATIONS_PATH,
            module_type=ModuleTypes.CORE,
        ),
    )

    for contrib in settings.CONTRIBS:
        contrib_root_path = contrib_to_module_root_path(contrib)
        _migrate_per_loader(
            executor,
            MigrationsLoader(
                migrations_dir=contrib_root_path / settings.MIGRATIONS_DIRECTORY_NAME,
                module_type=ModuleTypes.CONTRIB,
                module_name=contrib,
            ),
        )

    schema_loader = JsonClassSchemaLoader(app_schemas_path)

    for class_schema in schema_loader.iter_app_schemas():
        for _operation_data in FileMigrationGenerator.build_operations(
            SchemaTypes.USER,
            class_schema.object_schema,
            None,
        ):
            _operation_name = FileMigrationWriter.operation_name_map[_operation_data.type]
            kwargs = {}

            if _operation_data.old_schema:
                kwargs['old_schema'] = _operation_data.old_schema.model_dump()

            if _operation_data.new_schema:
                kwargs['new_schema'] = _operation_data.new_schema.model_dump()

            _operation = getattr(migrations, _operation_name)(
                schema_type=SchemaTypes.USER,
                class_name=_operation_data.class_name,
                **kwargs,
            )

            _operation.forward(executor)

    executor.flush_buffer()


@contextmanager
def init_manager_and_migrate(
    db_execution_type: DbExecutionType,
    lakehouse_option: LakehouseOption,
    state_option: StateOption,
) -> Generator[AmsdalManager, Any, None]:
    with init_manager(
        db_execution_type=db_execution_type,
        lakehouse_option=lakehouse_option,
        state_option=state_option,
    ) as manager:
        app_schemas_path = TESTS_DIR / 'src' / 'models'
        manager.build(
            source_models_path=app_schemas_path,
            source_fixtures_path=app_schemas_path,
            source_transactions_path=app_schemas_path,
            source_static_files_path=app_schemas_path,
            source_migrations_path=app_schemas_path,
        )
        manager.authenticate()
        migrate(app_schemas_path)
        manager.init_classes()

        yield manager
