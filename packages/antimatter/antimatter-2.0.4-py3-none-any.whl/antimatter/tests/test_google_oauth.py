import os
import unittest
import requests
from datetime import datetime, timedelta

from unittest.mock import patch, MagicMock, ANY
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from antimatter.authn.google_oauth import GoogleOAuthAuthentication
from antimatter.authn.oauth_domain import OAuthDomainAuthentication
from antimatter.authn.static_oauth import StaticOAuthAuthentication


class TestGoogleOAuthAuthentication(unittest.TestCase):
    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_init(self, mock_start_flow):
        mock_credentials = MagicMock()
        mock_credentials.id_token = "test"
        mock_credentials.refresh_token = "test"
        mock_credentials.expiry.timestamp.return_value = datetime.now().timestamp()
        mock_credentials.token = "test"
        mock_start_flow.return_value = mock_credentials

        auth = GoogleOAuthAuthentication()
        mock_start_flow.assert_called_once()

        auth = GoogleOAuthAuthentication(reset_credentials=True)
        self.assertEqual(mock_start_flow.call_count, 2)

        token = MagicMock()
        token.access_token = "test"
        auth = GoogleOAuthAuthentication(token=token)
        self.assertEqual(mock_start_flow.call_count, 2)
        self.assertEqual(auth.credentials.token, "test")

        auth = GoogleOAuthAuthentication()
        self.assertEqual(mock_start_flow.call_count, 3)
        self.assertEqual(auth.credentials.token, "test")
        self.assertEqual(auth.credentials.refresh_token, "test")
        self.assertEqual(auth.credentials.id_token, "test")

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_oauth_needs_refresh(self, mock_start_flow):
        mock_start_flow.return_value = MagicMock()

        auth = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        auth.credentials = mock_credentials
        mock_credentials.expired = False
        self.assertFalse(auth.needs_refresh())

        mock_credentials.expired = True
        self.assertTrue(auth.needs_refresh())

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_other_methods(self, mock_start_flow):
        mock_start_flow.return_value = MagicMock()

        auth = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        auth.credentials = mock_credentials
        self.assertEqual(auth.get_token_scope(), "google_oauth_token")
        self.assertRaises(Exception, auth.get_session)
        self.assertRaises(Exception, auth.get_domain_id)

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_get_token(self, mock_start_flow):
        mock_start_flow.return_value = MagicMock()

        auth = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        auth.credentials = mock_credentials
        mock_credentials.expired = False
        mock_credentials.id_token = "valid_token"
        self.assertEqual(auth.get_token(), "valid_token")
        mock_credentials.refresh.assert_not_called()

        mock_credentials.expired = True
        self.assertEqual(auth.get_token(), "valid_token")
        mock_credentials.refresh.assert_called_once()

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_init_domain_auth(self, mock_start_flow):
        mock_start_flow.return_value = MagicMock()

        auth = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        auth.credentials = mock_credentials
        domain_id = "test_domain"
        auth = OAuthDomainAuthentication(domain_id=domain_id, oauth_authentication=auth)
        self.assertEqual(auth.get_domain_id(), domain_id)
        self.assertEqual(auth.get_token_scope(), "domain_identity")
        with self.assertRaises(Exception):
            auth.get_email()

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_domain_auth_other_methods(self, mock_start_flow):
        mock_start_flow.return_value = MagicMock()

        authn = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        authn.credentials = mock_credentials

        mock_credentials.id_token = "test_id_token"
        domain_id = "test_domain"
        auth = OAuthDomainAuthentication(domain_id=domain_id, oauth_authentication=authn)
        self.assertEqual(auth.get_domain_id(), domain_id)
        self.assertEqual(auth.get_token_scope(), "domain_identity")

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_get_email(self, mock_start_flow):
        mock_start_flow.return_value = MagicMock()

        auth = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        auth.credentials = mock_credentials

        mock_credentials.id_token = "test_id_token"
        with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify_oauth2_token:
            mock_verify_oauth2_token.return_value = {"email": "test_email"}
            self.assertEqual(auth.get_email(), "test_email")
            mock_verify_oauth2_token.assert_called_once_with("test_id_token", ANY, auth.client_id)

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication.needs_refresh")
    @patch("antimatter.authn.oauth_domain.is_token_valid", return_value=True)
    @patch("antimatter.authn.oauth_domain.decode_token", return_value=(None, None))
    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_needs_refresh(self, mock_start_flow, mock_decode_token, mock_is_token_valid, mock_needs_refresh):
        mock_start_flow.return_value = MagicMock()

        authn = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        authn.credentials = mock_credentials

        domain_id = "test_domain"

        auth = OAuthDomainAuthentication(domain_id=domain_id, oauth_authentication=authn)
        # Parent token is not expired yet, domain token is not expired yet
        mock_needs_refresh.return_value = False
        mock_is_token_valid.return_value = True
        self.assertFalse(auth.needs_refresh())

        # Parent token is not expired yet, domain token is expired
        mock_needs_refresh.return_value = False
        mock_is_token_valid.return_value = False
        self.assertTrue(auth.needs_refresh())

        # Parent token is expired, domain token is not expired yet
        mock_needs_refresh.return_value = True
        mock_is_token_valid.return_value = True
        self.assertTrue(auth.needs_refresh())

        # Parent token is expired, domain token is expired
        mock_needs_refresh.return_value = True
        mock_is_token_valid.return_value = False
        self.assertTrue(auth.needs_refresh())

    @patch("antimatter.authn.oauth_domain.authenticate")
    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication.needs_refresh")
    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication.authenticate")
    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_authenticate(
        self, mock_start_flow, mock_super_authenticate, mock_needs_refresh, mock_authenticate
    ):
        mock_start_flow.return_value = MagicMock()

        authn = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        authn.credentials = mock_credentials

        mock_credentials.id_token = "test_id_token"
        domain_id = "test_domain"
        mock_authenticate.return_value = "new_token"
        mock_needs_refresh.return_value = True

        auth = OAuthDomainAuthentication(domain_id=domain_id, oauth_authentication=authn)
        auth.authenticate()
        mock_authenticate.assert_called_once()
        mock_super_authenticate.assert_called_once()
        self.assertEqual(auth._token, "new_token")

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication.needs_refresh")
    @patch("antimatter.authn.oauth_domain.authenticate")
    @patch("antimatter.authn.oauth_domain.decode_token")
    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    def test_token_expiry(self, mock_start_flow, mock_decode_token, mock_authenticate, mock_needs_refresh):
        mock_start_flow.return_value = MagicMock()

        authn = GoogleOAuthAuthentication()
        mock_credentials = MagicMock()
        authn.credentials = mock_credentials

        domain_id = "test_domain"
        auth = OAuthDomainAuthentication(domain_id=domain_id, oauth_authentication=authn)

        mock_needs_refresh.return_value = False
        mock_decode_token.return_value = (None, None)
        mock_authenticate.return_value = "new_token"
        self.assertTrue(auth.needs_refresh())

        mock_needs_refresh.return_value = False
        # Expired token
        mock_decode_token.return_value = (
            (datetime.now() - timedelta(days=2)).astimezone(),
            (datetime.now() - timedelta(days=1)).astimezone(),
        )
        self.assertTrue(auth.needs_refresh())

        # not_before is in the future
        mock_decode_token.return_value = (
            (datetime.now() + timedelta(days=1)).astimezone(),
            (datetime.now() + timedelta(days=2)).astimezone(),
        )
        self.assertTrue(auth.needs_refresh())

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    @patch.object(requests, "post")
    def test_poll_for_token_success(self, mock_post, mock_start_flow):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600,
            "id_token": "test_id_token",
        }
        mock_post.return_value = mock_response
        auth = GoogleOAuthAuthentication()
        credentials = auth._poll_for_token("device_code", 0.1, 1)
        self.assertIsInstance(credentials, Credentials)
        self.assertEqual(credentials.token, "test_access_token")
        self.assertEqual(credentials.refresh_token, "test_refresh_token")
        self.assertEqual(credentials.id_token, "test_id_token")

    @patch("antimatter.authn.google_oauth.GoogleOAuthAuthentication._start_flow")
    @patch.object(requests, "post")
    def test_poll_for_token_errors(self, mock_post, mock_start_flow):

        # Access denied, 403
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "access_denied"}
        mock_response.status_code = 403
        mock_post.return_value = mock_response
        auth = GoogleOAuthAuthentication()

        with self.assertRaises(Exception) as context:
            auth._poll_for_token("device_code", 0.1, 1)
        self.assertTrue("User denied access" in str(context.exception))

        # Slow down, 403
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "slow_down"}
        mock_response.status_code = 403
        mock_post.return_value = mock_response
        auth = GoogleOAuthAuthentication()

        with self.assertRaises(Exception) as context:
            auth._poll_for_token("device_code", 0.1, 1)
        self.assertTrue("Device code expired" in str(context.exception))

        # Failed, 400
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        auth = GoogleOAuthAuthentication()

        with self.assertRaises(Exception) as context:
            auth._poll_for_token("device_code", 0.1, 1)
        self.assertTrue("Failed to get token" in str(context.exception))

        # Server error, 500
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        auth = GoogleOAuthAuthentication()

        with self.assertRaises(Exception) as context:
            auth._poll_for_token("device_code", 0.1, 1)
        self.assertTrue("Device code expired" in str(context.exception))

    @patch("antimatter.authn.oauth_domain.authenticate")
    @patch("antimatter.authn.oauth_domain.is_token_valid", return_value=True)
    @patch("antimatter.authn.oauth_domain.decode_token", return_value=(None, None))
    def test_domain_with_static_oauth(self, mock_decode_token, mock_is_token_valid, mock_authenticate):
        domain_id = "test_domain"
        mock_authenticate.return_value = "test_token"
        authn = StaticOAuthAuthentication(token="test_token")
        auth = OAuthDomainAuthentication(domain_id=domain_id, oauth_authentication=authn)

        self.assertEqual(auth.get_domain_id(), domain_id)
        self.assertEqual(auth.get_token_scope(), "domain_identity")
        with self.assertRaises(Exception):
            auth.get_email()

        self.assertFalse(auth.needs_refresh())

        mock_is_token_valid.return_value = False
        self.assertTrue(auth.needs_refresh())
        self.assertEqual(auth.get_token(), "test_token")
        self.assertFalse(authn.needs_refresh())
        self.assertEqual(authn.get_token(), "test_token")
        self.assertEqual(authn.get_token_scope(), "google_oauth_token")

        with self.assertRaises(Exception):
            authn.get_session()
        with self.assertRaises(Exception):
            authn.get_domain_id()
        with self.assertRaises(Exception):
            authn.get_email()


if __name__ == "__main__":
    unittest.main()
