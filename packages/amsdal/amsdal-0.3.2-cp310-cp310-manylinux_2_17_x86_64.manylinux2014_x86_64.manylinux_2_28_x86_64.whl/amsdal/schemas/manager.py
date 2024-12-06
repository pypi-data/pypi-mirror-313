from amsdal_models.schemas.manager import SchemaManagerHandler
from amsdal_utils.models.data_models.enums import BaseClasses
from amsdal_utils.models.data_models.schema import ObjectSchema
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.utils.singleton import Singleton

from amsdal.configs.main import settings


class SchemaManager(metaclass=Singleton):
    """
    Manages schema operations including retrieval, invalidation, and sorting.

    This class handles various schema-related operations such as invalidating user schemas,
    retrieving schemas by name or type, and sorting schemas based on predefined rules.
    """

    def __init__(self) -> None:
        self._schema_manager_handler = SchemaManagerHandler(settings.schemas_root_path)

    def invalidate_user_schemas(self) -> None:
        """
        Invalidates user schemas.

        This method calls the handler to invalidate all user schemas, ensuring that any cached or outdated schemas
            are refreshed.

        Returns:
            None
        """
        self._schema_manager_handler.invalidate_user_schemas()

    def class_schemas(self) -> list[tuple[ObjectSchema, SchemaTypes]]:
        """
        Returns a list of tuples containing object schemas and their types.

        This method retrieves and sorts various schemas managed by the schema manager handler.
        The schemas are categorized into types, core, user, and contrib schemas.

        Returns:
            list[tuple[ObjectSchema, SchemaTypes]]: A list of tuples where each tuple contains an object schema
                and its corresponding type.
        """
        return (
            [
                (type_schema, SchemaTypes.TYPE)
                for type_schema in self._schema_manager_handler.type_schemas
                if type_schema.title == BaseClasses.OBJECT
            ]
            + [
                (core_schema, SchemaTypes.CORE)
                for core_schema in sorted(self._schema_manager_handler.core_schemas, key=self._sort_key_for_schema)
            ]
            + [(user_schema, SchemaTypes.USER) for user_schema in self._schema_manager_handler.user_schemas]
            + [(contrib_schema, SchemaTypes.CONTRIB) for contrib_schema in self._schema_manager_handler.contrib_schemas]
        )

    @staticmethod
    def _sort_key_for_schema(schema: ObjectSchema) -> int:
        # We need to register ClassObject first, coz ClassObjectMeta has a reference to it.
        # All other classes have reference to ClassObject
        if schema.title == BaseClasses.CLASS_OBJECT:
            return 0
        elif schema.title == BaseClasses.CLASS_OBJECT_META:
            return 1
        else:
            return 2

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
        _schemas = self.get_schemas(schema_type)

        for schema in _schemas:
            if schema.title == title:
                return schema

        return None

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
        if schema_type == SchemaTypes.CONTRIB:
            return self._schema_manager_handler.contrib_schemas

        if schema_type == SchemaTypes.CORE:
            return self._schema_manager_handler.core_schemas

        if schema_type == SchemaTypes.TYPE:
            return self._schema_manager_handler.type_schemas

        if schema_type == SchemaTypes.USER:
            return self._schema_manager_handler.user_schemas

        return self._schema_manager_handler.all_schemas
