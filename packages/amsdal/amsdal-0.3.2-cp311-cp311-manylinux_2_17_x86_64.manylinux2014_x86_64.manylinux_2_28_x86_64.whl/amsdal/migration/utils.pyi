from _typeshed import Incomplete
from amsdal.migration.data_classes import ModuleTypes as ModuleTypes
from amsdal.schemas.manager import SchemaManager as SchemaManager
from amsdal_models.classes.model import Model
from amsdal_utils.models.data_models.core import DictSchema, LegacyDictSchema, TypeData as TypeData
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema, PropertyData as PropertyData
from amsdal_utils.models.data_models.table_schema import ArraySchemaModel, DictSchemaModel, JsonSchemaModel, NestedSchemaModel, TableColumnSchema, TableSchema
from amsdal_utils.models.enums import SchemaTypes
from pathlib import Path

reference_schema: Incomplete

def object_schema_to_table_schema(object_schema: ObjectSchema) -> TableSchema:
    """
    Converts an ObjectSchema to a TableSchema.

    Args:
        object_schema (ObjectSchema): The object schema to convert.

    Returns:
        TableSchema: The converted table schema.
    """
def _process_properties(properties: dict[str, PropertyData] | None, required: list[str]) -> list[TableColumnSchema]: ...
def _process_property_type(property_type: str, items: TypeData | DictSchema | LegacyDictSchema | None = None, context: dict[str, type | Model | NestedSchemaModel] | None = None) -> type | NestedSchemaModel | ArraySchemaModel | DictSchemaModel | type[JsonSchemaModel]: ...
def schema_to_nested_column_schema(schema: ObjectSchema, context: dict[str, type | Model | NestedSchemaModel]) -> NestedSchemaModel | type:
    """
    Converts an ObjectSchema to a NestedSchemaModel or type.

    Args:
        schema (ObjectSchema): The schema to convert.
        context (dict[str, type | Model | NestedSchemaModel]): The context for the conversion.

    Returns:
        NestedSchemaModel | type: The converted nested schema model or type.
    """
def contrib_to_module_root_path(contrib: str) -> Path:
    """
    Converts a contrib string to the root path of the module.

    Args:
        contrib (str): The contrib string to convert.

    Returns:
        Path: The root path of the module.
    """
def map_module_type_to_schema_type(module_type: ModuleTypes) -> SchemaTypes:
    """
    Maps a ModuleTypes value to a SchemaTypes value.

    Args:
        module_type (ModuleTypes): The module type to map.

    Returns:
        SchemaTypes: The corresponding schema type.

    Raises:
        ValueError: If the module type is unknown.
    """
