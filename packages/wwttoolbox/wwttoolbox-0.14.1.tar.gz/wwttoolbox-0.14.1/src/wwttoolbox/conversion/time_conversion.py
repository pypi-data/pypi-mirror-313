from datetime import datetime, timezone

from .time_expression_parser import TimeExpressionParser


def iso_string_2_datetime(iso_string: str) -> datetime:
    """Converts an ISO 8601 string to a datetime object.

    Any timezone information in the string is ignored.

    Parameters:
    iso_string (str): An ISO 8601 string.

    Returns:
    datetime: A datetime object with tzinfo=utc.
    """
    return datetime.fromisoformat(iso_string).replace(tzinfo=timezone.utc)


def unix_2_datetime(unix_seconds: float) -> datetime:
    """Converts a Unix timestamp to a datetime object.

    Using a float as parameter allows to represent fractions of seconds.

    Parameters:
    unix_seconds (float): A Unix timestamp.

    Returns:
    datetime: A datetime object with tzinfo=utc.
    """
    return datetime.fromtimestamp(unix_seconds, tz=timezone.utc)


def datetime_2_iso_string_without_leading_Z(datetime: datetime) -> str:
    """Converts a datetime object to an ISO 8601 string without a leading 'Z'.

    If the datetime object has a timezone, it will be converted to UTC.

    E.g. '2024-01-01T13:02:59Z'

    Parameters:
    datetime (datetime): A datetime object.

    Returns:
    str: An ISO 8601 string without a leading 'Z'. Always in UTC.
    """

    return datetime.astimezone(timezone.utc).isoformat()


def datetime_2_iso_string_with_leading_Z(datetime: datetime) -> str:
    """Converts a datetime object to an ISO 8601 string with a leading 'Z'.

    If the datetime object has a timezone, it will be converted to UTC.

    E.g. '2024-01-01T13:02:59Z'

    Parameters:
    datetime (datetime): A datetime object.

    Returns:
    str: An ISO 8601 string with a leading 'Z'. Always in UTC.
    """

    return datetime.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def datetime_2_unix(datetime: datetime) -> int:
    """Converts a datetime object to a Unix timestamp without fractions of seconds.

    If the datetime object has a timezone, it will be converted to UTC.
    Fraction of seconds are ignored.

    Parameters:
    datetime (datetime): A datetime object.

    Returns:
    int: A Unix timestamp.
    """

    return int(datetime.astimezone(timezone.utc).timestamp())


def datetime_2_unix_with_fraction(datetime: datetime) -> float:
    """Converts a datetime object to a Unix timestamp with fractions of seconds.

    If the datetime object has a timezone, it will be converted to UTC.

    Parameters:
    datetime (datetime): A datetime object.

    Returns:
    float: A Unix timestamp with fractions of seconds.
    """

    return datetime.astimezone(timezone.utc).timestamp()


def time_expression_2_datetime(
    time_expression: str, ref_time: datetime | None = None
) -> datetime:
    """Converts a time expression to a datetime object.

    The expression consist of 2 elements: a base time, the operator and a offset: <base><operator><offset>

    The base element:
    - 'now': use the current time in UTC
    - 'ref': use the provided reference time (ref_time)

    The operator element:
    - '+': add the offset to the base time
    - '-': subtract the offset from the base time

    The offset element:
    - 's': seconds
    - 'm': minutes
    - 'h': hours
    - 'd': days
    - 'y': years (365 days)

    The offset value is an integer.

    Examples:
    - 'now+1d': 1 day from now
    - 'now': now
    - 'ref-1h': 1 hour before the reference time
    - 'ref+2y': 2 years after the reference time

    Parameters:
    time_expression (str): A time expression.
    ref_time (datetime, optional): A reference time. Defaults to None.

    Returns:
    datetime: A datetime object.

    Raises:
    - ValueError: If the time expression is invalid.
    - ValueError: If base time is ref and ref_time is None
    """
    tep = TimeExpressionParser(time_expression)

    if not tep.is_valid():
        raise ValueError(f"Invalid time expression: '{time_expression}'")

    return tep.get_datetime(ref_time)
