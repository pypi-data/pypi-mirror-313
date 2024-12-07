from typing import Any, Callable, Dict, List, Union

import antimatter_api as openapi_client
from antimatter_api import KeyInfos, ActiveRootEncryptionKeyID

from antimatter.session_mixins.base import BaseMixin


class RootEncryptionKeyMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for root encryption keys
    """

    def get_active_root_encryption_key(self) -> openapi_client.RootEncryptionKeyItem:
        """
        Get the active root encryption key

        :return: The active root encryption key
        """
        return openapi_client.RootEncryptionKeyItem.from_json(
            self.authz.get_session().get_active_root_encryption_key()
        )

    def list_root_encryption_keys(self) -> List[openapi_client.RootEncryptionKeyItem]:
        """
        List all root encryption keys

        :return: A list of root encryption keys
        """
        return openapi_client.RootEncryptionKeyListResponse.from_json(
            self.authz.get_session().list_root_encryption_keys()
        ).keys

    def test_root_encryption_key(
        self, root_encryption_key_id: str
    ) -> openapi_client.RootEncryptionKeyTestResponse:
        """
        Attempt to test a root encryption key to encrypt and decrypt

        :param key: The key to test
        :return: The result of the test
        """
        return openapi_client.RootEncryptionKeyTestResponse.from_json(
            self.authz.get_session().test_root_encryption_key(root_encryption_key_id)
        )

    def add_root_encryption_key(self, key_infos: KeyInfos, description: str = "") -> str:
        """
        Add a new root encryption key.
        Use the builder functions in `antimatter.builders.root_encryption_key` to create the key information.

        For example:

        .. code-block:: python

            key_info = antimatter.builders.antimatter_delegated_aws_key_info(key_arn="key_arn")
            key_id = session.add_root_encryption_key(key_info)

            key_info = antimatter.builders.aws_service_account_key_info(
                access_key_id="access_key_id", secret_access_key
            )
            key_id = session.add_root_encryption_key(key_info)

            key_info = antimatter.builders.gcp_service_account_key_info(
                service_account_credentials="service_account_credentials", project_id="project_id", location="location"
            )
            key_id = session.add_root_encryption_key(key_info)

        :param key_infos: The key information to add
        :param description: The description of the key
        """
        assert key_infos is not None, "Key information is required"

        key_infos.description = description
        return openapi_client.RootEncryptionKeyIDResponse.from_json(
            self.authz.get_session().add_root_encryption_key(key_infos.to_json())
        ).rek_id

    def delete_root_encryption_key(self, root_encryption_key_id: str):
        """
        Delete a root encryption key. Only possible if key is not in use by any data key encryption keys

        :param key: The key to delete
        """
        self.authz.get_session().delete_root_encryption_key(root_encryption_key_id)

    def set_active_root_encryption_key(self, root_encryption_key_id: str) -> None:
        """
        Set the active root encryption key for the domain

        :param key: The key to set as active
        """
        self.authz.get_session().set_active_root_encryption_key(
            ActiveRootEncryptionKeyID(key_id=root_encryption_key_id).to_json()
        )

    def rotate_encryption_keys(self) -> None:
        """
        Rotates the root encryption keys. This is a batched operation and if 'True' is
        returned, this indicates whether there are more key encryption keys that can be rotated.
        """
        return openapi_client.RotateKeyEncryptionKeyResponse.from_json(
            self.authz.get_session().rotate_encryption_keys()
        ).has_more

    def list_key_providers(
        self,
    ) -> List[
        Union[
            openapi_client.AvailableDelegatedRootEncryptionKeyProvider,
            openapi_client.AvailableServiceAccountRootEncryptionKeyProvider,
        ]
    ]:
        """
        Retrieve the domain's key providers and a brief overview of their
        configuration.
        """
        res = openapi_client.AvailableRootEncryptionKeyProviders.from_json(
            self.authz.get_session().list_key_providers()
        )
        if not res.providers:
            return []
        return [
            provider.actual_instance for provider in res.providers if provider.actual_instance is not None
        ]
