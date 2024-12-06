from datetime import date
from datetime import datetime
from enum import Enum
from inspect import _empty
from inspect import signature
from types import FunctionType
from types import UnionType
from typing import Any
from typing import ClassVar
from typing import ForwardRef
from typing import Union

from amsdal_models.classes.manager import ClassManager
from amsdal_models.classes.model import LegacyModel
from amsdal_models.classes.model import Model
from amsdal_utils.models.data_models.reference import Reference
from pydantic import BaseModel
from pydantic_core import PydanticUndefined

from amsdal.schemas.manager import SchemaManager

default_types_map = {
    int: 'number',
    float: 'number',
    bool: 'checkbox',
    str: 'text',
    bytes: 'Bytes',
    date: 'date',
    datetime: 'datetime',
}


def _process_union(value: UnionType, *, is_transaction: bool = False) -> dict[str, Any]:
    arg_type = {'required': True}
    for arg in value.__args__:
        if arg is type(None):
            arg_type['required'] = False
            continue

        control = convert_to_frontend_config(arg, is_transaction=is_transaction)
        if control:
            arg_type.update(control)

    return arg_type


def convert_to_frontend_config(value: Any, *, is_transaction: bool = False) -> dict[str, Any]:
    """
    Converts a given value to a frontend configuration dictionary.

    This function takes a value and converts it into a dictionary that represents
    the configuration for a frontend form control. It handles various types such as
    Union, list, dict, BaseModel, and custom types.

    Args:
        value (Any): The value to be converted to frontend configuration.
        is_transaction (bool, optional): Indicates if the conversion is for a transaction. Defaults to False.

    Returns:
        dict[str, Any]: A dictionary representing the frontend configuration for the given value.
    """
    if hasattr(value, '__origin__'):
        origin_class = value.__origin__

        if origin_class in [ClassVar]:
            return {}

        if origin_class is Union:
            _union = _process_union(value, is_transaction=is_transaction)

            if 'entityType' in _union and _union['entityType'] == 'File':
                _union['type'] = 'file'
                del _union['entityType']

            return _union

        if origin_class is list:
            return {
                'type': 'array',
                'name': 'array_items',
                'label': 'array_items',
                'control': {
                    'name': 'array_items_values',
                    'label': 'array_items_values',
                    **convert_to_frontend_config(value.__args__[0], is_transaction=is_transaction),
                },
            }

        if origin_class is dict:
            return {
                'type': 'dict',
                'name': 'dict_items',
                'label': 'dict_items',
                'control': {
                    'name': 'dict_items_values',
                    'label': 'dict_items_values',
                    **convert_to_frontend_config(value.__args__[1], is_transaction=is_transaction),
                },
            }

    if isinstance(value, ForwardRef):
        class_name = value.__forward_arg__
        _class = ClassManager().import_class(class_name, ClassManager().resolve_schema_type(class_name))

        if issubclass(_class, Model):
            return {
                'entityType': value.__forward_arg__,
            }

        value = _class

    if isinstance(value, UnionType):
        _union = _process_union(value, is_transaction=is_transaction)

        if 'entityType' in _union and _union['entityType'] == 'File':
            _union['type'] = 'file'
            del _union['entityType']

        return _union

    if value in default_types_map:
        return {
            'type': default_types_map[value],
        }

    if value is Any:
        return {
            'type': 'text',
        }

    if isinstance(value, FunctionType):
        function_controls = []

        while hasattr(value, '__wrapped__'):
            value = value.__wrapped__

        _signature = signature(value)
        _parameters = _signature.parameters

        for arg_name in _parameters:
            if arg_name in value.__annotations__:
                arg_type = value.__annotations__[arg_name]
                control = convert_to_frontend_config(
                    arg_type,
                    is_transaction=True,
                )

                if not control:
                    continue

                control['name'] = arg_name
                control['label'] = arg_name
            else:
                control = {
                    'type': 'text',
                    'name': arg_name,
                    'label': arg_name,
                }

            control.setdefault('required', True)
            _param = _parameters[arg_name]
            if _param.default is not _empty:
                control['value'] = _param.default
                control['required'] = False

            function_controls.append(control)

        return {
            'type': 'group',
            'name': value.__name__,
            'label': value.__name__,
            'controls': function_controls,
        }

    if issubclass(value, Reference):
        return {
            'type': 'object_latest',
        }

    if is_transaction and issubclass(value, Model):
        if value.__name__ == 'File':
            return {
                'type': 'file',
            }
        return {
            'type': 'object_latest',
            'entityType': value.__name__,
        }

    if issubclass(value, LegacyModel):
        return {}

    if issubclass(value, BaseModel):
        model_controls = []

        try:
            schema = SchemaManager().get_schema_by_name(value.__name__)
        except FileNotFoundError:
            schema = None

        for field_name, field in value.__annotations__.items():
            control = convert_to_frontend_config(field, is_transaction=is_transaction)

            if not control:
                continue

            control.setdefault('required', True)

            if field_name in value.model_fields:
                _field = value.model_fields[field_name]

                if _field.default is not PydanticUndefined:
                    control['value'] = _field.default

            control['name'] = field_name
            control['label'] = field_name

            if schema and schema.properties and field_name in schema.properties:
                schema_property = schema.properties[field_name]

                if schema_property.options:
                    control['options'] = [
                        {
                            'label': option.key,
                            'value': option.value,
                        }
                        for option in schema_property.options
                    ]
                    if control.get('type') == 'text':
                        control['type'] = 'select'

                if schema_property.title:
                    control['label'] = schema_property.title

            model_controls.append(control)

        return {
            'type': 'group',
            'name': value.__name__,
            'label': value.__name__,
            'controls': model_controls,
        }

    if issubclass(value, Enum):
        return {
            'type': 'select',
            'options': [{'label': option.name, 'value': option.value} for option in value],
        }

    return {}
