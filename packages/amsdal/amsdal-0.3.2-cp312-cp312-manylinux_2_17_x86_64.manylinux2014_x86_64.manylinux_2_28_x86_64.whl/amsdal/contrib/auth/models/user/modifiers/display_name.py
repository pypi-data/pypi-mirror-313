@property  # type: ignore[misc]
def display_name(self) -> str:  # type: ignore[no-untyped-def]
    """
    Returns the display name of the user.

    This method returns the email of the user as their display name.

    Returns:
        str: The email of the user.
    """
    return self.email


def __str__(self) -> str:  # type: ignore[no-untyped-def]  # noqa: N807
    return f'User(email={self.email})'


def __repr__(self) -> str:  # type: ignore[no-untyped-def]  # noqa: N807
    return str(self)
