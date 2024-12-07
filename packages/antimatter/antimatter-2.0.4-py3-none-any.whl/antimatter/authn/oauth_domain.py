from typing import Optional

import antimatter_engine as am
from antimatter.authn import Authentication, OAuthAuthentication
from antimatter.utils import decode_token, is_token_valid, authenticate, get_base_client
import antimatter_api as openapi_client
from antimatter.utils.user_agent import get_user_agent


class OAuthDomainAuthentication(Authentication):
    """
    A domain authentication class which uses an oauth token for authentication.
    This class uses the oauth id token obtained from its parent to transmute them into a domain identity token.
    It uses the identity provider name "google" by default to authenticate the domain.
    """

    def __init__(
        self,
        domain_id: str,
        oauth_authentication: OAuthAuthentication,
        identity_provider_name: Optional[str] = None,
    ):
        if not isinstance(oauth_authentication, OAuthAuthentication):
            raise ValueError("oauth_authentication must be an instance of OAuthAuthentication")
        self.domain_id = domain_id
        self.oauth_authentication = oauth_authentication
        self.identity_provider_name = identity_provider_name
        self._session = None
        self._token = None

    def authenticate(self, token_lifetime: Optional[int] = None):
        oauth_token = self.oauth_authentication.get_token()
        self._token = authenticate(
            client=get_base_client(self.has_client_retry_policy()),
            domain_id=self.domain_id,
            domain_authenticate=openapi_client.DomainAuthenticate(token=oauth_token),
            identity_provider_name=self.identity_provider_name,
            token_lifetime=token_lifetime,
        )

    def get_token(self):
        if self.needs_refresh():
            self.authenticate()
        return self._token

    def needs_refresh(self):
        needs_refresh = self.oauth_authentication.needs_refresh() or not is_token_valid(
            *decode_token(self._token)
        )
        return needs_refresh

    def get_token_scope(self):
        return "domain_identity"

    def get_session(self):
        token = self.get_token()
        # Use the session if it already exists to reuse its cache
        if self._session is None:
            self._session = am.PySession.new_from_bearer_access_token(
                self.domain_id,
                token,
                get_user_agent(),
            )
        else:
            self._session.set_bearer_access_token(token)
        return self._session

    def get_domain_id(self):
        return self.domain_id

    def get_email(self):
        raise Exception("Email cannot be retrieved for domain identity token")

    def has_client_retry_policy(self) -> bool:
        return self.oauth_authentication.has_client_retry_policy()
