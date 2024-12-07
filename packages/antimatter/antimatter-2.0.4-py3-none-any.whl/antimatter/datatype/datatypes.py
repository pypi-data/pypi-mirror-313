import re
from enum import Enum, auto, unique


@unique
class Datatype(str, Enum):
    """
    Datatype is an enumeration of the compatible datatypes supported by
    antimatter, plus the 'Unknown' default placeholder.
    """

    def _generate_next_value_(self, start, count, last_values):
        return re.sub(r"(?<=[a-z])(?=[A-Z])|[^a-zA-Z]", "_", self).strip("_").lower()

    Unknown = auto()
    Scalar = auto()
    Dict = auto()
    DictList = auto()
    PandasDataframe = auto()
    PytorchDataLoader = auto()
    LangchainRetriever = auto()
