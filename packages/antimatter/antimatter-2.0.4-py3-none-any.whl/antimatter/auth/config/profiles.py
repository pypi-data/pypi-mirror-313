from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional
from antimatter.auth.config.tokens import OidcToken


@dataclass
class Profile:
    """
    Profile structure, containing the name, domain ID, API key, default
    read and write contexts and token
    """

    name: str
    domain_id: str
    api_key: str
    default_read_context: Optional[str]
    default_write_context: Optional[str]
    token: Optional[OidcToken]
    idp: Optional[str]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Profile":
        if data is None:
            return None
        data["oidc_token"] = OidcToken.from_dict(data["oidc_token"]) if data.get("oidc_token") else None

        return Profile(
            name=data["name"],
            domain_id=data["domain_id"],
            api_key=data["api_key"],
            default_read_context=data.get("default_read_context"),
            default_write_context=data.get("default_write_context"),
            idp=data.get("idp", None),
            token=data["oidc_token"],
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        del d["token"]
        d["oidc_token"] = self.token.to_dict() if self.token else None
        return d
