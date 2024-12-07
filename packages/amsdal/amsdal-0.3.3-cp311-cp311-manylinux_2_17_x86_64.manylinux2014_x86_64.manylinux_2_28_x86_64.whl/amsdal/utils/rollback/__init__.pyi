def rollback_to_timestamp(timestamp: float) -> None:
    """
    Rollback the data to the given timestamp
    Args:
        timestamp (float): The timestamp to rollback the data to.
    Returns:
        None
    """
def rollback_transaction(transaction_id: str) -> None:
    """
    Rollback the data to the point in time before the given transaction
    Args:
        transaction_id (str): The transaction ID to rollback the data to.
    Returns:
        None
    """
async def async_rollback_to_timestamp(timestamp: float) -> None:
    """
    Rollback the data to the given timestamp
    Args:
        timestamp (float): The timestamp to rollback the data to.
    Returns:
        None
    """
async def async_rollback_transaction(transaction_id: str) -> None:
    """
    Rollback the data to the point in time before the given transaction
    Args:
        transaction_id (str): The transaction ID to rollback the data to.
    Returns:
        None
    """
