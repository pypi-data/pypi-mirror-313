import datetime
import time

import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials

from antimatter.auth.config.tokens import GoogleOidcToken, OidcToken
from antimatter.authn import OAuthAuthentication


class GoogleOAuthAuthentication(OAuthAuthentication):
    """
    A base authentication class which uses google oauth device flow for authentication.

    This class is used to authenticate with Google OAuth using the device flow. It will prompt the user to go to a
    verification URL and enter a code to authenticate. This file does not take care of storing the tokens.
    Use the other derived oauth classes, global and domain to store the tokens.
    """

    def __init__(
        self, token: GoogleOidcToken = None, reset_credentials: bool = False, enable_retries: bool = True
    ):
        self.client_id = "212120322279-bj508kvp6f8465g1a2cv7ud5855s5bl0.apps.googleusercontent.com"
        self.client_secret = "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"
        self.scope = "https://www.googleapis.com/auth/userinfo.email"
        self.token = token
        self._enable_retries = enable_retries

        if self.token is None or reset_credentials:
            self.credentials = self._start_flow()
            self.token = GoogleOidcToken(
                access_token=self.credentials.token,
                refresh_token=self.credentials.refresh_token,
                expires_at=int(self.credentials.expiry.timestamp()),
                id_token=self.credentials.id_token,
            )
        else:
            self.credentials = Credentials(
                token=self.token.access_token,
                refresh_token=self.token.refresh_token,
                expiry=datetime.datetime.fromtimestamp(token.expires_at),
                id_token=token.id_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=[self.scope],
            )

    def get_config_token(self) -> OidcToken:
        token = self.get_token()
        return GoogleOidcToken(
            id_token=token,
            refresh_token=self.credentials.refresh_token,
            expires_at=int(self.credentials.expiry.timestamp()),
            access_token=self.credentials.token,
        )

    def authenticate(self, **kwargs):
        self.credentials.refresh(Request())
        self.token.notify_observers()

    def needs_refresh(self):
        return self.credentials.expired or self.credentials.id_token is None

    def get_token(self):
        if self.needs_refresh():
            self.authenticate()
        return self.credentials.id_token

    def get_token_scope(self):
        return "google_oauth_token"

    def get_session(self):
        raise Exception("oauth client does not support sessions, use with a domain instead")

    def get_domain_id(self):
        raise Exception("oauth client does not support domain id, use with a domain instead")

    def get_email(self):
        id_info = id_token.verify_oauth2_token(
            GoogleOAuthAuthentication.get_token(self), Request(), self.client_id
        )
        return id_info.get("email", None)

    def _start_flow(self):
        device_flow = self._init_device_flow()
        print(f"Go to {device_flow['verification_url']} and enter code {device_flow['user_code']}")
        return self._poll_for_token(
            device_flow["device_code"], device_flow["interval"], device_flow["expires_in"]
        )

    def _init_device_flow(self):
        device_authorization_endpoint = "https://oauth2.googleapis.com/device/code"
        device_authorization_params = {
            "client_id": self.client_id,
            "scope": self.scope,
        }

        response = requests.post(device_authorization_endpoint, data=device_authorization_params)
        if response.status_code != 200:
            raise Exception("Failed to get device code")

        return {
            "device_code": response.json()["device_code"],
            "user_code": response.json()["user_code"],
            "verification_url": response.json()["verification_url"],
            "expires_in": response.json()["expires_in"],
            "interval": response.json()["interval"],
        }

    def _poll_for_token(self, device_code, interval, expires_in, backoff=2):
        token_endpoint = "https://oauth2.googleapis.com/token"
        token_params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }

        # Start polling and wait for the user to authorize the device
        response = None
        # 403 with access_denied, don't retry
        # 428 with authorization_pending, retry
        # 403 with slow_down, retry but sleep for a bit
        # 200 with token, return
        start = time.time()
        while response is None or response.status_code > 400:
            time.sleep(interval)
            if time.time() - start > expires_in:
                raise Exception("Device code expired")
            response = requests.post(token_endpoint, data=token_params)
            if response.status_code == 403 and response.json()["error"] == "access_denied":
                raise Exception("User denied access")
            if response.status_code == 403 and response.json()["error"] == "slow_down":
                interval *= backoff
                continue
            if response.status_code == 200:
                break

        if response.status_code != 200:
            raise Exception("Failed to get token")

        return Credentials(
            token=response.json()["access_token"],
            refresh_token=response.json()["refresh_token"],
            expiry=(
                datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(seconds=response.json()["expires_in"])
            ).replace(tzinfo=None),
            id_token=response.json()["id_token"],
            token_uri=token_endpoint,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=[self.scope],
        )

    def has_client_retry_policy(self) -> bool:
        return self._enable_retries
