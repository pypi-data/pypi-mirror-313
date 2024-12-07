from _typeshed import Incomplete
from amsdal.configs.constants import CORE_SCHEMAS_PATH as CORE_SCHEMAS_PATH, TYPE_SCHEMAS_PATH as TYPE_SCHEMAS_PATH
from amsdal.configs.main import settings as settings
from amsdal_models.schemas.loaders.cli_fixtures_loader import CliFixturesLoader
from pathlib import Path

class CliMultiFixturesLoader(CliFixturesLoader):
    """
    Loads multiple fixtures from specified schema directories.

    Attributes:
        models_with_fixtures (list[tuple[Path, ObjectSchema]]): List of tuples containing the path and object schema
            of models with fixtures.
    """
    models_with_fixtures: Incomplete
    def __init__(self, schema_dirs: list[Path]) -> None: ...

class BuildMixin:
    """
    Provides methods to build models, transactions, static files, migrations, and fixtures for a CLI application.
    """
    @classmethod
    def build_models(cls, user_schemas_path: Path) -> None:
        """
        Builds models from the specified user schemas path and predefined schema directories.

        Args:
            user_schemas_path (Path): The path to the user schemas directory.

        Returns:
            None
        """
    @staticmethod
    def build_transactions(cli_app_path: Path) -> None:
        """
        Builds transactions from the specified CLI application path.

        Args:
            cli_app_path (Path): The path to the CLI application directory.

        Returns:
            None
        """
    @staticmethod
    def build_static_files(cli_app_path: Path) -> None:
        """
        Builds static files from the specified CLI application path.

        Args:
            cli_app_path (Path): The path to the CLI application directory.

        Returns:
            None
        """
    @staticmethod
    def build_migrations(cli_app_path: Path) -> None:
        """
        Builds migrations from the specified CLI application path.

        Args:
            cli_app_path (Path): The path to the CLI application directory.

        Returns:
            None
        """
    @staticmethod
    def build_fixtures(cli_app_path: Path) -> None:
        """
        Builds fixtures from the specified CLI application path.

        Args:
            cli_app_path (Path): The path to the CLI application directory.

        Returns:
            None
        """
    @staticmethod
    def _reimport_models() -> None: ...
