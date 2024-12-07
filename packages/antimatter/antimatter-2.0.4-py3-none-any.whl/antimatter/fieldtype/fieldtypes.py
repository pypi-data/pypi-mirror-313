import re
from enum import Enum, auto, unique


@unique
class FieldType(str, Enum):
    """
    FieldType is an enumeration of the compatible field types supported by
    antimatter.
    """

    def _generate_next_value_(self, start, count, last_values):
        return re.sub(r"(?<=[a-z0-9])(?=[A-Z])|[^a-zA-Z0-9]", "_", self).strip("_").lower()

    String = auto()
    Bytes = auto()
    Bool = auto()
    Int = auto()
    Float = auto()
    Date = auto()
    DateTime = auto()
    Time = auto()
    Timestamp = auto()
    Timedelta = auto()
    Decimal = auto()
