from typing import Optional

import antimatter_engine as am

import antimatter_api as openapi_client
from antimatter.authn import Authentication
from antimatter.utils import authenticate, decode_token, get_base_client, is_token_valid
from antimatter.utils.user_agent import get_user_agent


class ApiKeyAuthentication(Authentication):
    """
    This is an agent which uses an API key for authentication.
    """

    def __init__(
        self,
        domain_id: str = None,
        api_key: str = None,
        admin_email: Optional[str] = None,
        enable_retries: bool = True,
    ):
        self._api_key = api_key
        self._domain_id = domain_id
        self._token = None
        self._session = None
        self._email = admin_email
        self._enable_retries = enable_retries

    def needs_refresh(self):
        return not is_token_valid(*decode_token(self._token))

    def authenticate(self, token_lifetime: Optional[int] = None):
        self._token = authenticate(
            client=get_base_client(self._enable_retries),
            domain_id=self._domain_id,
            domain_authenticate=openapi_client.DomainAuthenticate(token=self._api_key),
            token_lifetime=token_lifetime,
        )

    def get_token(self):
        if self.needs_refresh():
            self.authenticate()
        return self._token

    def get_token_scope(self):
        return "domain_identity"

    def get_session(self):
        token = self.get_token()
        # Use the session if it already exists to reuse its cache
        if self._session is None:
            self._session = am.PySession.new_from_bearer_access_token(
                self._domain_id,
                token,
                get_user_agent(),
            )
        else:
            self._session.set_bearer_access_token(token)
        return self._session

    def get_domain_id(self):
        return self._domain_id

    def get_email(self):
        return self._email

    def has_client_retry_policy(self) -> bool:
        return self._enable_retries
