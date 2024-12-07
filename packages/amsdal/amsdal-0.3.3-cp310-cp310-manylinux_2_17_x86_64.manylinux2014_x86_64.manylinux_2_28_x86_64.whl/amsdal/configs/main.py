import importlib
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeAlias

from pydantic import field_validator
from pydantic import model_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class defines the configuration settings for the application, including paths,
    environment variables, and other settings.

    Attributes:
        model_config (SettingsConfigDict): Configuration for the settings model.
        APP_PATH (Path): Path to the app directory where the generated models and other files will be placed.
        CONFIG_PATH (Path | None): Path to the config.yml file. If not specified, the default APP_PATH/config.yml
            file will be used.
        MODELS_MODULE_NAME (str): The models module name. The generated models will be placed in this module.
        SCHEMAS_MODULE_NAME (str): The schemas module name. The schemas will be placed in this module.
        FIXTURES_MODULE_NAME (str): The fixtures module name. The fixtures will be placed in this module.
        STATIC_MODULE_NAME (str): The static module name. The static files will be placed in this module.
        TRANSACTIONS_MODULE_NAME (str): The transactions module name. The transactions will be placed in this module.
        MIGRATIONS_DIRECTORY_NAME (str): The migrations directory name. The migration files will be placed in this
            folder.
        ACCESS_KEY_ID (str | None): The access key that you will get during registering process.
        SECRET_ACCESS_KEY (str | None): The secret access key that you will get during registering process.
        ACCESS_TOKEN (str | None): The access token that you will get during sign in process.
        SANDBOX_ENVIRONMENT (bool | None): If True, the sandbox environment will be used. If False,
            the cloud environment will be used.
        CONTRIBS (list[str]): List of contrib modules that will be loaded and used.
            Can be specified via environment variable AMSDAL_CONTRIBS as comma separated string.
    """

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix='AMSDAL_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    APP_PATH: Path = Path('.')
    CONFIG_PATH: Path | None = None
    MODELS_MODULE_NAME: str = 'models'
    SCHEMAS_MODULE_NAME: str = 'schemas'
    FIXTURES_MODULE_NAME: str = 'fixtures'
    STATIC_MODULE_NAME: str = 'static'
    TRANSACTIONS_MODULE_NAME: str = 'transactions'
    MIGRATIONS_DIRECTORY_NAME: str = 'migrations'
    ACCESS_KEY_ID: str | None = None
    SECRET_ACCESS_KEY: str | None = None
    ACCESS_TOKEN: str | None = None
    SANDBOX_ENVIRONMENT: bool | None = None
    CONTRIBS: list[str] = [
        'amsdal.contrib.auth.app.AuthAppConfig',
        'amsdal.contrib.frontend_configs.app.FrontendConfigAppConfig',
    ]

    @field_validator('CONTRIBS', mode='after')
    def load_contrib_modules(cls, value: list[str]) -> list[str]:  # noqa: N805
        """
        Loads and initializes contrib modules.

        This method takes a list of contrib module paths, imports each module, and calls the `on_ready` method
        of the `AppConfig` class within each module.

        Args:
            value (list[str]): A list of contrib module paths in the format 'package.module.ClassName'.

        Returns:
            list[str]: The same list of contrib module paths after loading and initializing the modules.
        """
        from amsdal.contrib.app_config import AppConfig

        for contrib_module in value:
            package_name, class_name = contrib_module.rsplit('.', 1)
            _contrib_module = importlib.import_module(package_name)
            app_config_class: type[AppConfig] = getattr(_contrib_module, class_name)
            app_config_class().on_ready()

        return value

    @property
    def models_root_path(self) -> Path:
        """
        Returns the root path for models.

        This property constructs and returns the path to the models directory
        based on the `APP_PATH` and `MODELS_MODULE_NAME` attributes.

        Returns:
            Path: The root path for the models directory.
        """
        return self.APP_PATH / self.MODELS_MODULE_NAME

    @property
    def schemas_root_path(self) -> Path:
        """
        Returns the root path for schemas.

        This property constructs and returns the path to the schemas directory
        based on the `APP_PATH` and `SCHEMAS_MODULE_NAME` attributes.

        Returns:
            Path: The root path for the schemas directory.
        """
        return self.APP_PATH / self.SCHEMAS_MODULE_NAME

    @property
    def fixtures_root_path(self) -> Path:
        """
        Returns the root path for fixtures.

        This property constructs and returns the path to the fixtures directory
        based on the `APP_PATH` and `FIXTURES_MODULE_NAME` attributes.

        Returns:
            Path: The root path for the fixtures directory.
        """
        return self.APP_PATH / self.FIXTURES_MODULE_NAME

    @property
    def static_root_path(self) -> Path:
        """
        Returns the root path for static files.

        This property constructs and returns the path to the static files directory
        based on the `APP_PATH` and `STATIC_MODULE_NAME` attributes.

        Returns:
            Path: The root path for the static files directory.
        """
        return self.APP_PATH / self.STATIC_MODULE_NAME

    @property
    def transactions_root_path(self) -> Path:
        """
        Returns the root path for transactions.

        This property constructs and returns the path to the transactions directory
        based on the `models_root_path` and `TRANSACTIONS_MODULE_NAME` attributes.

        Returns:
            Path: The root path for the transactions directory.
        """
        return self.models_root_path / self.TRANSACTIONS_MODULE_NAME

    @property
    def migrations_root_path(self) -> Path:
        """
        Returns the root path for migrations.

        This property constructs and returns the path to the migrations directory
        based on the `models_root_path` and `MIGRATIONS_DIRECTORY_NAME` attributes.

        Returns:
            Path: The root path for the migrations directory.
        """
        return self.models_root_path / self.MIGRATIONS_DIRECTORY_NAME

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'Settings':
        """
        Ensures the configuration path is set.

        This method checks if the `CONFIG_PATH` attribute is set. If it is not set,
        it assigns a default path based on the `APP_PATH` attribute.

        Returns:
            Settings: The updated settings instance with the `CONFIG_PATH` attribute set.
        """
        config_path = self.CONFIG_PATH

        if not config_path:
            self.CONFIG_PATH = self.APP_PATH / 'config.yml'

        return self


if TYPE_CHECKING:
    base: TypeAlias = Settings
else:
    base: TypeAlias = object


class SettingsProxy(base):
    """
    Proxy class for accessing and modifying settings.

    This class acts as a proxy for the `Settings` class, allowing for dynamic
    overriding and accessing of settings attributes.
    """

    def __init__(self) -> None:
        self._settings = Settings()

    def override(self, **kwargs: Any) -> None:
        """
        Overrides settings with provided keyword arguments.

        This method updates the current settings with the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments representing settings to override.

        Returns:
            None
        """
        new_settings = self._settings.model_dump()
        new_settings.update(kwargs)
        self._settings = Settings(**new_settings)

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """
        Dumps the current settings model to a dictionary.

        This method returns the current settings as a dictionary.

        Args:
            *args: Additional positional arguments to pass to the underlying model dump method.
            **kwargs: Additional keyword arguments to pass to the underlying model dump method.

        Returns:
            dict[str, Any]: The current settings as a dictionary.
        """
        return self._settings.model_dump(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._settings, name)

    def __delattr__(self, name: str) -> None:
        try:
            getattr(self._settings, name)
            self._settings.__delattr__(name)
        except AttributeError:
            msg = f'Settings object has no attribute {name}'
            raise AttributeError(msg) from None

    def __setattr__(self, name: str, value: Any) -> None:
        if name == '_settings':
            super().__setattr__(name, value)
            return

        self._settings.__setattr__(name, value)


settings: SettingsProxy = SettingsProxy()
