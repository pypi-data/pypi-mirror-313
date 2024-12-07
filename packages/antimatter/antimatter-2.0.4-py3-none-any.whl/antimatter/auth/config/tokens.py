from enum import Enum
from typing import Any, Dict, List, Callable, Type
from dataclasses import dataclass, asdict


class OidcTokenFactory:
    """
    The token factory for converting config file keywords or CLI keywords into
    specific token formats.
    """

    @staticmethod
    def from_dict_type(token_type: str) -> Type["OidcToken"]:
        t = OidcTokenType(token_type)  # We'll raise an error here if the token type is invalid
        if t is OidcTokenType.Google:
            return GoogleOidcToken
        if t is OidcTokenType.Static:
            return StaticToken
        assert False  # Should be unreachable

    @staticmethod
    def from_cli_type(cli_type: str) -> Type["OidcToken"]:
        if cli_type == "google":
            return GoogleOidcToken
        if cli_type == "static":
            return StaticToken
        raise ValueError(f"'{cli_type}' is not a supported token type")


class OidcTokenType(str, Enum):
    """
    The enumerated supported OIDC token types.
    """

    Google = "GoogleToken"
    Static = "StaticToken"


class OidcToken:
    """
    The base OIDC token.
    """

    type: OidcTokenType
    observers: List[Callable] = []

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def from_dict(json: Dict[str, Any]) -> "OidcToken":
        token_type = json.get("type")

        cls = OidcTokenFactory.from_dict_type(token_type)
        if cls:
            return cls.from_dict(json)
        raise ValueError(f"Unsupported token type: {token_type}")

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("must serialize specific token type")

    def add_observer(self, observer: Callable):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer()


@dataclass
class StaticToken(OidcToken):
    """
    A static oauth token format.
    """

    token: str
    type: OidcTokenType = OidcTokenType.Static

    def to_dict(self) -> Dict[str, Any]:
        json = asdict(self)
        json["type"] = self.type.value
        return json

    @staticmethod
    def from_dict(json: Dict[str, Any]) -> "StaticToken":
        return StaticToken(**json)


@dataclass
class GoogleOidcToken(OidcToken):
    """
    The Google OIDC token format.
    """

    access_token: str
    id_token: str
    refresh_token: str
    expires_at: int
    type: OidcTokenType = OidcTokenType.Google

    def to_dict(self) -> Dict[str, Any]:
        json = asdict(self)
        json["type"] = self.type.value
        return json

    @staticmethod
    def from_dict(json: Dict[str, Any]) -> "GoogleOidcToken":
        return GoogleOidcToken(
            access_token=json["access_token"],
            id_token=json["id_token"],
            refresh_token=json["refresh_token"],
            expires_at=json["expires_at"],
            type=OidcTokenType.Google,
        )

    @staticmethod
    def init() -> "GoogleOidcToken":
        return GoogleOidcToken(
            access_token=None, id_token=None, refresh_token=None, expires_at=None, type=OidcTokenType.Google
        )
