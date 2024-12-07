from enum import Enum, auto


class Location(str, Enum):
    """
    Location is an enumeration of the compatible local and remote locations
    supported by antimatter, plus the 'Unknown' default placeholder.
    """

    Unknown = auto()
    File = auto()
    S3 = auto()
    GCS = auto()
