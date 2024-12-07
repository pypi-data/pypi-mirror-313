from amsdal.migration import migrations
from amsdal_utils.models.enums import SchemaTypes


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.UpdateClass(
            schema_type=SchemaTypes.CORE,
            class_name='ClassObjectMeta',
            old_schema={
                "title": "ClassObjectMeta",
                "type": "object",
                "properties": {
                    "title": {"title": "Title", "type": "string"},
                    "type": {"title": "Type", "type": "string"},
                    "default": {"title": "Default", "type": "anything"},
                    "properties": {
                        "title": "Properties",
                        "type": "dictionary",
                        "items": {"key": {"type": "string"}, "value": {"type": "ClassPropertyMeta"}},
                    },
                    "indexed": {"title": "Indexed", "type": "array", "items": {"type": "string"}},
                    "unique": {
                        "title": "Unique Fields",
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "string"}},
                    },
                    "custom_code": {"title": "Custom Code", "type": "string"},
                },
                "required": ["title", "type"],
            },
            new_schema={
                "title": "ClassObjectMeta",
                "type": "object",
                "properties": {
                    "title": {"title": "Title", "type": "string"},
                    "type": {"title": "Type", "type": "string"},
                    "default": {"title": "Default", "type": "anything"},
                    "class_schema_type": {"title": "Schema Type", "type": "string"},
                    "properties": {
                        "title": "Properties",
                        "type": "dictionary",
                        "items": {"key": {"type": "string"}, "value": {"type": "ClassPropertyMeta"}},
                    },
                    "indexed": {"title": "Indexed", "type": "array", "items": {"type": "string"}},
                    "unique": {
                        "title": "Unique Fields",
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "string"}},
                    },
                    "custom_code": {"title": "Custom Code", "type": "string"},
                },
                "required": ["title", "type"],
            },
        ),
    ]
