from typing import Any, Callable, Dict, List, Optional

import antimatter_api as openapi_client

from antimatter.session_mixins.base import BaseMixin


class FactMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for facts and fact types.
    """

    def list_fact_types(self) -> List[openapi_client.FactTypeDefinition]:
        """
        Returns a list of fact types available for the current domain and auth
        """
        return openapi_client.DomainFactList.from_json(self.authz.get_session().list_fact_types()).fact_types

    def list_facts(self, fact_type: str) -> List[openapi_client.Fact]:
        """
        Returns a list of facts for the given fact type
        """
        return openapi_client.FactList.from_json(self.authz.get_session().list_facts(fact_type)).facts

    def add_fact_type(
        self,
        name: str,
        description: str,
        arguments: Dict[str, str],
    ) -> None:
        """
        Upserts a fact type for the current domain and auth

        :param name: The "type name" for this fact, like "has_role"
        :param description: The human-readable description of the fact type
        :param arguments: Name:description argument pairs for the fact type
        """
        self.authz.get_session().add_fact_type(
            fact_type=name,
            arguments=openapi_client.NewFactTypeDefinition(
                description=description,
                arguments=[
                    openapi_client.NewFactTypeDefinitionArgumentsInner(name=name, description=desc)
                    for name, desc in arguments.items()
                ],
            ).to_json(),
        )

    def add_fact(
        self,
        fact_type: str,
        *arguments: str,
    ) -> openapi_client.Fact:
        """
        Upserts a fact for the current domain and auth

        :param fact_type: The name of the type of fact being added
        :param arguments: The fact arguments to add
        :return: The upserted fact
        """
        return openapi_client.Fact.from_json(
            self.authz.get_session().add_fact(
                fact_type=fact_type,
                arguments=openapi_client.NewFact(arguments=arguments).to_json(),
            )
        )

    def get_fact_type(self, fact_type: str) -> openapi_client.FactTypeDefinition:
        """
        Get the fact type details for the given fact type

        :param fact_type: The "type name" for this fact, like "has_role"
        :return: The fact type details
        """
        return openapi_client.FactTypeDefinition.from_json(self.authz.get_session().get_fact_type(fact_type))

    def get_fact(self, fact_type: str, fact_id: str) -> openapi_client.Fact:
        """
        Returns the fact details for the given fact type and name

        :param fact_type: The "type name" for this fact, like "has_role"
        :param fact_id: The ID for the fact to be retrieved
        :return: The fact details
        """
        return openapi_client.Fact.from_json(self.authz.get_session().get_fact(fact_type, fact_id))

    def delete_fact_type(self, fact_type: str) -> None:
        """
        Delete a fact type AND ALL FACTS INSIDE IT.

        :param fact_type: The "type name" for this fact, like "has_role"
        """
        self.authz.get_session().delete_fact_type(fact_type=fact_type, confirm=fact_type)

    def delete_fact(
        self,
        fact_type: str,
        *arguments: str,
        fact_id: Optional[str] = None,
    ) -> None:
        """
        Delete a fact by ID or argument. One of 'fact_id' or 'arguments' must be
        provided. If 'fact_id' is provided, it will be used solely. If arguments
        are provided, each must fully match the name and/or arguments of the fact
        for it to be deleted.

        :param fact_type: The "type name" for this fact, like "has_role"
        :param fact_id: The ID for the fact to be deleted
        :param arguments: The arguments for the fact to be deleted
        """
        self.authz.get_session().delete_fact(
            fact_type=fact_type,
            arguments=arguments,
            fact_id=fact_id,
        )

    def delete_all_facts(self, fact_type: str) -> None:
        """
        Delete all the facts for the given fact type.

        :param fact_type: The "type name" for this fact, like "has_role"
        """
        self.authz.get_session().delete_all_facts(fact_type=fact_type)
