from typing import Any, Callable, Dict, List, Optional, Union

import antimatter_api as openapi_client
from antimatter.constants.identity_provider import PrincipalType, ProviderType

from antimatter.converters import CapabilityConverter
from antimatter.session_mixins.base import BaseMixin
from antimatter.builders import IdentityProviderBuilder


class OverrideDomainIdentityPrincipalDetails(openapi_client.DomainIdentityPrincipalDetails):
    """
    This override provides a local way to pass domain identity principal details
    to the openapi generated client that mitigates the pydantic serializing error
    it produces due to a bug in the generator.

    The code that the generator currently produces looks like:
    .. code-block:: python

        one_of_schemas: List[str] = Literal["APIKeyDomainIdentityProviderDetails", "GoogleOAuthDomainIdentityProviderDetails"]

    that will produce the error:

    .. code-block:: text

        /Users/daniel/.pyenv/versions/pycapsule-3.11/lib/python3.11/site-packages/pydantic/main.py:308: UserWarning: Pydantic serializer warnings:
        Expected `list[str]` but got `_LiteralGenericAlias` - serialized value may not be as expected
        return self.__pydantic_serializer__.to_python(

    """

    one_of_schemas: List[str] = [
        "DomainIdentityAPIKeyPrincipalParams",
        "DomainIdentityEmailPrincipalParams",
        "DomainIdentityHostedDomainPrincipalParams",
    ]


