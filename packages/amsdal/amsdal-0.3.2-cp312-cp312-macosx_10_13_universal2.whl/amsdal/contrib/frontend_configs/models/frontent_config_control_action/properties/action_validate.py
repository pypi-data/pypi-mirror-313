from pydantic import field_validator


@field_validator('action', mode='after')  # type: ignore[misc]
@classmethod
def validate_action(cls, v: str) -> str:  # type: ignore[no-untyped-def] # noqa: ARG001
    """
    Validates the action string to ensure it is one of the allowed values.

    This method checks if the action string starts with 'navigate::' or is one of the predefined
    actions. If the action string is invalid, it raises a ValueError.

    Args:
        cls: The class this method is attached to.
        v (str): The action string to validate.

    Returns:
        str: The validated action string.

    Raises:
        ValueError: If the action string is not valid.
    """
    if not v.startswith('navigate::') and v not in [
        'goPrev',
        'goNext',
        'goNextWithSubmit',
        'submit',
        'submitWithDataLayer',
    ]:
        msg = 'Action must be one of: goPrev, goNext, goNextWithSubmit, submit, submitWithDataLayer, navigate::{string}'
        raise ValueError(msg)

    return v
