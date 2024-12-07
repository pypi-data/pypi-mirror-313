from enum import Enum


class CapabilityOperator(str, Enum):
    """
    Enum class for defining the operator of the match expression.

    """

    In = "In"
    NotIn = "NotIn"
    Exists = "Exists"
    NotExists = "NotExists"
