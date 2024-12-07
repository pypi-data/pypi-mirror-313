from dataclasses import dataclass
from typing import Any, Dict, Type

from antimatter.auth.config.tokens import OidcToken, OidcTokenFactory


_NAME_KEY = "name"
_TOKEN_KEY = "token"
_TYPE_KEY = "type"


@dataclass
class GlobalIdentity:
    """
    Global identity structure, containing name and token.
    """

    name: str
    token: OidcToken

    @staticmethod
    def from_dict(identity_dict: Dict[str, Any]) -> "GlobalIdentity":
        """
        Parse a GlobalIdentity from the json. The json must contain a 'token'
        property, which itself must contain a 'type' property that has a value
        that can be parsed into a specific token type.

        :param identity_dict: The json to parse
        :return: The parsed GlobalIdentity
        """
        name = identity_dict.get(_NAME_KEY)
        token = identity_dict.get(_TOKEN_KEY, {})
        token_cls = OidcTokenFactory.from_dict_type(token.get(_TYPE_KEY))
        token = {k: v for k, v in token.items() if k != _TYPE_KEY}
        return GlobalIdentity(name=name, token=token_cls(**token))

    def to_dict(self) -> Dict[str, Any]:
        return {
            _NAME_KEY: self.name,
            _TOKEN_KEY: self.token.to_dict(),
        }
