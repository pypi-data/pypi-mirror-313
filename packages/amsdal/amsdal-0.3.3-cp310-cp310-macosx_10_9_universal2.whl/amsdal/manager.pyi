from _typeshed import Incomplete
from amsdal.cloud.services.actions.manager import CloudActionsManager as CloudActionsManager
from amsdal.cloud.services.auth.manager import AuthManager as AuthManager
from amsdal.cloud.services.auth.signup_service import SignupService as SignupService
from amsdal.configs.main import settings as settings
from amsdal.errors import AmsdalAuthenticationError as AmsdalAuthenticationError, AmsdalMissingCredentialsError as AmsdalMissingCredentialsError, AmsdalRuntimeError as AmsdalRuntimeError, AmsdalSignupError as AmsdalSignupError
from amsdal.fixtures.manager import AsyncFixturesManager as AsyncFixturesManager, FixturesManager as FixturesManager
from amsdal.mixins.build_mixin import BuildMixin as BuildMixin
from amsdal.mixins.class_versions_mixin import ClassVersionsMixin as ClassVersionsMixin
from amsdal.schemas.manager import SchemaManager as SchemaManager
from amsdal_models.classes.manager import ClassManager
from amsdal_utils.config.data_models.amsdal_config import AmsdalConfig as AmsdalConfig
from amsdal_utils.utils.singleton import Singleton
from pathlib import Path

class AmsdalManager(BuildMixin, ClassVersionsMixin, metaclass=Singleton):
    """
    Manages the AMSDAL framework components and operations.

    This class is responsible for initializing, setting up, and managing various components
    of the AMSDAL framework, including connections, data management, schema management,
    and authentication. It also provides methods for building and tearing down the framework.
    """
    _class_manager: ClassManager
    _config_manager: Incomplete
    _config: Incomplete
    _data_application: Incomplete
    _is_setup: bool
    __is_authenticated: bool
    _schema_manager: Incomplete
    _metadata_manager: Incomplete
    _auth_manager: Incomplete
    def __init__(self, *, raise_on_new_signup: bool = False) -> None:
        """
        Initializes all sub managers. Reads the configuration.

        Returns:
            None
        """
    @property
    def is_setup(self) -> bool: ...
    @property
    def is_authenticated(self) -> bool:
        """
        Indicates if the AMSDAL license authentication process has been passed.

        This property returns a boolean value indicating whether the AMSDAL license
        authentication process has been successfully completed.

        Returns:
            bool: True if authenticated, False otherwise.
        """
    def pre_setup(self) -> None:
        """
        Initiates models root path and adds it into sys.path.

        This method initializes the class manager and sets up the models root path
        as specified in the settings. It ensures that the models root path is added
        to the system path for proper module resolution.

        Returns:
            None
        """
    def setup(self) -> None:
        """
        Initiates models root path and the connections.

        This method sets up the AMSDAL framework by initializing the models root path and
        establishing connections. It ensures that the setup process is only performed once.

        Raises:
            AmsdalRuntimeError: If the AMSDAL manager is already set up.

        Returns:
            None
        """
    def post_setup(self) -> None:
        """
        Registers internal classes and prepares connections (creates internal tables).
        """
    def build(self, source_models_path: Path, source_transactions_path: Path, source_static_files_path: Path, source_fixtures_path: Path, source_migrations_path: Path) -> None:
        """
        Builds the necessary components for the Amsdal framework.

        This method is used to build the necessary components for the Amsdal framework.
        It takes five parameters which are all of type `Path`.
        These parameters represent the paths to the directories where the corresponding components are located.

        Args:
            source_models_path (Path): Path to the directory where the source models are located.
            source_transactions_path (Path): Path to the directory where the source transactions are located.
            source_static_files_path (Path): Path to the directory where the source static files are located.
            source_fixtures_path (Path): Path to the directory where the source fixtures are located.
            source_migrations_path (Path): Path to the directory where the source migrations are located.

        Returns:
            None

        The method performs the following build steps in order:
        - Builds the models from the `source_models_path` by calling the `build_models` method.
        - Builds the transactions from the `source_transactions_path` by calling the `build_transactions` method.
        - Builds the static files from the `source_static_files_path` by calling the `build_static_files` method.
        - Builds the fixtures from the `source_fixtures_path` by calling the `build_fixtures` method.

        Note:
            This method is part of the `AmsdalManager` class which includes mixins for `BuildMixin`
            and `ClassVersionsMixin`. It is intended to be used in the Amsdal framework for managing
            and building components.
        """
    def migrate(self) -> None:
        """
        DEPRECATED: Check changes in the models and apply them to the database.

        This method is deprecated and should not be used. It checks for changes in the models
        and applies them to the database. Use `amsdal.migration.file_migration_generator.FileMigrationGenerator`
            instead.

        Raises:
            DeprecationWarning: Always raised to indicate that this method is deprecated.

        Returns:
            None
        """
    def _check_auth(self) -> None: ...
    @property
    def cloud_actions_manager(self) -> CloudActionsManager:
        """
        Provides access to the CloudActionsManager.

        This property checks if the AMSDAL manager is authenticated and then returns
        an instance of the CloudActionsManager.

        Returns:
            CloudActionsManager: An instance of the CloudActionsManager.

        Raises:
            AmsdalAuthenticationError: If the AMSDAL manager is not authenticated.
        """
    def authenticate(self) -> None:
        """
        Run AMSDAL license authentication process.

        This method runs the AMSDAL license authentication process and sets the
        authentication status accordingly.

        Returns:
            None
        """
    def apply_fixtures(self) -> None:
        """
        Loads and applies fixtures defined in your application.

        This method loads the fixtures from the specified path and applies them to the
        AMSDAL framework. It uses the `FixturesManager` to manage the loading and application
        of the fixtures.

        Returns:
            None
        """
    def init_classes(self) -> None:
        """
        Initializes and imports classes based on the schema manager's class schemas.

        This method iterates over the class schemas provided by the schema manager and imports
        the classes into the class manager, excluding those of type `SchemaTypes.TYPE`.

        Returns:
            None
        """
    def teardown(self) -> None:
        """
        Clean up everything on the application exit.

        This method performs a cleanup of all components managed by the AMSDAL framework
        when the application exits. It disconnects and invalidates connections, clears caches,
        and resets the setup status.

        Raises:
            AmsdalRuntimeError: If the AMSDAL manager is not set up.

        Returns:
            None
        """

