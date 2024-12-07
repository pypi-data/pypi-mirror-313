from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Union
from unittest.mock import Mock, patch, MagicMock

import pytest
from dateutil.relativedelta import relativedelta

from antimatter.utils.time import (
    get_time_range,
    normalize_datetime,
    normalize_duration,
    parse_datetime,
    parse_duration,
)

# Local timezone offset
_l_off = datetime.now().astimezone().tzinfo.utcoffset(None)


@pytest.mark.parametrize(
    ("start_date", "end_date", "duration", "expected"),
    (
        (None, None, None, (None, None)),
        (
            datetime(2020, 10, 1, tzinfo=timezone.utc),
            datetime(2022, 5, 1, tzinfo=timezone.utc),
            timedelta(5, 50),
            (datetime(2020, 10, 1, tzinfo=timezone.utc), datetime(2022, 5, 1, tzinfo=timezone.utc)),
        ),
        (None, None, timedelta(5, 50), (datetime(2024, 5, 17, 11, 59, 10, 0, tzinfo=timezone.utc), None)),
        (
            None,
            datetime(2022, 5, 6, tzinfo=timezone.utc),
            timedelta(5),
            (datetime(2022, 5, 1, tzinfo=timezone.utc), datetime(2022, 5, 6, tzinfo=timezone.utc)),
        ),
        (
            datetime(2022, 5, 1, tzinfo=timezone.utc),
            None,
            timedelta(5),
            (datetime(2022, 5, 1, tzinfo=timezone.utc), datetime(2022, 5, 6, tzinfo=timezone.utc)),
        ),
    ),
    ids=(
        "start_date, end_date, duration are all None",
        "start_date, end_date, duration all have values",
        "start_date and end_date None; duration has a value",
        "start_date None; end_date and duration have values",
        "end_date None; start_date and duration have values",
    ),
)
@patch("antimatter.utils.time.datetime", wraps=datetime)
def test_get_time_range(
    mock_time,
    start_date: Optional[Union[datetime, str]],
    end_date: Optional[Union[datetime, str]],
    duration: Optional[Union[timedelta, relativedelta, str]],
    expected: Tuple[Optional[datetime], Optional[datetime]],
):
    mock_time.now.return_value = datetime(2024, 5, 22, 12, 0, 0, 0, tzinfo=timezone.utc)

    norm_start, norm_end = get_time_range(start_date, end_date, duration)
    assert norm_start == expected[0]
    assert norm_end == expected[1]


@pytest.mark.parametrize(
    ("dt", "expected"),
    (
        (None, None),
        (
            "2014-05-03",
            datetime(2014, 5, 3, tzinfo=timezone.utc) - _l_off,
        ),
        (
            "2014-05-03T12:05:11",
            datetime(2014, 5, 3, 12, 5, 11, tzinfo=timezone.utc) - _l_off,
        ),
        (
            "2014-05-03T12:05:11+08",
            datetime(2014, 5, 3, 4, 5, 11, tzinfo=timezone.utc),
        ),
        (
            "2014-05-03T12:05:11Z",
            datetime(2014, 5, 3, 12, 5, 11, tzinfo=timezone.utc),
        ),
        (
            datetime(2014, 5, 3),
            datetime(2014, 5, 3, tzinfo=timezone.utc) - _l_off,
        ),
        (
            datetime(2014, 5, 3, 6, tzinfo=timezone(timedelta(hours=-4))),
            datetime(2014, 5, 3, 10, tzinfo=timezone.utc),
        ),
    ),
    ids=(
        "datetime is None",
        "datetime is date string",
        "datetime is datetime string without timezone",
        "datetime is datetime string with timezone",
        "datetime is datetime string with UTC timezone",
        "datetime is timezone naive datetime",
        "datetime is timezone aware datetime",
    ),
)
def test_normalize_datetime(dt: Optional[Union[datetime, str]], expected: Optional[datetime]):
    norm = normalize_datetime(dt)
    assert norm == expected
    if expected is not None:
        assert (
            norm.tzinfo is not None and norm.tzinfo.utcoffset(norm) is not None,
            "normalized datetime must be timezone aware",
        )


