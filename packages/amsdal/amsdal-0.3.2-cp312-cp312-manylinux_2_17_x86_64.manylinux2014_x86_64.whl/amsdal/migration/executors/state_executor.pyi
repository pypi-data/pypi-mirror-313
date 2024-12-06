from _typeshed import Incomplete
from amsdal.migration.base_migration_schemas import BaseMigrationSchemas as BaseMigrationSchemas
from amsdal.migration.executors.base import BaseMigrationExecutor as BaseMigrationExecutor
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema
from amsdal_utils.models.enums import SchemaTypes

class StateMigrationExecutor(BaseMigrationExecutor):
    """
    Executes state migrations for database schemas.

    This class handles the creation, updating, and deletion of classes in the database schema,
    as well as flushing buffered migration operations.

    Attributes:
        schemas (BaseMigrationSchemas): The migration schemas used for the operations.
        do_fetch_latest_version (bool): Flag indicating whether to fetch the latest version of the schema.
    """
    schemas: Incomplete
    do_fetch_latest_version: Incomplete
    def __init__(self, schemas: BaseMigrationSchemas, *, do_fetch_latest_version: bool = True) -> None: ...
    def create_class(self, schemas: BaseMigrationSchemas, class_name: str, object_schema: ObjectSchema, schema_type: SchemaTypes) -> None:
        """
        Creates a class in the database schema.

        This method registers a new class in the database schema or buffers the class migration
        operation based on the schema type and class name.

        Args:
            schemas (BaseMigrationSchemas): The migration schemas used for the operations.
            class_name (str): The name of the class to be created.
            object_schema (ObjectSchema): The current object schema.
            schema_type (SchemaTypes): The type of the schema.

        Returns:
            None
        """
    def update_class(self, schemas: BaseMigrationSchemas, class_name: str, object_schema: ObjectSchema, schema_type: SchemaTypes) -> None:
        """
        Buffers the class update operation.

        This method adds the class update operation to the migration buffer, which will be processed
        when the buffer is flushed.

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

        This method unregisters a class from the database schema based on the provided class name
        and schema type.

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

        This method registers all classes in the migration buffer to the database schema and compiles
        the buffered classes. If the `do_fetch_latest_version` flag is set, it also fetches and registers
        the latest version of each class.

        Returns:
            None
        """
