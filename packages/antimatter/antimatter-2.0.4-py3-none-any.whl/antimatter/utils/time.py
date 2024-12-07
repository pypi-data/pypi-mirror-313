from datetime import (
    datetime as dt_type,
)  # We do an extra import here as tests will patch the other datetime import
from datetime import datetime, timedelta, timezone
import re
from typing import Optional, Tuple, Union

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil.tz import gettz

# Constants defining duration of time in microseconds
microsecond = 1
millisecond = microsecond * 1000
second = millisecond * 1000
minute = second * 60
hour = minute * 60
day = hour * 24
month = day * 30
year = day * 365

# Regex pattern for parsing a time duration
_delta_pattern = re.compile(
    r"^((\d+)y ?)?((\d+)mo ?)?((\d+)d ?)?((\d+)h ?)?((\d+)m ?)?((\d+)s ?)?((\d+)ms ?)?((\d+)[uµ]s ?)?$"
)


def get_time_range(
    start_date: Optional[Union[datetime, str]],
    end_date: Optional[Union[datetime, str]],
    duration: Optional[Union[timedelta, relativedelta, str]],
) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Build a time range from the provided start date, end date, and duration.
    Start and end dates can be a datetime or a string representing a date. The
    duration can be a timedelta, a relativedelta from the dateutil library, or
    a string representing a span of time, such as 1d5h12m (1 day, 5 hours, 12
    minutes) where y (year), mo (month), d (day), h (hour), m (minute), s (second),
    ms (millisecond), and us/µs (microsecond) are all supported units of time.

    There are several combinations of parameters that can be provided, and a
    start and end date matching the parameters will be returned. The expectation
    is that the caller treats a None start date as 'the beginning of time' and a
    None end date as 'now'.

    Note that the returned start date and end date will always be timezone aware.
    If no timezone information is provided, the system timezone will be used.

    1.
    Input: start_date, end_date, duration are all None
    Output: None will be returned for the start and end date

    2.
    Input: start_date, end_date, duration all have values
    Output: start_date and end_date will be returned as is, and duration ignored

    3.
    Input: start_date and end_date None; duration has a value
    Output: start_date will be 'now' minus duration; end_date will be None

    4.
    Input: start_date None; end_date and duration have values
    Output: start_date will be end_date minus duration; end_date will be returned as is

    5.
    Input: end_date None; start_date and duration have values
    Output: start_date will be returned as is; end_date will be start_date plus duration

    :param start_date: The optional provided start date as a datetime or string
    :param end_date: The optional provided end date as a datetime or string
    :param duration: The optional provided duration as a timedelta, relativedelta, or string
    :return: The processed start and end dates based on the inputs
    """
    start_date = normalize_datetime(start_date)
    end_date = normalize_datetime(end_date)
    duration = normalize_duration(duration)

    if duration:
        if not start_date and not end_date:
            start_date = datetime.now(tz=timezone.utc) - duration
        elif start_date and not end_date:
            end_date = start_date + duration
        elif not start_date and end_date:
            start_date = end_date - duration

    return normalize_datetime(start_date), normalize_datetime(end_date)


def normalize_datetime(dt: Optional[Union[datetime, str]]) -> Optional[datetime]:
    """
    Normalize the datetime, either ensuring the datetime object has a timezone
    or parsing the datetime string.

    :param dt: The datetime as a string or object
    :return: The parsed, normalized datetime
    """
    if not dt:
        return None
    if not isinstance(dt, dt_type):
        dt = parse_datetime(dt)
    return dt.astimezone(timezone.utc)


def parse_datetime(dt: str, default: Optional[datetime] = None) -> datetime:
    """
    Parse the datetime from a string using the dateutil parser. Default date
    is 1900-01-01T00:00:00.000000 at local timezone, unless otherwise specified.

    :param dt: The string to parse as a datetime
    :param default: The default datetime to use for filling in missing details
    :return: The parsed datetime
    """
    if default is None:
        default = datetime(1900, 1, 1, 0, 0, 0, 0, tzinfo=datetime.now().astimezone().tzinfo)
    return parse(dt, default=default)


def normalize_duration(duration: Optional[Union[timedelta, relativedelta, str]]) -> Optional[relativedelta]:
    """
    Normalize the duration into a relativedelta. This supports relativedelta,
    timedelta, and duration strings.

    :param duration: The duration span
    :return: The normalized duration span
    """
    if not duration:
        return None
    if isinstance(duration, timedelta):
        return relativedelta(days=duration.days, seconds=duration.seconds, microseconds=duration.microseconds)
    if isinstance(duration, relativedelta):
        return duration
    return parse_duration(duration)


def parse_duration(duration: Optional[str]) -> Optional[relativedelta]:
    """
    Parse the duration from a string.

    :param duration: The duration span string
    :return: The parsed relativedelta
    """
    if not duration:
        return None
    match = _delta_pattern.match(duration)
    if not match:
        raise ValueError(f"invalid duration '{duration}'")

    # Helper function for getting the integer value of the match group, or 0
    # if the match group is empty
    def _int_from_group(i) -> Optional[int]:
        if not match.group(i):
            return 0
        return int(match.group(i))

    # We iterate through every other match (which is just the number from the
    # unit group, or an empty string if the unit was not present), getting the
    # unit quantity, or 0 if not present. The result is unpacked into the
    # respective units.
    y, mo, d, h, m, s, ms, us = [_int_from_group((i + 1) * 2) for i in range(8)]
    return relativedelta(
        years=y, months=mo, days=d, hours=h, minutes=m, seconds=s, microseconds=us + 1000 * ms
    )
