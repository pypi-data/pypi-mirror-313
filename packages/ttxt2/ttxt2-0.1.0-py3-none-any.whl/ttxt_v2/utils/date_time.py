from datetime import datetime, timedelta, timezone


def convert_date_to_utc_timestamp(date: str) -> float:
    """
    Date should be in the format %d/%m/%Y %H:%M
    """
    dt_format = "%d/%m/%Y %H:%M"
    return datetime.strptime(date, dt_format).replace(tzinfo=timezone.utc).timestamp()


def timestamp_to_human_readable(timestamp_ms: int) -> str:
    """
    Convert a UTC timestamp in milliseconds to a human-readable date with precision to the second.

    :param timestamp_ms: Timestamp in milliseconds.
    :return: Human-readable date string in the format "%Y-%m-%d %H:%M:%S".
    """
    timestamp_s = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_dates(delta: int = 7):
    current_datetime = datetime.now()
    current_date_str = current_datetime.strftime("%d/%m/%Y %H:%M")
    past_datetime = current_datetime - timedelta(days=delta)
    past_date_str = past_datetime.strftime("%d/%m/%Y %H:%M")
    return current_date_str, past_date_str
