import amsdal_glue as glue
from _typeshed import Incomplete
from amsdal.errors import MigrationsError as MigrationsError
from amsdal.migration.base_migration_schemas import BaseMigrationSchemas as BaseMigrationSchemas
from amsdal.migration.data_classes import Action as Action
from amsdal.migration.executors.base import AsyncBaseMigrationExecutor as AsyncBaseMigrationExecutor, BaseMigrationExecutor as BaseMigrationExecutor
from amsdal_models.classes.model import Model
from amsdal_utils.models.data_models.schema import ObjectSchema
from amsdal_utils.models.enums import SchemaTypes, Versions
from typing import Any

class DefaultMigrationExecutor(BaseMigrationExecutor):
    """
    Default implementation of the BaseMigrationExecutor for handling database schema migrations.

    This class provides concrete implementations for creating, updating, and deleting classes
    in the database schema. It also manages schema migration buffers and processes object schemas.
    """
    schemas: Incomplete
    _table_schemas_manager: Incomplete
    def __init__(self, schemas: BaseMigrationSchemas) -> None: ...
    def create_class(self, schemas: BaseMigrationSchemas, class_name: str, object_schema: ObjectSchema, schema_type: SchemaTypes) -> None:
        """
        Creates a class in the database schema.

        This method registers a new class version if the schema type is `TYPE` and the class name
            is not `BaseClasses.OBJECT`.
        Otherwise, it buffers the class migration operation for further processing.

        Args:
            schemas (BaseMigrationSchemas): The migration schemas used for the operations.
            class_name (str): The name of the class to be created.
            object_schema (ObjectSchema): The schema of the object to be created.
            schema_type (SchemaTypes): The type of the schema.

        Returns:
            None
        """
    def update_class(self, schemas: BaseMigrationSchemas, class_name: str, object_schema: ObjectSchema, schema_type: SchemaTypes) -> None:
        """
        Buffers the class update operation.

        This method appends the given class name, object schema, and schema type to both
        the non-flushable buffer and the main buffer for further processing.

        Args:
            schemas (BaseMigrationSchemas): The migration schemas used for the operations.
            class_name (str): The name of the class to be updated.
            object_schema (ObjectSchema): The current object schema.
            schema_type (SchemaTypes): The type of the schema.

        Returns:
            None
        """
    def delete_class(self, schemas: BaseMigrationSchemas, class_name: str, schema_type: SchemaTypes) -> None:
        """
        Deletes a class from the database schema.

        This method removes the specified class from the database schema and unregisters it from the migration schemas.

        Args:
            schemas (BaseMigrationSchemas): The migration schemas used for the operations.
            class_name (str): The name of the class to be deleted.
            schema_type (SchemaTypes): The type of the schema.

        Returns:
            None
        """
    def flush_buffer(self) -> None:
        """
        Flushes the migration buffer and processes the buffered classes.

        This method registers the buffered classes in the migration schemas, compiles the buffered classes,
        and processes each class in the buffer to create tables, save class objects, and migrate historical data.
        Finally, it clears the main migration buffer.

        Returns:
            None
        """
    def _check_class(self, schema_reference: glue.SchemaReference, object_schema: ObjectSchema, base_class: type[Model]) -> Action: ...
    def _save_class(self, schema_reference: glue.SchemaReference, base_class: type[Model], object_schema: ObjectSchema, action: Action) -> dict[str, Any]: ...
    def _save_object_class_meta(self, base_class: type[Model], object_schema: ObjectSchema, schema_type: str) -> None: ...
    def _create_table(self, object_schema: ObjectSchema, class_version: str | Versions, using: str | None = None) -> None: ...
    def _migrate_historical_data(self, schemas: BaseMigrationSchemas, class_name: str, prior_version: str, new_version: str) -> None: ...
    def _clean_data(self, model_class: type[Model], data: dict[str, Any]) -> dict[str, Any]: ...
    def _process_object_schema(self, object_schema: ObjectSchema, class_name: str, buffer: list[tuple[str, ObjectSchema, SchemaTypes]]) -> ObjectSchema: ...
    def register_schemas(self) -> None:
        """
        Registers the schemas in the table schemas manager.

        This method retrieves the object schemas from the database, processes them, and registers
        them in the table schemas manager. It handles both `ClassObject` and `ClassObjectMeta` schemas,
        and ensures that all necessary references are loaded and processed.

        Returns:
            None
        """

