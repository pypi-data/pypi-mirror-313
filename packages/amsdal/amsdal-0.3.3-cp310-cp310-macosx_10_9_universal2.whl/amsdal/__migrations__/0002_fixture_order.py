from amsdal.migration import migrations
from amsdal_utils.models.enums import SchemaTypes


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.UpdateClass(
            schema_type=SchemaTypes.CORE,
            class_name='Fixture',
            old_schema={
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
            new_schema={
                'title': 'Fixture',
                'required': ['data', 'external_id'],
                'properties': {
                    'class_name': {'type': 'string', 'title': 'Class Name'},
                    'order': {'type': 'number', 'title': 'Order'},
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
    ]
