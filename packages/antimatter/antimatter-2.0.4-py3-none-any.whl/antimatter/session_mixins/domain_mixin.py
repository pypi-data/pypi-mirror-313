from typing import Any, Callable, Dict, List, Optional

import antimatter_api as openapi_client
from antimatter.session_mixins.base import BaseMixin


class DomainMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for domains, including peering.
    """

    def new_peer_domain(
        self,
        import_alias_for_child: str,
        display_name_for_child: str,
        nicknames: Optional[List[str]] = None,
        import_alias_for_parent: Optional[str] = None,
        display_name_for_parent: Optional[str] = None,
        link_all: bool = True,
        link_identity_providers: bool = None,
        link_facts: bool = None,
        link_read_contexts: bool = None,
        link_write_contexts: bool = None,
        link_capabilities: bool = None,
        link_domain_policy: bool = None,
        link_root_encryption_keys: bool = None,
        link_capsule_access_log: bool = None,
        link_control_log: bool = None,
        link_capsule_manifest: bool = None,
    ) -> openapi_client.NewDomainResponse:
        """
        Creates a new peer domain

        :param import_alias_for_child: The import alias for the child domain
        :param display_name_for_child: The display name for the child domain
        :param nicknames: The nicknames for the child domain
        :param import_alias_for_parent: The import alias for the parent domain
        :param display_name_for_parent: The display name for the parent domain
        :param link_all: Whether to link all capabilities
        :param link_identity_providers: Whether to link identity providers
        :param link_facts: Whether to link facts
        :param link_read_contexts: Whether to link read contexts
        :param link_write_contexts: Whether to link write contexts
        :param link_capabilities: Whether to link capabilities
        :param link_domain_policy: Whether to link domain policy
        :param link_root_encryption_keys: Whether to link root encryption keys
        :param link_capsule_access_log: Whether to link capsule access log
        :param link_control_log: Whether to link control log
        :param link_capsule_manifest: Whether to link capsule manifest

        :return: The new peer domain
        """
        return openapi_client.NewDomainResponse.from_json(
            self.authz.get_session().new_peer_domain(
                import_alias_for_child=import_alias_for_child,
                display_name_for_child=display_name_for_child,
                nicknames=nicknames,
                import_alias_for_parent=import_alias_for_parent,
                display_name_for_parent=display_name_for_parent,
                link_all=link_all,
                link_identity_providers=link_identity_providers,
                link_facts=link_facts,
                link_read_contexts=link_read_contexts,
                link_write_contexts=link_write_contexts,
                link_capabilities=link_capabilities,
                link_domain_policy=link_domain_policy,
                link_root_encryption_keys=link_root_encryption_keys,
                link_capsule_access_log=link_capsule_access_log,
                link_control_log=link_control_log,
                link_capsule_manifest=link_capsule_manifest,
            )
        )

    def get_peer(self, nickname: Optional[str] = None, alias: Optional[str] = None) -> str:
        """
        Retrieve the domain ID of a domain that is configured as a peer of this
        session's domain by using either its alias or one of its nicknames.

        :param nickname: The nickname for the peer domain
        :param alias: One of the aliases of the peer domain
        :return: The domain ID
        """
        return openapi_client.Domain.from_json(
            self.authz.get_session().get_peer(nickname=nickname, alias=alias)
        ).id

    def list_peers(self) -> List[openapi_client.DomainPeerListPeersInner]:
        """
        Return a list of the peers of this session's domain.

        :return: The peer list, containing IDs and other information about the domains
        """
        return openapi_client.DomainPeerList.from_json(self.authz.get_session().list_peers()).peers

    def get_peer_config(
        self,
        peer_domain_id: Optional[str] = None,
        nickname: Optional[str] = None,
        alias: Optional[str] = None,
    ) -> openapi_client.DomainPeerConfig:
        """
        Get a peer configuration using one of the peer's domain ID, nickname, or
        alias.

        :param peer_domain_id: The domain ID of the peer
        :param nickname: The nickname for the peer domain
        :param alias: One of the aliases of the peer domain
        :return: The full peer configuration
        """
        if not peer_domain_id and (nickname or alias):
            peer_domain_id = self.get_peer(nickname=nickname, alias=alias)
        return openapi_client.DomainPeerConfig.from_json(
            self.authz.get_session().get_peer_config(peer_domain_id=peer_domain_id)
        )

    def update_peer(
        self,
        display_name: str,
        peer_domain_id: Optional[str] = None,
        nickname: Optional[str] = None,
        alias: Optional[str] = None,
        export_identity_providers: Optional[List[str]] = None,
        export_all_identity_providers: Optional[bool] = None,
        export_facts: Optional[List[str]] = None,
        export_all_facts: Optional[bool] = None,
        export_read_contexts: Optional[List[str]] = None,
        export_all_read_contexts: Optional[bool] = None,
        export_write_contexts: Optional[List[str]] = None,
        export_all_write_contexts: Optional[bool] = None,
        export_capabilities: Optional[List[str]] = None,
        export_all_capabilities: Optional[bool] = None,
        export_domain_policy: Optional[bool] = None,
        export_root_encryption_keys: Optional[bool] = None,
        export_capsule_access_log: Optional[bool] = None,
        export_control_log: Optional[bool] = None,
        export_capsule_manifest: Optional[bool] = None,
        export_billing: Optional[bool] = None,
        export_admin_contact: Optional[bool] = None,
        export_data_policies: Optional[str] = None,
        export_all_data_policies: Optional[bool] = None,
        nicknames: Optional[List[str]] = None,
        import_alias: Optional[str] = None,
        forward_billing: Optional[bool] = None,
        forward_admin_communications: Optional[bool] = None,
        import_identity_providers: Optional[List[str]] = None,
        import_all_identity_providers: Optional[bool] = None,
        import_facts: Optional[List[str]] = None,
        import_all_facts: Optional[bool] = None,
        import_read_contexts: Optional[List[str]] = None,
        import_all_read_contexts: Optional[bool] = None,
        import_write_contexts: Optional[List[str]] = None,
        import_all_write_contexts: Optional[bool] = None,
        import_capabilities: Optional[List[str]] = None,
        import_all_capabilities: Optional[bool] = None,
        import_domain_policy: Optional[bool] = None,
        import_root_encryption_keys: Optional[bool] = None,
        import_precedence: Optional[int] = None,
        import_capsule_access_log: Optional[bool] = None,
        import_control_log: Optional[bool] = None,
        import_capsule_manifest: Optional[bool] = None,
        import_data_policies: Optional[str] = None,
        import_all_data_policies: Optional[bool] = None,
    ) -> None:
        """
        Create or update the configuration for this peer using one of the peer's
        domain ID, nickname, or alias. Please note, if the configuration already
        exists, it is updated to reflect the values in the request. This will
        include setting the fields to their default value if not supplied.

        :param display_name: The display name for the peer domain
        :param peer_domain_id: The domain ID of the peer
        :param nickname: The nickname for the peer domain
        :param alias: One of the aliases of the peer domain
        :param export_identity_providers: The identity providers to export
        :param export_all_identity_providers: Whether to export all identity providers
        :param export_facts: The facts to export
        :param export_all_facts: Whether to export all facts
        :param export_read_contexts: The read contexts to export
        :param export_all_read_contexts: Whether to export all read contexts
        :param export_write_contexts: The write contexts to export
        :param export_all_write_contexts: Whether to export all write contexts
        :param export_capabilities: The capabilities to export
        :param export_all_capabilities: Whether to export all capabilities
        :param export_domain_policy: Whether to export the domain policy
        :param export_root_encryption_keys: Whether to export the root encryption keys
        :param export_capsule_access_log: Whether to export the capsule access log
        :param export_control_log: Whether to export the control log
        :param export_capsule_manifest: Whether to export the capsule manifest
        :param export_billing: Whether to export billing information
        :param export_admin_contact: Whether to export the admin contact
        :param nicknames: The nicknames for the peer domain
        :param import_alias: The import alias for the peer domain
        :param forward_billing: Whether to forward billing information
        :param forward_admin_communications: Whether to forward admin communications
        :param import_identity_providers: The identity providers to import
        :param import_all_identity_providers: Whether to import all identity providers
        :param import_facts: The facts to import
        :param import_all_facts: Whether to import all facts
        :param import_read_contexts: The read contexts to import
        :param import_all_read_contexts: Whether to import all read contexts
        :param import_write_contexts: The write contexts to import
        :param import_all_write_contexts: Whether to import all write contexts
        :param import_capabilities: The capabilities to import
        :param import_all_capabilities: Whether to import all capabilities
        :param import_domain_policy: Whether to import the domain policy
        :param import_root_encryption_keys: Whether to import the root encryption keys
        :param import_precedence: The precedence of the import
        :param import_capsule_access_log: Whether to import the capsule access log
        :param import_control_log: Whether to import the control log
        :param import_capsule_manifest: Whether to import the capsule manifest
        """
        if not peer_domain_id and (nickname or alias):
            peer_domain_id = self.get_peer(nickname=nickname, alias=alias)
        self.authz.get_session().update_peer(
            peer_domain_id=peer_domain_id,
            nickname=nickname,
            alias=alias,
            display_name=display_name,
            export_identity_providers=export_identity_providers,
            export_all_identity_providers=export_all_identity_providers,
            export_facts=export_facts,
            export_all_facts=export_all_facts,
            export_read_contexts=export_read_contexts,
            export_all_read_contexts=export_all_read_contexts,
            export_write_contexts=export_write_contexts,
            export_all_write_contexts=export_all_write_contexts,
            export_capabilities=export_capabilities,
            export_all_capabilities=export_all_capabilities,
            export_domain_policy=export_domain_policy,
            export_root_encryption_keys=export_root_encryption_keys,
            export_capsule_access_log=export_capsule_access_log,
            export_control_log=export_control_log,
            export_capsule_manifest=export_capsule_manifest,
            export_billing=export_billing,
            export_admin_contact=export_admin_contact,
            export_data_policies=export_data_policies,
            export_all_data_policies=export_all_data_policies,
            nicknames=nicknames,
            import_alias=import_alias,
            forward_billing=forward_billing,
            forward_admin_communications=forward_admin_communications,
            import_identity_providers=import_identity_providers,
            import_all_identity_providers=import_all_identity_providers,
            import_facts=import_facts,
            import_all_facts=import_all_facts,
            import_read_contexts=import_read_contexts,
            import_all_read_contexts=import_all_read_contexts,
            import_write_contexts=import_write_contexts,
            import_all_write_contexts=import_all_write_contexts,
            import_capabilities=import_capabilities,
            import_all_capabilities=import_all_capabilities,
            import_domain_policy=import_domain_policy,
            import_root_encryption_keys=import_root_encryption_keys,
            import_precedence=import_precedence,
            import_capsule_access_log=import_capsule_access_log,
            import_control_log=import_control_log,
            import_capsule_manifest=import_capsule_manifest,
            import_data_policies=import_data_policies,
            import_all_data_policies=import_all_data_policies,
        )

    def delete_peer(
        self,
        peer_domain_id: Optional[str] = None,
        nickname: Optional[str] = None,
        alias: Optional[str] = None,
    ) -> None:
        """
        Remove the peering relationship with the given domain, using one of the
        peer's domain ID, nickname, or alias.

        :param peer_domain_id: The domain ID of the peer
        :param nickname: The nickname for the peer domain
        :param alias: One of the aliases of the peer domain
        """
        if not peer_domain_id and (nickname or alias):
            peer_domain_id = self.get_peer(nickname=nickname, alias=alias)
        self.authz.get_session().delete_peer(peer_domain_id=peer_domain_id)

    def get_top_tags(self) -> List[str]:
        """
        Get domain tag info returns a list containing the top 100 tag names for the current session's domain.
        """
        res = openapi_client.DomainTagInfoResults.from_json(self.authz.get_session().get_top_tags())
        return [r.name for r in res.tags]
