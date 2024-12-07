import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from antimatter.authn.apikey import ApiKeyAuthentication
from antimatter.utils.user_agent import get_user_agent


class TestApiKeyAuthentication(unittest.TestCase):
    def setUp(self):
        self.api_key_auth = ApiKeyAuthentication("test_domain", "test_api_key")

    @patch("antimatter.authn.apikey.decode_token", return_value=(None, None))
    @patch("antimatter.authn.apikey.is_token_valid", return_value=True)
    def test_needs_refresh_valid_token(self, mock_is_token_valid, mock_decode_token):
        self.api_key_auth._token = "valid_token"
        self.assertFalse(self.api_key_auth.needs_refresh())
        mock_decode_token.assert_called_once_with("valid_token")

    @patch("antimatter.authn.apikey.decode_token", return_value=(None, None))
    @patch("antimatter.authn.apikey.is_token_valid", return_value=False)
    def test_needs_refresh_invalid_token(self, mock_is_token_valid, mock_decode_token):
        self.api_key_auth._token = "invalid_token"
        self.assertTrue(self.api_key_auth.needs_refresh())
        mock_decode_token.assert_called_once_with("invalid_token")

    @patch("antimatter.authn.apikey.authenticate")
    def test_authenticate(self, mock_authenticate):
        mock_authenticate.return_value = "new_token"
        self.api_key_auth.authenticate()
        self.assertEqual(self.api_key_auth._token, "new_token")
        mock_authenticate.assert_called_once()

    @patch("antimatter.authn.apikey.decode_token", return_value=(None, None))
    @patch("antimatter.authn.apikey.is_token_valid", return_value=False)
    @patch("antimatter.authn.apikey.authenticate")
    def test_get_token_needs_refresh(self, mock_authenticate, mock_is_token_valid, mock_decode_token):
        mock_authenticate.return_value = "new_token"
        token = self.api_key_auth.get_token()
        self.assertEqual(token, "new_token")
        mock_authenticate.assert_called_once()
        mock_is_token_valid.assert_called_once()
        mock_decode_token.assert_called_once()

    @patch("antimatter.authn.apikey.is_token_valid", return_value=True)
    def test_get_token_no_refresh(self, mock_is_token_valid):
        self.api_key_auth._token = "valid_token"
        token = self.api_key_auth.get_token()
        self.assertEqual(token, "valid_token")
        mock_is_token_valid.assert_called_once()

    def test_get_token_scope(self):
        self.assertEqual(self.api_key_auth.get_token_scope(), "domain_identity")

    @patch("antimatter.authn.apikey.am.PySession.new_from_bearer_access_token")
    def test_get_session_no_existing_session(self, mock_new_session):
        mock_session = MagicMock()
        mock_new_session.return_value = mock_session
        self.api_key_auth._token = "valid_token"
        self.api_key_auth.get_token = MagicMock(return_value="valid_token")
        session = self.api_key_auth.get_session()
        self.assertEqual(session, mock_session)
        mock_new_session.assert_called_once_with("test_domain", "valid_token", get_user_agent())

        self.api_key_auth.get_token = MagicMock(return_value="new_valid_token")
        session = self.api_key_auth.get_session()
        self.assertEqual(session, mock_session)
        mock_session.set_bearer_access_token.assert_called_once_with("new_valid_token")

    def test_get_domain_id(self):
        self.assertEqual(self.api_key_auth.get_domain_id(), "test_domain")

    def test_get_email(self):
        self.assertIsNone(self.api_key_auth.get_email())

    @patch("antimatter.authn.apikey.authenticate")
    @patch("antimatter.authn.apikey.decode_token")
    def test_token_expiry(self, mock_decode_token, mock_authenticate):
        mock_authenticate.return_value = "new_token"
        mock_decode_token.return_value = (None, None)
        needs_refresh = self.api_key_auth.needs_refresh()
        self.assertTrue(needs_refresh)

        # Expired token
        mock_decode_token.return_value = (
            (datetime.now() - timedelta(days=2)).astimezone(),
            (datetime.now() - timedelta(days=1)).astimezone(),
        )
        needs_refresh = self.api_key_auth.needs_refresh()
        self.assertTrue(needs_refresh)

        # not_before is in the future
        mock_decode_token.return_value = (
            (datetime.now() + timedelta(days=1)).astimezone(),
            (datetime.now() + timedelta(days=2)).astimezone(),
        )
        needs_refresh = self.api_key_auth.needs_refresh()
        self.assertTrue(needs_refresh)


if __name__ == "__main__":
    unittest.main()
