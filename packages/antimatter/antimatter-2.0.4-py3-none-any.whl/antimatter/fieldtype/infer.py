import datetime
import decimal
from typing import Any

from antimatter import errors
from antimatter.fieldtype.fieldtypes import FieldType


def infer_fieldtype(field: Any) -> FieldType:
    """
    Convenience handler for inferring the FieldType from an instance of a data
    field. Supported data types include scalar python values, decimal types,
    and datetime types

    :param field: a field data value
    :return: the FieldType inferred from the field
    """
    if isinstance(field, str):
        return FieldType.String
    elif isinstance(field, bytes):
        return FieldType.Bytes
    elif isinstance(field, bool):
        return FieldType.Bool
    elif isinstance(field, int):
        return FieldType.Int
    elif isinstance(field, float):
        return FieldType.Float
    elif isinstance(field, decimal.Decimal):
        return FieldType.Decimal
    elif isinstance(field, datetime.datetime):  # needs to be checked before datetime.date
        return FieldType.DateTime
    elif isinstance(field, datetime.date):
        return FieldType.Date
    elif isinstance(field, datetime.time):
        return FieldType.Time
    elif isinstance(field, datetime.timedelta):
        return FieldType.Timedelta

    raise errors.DataFormatError(f"field '{field}' has an unsupported type: {type(field)}")
