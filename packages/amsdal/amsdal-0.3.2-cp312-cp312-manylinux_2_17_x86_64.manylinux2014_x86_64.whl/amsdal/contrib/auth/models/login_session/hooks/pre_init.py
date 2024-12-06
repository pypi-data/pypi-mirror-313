from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

# import bcrypt
import jwt

# from amsdal_utils.models.enums import Versions


def pre_init(self, *, is_new_object: bool, kwargs: dict[str, Any]) -> None:  # type: ignore[no-untyped-def]  # noqa: ARG001
    """
    Pre-initializes a user object by validating email and password, and generating a JWT token.

    This method checks if the object is new and validates the provided email and password.
    If the email and password are valid, it generates a JWT token and adds it to the kwargs.

    Args:
        is_new_object (bool): Indicates if the object is new.
        kwargs (dict[str, Any]): The keyword arguments containing user details.

    Raises:
        AuthenticationError: If the email or password is invalid.
    """
    if not is_new_object or '_metadata' in kwargs:
        return

    from amsdal.contrib.auth.errors import AuthenticationError
    from amsdal.contrib.auth.settings import auth_settings

    email = kwargs.get('email', None)
    password = kwargs.get('password', None)

    if not email:
        msg = "Email can't be empty"
        raise AuthenticationError(msg)

    if not password:
        msg = "Password can't be empty"
        raise AuthenticationError(msg)

    lowercased_email = email.lower()

    # from models.contrib.user import User  # type: ignore[import-not-found]

    # user = User.objects.filter(
    #     email=lowercased_email,
    #     _address__object_version=Versions.LATEST
    # ).get_or_none().execute()

    # if not user:
    #     msg = 'Invalid email / password'
    #     raise AuthenticationError(msg)

    # if not bcrypt.checkpw(password.encode('utf-8') if isinstance(password, str) else password, user.password):
    #     msg = 'Invalid email / password'
    #     raise AuthenticationError(msg)

    kwargs['password'] = 'validated'
    expiration_time = datetime.now(tz=timezone.utc) + timedelta(seconds=auth_settings.AUTH_TOKEN_EXPIRATION)
    token = jwt.encode(
        {'email': lowercased_email, 'exp': expiration_time},
        key=auth_settings.AUTH_JWT_KEY,  # type: ignore[arg-type]
        algorithm='HS256',
    )

    kwargs['token'] = token
