from antimatter.authn import Authentication, OAuthAuthentication


class OauthGlobalAuthentication(Authentication):
    """
    A global authentication class which uses an oauth token for authentication.
    """

    def __init__(
        self,
        domain_id: str,
        oauth_authentication: OAuthAuthentication,
        identity_provider_name: str = "google",
    ):
        if not isinstance(oauth_authentication, OAuthAuthentication):
            raise ValueError("oauth_authentication must be an instance of OAuthAuthentication")
        self.domain_id = domain_id
        self.oauth_authentication = oauth_authentication
        self.identity_provider_name = identity_provider_name
        self._session = None
        self._token = None

    def get_token(self):
        return self.oauth_authentication.get_token()

    def needs_refresh(self):
        return self.oauth_authentication.needs_refresh()

    def get_token_scope(self):
        return self.oauth_authentication.get_token_scope()

    def get_session(self):
        raise Exception("Session cannot be created for global oauth token")

    def get_domain_id(self):
        raise Exception("Domain id cannot be retrieved for global oauth token")

    def get_email(self):
        return self.oauth_authentication.get_email()

    def authenticate(self, **kwargs):
        self.oauth_authentication.authenticate()

    def has_client_retry_policy(self) -> bool:
        return self.oauth_authentication.has_client_retry_policy()
