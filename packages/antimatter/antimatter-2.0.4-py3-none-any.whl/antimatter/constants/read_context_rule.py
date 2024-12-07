from enum import Enum


class Source(str, Enum):
    """
    Enum class for defining the source of the match expression.
    """

    DomainIdentity = "domainIdentity"
    ReadParameters = "readParameters"
    Tags = "tags"
    Literal = "literal"


class Operator(str, Enum):
    """
    Enum class for defining the operator of the match expression.
    """

    In = "In"
    NotIn = "NotIn"
    Exists = "Exists"
    NotExists = "NotExists"
    DateDeltaLessThan = "DateDeltaLessThan"
    DateDeltaGreaterThan = "DateDeltaGreaterThan"
    Any = "Any"


class Action(str, Enum):
    """
    Enum class for defining the action of the rule.
    """

    DenyCapsule = "DenyCapsule"
    DenyRecord = "DenyRecord"
    Redact = "Redact"
    Tokenize = "Tokenize"
    Allow = "Allow"


class TokenScope(str, Enum):
    """
    Enum class for defining the scope of the token.
    """

    Unique = "unique"
    Capsule = "capsule"
    Domain = "domain"


class TokenFormat(str, Enum):
    """
    Enum class for defining the format of the token.
    """

    Explicit = "explicit"
    Synthetic = "synthetic"
