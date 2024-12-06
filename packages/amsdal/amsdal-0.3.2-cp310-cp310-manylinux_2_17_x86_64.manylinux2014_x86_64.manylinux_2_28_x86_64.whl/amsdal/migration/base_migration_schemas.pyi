import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from amsdal.configs.constants import BASE_DIR as BASE_DIR
from amsdal_models.classes.model import Model
from amsdal_utils.models.data_models.core import DictSchema, LegacyDictSchema, TypeData as TypeData
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema, PropertyData as PropertyData
from amsdal_utils.models.enums import SchemaTypes as SchemaTypes, Versions
from pathlib import Path

class BaseMigrationSchemas(ABC, metaclass=abc.ABCMeta):
    """
    Abstract base class for migration schemas.

    This class provides the interface for managing and compiling database schema migrations.
    It includes methods for registering, unregistering, and compiling classes, as well as
    managing class versions.
    """
    _classes: Incomplete
    _classes_versions: Incomplete
    _buffered_classes: Incomplete
    def __init__(self) -> None: ...
    def get_model(self, name: str) -> type[Model]:
        """
        Retrieves the model type for the given class name.

        Args:
            name (str): The name of the class whose model type is to be retrieved.

        Returns:
            type[Model]: The model type associated with the given class name.
        """
    @abstractmethod
    def register_model(self, class_name: str, object_schema: ObjectSchema, schema_type: SchemaTypes, class_version: str | Versions = ...) -> None: ...
    @abstractmethod
    def unregister_model(self, class_name: str) -> None: ...
    @abstractmethod
    def compile_buffered_classes(self) -> None: ...
    @staticmethod
    def register_model_version(class_name: str, class_version: str | Versions) -> None:
        """
        Registers a specific version of a model class.

        This method registers a specific version of a model class using the ClassVersionManager.

        Args:
            class_name (str): The name of the class to register the version for.
            class_version (str | Versions): The version of the class to be registered.

        Returns:
            None
        """

class DefaultMigrationSchemas(BaseMigrationSchemas):
    """
    Default implementation of the BaseMigrationSchemas.

    This class provides the default implementation for managing and compiling database schema migrations.
    It includes methods for registering, unregistering, and compiling classes, as well as managing class versions.

    Attributes:
        model_class_template_layout (Path): Path to the model class layout template.
        model_class_template (Path): Path to the model class template.
        dict_validator_template (Path): Path to the dictionary validator template.
        options_validator_template (Path): Path to the options validator template.
    """
    model_class_template_layout: Path
    model_class_template: Path
    dict_validator_template: Path
    options_validator_template: Path
    def register_model(self, class_name: str, object_schema: ObjectSchema, schema_type: SchemaTypes, class_version: str | Versions = ...) -> None:
        """
        Registers a model class for migration.

        This method registers a model class for migration by adding it to the buffered classes
        and registering its latest version.

        Args:
            class_name (str): The name of the class to be registered.
            object_schema (ObjectSchema): The schema of the object to be registered.
            schema_type (SchemaTypes): The type of the schema.

        Returns:
            None
        """
    def compile_buffered_classes(self) -> None:
        """
        Compiles all buffered classes for migration.

        This method compiles all classes that have been buffered for migration and updates the
        internal class dictionary with the compiled class types. It clears the buffer after
        compilation.

        Returns:
            None
        """
    def unregister_model(self, class_name: str) -> None:
        """
        Unregisters a model class from the migration schemas.

        This method removes the specified model class from the internal class dictionary,
        effectively unregistering it from the migration schemas.

        Args:
            class_name (str): The name of the class to be unregistered.

        Returns:
            None
        """
    def _compile_buffered_classes(self) -> list[tuple[str, type[Model]]]: ...
    def _build_class_source(self, class_name: str, schema: ObjectSchema, schema_type: SchemaTypes) -> tuple[str, str]: ...
    @staticmethod
    def _resolve_class_inheritance(schema: ObjectSchema) -> str: ...
    @staticmethod
    def _process_custom_code(custom_code: str | None) -> tuple[str, str]: ...
    def _render_property(self, name: str, property_schema: PropertyData, required: list[str]) -> str: ...
    def _render_type_annotation(self, type_: str, items: TypeData | DictSchema | LegacyDictSchema | None) -> str: ...
    def _render_validators(self, schema: ObjectSchema) -> list[str]: ...
    def _get_all_types(self, type_: str, items: TypeData | DictSchema | LegacyDictSchema | None) -> set[str]: ...
    def _is_reference(self, type_: str) -> bool: ...
