import pytz
from datetime import datetime


def get_midnight_utc_timestamp() -> int:
    """
    Get the UTC midnight timestamp for the current date.

    Returns:
        int: Unix timestamp for midnight UTC of the current date.
    """
    # Get the current date and midnight in UTC timezone
    current_date = datetime.now()
    midnight_utc = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0, tzinfo=pytz.utc)

    # Then convert it to Unix timestamp using the timestamp() method of datetime object
    midnight_utc_timestamp = int(midnight_utc.timestamp())

    # Return the Unix timestamp as the result
    return midnight_utc_timestamp
