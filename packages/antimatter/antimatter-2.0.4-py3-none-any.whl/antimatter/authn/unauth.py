from typing import Optional

from antimatter.authn import Authentication


class Unauthenticated(Authentication):
    """
    An unauthenticated agent which does not have any authentication.
    Can be used to create a session for an unauthenticated user.
    """

    def __init__(self, admin_email: Optional[str] = None, enable_retries: bool = True):
        self._email = admin_email
        self._enable_retries = enable_retries

    def authenticate(self, **kwargs):
        pass

    def get_token(self):
        return None

    def needs_refresh(self):
        return False

    def get_token_scope(self):
        return None

    def get_session(self):
        raise Exception("Unauthenticated session cannot be created")

    def get_domain_id(self):
        return None

    def get_email(self):
        return self._email

    def has_client_retry_policy(self) -> bool:
        return self._enable_retries
