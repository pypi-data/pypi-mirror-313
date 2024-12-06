from typing import List

def generate_daily_timestamps(start_timestamp: int, hours: int = 24) -> List[int]:
    """
    Generate timestamps for a given number of hours.

    Args:
        start_timestamp (int): Starting Unix timestamp.
        hours (int, optional): Number of hours to generate timestamps for. Defaults to 24 for one whole day.

    Returns:
        List[int]: List of hourly Unix timestamps.
    """
    return [start_timestamp + i * 3600 for i in range(hours)]
