import datetime
import decimal

import pytest

from antimatter import errors
from antimatter.handlers import Dictionary


class TestDictionary:
    @pytest.mark.parametrize(
        "data",
        (
            {},
            {"a": "1", "b": "2", "c": "4"},
            {"a": 1, "b": 2, "c": 4},
            {"a": 1.4, "b": 2.1, "c": 4.0},
            {"a": decimal.Decimal(1.4), "b": decimal.Decimal(2.1), "c": decimal.Decimal(4.0)},
            {
                "a": datetime.date(2000, 1, 4),
                "b": datetime.date(2000, 2, 12),
                "c": datetime.date(2005, 3, 22),
            },
            {
                "a": datetime.datetime(2000, 1, 4, 0, 30),
                "b": datetime.datetime(2000, 2, 12, 12, 49),
                "c": datetime.datetime(2005, 3, 22, 7, 33, 10, 11),
            },
            {
                "a": datetime.time(0, 30),
                "b": datetime.time(12, 49),
                "c": datetime.time(7, 33, 10, 11),
            },
            {
                "a": datetime.timedelta(0, 30),
                "b": datetime.timedelta(12, 49),
                "c": datetime.timedelta(7, 33, 10, 11),
            },
            {
                "a": "1",
                "b": 2,
                "c": 3.2,
                "d": decimal.Decimal(4.55),
                "e": datetime.date(2023, 12, 30),
                "f": datetime.datetime(2023, 10, 10, 12, 49),
                "g": datetime.time(7, 33, 10, 11),
                "h": datetime.timedelta(7, 33, 10, 11),
            },
        ),
        ids=(
            "empty dictionary",
            "dictionary with string values",
            "dictionary with integer values",
            "dictionary with float values",
            "dictionary with decimal values",
            "dictionary with date values",
            "dictionary with datetime values",
            "dictionary with time values",
            "dictionary with timedelta values",
            "dictionary with mixed value types",
        ),
    )
    def test_lossless_conversions(self, data):
        handler = Dictionary()
        cols, rows, extra = handler.to_generic(data)

        # Assert it's actually converting to generic
        for row in rows:
            for val in row:
                assert isinstance(val, bytes)

        # Assert the conversion is lossless
        rebuilt = handler.from_generic(cols, rows, extra)
        assert rebuilt == data

    def test_invalid_type(self):
        with pytest.raises(errors.DataFormatError):
            handler = Dictionary()
            _ = handler.to_generic({"a": []})
