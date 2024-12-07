import abc
from typing import Optional

from antimatter.auth.config.tokens import OidcToken


class Authentication(abc.ABC):
    """
    This is an abstract class for authentication. These methods must be implemented by the child classes.
    Authentication should return a domain identity token which can then be used to perform actions on behalf of the domain.
    """

    @abc.abstractmethod
    def authenticate(self, token_lifetime: Optional[int] = None):
        raise NotImplementedError("authenticate method must be implemented")

    @abc.abstractmethod
    def get_token(self):
        raise NotImplementedError("get_token method must be implemented")

    @abc.abstractmethod
    def needs_refresh(self):
        raise NotImplementedError("needs_refresh method must be implemented")

    @abc.abstractmethod
    def get_token_scope(self):
        raise NotImplementedError("get_token_scope method must be implemented")

    @abc.abstractmethod
    def get_session(self):
        raise NotImplementedError("get_session method must be implemented")

    @abc.abstractmethod
    def get_domain_id(self):
        raise NotImplementedError("get_domain_id method must be implemented")

    @abc.abstractmethod
    def get_email(self):
        raise NotImplementedError("get_email method must be implemented")

    @abc.abstractmethod
    def has_client_retry_policy(self) -> bool:
        raise NotImplementedError("has_client_retry_policy must be implemented")


class OAuthAuthentication(Authentication, abc.ABC):
    """
    This is an abstract class which should be used by OAuth clients for authentication.
    """

    @abc.abstractmethod
    def get_config_token(self) -> OidcToken:
        """
        Get the token from the configuration
        """
        raise NotImplementedError("get_config_token method must be implemented")
