from amsdal_utils.models.enums import SchemaTypes

from amsdal.migration import migrations


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.CreateClass(
            schema_type=SchemaTypes.CONTRIB,
            class_name='Permission',
            new_schema={
                'title': 'Permission',
                'required': ['model', 'action'],
                'properties': {
                    'model': {'type': 'string', 'title': 'Model'},
                    'action': {'type': 'string', 'title': 'Action'},
                },
                'custom_code': "@property  # type: ignore[misc]\ndef display_name(self) -> str:  # type: ignore[no-untyped-def]\n    return f'{self.model}:{self.action}'",
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CONTRIB,
            class_name='User',
            new_schema={
                'title': 'User',
                'required': ['email', 'password'],
                'properties': {
                    'email': {'type': 'string', 'title': 'Email'},
                    'password': {'type': 'binary', 'title': 'Password (hash)'},
                    'permissions': {'type': 'array', 'items': {'type': 'Permission'}, 'title': 'Permissions'},
                },
                'custom_code': "from typing import Any\n\n\ndef pre_init(self, *, is_new_object: bool, kwargs: dict[str, Any]) -> None:  # type: ignore[no-untyped-def]  # noqa: ARG001\n    import bcrypt\n\n    from amsdal.contrib.auth.errors import UserCreationError\n\n    email = kwargs.get('email', None)\n    password = kwargs.get('password', None)\n\n    if email is None or email == '':\n        msg = \"Email can't be empty\"\n        raise UserCreationError(msg)\n\n    if password is None or password == '':\n        msg = \"Password can't be empty\"\n        raise UserCreationError(msg)\n\n    kwargs['email'] = email.lower()\n\n    if is_new_object and '_metadata' not in kwargs:\n        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())\n        kwargs['password'] = hashed_password\n        kwargs['_object_id'] = email.lower()\n\ndef pre_create(self) -> None:  # type: ignore[no-untyped-def]  # noqa: ARG001\n    pass\n\n@property  # type: ignore[misc]\ndef display_name(self) -> str:  # type: ignore[no-untyped-def]\n    return self.email",
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.CONTRIB,
            class_name='LoginSession',
            new_schema={
                'title': 'LoginSession',
                'required': ['email', 'password'],
                'properties': {
                    'email': {'type': 'string', 'title': 'Email'},
                    'password': {'type': 'string', 'title': 'Password (hash)'},
                    'token': {'type': 'string', 'title': 'Token', 'mark_as_read_only': True},
                },
                'custom_code': "from datetime import datetime\nfrom datetime import timedelta\nfrom datetime import timezone\nfrom typing import Any\n\nimport bcrypt\nimport jwt\nfrom amsdal_utils.models.enums import Versions\n\n\ndef pre_init(self, *, is_new_object: bool, kwargs: dict[str, Any]) -> None:  # type: ignore[no-untyped-def]  # noqa: ARG001\n    if not is_new_object or '_metadata' in kwargs:\n        return\n\n    from amsdal.contrib.auth.errors import AuthenticationError\n    from amsdal.contrib.auth.settings import auth_settings\n\n    email = kwargs.get('email', None)\n    password = kwargs.get('password', None)\n\n    if not email:\n        msg = \"Email can't be empty\"\n        raise AuthenticationError(msg)\n\n    if not password:\n        msg = \"Password can't be empty\"\n        raise AuthenticationError(msg)\n\n    lowercased_email = email.lower()\n\n    from models.contrib.user import User  # type: ignore[import-not-found]\n\n    user = User.objects.filter(email=lowercased_email, _address__object_version=Versions.LATEST).get_or_none().execute()\n\n    if not user:\n        msg = 'Invalid email / password'\n        raise AuthenticationError(msg)\n\n    if not bcrypt.checkpw(password.encode('utf-8') if isinstance(password, str) else password, user.password):\n        msg = 'Invalid email / password'\n        raise AuthenticationError(msg)\n\n    kwargs['password'] = 'validated'\n    expiration_time = datetime.now(tz=timezone.utc) + timedelta(seconds=1200)\n    token = jwt.encode(\n        {'email': lowercased_email, 'exp': expiration_time},\n        key=auth_settings.AUTH_JWT_KEY,  # type: ignore[arg-type]\n        algorithm='HS256',\n    )\n\n    kwargs['token'] = token\n\n@property  # type: ignore[misc]\ndef display_name(self) -> str:  # type: ignore[no-untyped-def]\n    return self.email",
            },
        ),
    ]
