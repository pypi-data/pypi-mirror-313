from typing import Callable

import antimatter_api as openapi_client

from antimatter.session_mixins.base import BaseMixin


class EncryptionMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for encryption functionality.
    """

    def flush_encryption_keys(self):
        """
        Flush all keys in memory. The keys will be immediately reloaded from persistent
        storage, forcing a check that the domain's root key is still available
        """
        self.authz.get_session().flush_encryption_keys()
