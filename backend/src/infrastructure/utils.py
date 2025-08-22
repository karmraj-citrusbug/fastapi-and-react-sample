from datetime import UTC, datetime, timedelta

import pytz

from config.settings import app_settings
from src.schema.utils import GetTimeRangeResponseDTO


def get_time_range() -> GetTimeRangeResponseDTO:
    """
    Get the time range for the API call.

    Calculate the time range based on the current time and the API call interval duration in minutes
    """
    now = datetime.now(UTC)
    time_to = now.replace(second=0, microsecond=0)
    time_from = time_to - timedelta(
        minutes=app_settings.API_CALL_INTERVAL_DURATION_IN_SECONDS
    )
    return GetTimeRangeResponseDTO(
        time_from=time_from.strftime("%Y%m%dT%H%M"),
        time_to=time_to.strftime("%Y%m%dT%H%M"),
    )


def get_current_timestamp_with_timezone() -> str:
    # Define the desired timezone (India Standard Time)
    ist = pytz.timezone("Asia/Kolkata")

    # Get the current time in IST
    current_time_ist = datetime.now(ist)

    # Format the datetime in ISO 8601 format with microseconds and timezone offset
    formatted_time = current_time_ist.isoformat()

    return formatted_time
