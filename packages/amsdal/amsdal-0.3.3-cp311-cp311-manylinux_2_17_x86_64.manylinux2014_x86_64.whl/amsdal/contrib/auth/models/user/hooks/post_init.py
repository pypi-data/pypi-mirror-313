from typing import Any


def post_init(self, *, is_new_object: bool, kwargs: dict[str, Any]) -> None:  # type: ignore[no-untyped-def]
    """
    Post-initializes a user object by validating email and password, and hashing the password.

    This method checks if the email and password are provided and valid. If the object is new,
    it hashes the password and sets the object ID to the lowercased email.

    Args:
        is_new_object (bool): Indicates if the object is new.
        kwargs (dict[str, Any]): The keyword arguments containing user details.

    Raises:
        UserCreationError: If the email or password is invalid.
    """
    import bcrypt

    from amsdal.contrib.auth.errors import UserCreationError

    email = kwargs.get('email', None)
    password = kwargs.get('password', None)

    if email is None or email == '':
        msg = "Email can't be empty"
        raise UserCreationError(msg)

    if password is None or password == '':
        msg = "Password can't be empty"
        raise UserCreationError(msg)

    kwargs['email'] = email.lower()

    if is_new_object and '_metadata' not in kwargs:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password
        self._object_id = email.lower()


def pre_update(self) -> None:  # type: ignore[no-untyped-def]
    import bcrypt

    original_object = self.refetch_from_db()

    password = self.password

    if original_object.password and password is not None:
        if isinstance(password, str):
            password = password.encode('utf-8')

        try:
            if not bcrypt.checkpw(password, original_object.password):
                self.password = password
        except ValueError:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            self.password = hashed_password


async def apre_update(self) -> None:  # type: ignore[no-untyped-def]
    import bcrypt

    original_object = await self.arefetch_from_db()

    password = self.password

    if original_object.password and password is not None:
        if isinstance(password, str):
            password = password.encode('utf-8')

        try:
            if not bcrypt.checkpw(password, original_object.password):
                self.password = password
        except ValueError:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            self.password = hashed_password
