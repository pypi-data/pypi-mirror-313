import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from amsdal.configs.main import settings as settings
from amsdal.migration.data_classes import MigrationFile as MigrationFile, ModuleTypes as ModuleTypes
from amsdal.migration.utils import contrib_to_module_root_path as contrib_to_module_root_path, map_module_type_to_schema_type as map_module_type_to_schema_type
from amsdal_utils.models.data_models.address import Address
from typing import Any, ClassVar

class BaseMigrationStore(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def fetch_migrations(self) -> list[MigrationFile]: ...
    @abstractmethod
    def save_migration(self, migration: MigrationFile) -> None: ...
    @abstractmethod
    def delete_migration(self, migration: MigrationFile) -> None: ...

class FileMigrationStore(BaseMigrationStore):
    """
    Manages the storage and retrieval of migration files.

    Attributes:
        migration_address (Address): The address associated with the migration.
    """
    MIGRATION_TABLE: ClassVar[str]
    migration_address: Address
    _operation_manager: Incomplete
    def __init__(self) -> None: ...
    def fetch_migrations(self) -> list[MigrationFile]:
        """
        Fetches the list of applied migrations.

        Returns:
            list[MigrationFile]: List of applied migration files.
        """
    def save_migration(self, migration: MigrationFile) -> None:
        """
        Saves a migration file.

        Args:
            migration (MigrationFile): The migration file to save.

        Returns:
            None
        """
    def delete_migration(self, migration: MigrationFile) -> None:
        """
        Deletes a migration file.

        Args:
            migration (MigrationFile): The migration file to delete.

        Returns:
            None
        """
    def _save_historical_data(self, address: Address, data: dict[str, Any], metadata: dict[str, Any]) -> None: ...
    @staticmethod
    def _build_migration_data(migration: MigrationFile) -> dict[str, Any]: ...
    @classmethod
    def _build_migration_metadata(cls, migration: MigrationFile, object_id: str | None = None) -> tuple[Address, dict[str, Any]]: ...
    def _init_migration_table(self) -> None: ...
