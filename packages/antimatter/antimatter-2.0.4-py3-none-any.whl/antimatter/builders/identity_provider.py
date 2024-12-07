from typing import List
from antimatter.constants import ProviderType
import antimatter_api as openapi_client


class GoogleOAuthGroupCapabilityMappingBuilder:
    def __init__(self):
        self.group = ""
        self.capabilities = []

    def set_group(self, group: str) -> "GoogleOAuthGroupCapabilityMappingBuilder":
        self.group = group
        return self

    def add_capability(self, capability_name: str) -> "GoogleOAuthGroupCapabilityMappingBuilder":
        self.capabilities.append(capability_name)
        return self

    def build(self) -> openapi_client.GoogleOAuthDomainIdentityProviderGroupCapabilityMappings:
        return openapi_client.GoogleOAuthDomainIdentityProviderGroupCapabilityMappings(
            group=self.group, capabilities=[openapi_client.Capability(name=x) for x in self.capabilities]
        )


class IdentityProviderBuilder:
    def __init__(self):
        self.provider_type = ""
        self.client_id = ""
        self.google_oauth_group_mappings = []

    def set_provider_type(self, provider_type: ProviderType) -> "IdentityProviderBuilder":
        self.provider_type = provider_type
        return self

    def set_client_id(self, client_id: str) -> "IdentityProviderBuilder":
        self.client_id = client_id
        return self

    def add_google_oauth_group_mappings(
        self,
        group_domain: str,
        domain_group_reader_admin: str,
        capability_mappings: List[GoogleOAuthGroupCapabilityMappingBuilder] = [],
    ) -> "IdentityProviderBuilder":
        self.google_oauth_group_mappings.append(
            openapi_client.GoogleOAuthDomainIdentityProviderGroupMappingDetails(
                group_domain=group_domain,
                domain_group_reader_admin=domain_group_reader_admin,
                group_capabilities=[x.build() for x in capability_mappings],
            )
        )
        return self

    def build(self) -> openapi_client.DomainIdentityProviderDetails:
        if self.provider_type is ProviderType.GoogleOAuth:
            return openapi_client.DomainIdentityProviderDetails(
                google_o_auth=openapi_client.GoogleOAuthDomainIdentityProviderDetails(
                    type=self.provider_type.value,
                    client_id=self.client_id,
                    group_mappings=openapi_client.GoogleOAuthDomainIdentityProviderDetailsGroupMappings(
                        mappings=self.google_oauth_group_mappings,
                    ),
                )
            )
        elif self.provider_type is ProviderType.MicrosoftOAuth:
            return openapi_client.DomainIdentityProviderDetails(
                microsoft_o_auth=openapi_client.MicrosoftOAuthDomainIdentityProviderDetails(
                    type=self.provider_type.value,
                    client_id=self.client_id,
                )
            )
        elif self.provider_type is ProviderType.ApiKey:
            return openapi_client.DomainIdentityProviderDetails(
                api_key=openapi_client.APIKeyDomainIdentityProviderDetails(
                    type=self.provider_type.value,
                )
            )
        raise ValueError(f"unrecognized provider type '{self.provider_type}'")
