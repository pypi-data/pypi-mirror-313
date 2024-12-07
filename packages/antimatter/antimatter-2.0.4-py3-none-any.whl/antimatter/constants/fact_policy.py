from enum import Enum


class FactOperator(str, Enum):
    """
    Enum class for defining the operator of a fact policy.
    """

    Exists = "Exists"
    NotExists = "NotExists"


class FactArgumentSource(str, Enum):
    """
    Enum class for defining the source of a fact policy argument.
    """

    DomainIdentity = "domainIdentity"
    Literal = "literal"
    Any = "any"
