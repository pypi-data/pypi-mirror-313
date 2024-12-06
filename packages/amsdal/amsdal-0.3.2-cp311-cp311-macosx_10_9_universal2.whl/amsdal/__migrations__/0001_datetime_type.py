from amsdal_utils.models.enums import SchemaTypes

from amsdal.migration import migrations


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Date',
            new_schema={'title': 'Date', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.TYPE,
            class_name='Datetime',
            new_schema={'title': 'Datetime', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
    ]
