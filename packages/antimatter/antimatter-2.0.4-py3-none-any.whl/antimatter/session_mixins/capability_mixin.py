from typing import Any, Callable, Dict, List, Optional

import antimatter_api as openapi_client

from antimatter.session_mixins.base import BaseMixin


class CapabilityMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for capabilities.
    """

    def list_capabilities(self) -> List[openapi_client.CapabilityDefinition]:
        """
        Get the capabilities for the session's domain.

        :return: A list of capabilities.
        """
        return openapi_client.CapabilityDefinitionList.from_json(
            self.authz.get_session().list_capabilities()
        ).capabilities

    def get_capability(self, name: str) -> openapi_client.CapabilityDefinition:
        """
        Get a specific capability for the session's domain.

        :param name: The name for this capability, like "admin"
        :return: The details of the capability.
        """
        return openapi_client.CapabilityDefinition.from_json(self.authz.get_session().get_capability(name))

    def put_capability(
        self,
        name: str,
        summary: str,
        description: Optional[str] = None,
        unary: bool = True,
        create_only: bool = False,
    ) -> None:
        """
        Create or update a capability. A capability is attached to authenticated
        domain identities by an identity provider, and confers additional permissions
        upon the identity. This is done by writing domain policy rules that reference
        the capability.

        :param name: The name for this capability, like "admin"
        :param summary: A short, single sentence description of this capability
        :param description: An optional longer form description of this capability
        :param unary: A unary capability does not have a value
        :param create_only:
            If True, an error will be returned if a capability with the name already exists
        """
        if description is None:
            description = ""
        self.authz.get_session().put_capability(
            name=name,
            summary=summary,
            description=description,
            unary=unary,
            create_only=create_only,
        )

    def delete_capability(self, name: str) -> None:
        """
        Delete a capability.

        :param name: The name of the capability, like "admin"
        """
        self.authz.get_session().delete_capability(name)
