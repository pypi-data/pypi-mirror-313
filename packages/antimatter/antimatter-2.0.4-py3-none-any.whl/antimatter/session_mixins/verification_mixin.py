from typing import Optional

import antimatter_api as openapi_client
from antimatter.authn import Unauthenticated
from antimatter.authz import TokenAuthorization
from antimatter import errors
from antimatter.session_mixins.base import BaseMixin


class VerificationMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for verification actions.
    """

    def resend_verification_email(self, email: Optional[str] = None):
        """
        Resend the verification email to the admin contact email. If the session
        was called with an email, that will be used if none is provided.

        :param email: The email to resend the verification email for.
        """
        self.authz.get_session().resend_verification_email(email)
