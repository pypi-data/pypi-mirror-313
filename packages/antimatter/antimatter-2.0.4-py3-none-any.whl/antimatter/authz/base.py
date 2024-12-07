import abc

import antimatter_engine as am
from antimatter.authn import Authentication
from antimatter_api import ApiClient


class Authorization(abc.ABC):

    def __init__(self, auth_client: Authentication) -> None:
        self.auth_client = auth_client
        if not isinstance(self.auth_client, Authentication):
            raise ValueError("Authentication client must be an Authentication instance")

    @abc.abstractmethod
    def get_client(self) -> ApiClient:
        raise NotImplementedError("authorize method must be implemented")

    @abc.abstractmethod
    def get_session(self) -> am.PySession:
        raise NotImplementedError("get_session method must be implemented")