class IdentityProviderMixin(BaseMixin):
    """
    Session mixin defining identity provider CRUD functionality.
    """

    def upsert_identity_provider(
        self,
        provider_name: str,
        idp: IdentityProviderBuilder,
    ) -> openapi_client.DomainIdentityProviderInfo:
        """
        Create or update an identity provider.

        :param provider_name: The name of a new or existing identity provider
        :param idp: The identity provider definition, constructed using the IdentityProviderBuilder
        :return: The identity provider summary
        """
        return openapi_client.DomainIdentityProviderInfo.from_json(
            self.authz.get_session().upsert_identity_providers(
                name=provider_name,
                domain_identity_provider=idp.build().to_json(),
            )
        )

    def insert_identity_provider_principal(
        self,
        provider_name: str,
        capabilities: List[Union[str, Dict[str, Any]]],
        principal_type: Union[str, PrincipalType],
        principal_value: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> openapi_client.DomainInsertIdentityProviderPrincipal200Response:
        """
        Creates a new principal for the provider. Note that the provider_name
        must refer to an existing identity provider. The principal_value is
        optional if the type is APIKey.

        :param provider_name: The name of an existing identity provider
        :param capabilities: The capabilities to attach to the principal. These can be in one of the following forms:
                - A list of unary capabilities, like ['admin', 'read_only']
                - A list of key-value pairs, like ["admin=True", "read_only=False"]
                - A list of dictionaries, like [{"admin": "True"}, {"read_only": "False"}]
                - A list of dictionaries as a name/value pair, like [{"name": "admin", "value": "True"}, {"name": "read_only", "value": "False"}]
                - Any combination of the above
        :param principal_type: The type of principal to create. One of 'APIKey', 'Email', or 'HostedDomain'
        :param principal_value: The appropriate identifying value for the principal, depending on type
        :param comment: An optional comment for the identity provider principal
        :return: The ID of the inserted principal and any additional metadata
        """
        capabilities = CapabilityConverter.convert_capabilities(capabilities)
        principal_type = PrincipalType(principal_type)
        inner_params = None
        if PrincipalType(principal_type) is PrincipalType.ApiKey:
            inner_params = openapi_client.DomainIdentityAPIKeyPrincipalParams(
                type=principal_type.value,
                api_key_id=principal_value,
                comment=comment,
            )
        elif PrincipalType(principal_type) is PrincipalType.Email:
            inner_params = openapi_client.DomainIdentityEmailPrincipalParams(
                type=principal_type.value,
                email=principal_value,
                comment=comment,
            )
        elif PrincipalType(principal_type) is PrincipalType.HostedDomain:
            inner_params = openapi_client.DomainIdentityHostedDomainPrincipalParams(
                type=principal_type.value,
                hosted_domain=principal_value,
                comment=comment,
            )
        return openapi_client.DomainInsertIdentityProviderPrincipal200Response.from_json(
            self.authz.get_session().insert_identity_provider_principal(
                identity_provider_name=provider_name,
                domain_identity_provider_principal_params=openapi_client.DomainIdentityProviderPrincipalParams(
                    capabilities=[
                        openapi_client.Capability(name=k, value=v) for k, v in capabilities.items()
                    ],
                    details=OverrideDomainIdentityPrincipalDetails(inner_params),
                ).to_json(),
            )
        )

    def update_identity_provider_principal(
        self,
        provider_name: str,
        principal_id: str,
        capabilities: List[Union[str, Dict[str, Any]]],
    ) -> None:
        """
        Update the capabilities for an identity provider principal.

        :param provider_name: The name of an existing identity provider
        :param principal_id: The ID of the principal
        :param capabilities: The capabilities to attach to the principal. These can be in one of the following forms:
                - A list of unary capabilities, like ['admin', 'read_only']
                - A list of key-value pairs, like ["admin=True", "read_only=False"]
                - A list of dictionaries, like [{"admin": "True"}, {"read_only": "False"}]
                - A list of dictionaries as a name/value pair, like [{"name": "admin", "value": "True"}, {"name": "read_only", "value": "False"}]
                - Any combination of the above
        """
        capabilities = CapabilityConverter.convert_capabilities(capabilities)
        self.authz.get_session().update_identity_provider_principal(
            identity_provider_name=provider_name,
            principal_id=principal_id,
            capability_list=openapi_client.UpdatePrincipalParams(
                capabilities=[openapi_client.Capability(name=k, value=v) for k, v in capabilities.items()]
            ).to_json(),
        )

    def get_identity_provider(self, provider_name: str) -> openapi_client.DomainIdentityProviderInfo:
        """
        Retrieve detailed information and configuration of an identity provider

        :param provider_name: The name of an existing identity provider
        :return: The identity provider details
        """
        return openapi_client.DomainIdentityProviderInfo.from_json(
            self.authz.get_session().get_identity_provider(provider_name)
        )

    def list_identity_providers(self) -> List[openapi_client.DomainIdentityProviderInfo]:
        """
        Retrieve the domain's identity providers and a brief overview of their
        configuration.
        """
        return (
            openapi_client.DomainIdentityProviderList.from_json(
                self.authz.get_session().list_identity_providers()
            ).identity_providers
            or []
        )

    def get_identity_provider_principal(
        self,
        provider_name: str,
        principal_id: Optional[str] = None,
    ) -> Union[List[openapi_client.PrincipalSummary], openapi_client.PrincipalSummary]:
        """
        Get either a summary of all the principals for an identity provider, or
        detailed information about a single principal if a principal_id is
        provided

        :param provider_name: The name of an existing identity provider
        :param principal_id: The ID of the principal; None to get all principals
        :return: The principal information
        """
        if principal_id is None:
            return openapi_client.DomainIdentityProviderPrincipalList.from_json(
                self.authz.get_session().get_identity_provider_principals(provider_name)
            ).principals
        else:
            return openapi_client.PrincipalSummary.from_json(
                self.authz.get_session().get_identity_provider_principal(provider_name, principal_id)
            )

    def delete_identity_provider(self, provider_name: str) -> None:
        """
        Delete an identity provider. All domain tokens created using this
        identity provider will be invalidated. Take care not to remove the
        identity provider that is providing you admin access to your domain, as
        you may lock yourself out.

        :param provider_name: The name of the identity provider to fully delete
        """
        self.authz.get_session().delete_identity_provider(provider_name)

    def delete_identity_provider_principal(
        self,
        provider_name: str,
        principal_id: str,
    ) -> None:
        """
        Delete an identity provider principal.

        :param provider_name: The name of the identity provider to delete a principal from
        :param principal_id: The ID of the principal to delete
        """
        self.authz.get_session().delete_identity_provider_principal(provider_name, principal_id)

    def list_group_providers(self) -> List[openapi_client.GoogleOAuthDomainIdentityProviderDetails]:
        """
        Retrieve the domain's identity providers that support group mappings along with details on how
        implement them.
        """

        return (
            openapi_client.DomainIdentityGroupProviderDetails.from_json(
                self.authz.get_session().list_group_providers()
            ).group_identity_providers
            or []
        )
