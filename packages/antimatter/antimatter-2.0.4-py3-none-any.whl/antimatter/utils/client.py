import os
from typing import List

import urllib3

from antimatter_api import ApiClient, Configuration
from antimatter.utils.constants import API_TARGET_VERSION
from antimatter.utils.user_agent import get_user_agent


class ClientWrapper:
    """
    This is a wrapper around the real client which checks for the security scope of the client
    It is checking the auth_settings in the kwargs of the param_serialize method and verifying the
    permissions of the client. If the permissions are not valid, it will raise a PermissionError.
    """

    def __init__(self, real_client: ApiClient, supported_auth_type: str = None):
        self._real_client = real_client
        self._supported_auth_type = supported_auth_type

    def __getattr__(self, item):
        attr = getattr(self._real_client, item)
        if item != "param_serialize":
            return attr

        if callable(attr):

            def wrapped(*args, **kwargs):
                # Specifically check the 'auth_settings' in kwargs
                if "auth_settings" in kwargs:
                    auth_settings = kwargs.get("auth_settings", [])
                    if not self._verify_auth(auth_settings):
                        raise PermissionError("Invalid permissions used to access this method")
                return attr(*args, **kwargs)

            return wrapped
        else:
            return attr

    def _verify_auth(self, auth_settings: List[str]):
        if auth_settings:  # Non-empty list, check for a matching token
            if self._supported_auth_type not in auth_settings:
                return False
        return True


def get_base_client(enable_retries: bool = True) -> ApiClient:
    """
    Get the base client for the API.

    :param enable_retries: If True, retry gateway, DNS, and general connection errors
    """
    host = os.getenv("ANTIMATTER_API_URL", "https://api.antimatter.io")
    config = Configuration(host=f"{host}/{API_TARGET_VERSION}")
    if enable_retries:
        # configure retries with backup for all HTTP verbs; we do not limit this to only
        # idempotent verbs as the subset of retries we allow indicates the API was never
        # reached
        config.retries = urllib3.Retry(
            total=5, backoff_factor=0.1, allowed_methods=None, status_forcelist=[502, 503]
        )
    _api_client = ApiClient(configuration=config)
    _api_client.user_agent = get_user_agent()
    return ClientWrapper(_api_client)
