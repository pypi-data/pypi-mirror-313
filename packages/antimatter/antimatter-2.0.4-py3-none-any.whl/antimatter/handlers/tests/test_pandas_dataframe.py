import datetime
import decimal

import numpy as np
import pandas as pd
import pyarrow
import pytest

from antimatter import errors
from antimatter.handlers import PandasDataFrame


class TestPandasDataFrame:
    @pytest.mark.parametrize(
        "data",
        (
            pd.DataFrame(),
            pd.DataFrame([]),
            pd.DataFrame([{"a": "1", "b": "2", "c": "4"}]),
            pd.DataFrame({"a": ["1", "5", "4"], "b": ["2", "7", "8"], "c": ["4", "3", "0"]}),
            pd.DataFrame(
                [{"a": "1", "b": "2", "c": "4", "d": "6"}, {"a": "5", "b": "3", "c": "1", "d": "8"}]
            ),
            pd.DataFrame([{"a": True, "b": True, "c": False}, {"a": True, "b": False, "c": True}]),
            pd.DataFrame([{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}]),
            pd.DataFrame(
                [{"a": 1.4, "b": 2.9, "c": 4.4, "d": 6.6}, {"a": 5.3, "b": 3.6, "c": 1.1, "d": 8.5}]
            ),
            pd.DataFrame(
                [
                    {"a": decimal.Decimal(1.4), "b": decimal.Decimal(2.9), "c": decimal.Decimal(4.4)},
                    {"a": decimal.Decimal(5.3), "b": decimal.Decimal(3.6), "c": decimal.Decimal(1.1)},
                    {"a": decimal.Decimal(0.8), "b": decimal.Decimal(7.1), "c": decimal.Decimal(6.2)},
                ]
            ),
            pd.DataFrame(
                [
                    {"a": datetime.date(2000, 1, 4), "b": datetime.date(2000, 2, 12)},
                    {"a": datetime.date(2002, 1, 4), "b": datetime.date(2002, 2, 12)},
                ]
            ),
            pd.DataFrame(
                [
                    {
                        "a": datetime.datetime(2000, 1, 4, 10, 33),
                        "b": datetime.datetime(2000, 2, 12, 9, 11),
                    },
                    {
                        "a": datetime.datetime(2002, 1, 4, 12, 30),
                        "b": datetime.datetime(2002, 2, 12, 9, 18),
                    },
                ]
            ),
            pd.DataFrame(
                [
                    {"a": datetime.time(1, 4), "b": datetime.time(2, 12)},
                    {"a": datetime.time(1, 4), "b": datetime.time(2, 12)},
                ]
            ),
            pd.DataFrame(
                [
                    {"a": datetime.timedelta(1, 4), "b": datetime.timedelta(2, 12)},
                    {"a": datetime.timedelta(1, 4), "b": datetime.timedelta(2, 12)},
                ]
            ),
            pd.DataFrame(
                [{"a": True, "b": True, "c": False}, {"a": True, "b": False, "c": True}], dtype=np.bool_
            ),
            pd.DataFrame([{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.int_),
            pd.DataFrame([{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.int8),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.int16
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.int32
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.int64
            ),
            pd.DataFrame([{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.uint),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.uint8
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.uint16
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.uint32
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}], dtype=np.uint64
            ),
            pd.DataFrame([{"a": 1.4, "b": 2.9, "c": 4.4}, {"a": 5.3, "b": 3.6, "c": 1.1}], dtype=np.float_),
            pd.DataFrame([{"a": 1.4, "b": 2.9, "c": 4.4}, {"a": 5.3, "b": 3.6, "c": 1.1}], dtype=np.float32),
            pd.DataFrame([{"a": 1.4, "b": 2.9, "c": 4.4}, {"a": 5.3, "b": 3.6, "c": 1.1}], dtype=np.float64),
            pd.DataFrame([{"a": "1", "b": "2", "c": "4"}, {"a": "5", "b": "3", "c": "1"}], dtype=np.str_),
            pd.DataFrame(
                [
                    {"a": np.datetime64("2020-05-03T12:33:42"), "b": np.datetime64("2022-03-02T09:13:15")},
                    {"a": np.datetime64("2021-10-19T02:54:11"), "b": np.datetime64("1989-02-01T07:19:51")},
                ]
            ),
            pd.DataFrame(
                [
                    {
                        "a": np.timedelta64(datetime.timedelta(1, 4)),
                        "b": np.timedelta64(datetime.timedelta(2, 12)),
                    },
                    {
                        "a": np.timedelta64(datetime.timedelta(1, 4)),
                        "b": np.timedelta64(datetime.timedelta(2, 12)),
                    },
                ]
            ),
            pd.DataFrame(
                [{"a": True, "b": True, "c": False}, {"a": True, "b": False, "c": True}],
                dtype=pd.ArrowDtype(pyarrow.bool_()),
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}],
                dtype=pd.ArrowDtype(pyarrow.int8()),
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}],
                dtype=pd.ArrowDtype(pyarrow.int16()),
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}],
                dtype=pd.ArrowDtype(pyarrow.int32()),
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}],
                dtype=pd.ArrowDtype(pyarrow.int64()),
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}],
                dtype=pd.ArrowDtype(pyarrow.uint8()),
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}],
                dtype=pd.ArrowDtype(pyarrow.uint16()),
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}],
                dtype=pd.ArrowDtype(pyarrow.uint32()),
            ),
            pd.DataFrame(
                [{"a": 1, "b": 2, "c": 4, "d": 6}, {"a": 5, "b": 3, "c": 1, "d": 8}],
                dtype=pd.ArrowDtype(pyarrow.uint64()),
            ),
            pd.DataFrame(
                [{"a": 1.4, "b": 2.9, "c": 4.4, "d": 6.6}, {"a": 5.3, "b": 3.6, "c": 1.1, "d": 8.5}],
                dtype=pd.ArrowDtype(pyarrow.float32()),
            ),
            pd.DataFrame(
                [{"a": 1.4, "b": 2.9, "c": 4.4, "d": 6.6}, {"a": 5.3, "b": 3.6, "c": 1.1, "d": 8.5}],
                dtype=pd.ArrowDtype(pyarrow.float64()),
            ),
            pd.DataFrame(
                [
                    {"a": datetime.time(1, 4), "b": datetime.time(2, 12)},
                    {"a": datetime.time(1, 4), "b": datetime.time(2, 12)},
                ],
                dtype=pd.ArrowDtype(pyarrow.time32("s")),
            ),
            pd.DataFrame(
                [
                    {"a": datetime.time(1, 4), "b": datetime.time(2, 12)},
                    {"a": datetime.time(1, 4), "b": datetime.time(2, 12)},
                ],
                dtype=pd.ArrowDtype(pyarrow.time64("ns")),
            ),
            pd.DataFrame(
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
                dtype=pd.ArrowDtype(pyarrow.timestamp("s")),
            ),
            pd.DataFrame(
                [
                    {"a": datetime.date(2000, 1, 4), "b": datetime.date(2000, 2, 12)},
                    {"a": datetime.date(2002, 1, 4), "b": datetime.date(2002, 2, 12)},
                ],
                dtype=pd.ArrowDtype(pyarrow.date32()),
            ),
            pd.DataFrame(
                [
                    {"a": datetime.date(2000, 1, 4), "b": datetime.date(2000, 2, 12)},
                    {"a": datetime.date(2002, 1, 4), "b": datetime.date(2002, 2, 12)},
                ],
                dtype=pd.ArrowDtype(pyarrow.date64()),
            ),
            pd.DataFrame(
                [
                    {"a": datetime.timedelta(1, 4), "b": datetime.timedelta(2, 12)},
                    {"a": datetime.timedelta(1, 4), "b": datetime.timedelta(2, 12)},
                ],
                dtype=pd.ArrowDtype(pyarrow.duration("s")),
            ),
            # TODO (SKIPPED): this one isn't recreated completely correctly by pandas, and an equality check will fail
            # pd.DataFrame(
            #     [{"a": "1", "b": "2", "c": "4"}, {"a": "5", "b": "3", "c": "1"}],
            #     dtype=pd.ArrowDtype(pyarrow.string())
            # ),
            pd.DataFrame(
                [{"a": 1.4, "b": 2.9, "c": 4.4, "d": 6.6}, {"a": 5.3, "b": 3.6, "c": 1.1, "d": 8.5}],
                dtype=pd.ArrowDtype(pyarrow.decimal128(5, 2)),
            ),
        ),
        ids=(
            "dataframe with no data",
            "dataframe data of one empty list",
            "dataframe data of list with one dictionary with string values",
            "dataframe data of one dictionary with string values",
            "dataframe data of multiples dictionaries with string values",
            "dataframe data of multiples dictionaries with bool values",
            "dataframe data of multiples dictionaries with int values",
            "dataframe data of multiples dictionaries with float values",
            "dataframe data of multiples dictionaries with decimal values",
            "dataframe data of multiples dictionaries with date values",
            "dataframe data of multiples dictionaries with datetime values",
            "dataframe data of multiples dictionaries with time values",
            "dataframe data of multiples dictionaries with timedelta values",
            "dataframe data of multiples dictionaries with np bool values",
            "dataframe data of multiples dictionaries with np int values",
            "dataframe data of multiples dictionaries with np int8 values",
            "dataframe data of multiples dictionaries with np int16 values",
            "dataframe data of multiples dictionaries with np int32 values",
            "dataframe data of multiples dictionaries with np int64 values",
            "dataframe data of multiples dictionaries with np uint values",
            "dataframe data of multiples dictionaries with np uint8 values",
            "dataframe data of multiples dictionaries with np uint16 values",
            "dataframe data of multiples dictionaries with np uint32 values",
            "dataframe data of multiples dictionaries with np uint64 values",
            "dataframe data of multiples dictionaries with np float values",
            "dataframe data of multiples dictionaries with np float32 values",
            "dataframe data of multiples dictionaries with np float64 values",
            "dataframe data of multiples dictionaries with np str values",
            "dataframe data of multiples dictionaries with np datetime64 values",
            "dataframe data of multiples dictionaries with np timedelta64 values",
            "dataframe data of multiples dictionaries with pyarrow bool values",
            "dataframe data of multiples dictionaries with pyarrow int8 values",
            "dataframe data of multiples dictionaries with pyarrow int16 values",
            "dataframe data of multiples dictionaries with pyarrow int32 values",
            "dataframe data of multiples dictionaries with pyarrow int64 values",
            "dataframe data of multiples dictionaries with pyarrow uint8 values",
            "dataframe data of multiples dictionaries with pyarrow uint16 values",
            "dataframe data of multiples dictionaries with pyarrow uint32 values",
            "dataframe data of multiples dictionaries with pyarrow uint64 values",
            "dataframe data of multiples dictionaries with pyarrow float32 values",
            "dataframe data of multiples dictionaries with pyarrow float64 values",
            "dataframe data of multiples dictionaries with pyarrow time32 values",
            "dataframe data of multiples dictionaries with pyarrow time64 values",
            "dataframe data of multiples dictionaries with pyarrow timestamp values",
            "dataframe data of multiples dictionaries with pyarrow date32 values",
            "dataframe data of multiples dictionaries with pyarrow date64 values",
            "dataframe data of multiples dictionaries with pyarrow duration values",
            # "dataframe data of multiples dictionaries with pyarrow string values",
            "dataframe data of multiples dictionaries with pyarrow decimal128 values",
        ),
    )
    def test_lossless_conversions(self, data):
        handler = PandasDataFrame()
        cols, rows, extra = handler.to_generic(data)

        # Assert it's actually converting to generic
        for row in rows:
            for val in row:
                assert isinstance(val, bytes)

        # Assert the conversion is lossless
        rebuilt = handler.from_generic(cols, rows, extra)
        assert np.array_equal(rebuilt.values, data.values)
        assert rebuilt.dtypes.equals(data.dtypes)

    def test_invalid_type(self):
        with pytest.raises(errors.DataFormatError):
            handler = PandasDataFrame()
            _ = handler.to_generic(pd.DataFrame({"a": [[], [], []]}))

    def test_inconsistent_type(self):
        data = pd.DataFrame(
            [
                {"a": "1", "b": 2, "c": 3.2},
                {"a": "1", "b": 2, "c": "hello"},
            ]
        )

        with pytest.raises(ValueError):
            handler = PandasDataFrame()
            cols, rows, extra = handler.to_generic(data)
            rebuilt = handler.from_generic(cols, rows, extra)
            assert rebuilt == data
