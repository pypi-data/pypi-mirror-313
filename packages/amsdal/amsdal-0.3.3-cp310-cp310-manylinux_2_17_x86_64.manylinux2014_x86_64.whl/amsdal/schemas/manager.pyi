from _typeshed import Incomplete
from amsdal.configs.main import settings as settings
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.utils.singleton import Singleton

class SchemaManager(metaclass=Singleton):
    """
    Manages schema operations including retrieval, invalidation, and sorting.

    This class handles various schema-related operations such as invalidating user schemas,
    retrieving schemas by name or type, and sorting schemas based on predefined rules.
    """
    _schema_manager_handler: Incomplete
    def __init__(self) -> None: ...
    def invalidate_user_schemas(self) -> None:
        """
        Invalidates user schemas.

        This method calls the handler to invalidate all user schemas, ensuring that any cached or outdated schemas
            are refreshed.

        Returns:
            None
        """
    def class_schemas(self) -> list[tuple[ObjectSchema, SchemaTypes]]:
        """
        Returns a list of tuples containing object schemas and their types.

        This method retrieves and sorts various schemas managed by the schema manager handler.
        The schemas are categorized into types, core, user, and contrib schemas.

        Returns:
            list[tuple[ObjectSchema, SchemaTypes]]: A list of tuples where each tuple contains an object schema
                and its corresponding type.
        """
    @staticmethod
    def _sort_key_for_schema(schema: ObjectSchema) -> int: ...
    def get_schema_by_name(self, title: str, schema_type: SchemaTypes | None = None) -> ObjectSchema | None:
        """
        Retrieves a schema by its title and optional type.

        This method searches for a schema with the specified title and optional type
        among the schemas managed by the schema manager handler.

        Args:
            title (str): The title of the schema to be retrieved.
            schema_type (SchemaTypes | None, optional): The type of the schema to be retrieved. Defaults to None.

        Returns:
            ObjectSchema | None: The schema with the specified title and type, or None if not found.
        """
    def get_schemas(self, schema_type: SchemaTypes | None = None) -> list[ObjectSchema]:
        """
        Retrieves schemas based on the provided type.

        This method returns a list of schemas filtered by the specified type. If no type is provided,
        it returns all schemas managed by the schema manager handler.

        Args:
            schema_type (SchemaTypes | None, optional): The type of schemas to retrieve. Defaults to None.

        Returns:
            list[ObjectSchema]: A list of schemas filtered by the specified type, or all schemas if no type is provided.
        """