class AsyncAmsdalManager(BuildMixin, ClassVersionsMixin, metaclass=Singleton):
    """
    Manages the AMSDAL framework components and operations.

    This class is responsible for initializing, setting up, and managing various components
    of the AMSDAL framework, including connections, data management, schema management,
    and authentication. It also provides methods for building and tearing down the framework.
    """
    _class_manager: ClassManager
    _config_manager: Incomplete
    _config: Incomplete
    _data_application: Incomplete
    _is_setup: bool
    __is_authenticated: bool
    _schema_manager: Incomplete
    _metadata_manager: Incomplete
    _auth_manager: Incomplete
    def __init__(self, *, raise_on_new_signup: bool = False) -> None:
        """
        Initializes all sub managers. Reads the configuration.

        Returns:
            None
        """
    @property
    def is_setup(self) -> bool: ...
    @property
    def is_authenticated(self) -> bool:
        """
        Indicates if the AMSDAL license authentication process has been passed.

        This property returns a boolean value indicating whether the AMSDAL license
        authentication process has been successfully completed.

        Returns:
            bool: True if authenticated, False otherwise.
        """
    def pre_setup(self) -> None:
        """
        Initiates models root path and adds it into sys.path.

        This method initializes the class manager and sets up the models root path
        as specified in the settings. It ensures that the models root path is added
        to the system path for proper module resolution.

        Returns:
            None
        """
    async def setup(self) -> None:
        """
        Initiates models root path and the connections.

        This method sets up the AMSDAL framework by initializing the models root path and
        establishing connections. It ensures that the setup process is only performed once.

        Raises:
            AmsdalRuntimeError: If the AMSDAL manager is already set up.

        Returns:
            None
        """
    async def post_setup(self) -> None:
        """
        Registers internal classes and prepares connections (creates internal tables).
        """
    def build(self, source_models_path: Path, source_transactions_path: Path, source_static_files_path: Path, source_fixtures_path: Path, source_migrations_path: Path) -> None:
        """
        Builds the necessary components for the Amsdal framework.

        This method is used to build the necessary components for the Amsdal framework.
        It takes five parameters which are all of type `Path`.
        These parameters represent the paths to the directories where the corresponding components are located.

        Args:
            source_models_path (Path): Path to the directory where the source models are located.
            source_transactions_path (Path): Path to the directory where the source transactions are located.
            source_static_files_path (Path): Path to the directory where the source static files are located.
            source_fixtures_path (Path): Path to the directory where the source fixtures are located.
            source_migrations_path (Path): Path to the directory where the source migrations are located.

        Returns:
            None

        The method performs the following build steps in order:
        - Builds the models from the `source_models_path` by calling the `build_models` method.
        - Builds the transactions from the `source_transactions_path` by calling the `build_transactions` method.
        - Builds the static files from the `source_static_files_path` by calling the `build_static_files` method.
        - Builds the fixtures from the `source_fixtures_path` by calling the `build_fixtures` method.

        Note:
            This method is part of the `AmsdalManager` class which includes mixins for `BuildMixin`
            and `ClassVersionsMixin`. It is intended to be used in the Amsdal framework for managing
            and building components.
        """
    def migrate(self) -> None:
        """
        DEPRECATED: Check changes in the models and apply them to the database.

        This method is deprecated and should not be used. It checks for changes in the models
        and applies them to the database. Use `amsdal.migration.file_migration_generator.FileMigrationGenerator`
            instead.

        Raises:
            DeprecationWarning: Always raised to indicate that this method is deprecated.

        Returns:
            None
        """
    def _check_auth(self) -> None: ...
    @property
    def cloud_actions_manager(self) -> CloudActionsManager:
        """
        Provides access to the CloudActionsManager.

        This property checks if the AMSDAL manager is authenticated and then returns
        an instance of the CloudActionsManager.

        Returns:
            CloudActionsManager: An instance of the CloudActionsManager.

        Raises:
            AmsdalAuthenticationError: If the AMSDAL manager is not authenticated.
        """
    def authenticate(self) -> None:
        """
        Run AMSDAL license authentication process.

        This method runs the AMSDAL license authentication process and sets the
        authentication status accordingly.

        Returns:
            None
        """
    async def apply_fixtures(self) -> None:
        """
        Loads and applies fixtures defined in your application.

        This method loads the fixtures from the specified path and applies them to the
        AMSDAL framework. It uses the `FixturesManager` to manage the loading and application
        of the fixtures.

        Returns:
            None
        """
    def init_classes(self) -> None:
        """
        Initializes and imports classes based on the schema manager's class schemas.

        This method iterates over the class schemas provided by the schema manager and imports
        the classes into the class manager, excluding those of type `SchemaTypes.TYPE`.

        Returns:
            None
        """
    async def teardown(self) -> None:
        """
        Clean up everything on the application exit.

        This method performs a cleanup of all components managed by the AMSDAL framework
        when the application exits. It disconnects and invalidates connections, clears caches,
        and resets the setup status.

        Raises:
            AmsdalRuntimeError: If the AMSDAL manager is not set up.

        Returns:
            None
        """
