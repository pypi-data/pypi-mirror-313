import pytest

from antimatter.authn import Unauthenticated
from antimatter.authz import TokenAuthorization
from antimatter.errors import errors
from antimatter.session_mixins import VerificationMixin


def test_resend_verification_email__error_when_no_email():
    authz = TokenAuthorization(auth_client=Unauthenticated(admin_email=None))
    verif = VerificationMixin(authz=authz)

    with pytest.raises(Exception) as e:
        verif.resend_verification_email(email=None)

    assert str(e.value) == "Unauthenticated session cannot be created"
