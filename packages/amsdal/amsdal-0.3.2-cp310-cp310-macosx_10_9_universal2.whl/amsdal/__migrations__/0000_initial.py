from amsdal_utils.models.enums import SchemaTypes

from amsdal.migration import migrations


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Object',
            new_schema={
                'title': 'Object',
                'properties': {
                    'title': {'type': 'string', 'title': 'Title'},
                    'type': {'type': 'string', 'title': 'Type'},
                    'default': {'type': 'anything', 'title': 'Default'},
                    'properties': {
                        'type': 'dictionary',
                        'items': {'key': {'type': 'string'}, 'value': {'type': 'anything'}},
                        'title': 'Properties',
                    },
                    'required': {'type': 'array', 'items': {'type': 'string'}, 'title': 'Required'},
                    'unique': {
                        'type': 'array',
                        'items': {'type': 'array', 'items': {'type': 'string'}},
                        'title': 'Unique Fields',
                    },
                    'custom_code': {'type': 'string', 'title': 'Custom Code'},
                    'meta_class': {'type': 'string', 'title': 'Meta Class'},
                },
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Binary',
            new_schema={'title': 'Binary', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Dictionary',
            new_schema={'title': 'Dictionary', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Anything',
            new_schema={'title': 'Anything', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='String',
            new_schema={'title': 'String', 'default': '', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Array',
            new_schema={'title': 'Array', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Number',
            new_schema={'title': 'Number', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Boolean',
            new_schema={
                'title': 'Boolean',
                'properties': {},
                'options': [{'key': 'true', 'value': True}, {'key': 'false', 'value': False}],
                'meta_class': 'TypeMeta',
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CORE,
            class_name='Option',
            new_schema={
                'title': 'Option',
                'required': ['key', 'value'],
                'properties': {
                    'key': {'type': 'string', 'title': 'Key'},
                    'value': {'type': 'string', 'title': 'Value Type'},
                },
                'meta_class': 'TypeMeta',
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CORE,
            class_name='Validator',
            new_schema={
                'title': 'Validator',
                'required': ['name', 'data'],
                'properties': {
                    'name': {'type': 'string', 'title': 'Validator Name'},
                    'data': {'type': 'anything', 'title': 'Validator Data'},
                },
                'meta_class': 'TypeMeta',
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CORE,
            class_name='ClassPropertyMeta',
            new_schema={
                'title': 'ClassPropertyMeta',
                'properties': {
                    'title': {'type': 'string', 'title': 'Title'},
                    'default': {'type': 'anything', 'title': 'Default'},
                    'options': {'type': 'array', 'items': {'type': 'Option'}, 'title': 'Options'},
                },
                'meta_class': 'TypeMeta',
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CORE,
            class_name='ClassProperty',
            new_schema={
                'title': 'ClassProperty',
                'required': ['type'],
                'properties': {
                    'type': {'type': 'string', 'title': 'Type'},
                    'items': {
                        'type': 'dictionary',
                        'items': {'key': {'type': 'string'}, 'value': {'type': 'anything'}},
                        'title': 'Items',
                    },
                },
                'meta_class': 'TypeMeta',
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CORE,
            class_name='ClassObject',
            new_schema={
                'title': 'ClassObject',
                'properties': {
                    'properties': {
                        'type': 'dictionary',
                        'items': {'key': {'type': 'string'}, 'value': {'type': 'ClassProperty'}},
                        'title': 'Properties',
                    },
                    'required': {'type': 'array', 'items': {'type': 'string'}, 'title': 'Required'},
                    'meta_class': {'type': 'string', 'default': 'ClassObject', 'title': 'Meta Class'},
                },
                'custom_code': '@property  # type: ignore[misc]\ndef display_name(self) -> str:  # type: ignore[no-untyped-def]\n    return self.title',
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CORE,
            class_name='ClassObjectMeta',
            new_schema={
                'title': 'ClassObjectMeta',
                'required': ['title', 'type'],
                'properties': {
                    'title': {'type': 'string', 'title': 'Title'},
                    'type': {'type': 'string', 'title': 'Type'},
                    'default': {'type': 'anything', 'title': 'Default'},
                    'properties': {
                        'type': 'dictionary',
                        'items': {'key': {'type': 'string'}, 'value': {'type': 'ClassPropertyMeta'}},
                        'title': 'Properties',
                    },
                    'indexed': {'type': 'array', 'items': {'type': 'string'}, 'title': 'Indexed'},
                    'unique': {
                        'type': 'array',
                        'items': {'type': 'array', 'items': {'type': 'string'}},
                        'title': 'Unique Fields',
                    },
                    'custom_code': {'type': 'string', 'title': 'Custom Code'},
                },
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CORE,
            class_name='Fixture',
            new_schema={
                'title': 'Fixture',
                'required': ['data', 'external_id'],
                'properties': {
                    'class_name': {'type': 'string', 'title': 'Class Name'},
                    'external_id': {'type': 'string', 'title': 'External ID'},
                    'data': {
                        'type': 'dictionary',
                        'items': {'key': {'type': 'string'}, 'value': {'type': 'anything'}},
                        'title': 'Data',
                    },
                },
                'unique': [['external_id']],
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CORE,
            class_name='File',
            new_schema={
                'title': 'File',
                'required': ['filename', 'data'],
                'properties': {
                    'filename': {'type': 'string', 'title': 'Filename'},
                    'data': {'type': 'binary', 'title': 'Data'},
                    'size': {'type': 'number', 'title': 'Size'},
                },
                'custom_code': "def pre_update(self):  # type: ignore[no-untyped-def]\n    self.size = len(self.data or b'')\n\ndef pre_create(self) -> None:  # type: ignore[no-untyped-def]\n    self.size = len(self.data or b'')\n\nfrom pathlib import Path\nfrom typing import BinaryIO\n\n\ndef to_file(self, file_or_path: Path | BinaryIO) -> None:  # type: ignore[no-untyped-def]\n    if isinstance(file_or_path, Path):\n        if file_or_path.is_dir():\n            file_or_path = file_or_path / self.name\n        file_or_path.write_bytes(self.data)  # type: ignore[union-attr]\n    else:\n        file_or_path.write(self.data)\n        file_or_path.seek(0)\n\nfrom pathlib import Path\nfrom typing import BinaryIO\n\n\n@classmethod  # type: ignore[misc, no-untyped-def]\ndef from_file(\n    cls,\n    file_or_path: Path | BinaryIO,\n) -> 'File':  # type: ignore[name-defined]  # noqa: F821\n    if isinstance(file_or_path, Path):\n        if file_or_path.is_dir():\n            msg = f'{file_or_path} is a directory'\n            raise ValueError(msg)\n\n        data = file_or_path.read_bytes()\n        filename = file_or_path.name\n    else:\n        file_or_path.seek(0)\n        data = file_or_path.read()\n        filename = Path(file_or_path.name).name\n\n    return cls(data=data, filename=filename)\n\nimport base64\n\nfrom pydantic import field_validator\n\n\n@field_validator('data')  # type: ignore[misc]\n@classmethod\ndef data_base64_decode(cls, v: bytes) -> bytes:  # type: ignore[no-untyped-def]  # noqa: ARG001\n    is_base64: bool = False\n\n    try:\n        is_base64 = base64.b64encode(base64.b64decode(v)) == v\n    except Exception:\n        ...\n\n    if is_base64:\n        return base64.b64decode(v)\n\n    return v\n\n@property  # type: ignore[misc]\ndef mimetype(self) -> str | None:  # type: ignore[no-untyped-def]\n    import mimetypes\n\n    return mimetypes.guess_type(self.filename)[0]",
            },
        ),
    ]
