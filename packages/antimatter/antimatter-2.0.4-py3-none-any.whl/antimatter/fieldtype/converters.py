import datetime
import decimal
from typing import Any, Callable, Optional

from antimatter.fieldtype.fieldtypes import FieldType


class Standard:
    @staticmethod
    def field_converter_from_generic(ft: FieldType) -> Optional[Callable[[bytes], Any]]:
        """
        field_converter_from_generic gets a field converter function for the
        given field type that can be used to convert fields from their generic
        string type to their specific type.

        :param ft: the FieldType to get the converter function for
        :return: a function that can convert field values from generic form
        """
        # In all the lambdas below, if the value is 'redacted', it should be converted
        # to a default redacted value based on the FieldType
        redacted = b"{redacted}"
        if ft is FieldType.String:
            return lambda x: x.decode("utf-8", errors="replace")
        elif ft is FieldType.Bytes:
            return lambda x: bytes(x)
        elif ft is FieldType.Bool:
            return lambda x: False if redacted in x else x == b"True"
        elif ft is FieldType.Int:
            return lambda x: 0 if redacted in x else int(x.decode("utf-8", errors="replace"))
        elif ft is FieldType.Timestamp:
            return lambda x: 0 if redacted in x else int(x.decode("utf-8", errors="replace"))
        elif ft is FieldType.Float:
            return lambda x: 0.0 if redacted in x else float(x.decode("utf-8", errors="replace"))
        elif ft is FieldType.Decimal:
            return lambda x: (
                decimal.Decimal(0) if redacted in x else decimal.Decimal(x.decode("utf-8", errors="replace"))
            )
        elif ft is FieldType.Date:
            return lambda x: (
                datetime.date(1970, 1, 1)
                if redacted in x
                else datetime.date.fromisoformat(x.decode("utf-8", errors="replace"))
            )
        elif ft is FieldType.DateTime:
            return lambda x: (
                datetime.datetime(1970, 1, 1)
                if redacted in x
                else datetime.datetime.fromisoformat(x.decode("utf-8", errors="replace"))
            )
        elif ft is FieldType.Time:
            return lambda x: (
                datetime.time(0, 0, 0)
                if redacted in x
                else datetime.time.fromisoformat(x.decode("utf-8", errors="replace"))
            )
        elif ft is FieldType.Timedelta:
            return lambda x: (
                datetime.timedelta(0)
                if redacted in x
                else datetime.timedelta(microseconds=int(x.decode("utf-8", errors="replace")) / 1000)
            )

        return None

    @staticmethod
    def field_converter_to_generic(ft: FieldType) -> Optional[Callable[[Any], bytes]]:
        """
        field_converter_to_generic gets a field converter function for the given
        field type that can be used to convert fields from their specific type
        to their generic type.

        :param ft: the FieldType to get the converter function for
        :return: a function that can convert field values to generic form
        """
        if ft is FieldType.String:
            return lambda x: x.encode("utf-8")
        elif ft is FieldType.Bytes:
            return lambda x: x
        elif ft in [FieldType.Float, FieldType.Decimal, FieldType.Bool, FieldType.Timestamp, FieldType.Int]:
            return lambda x: str(x).encode("utf-8")
        elif ft in [FieldType.Date, FieldType.Time, FieldType.DateTime]:
            return lambda x: x.isoformat().encode("utf-8")
        elif ft is FieldType.Timedelta:
            return lambda x: str(
                (x.days * 86_400_000_000 + x.seconds * 1_000_000 + x.microseconds) * 1000
            ).encode("utf-8")

        return None
