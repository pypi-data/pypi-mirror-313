from enum import Enum


class ProviderType(str, Enum):
    """
    Enum class for defining the type of identity provider.
    """

    GoogleOAuth = "GoogleOAuth"
    ApiKey = "APIKey"
    MicrosoftOAuth = "MicrosoftOAuth"


class PrincipalType(str, Enum):
    """
    Enum class for defining the principal type.
    """

    ApiKey = "APIKey"
    Email = "Email"
    HostedDomain = "HostedDomain"
