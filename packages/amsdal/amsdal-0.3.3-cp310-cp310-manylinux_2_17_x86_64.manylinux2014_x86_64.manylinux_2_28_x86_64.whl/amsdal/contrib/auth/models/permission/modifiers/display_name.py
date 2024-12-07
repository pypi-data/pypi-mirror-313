@property  # type: ignore[misc]
def display_name(self) -> str:  # type: ignore[no-untyped-def]
    """
    Returns the display name of the user.

    This method returns a formatted string combining the model and action of the user.

    Returns:
        str: The formatted display name in the format 'model:action'.
    """
    return f'{self.model}:{self.action}'
