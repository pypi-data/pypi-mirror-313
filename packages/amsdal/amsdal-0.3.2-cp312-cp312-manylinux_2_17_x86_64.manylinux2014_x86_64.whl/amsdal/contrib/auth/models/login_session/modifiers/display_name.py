@property  # type: ignore[misc]
def display_name(self) -> str:  # type: ignore[no-untyped-def]
    """
    Returns the display name of the user.

    This method returns the email of the user as their display name.

    Returns:
        str: The email of the user.
    """
    return self.email
