import datetime
import decimal
import os

import pytest

from antimatter import errors
from antimatter.handlers import ScalarHandler


class TestScalar:
    @pytest.mark.parametrize(
        "data",
        (
            "",
            os.urandom(16 * 1024),
            "value",
            404,
            100.01,
            decimal.Decimal(100.01),
            datetime.date(2000, 10, 31),
            datetime.datetime(2000, 10, 31, 5, 30),
            datetime.time(10, 10, 31, 5),
            datetime.timedelta(10, 10, 31),
            "[{'val':1}]",
        ),
        ids=(
            "empty string",
            "bytes value",
            "non-empty string",
            "integer value",
            "float value",
            "decimal value",
            "date value",
            "datetime value",
            "time value",
            "timedelta value",
            "string that looks like json",
        ),
    )
    def test_lossless_conversions(self, data):
        handler = ScalarHandler()
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
            handler = ScalarHandler()
            _ = handler.to_generic([])