@pytest.mark.parametrize(
    ("dt", "expected"),
    (
        ("2020", datetime(2020, 1, 1, tzinfo=timezone.utc) - _l_off),
        ("2020-02", datetime(2020, 2, 1, tzinfo=timezone.utc) - _l_off),
        ("2020-2", datetime(2020, 2, 1, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05", datetime(2020, 2, 5, tzinfo=timezone.utc) - _l_off),
        ("2020-2-5", datetime(2020, 2, 5, tzinfo=timezone.utc) - _l_off),
        ("2020-02-5", datetime(2020, 2, 5, tzinfo=timezone.utc) - _l_off),
        ("2020-2-05", datetime(2020, 2, 5, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05 15", datetime(2020, 2, 5, 15, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05T15", datetime(2020, 2, 5, 15, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05t15", datetime(2020, 2, 5, 15, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05 15:45", datetime(2020, 2, 5, 15, 45, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05T15:45", datetime(2020, 2, 5, 15, 45, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05 15:45:30", datetime(2020, 2, 5, 15, 45, 30, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05T15:45:30", datetime(2020, 2, 5, 15, 45, 30, tzinfo=timezone.utc) - _l_off),
        ("2020-02-05T15:45:30.1", datetime(2020, 2, 5, 15, 45, 30, 100000, tzinfo=timezone.utc) - _l_off),
        (
            "2020-02-05 15:45:30.123456",
            datetime(2020, 2, 5, 15, 45, 30, 123456, tzinfo=timezone.utc) - _l_off,
        ),
        ("2020-02-05T15:45:30.123Z", datetime(2020, 2, 5, 15, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123z", datetime(2020, 2, 5, 15, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123+08:00", datetime(2020, 2, 5, 7, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123+08:30", datetime(2020, 2, 5, 7, 15, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123+08", datetime(2020, 2, 5, 7, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123+8", datetime(2020, 2, 5, 7, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123+8:30", datetime(2020, 2, 5, 7, 15, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123-08:00", datetime(2020, 2, 5, 23, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123-08", datetime(2020, 2, 5, 23, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05T15:45:30.123-8", datetime(2020, 2, 5, 23, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-02-05 15:45:30.123-08:00", datetime(2020, 2, 5, 23, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-2-5T15:45:30.123-08:00", datetime(2020, 2, 5, 23, 45, 30, 123000, tzinfo=timezone.utc)),
        ("2020-2-5 15:45:30.123-08:00", datetime(2020, 2, 5, 23, 45, 30, 123000, tzinfo=timezone.utc)),
    ),
)
def test_parse_datetime(dt: Optional[str], expected: Optional[datetime]):
    parsed = parse_datetime(dt)
    assert parsed == expected


@pytest.mark.parametrize(
    ("duration", "expected"),
    (
        (None, None),
        ("24h33m12s", relativedelta(hours=24, minutes=33, seconds=12)),
        (
            timedelta(days=3, hours=10, minutes=11, seconds=2, milliseconds=10, microseconds=5),
            relativedelta(days=3, hours=10, minutes=11, seconds=2, microseconds=10005),
        ),
        (
            relativedelta(microseconds=295862010005),
            relativedelta(days=3, hours=10, minutes=11, seconds=2, microseconds=10005),
        ),
    ),
    ids=(
        "duration is None",
        "duration is string",
        "duration is timedelta",
        "duration is relativedelta",
    ),
)
def test_normalize_duration(
    duration: Optional[Union[timedelta, relativedelta, str]],
    expected: Optional[relativedelta],
):
    norm = normalize_duration(duration)
    assert norm == expected


@pytest.mark.parametrize(
    ("duration", "expected", "error"),
    (
        (None, None, False),
        (
            "1y2mo3d4h5m6s7ms8us",
            relativedelta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6, microseconds=7008),
            False,
        ),
        (
            "1y2mo3d4h5m6s7ms8µs",
            relativedelta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6, microseconds=7008),
            False,
        ),
        ("4mo1h55ms", relativedelta(months=4, hours=1, microseconds=55000), False),
        ("32s", relativedelta(seconds=32), False),
        ("910543m", relativedelta(minutes=910543), False),
        ("5", None, True),
        ("1n", None, True),
        ("2S", None, True),
        ("5mo1y", None, True),
        ("1y2y", None, True),
        ("5s103ms14us14µs", None, True),
        ("50.34s", None, True),
    ),
    ids=(
        "None duration",
        "all unit arguments",
        "all unit arguments (µs instead of us)",
        "some unit arguments",
        "single unit argument",
        "long unit argument",
        "error when no units",
        "error when invalid unit",
        "error when uppercase",
        "error when units out of order",
        "error when units repeated",
        "error when 'us' and 'µs' units",
        "error when decimal places used",
    ),
)
def test_parse_duration(duration: Optional[str], expected: Optional[relativedelta], error: bool):
    if error:
        with pytest.raises(ValueError):
            parse_duration(duration)
    else:
        parsed = parse_duration(duration)
        assert parsed == expected