class DefaultAsyncMigrationExecutor(AsyncBaseMigrationExecutor):
    """
    Default implementation of the BaseMigrationExecutor for handling database schema migrations.

    This class provides concrete implementations for creating, updating, and deleting classes
    in the database schema. It also manages schema migration buffers and processes object schemas.
    """
    schemas: Incomplete
    _table_schemas_manager: Incomplete
    def __init__(self, schemas: BaseMigrationSchemas) -> None: ...
    def create_class(self, schemas: BaseMigrationSchemas, class_name: str, object_schema: ObjectSchema, schema_type: SchemaTypes) -> None:
        """
        Creates a class in the database schema.

        This method registers a new class version if the schema type is `TYPE` and the class name
            is not `BaseClasses.OBJECT`.
        Otherwise, it buffers the class migration operation for further processing.

        Args:
            schemas (BaseMigrationSchemas): The migration schemas used for the operations.
            class_name (str): The name of the class to be created.
            object_schema (ObjectSchema): The schema of the object to be created.
            schema_type (SchemaTypes): The type of the schema.

        Returns:
            None
        """
    def update_class(self, schemas: BaseMigrationSchemas, class_name: str, object_schema: ObjectSchema, schema_type: SchemaTypes) -> None:
        """
        Buffers the class update operation.

        This method appends the given class name, object schema, and schema type to both
        the non-flushable buffer and the main buffer for further processing.

        Args:
            schemas (BaseMigrationSchemas): The migration schemas used for the operations.
            class_name (str): The name of the class to be updated.
            object_schema (ObjectSchema): The current object schema.
            schema_type (SchemaTypes): The type of the schema.

        Returns:
            None
        """
    async def delete_class(self, schemas: BaseMigrationSchemas, class_name: str, schema_type: SchemaTypes) -> None:
        """
        Deletes a class from the database schema.

        This method removes the specified class from the database schema and unregisters it from the migration schemas.

        Args:
            schemas (BaseMigrationSchemas): The migration schemas used for the operations.
            class_name (str): The name of the class to be deleted.
            schema_type (SchemaTypes): The type of the schema.

        Returns:
            None
        """
    async def flush_buffer(self) -> None:
        """
        Flushes the migration buffer and processes the buffered classes.

        This method registers the buffered classes in the migration schemas, compiles the buffered classes,
        and processes each class in the buffer to create tables, save class objects, and migrate historical data.
        Finally, it clears the main migration buffer.

        Returns:
            None
        """
    async def _check_class(self, schema_reference: glue.SchemaReference, object_schema: ObjectSchema, base_class: type[Model]) -> Action: ...
    async def _save_class(self, schema_reference: glue.SchemaReference, base_class: type[Model], object_schema: ObjectSchema, action: Action) -> dict[str, Any]: ...
    async def _save_object_class_meta(self, base_class: type[Model], object_schema: ObjectSchema, schema_type: SchemaTypes) -> None: ...
    async def _create_table(self, object_schema: ObjectSchema, class_version: str | Versions, using: str | None = None) -> None: ...
    async def _migrate_historical_data(self, schemas: BaseMigrationSchemas, class_name: str, prior_version: str, new_version: str) -> None: ...
    def _clean_data(self, model_class: type[Model], data: dict[str, Any]) -> dict[str, Any]: ...
    def _process_object_schema(self, object_schema: ObjectSchema, class_name: str, buffer: list[tuple[str, ObjectSchema, SchemaTypes]]) -> ObjectSchema: ...
    async def register_schemas(self) -> None:
        """
        Registers the schemas in the table schemas manager.

        This method retrieves the object schemas from the database, processes them, and registers
        them in the table schemas manager. It handles both `ClassObject` and `ClassObjectMeta` schemas,
        and ensures that all necessary references are loaded and processed.

        Returns:
            None
        """
