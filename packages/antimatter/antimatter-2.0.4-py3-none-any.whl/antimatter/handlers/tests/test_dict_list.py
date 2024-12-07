import datetime
import decimal

import pytest

from antimatter import errors
from antimatter.handlers import DictList


class TestDictList:
    @pytest.mark.parametrize(
        "data",
        (
            [],
            [{}],
            [{"a": "1", "b": "2", "c": "4"}],
            # [
            #     {"a": "1", "b": "2", "c": "4"},
            #     {"a": "5", "b": "3", "d": "8"},
            #     {"a": "0", "b": "7", "c": "6", "d": "9"},
            # ],
            [
                {"a": "1", "b": "2", "c": "4", "d": "6"},
                {"a": "5", "b": "3", "c": "1", "d": "8"},
                {"a": "0", "b": "7", "c": "6", "d": "9"},
            ],
            # [
            #     {"a": 1, "b": 2, "c": 4},
            #     {"a": 5, "b": 3, "c": 1, "d": 8},
            #     {"a": 0, "b": 7, "c": 6, "d": 9},
            # ],
            [
                {"a": 1, "b": 2, "c": 4, "d": 6},
                {"a": 5, "b": 3, "c": 1, "d": 8},
                {"a": 0, "b": 7, "c": 6, "d": 9},
            ],
            [
                {"a": 1.4, "b": 2.9, "c": 4.4, "d": 6.6},
                {"a": 5.3, "b": 3.6, "c": 1.1, "d": 8.5},
                {"a": 0.8, "b": 7.1, "c": 6.2, "d": 9.7},
            ],
            [
                {"a": decimal.Decimal(1.4), "b": decimal.Decimal(2.9), "c": decimal.Decimal(4.4)},
                {"a": decimal.Decimal(5.3), "b": decimal.Decimal(3.6), "c": decimal.Decimal(1.1)},
                {"a": decimal.Decimal(0.8), "b": decimal.Decimal(7.1), "c": decimal.Decimal(6.2)},
            ],
            [
                {"a": datetime.date(2000, 1, 4), "b": datetime.date(2000, 2, 12)},
                {"a": datetime.date(2002, 1, 4), "b": datetime.date(2002, 2, 12)},
            ],
            [
                {
                    "a": datetime.datetime(2000, 1, 4, 10, 33),
                    "b": datetime.datetime(2000, 2, 12, 9, 11),
                },
                {
                    "a": datetime.datetime(2002, 1, 4, 12, 30),
                    "b": datetime.datetime(2002, 2, 12, 9, 18),
                },
            ],
            [
                {"a": datetime.time(1, 4), "b": datetime.time(2, 12)},
                {"a": datetime.time(1, 4), "b": datetime.time(2, 12)},
            ],
            [
                {"a": datetime.timedelta(1, 4), "b": datetime.timedelta(2, 12)},
                {"a": datetime.timedelta(1, 4), "b": datetime.timedelta(2, 12)},
            ],
            [
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
                {
                    "a": "2",
                    "b": 5,
                    "c": 7.3,
                    "d": decimal.Decimal(6.22),
                    "e": datetime.date(2019, 12, 30),
                    "f": datetime.datetime(2019, 10, 10, 12, 49),
                    "g": datetime.time(12, 33, 10, 11),
                    "h": datetime.timedelta(12, 33, 10, 11),
                },
            ],
        ),
        ids=(
            "empty list",
            "list with only empty dictionary",
            "list with one dictionary",
            # "list with dictionaries having variations in keys",
            "list with multiple dictionaries having matching keys and string values",
            # "list with multiple dictionaries having variations in keys and int values",
            "list with multiple dictionaries having matching keys and int values",
            "list with multiple dictionaries having matching keys and float values",
            "list with multiple dictionaries having matching keys and decimal values",
            "list with multiple dictionaries having matching keys and date values",
            "list with multiple dictionaries having matching keys and datetime values",
            "list with multiple dictionaries having matching keys and time values",
            "list with multiple dictionaries having matching keys and timedelta values",
            "list with multiple dictionaries having matching keys and mixed value types",
        ),
    )
    def test_lossless_conversions(self, data):
        handler = DictList()
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
            handler = DictList()
            _ = handler.to_generic([{"a": []}])

    def test_inconsistent_type(self):
        data = [
            {"a": "1", "b": 2, "c": 3.2},
            {"a": "1", "b": 2, "c": "hello"},
        ]

        with pytest.raises(ValueError):
            handler = DictList()
            cols, rows, extra = handler.to_generic(data)
            rebuilt = handler.from_generic(cols, rows, extra)
            assert rebuilt == data
