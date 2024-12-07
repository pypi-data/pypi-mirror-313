from enum import Enum


class Operation(str, Enum):
    """
    Enum class for defining the operation.
    """

    Edit = "edit"
    View = "view"
    Use = "use"


class Result(str, Enum):
    """
    Enum class for defining the result.
    """

    Allow = "allow"
    Deny = "deny"
