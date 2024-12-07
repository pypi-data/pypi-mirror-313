from typing import Any, Callable, Dict, List, Optional, Tuple

import antimatter_api as openapi_client
from antimatter.session_mixins.base import BaseMixin
from antimatter.builders.data_policy import DataPolicyRuleChangesBuilder, Attachment, NewDataPolicyRuleBuilder


class DataPolicyMixin(BaseMixin):
    """
    Data policy mixin defining CRUD functionality for data policies
    """

    def list_data_policies(self) -> List[openapi_client.DataPolicy]:
        """
        Returns a list of data policies available for the current domain and auth

        :return: A list of data policies
        """
        return openapi_client.DataPolicyList.from_json(self.authz.get_session().list_data_policies()).policies

    def create_data_policy(
        self, name: str, description: str
    ) -> openapi_client.DomainCreateDataPolicy200Response:
        """
        Create a new data policy for the current domain and auth

        :param name: The name for this data policy
        :param description: The human-readable description of the data policy
        """
        return openapi_client.DomainCreateDataPolicy200Response.from_json(
            self.authz.get_session().create_data_policy(
                openapi_client.NewDataPolicy(name=name, description=description).to_json()
            )
        )

    def describe_data_policy(self, policy_id: str) -> openapi_client.ExtendedDataPolicy:
        """
        Describe a data policy by ID

        :param policy_id: The ID of the data policy

        :return: The data policy details
        """
        return openapi_client.ExtendedDataPolicy.from_json(
            self.authz.get_session().describe_data_policy(policy_id)
        )

    def update_data_policy(self, policy_id: str, name: str, description: str) -> None:
        """
        Update a data policy by ID

        :param policy_id: The ID of the data policy
        :param name: The name for this data policy
        :param description: The human-readable description of the data policy
        """
        self.authz.get_session().update_data_policy(
            policy_id, openapi_client.NewDataPolicy(name=name, description=description).to_json()
        )

    def delete_data_policy(self, policy_id: str) -> None:
        """
        Delete a data policy by ID

        :param policy_id: The ID of the data policy
        """
        self.authz.get_session().delete_data_policy(policy_id)

    def renumber_data_policy_rules(self, policy_id: str) -> None:
        """
        Renumber the rules of a data policy by ID

        :param policy_id: The ID of the data policy
        """
        self.authz.get_session().renumber_data_policy_rules(policy_id)

    def update_data_policy_rules(
        self, policy_id: str, rules: DataPolicyRuleChangesBuilder
    ) -> openapi_client.DataPolicyRuleChangeResponse:
        """
        Update a rule of a data policy by ID

        :param policy_id: The ID of the data policy
        :param rules: The rules to apply to the data policy, constructed using the DataPolicyRuleChangesBuilder
        """
        if rules is None:
            raise ValueError("Data policy rules are required")
        policy = rules.build().to_json()
        return openapi_client.DataPolicyRuleChangeResponse.from_json(
            self.authz.get_session().update_data_policy_rules(policy_id, policy)
        )

    def describe_data_policy_rule(self, policy_id: str, rule_id: str) -> openapi_client.DataPolicyRule:
        """
        Describe a rule of a data policy by ID

        :param policy_id: The ID of the data policy
        :param rule_id: The ID of the rule to describe

        :return: The data policy rule details for the given policy and rule
        """
        return openapi_client.DataPolicyRule.from_json(
            self.authz.get_session().describe_data_policy_rule(policy_id, rule_id)
        )

    def update_data_policy_rule(self, policy_id: str, rule_id: str, rules: NewDataPolicyRuleBuilder) -> None:
        """
        Update a rule of a data policy by ID

        :param policy_id: The ID of the data policy
        :param rule_id: The ID of the rule to update
        :param rules: The rules to apply to the data policy, constructed using the NewDataPolicyRuleBuilder
        """
        if rules is None:
            raise ValueError("Data policy rules are required")
        self.authz.get_session().update_data_policy_rule(policy_id, rule_id, rules.build().to_json())

    def delete_data_policy_rule(self, policy_id: str, rule_id: str) -> None:
        """
        Delete a rule of a data policy by ID

        :param policy_id: The ID of the data policy
        :param rule_id: The ID of the rule to delete
        """
        self.authz.get_session().delete_data_policy_rule(policy_id, rule_id)

    def describe_data_policy_binding(
        self, policy_id: str, binding_id: str
    ) -> openapi_client.DataPolicyBindingInfo:
        """
        Describe a binding of a data policy by ID

        :param policy_id: The ID of the data policy
        :param binding_id: The ID of the binding to describe

        :return: The data policy binding details for the given policy and binding ID
        """
        return openapi_client.DataPolicyBindingInfo.from_json(
            self.authz.get_session().describe_data_policy_binding(policy_id, binding_id)
        )

    def set_data_policy_binding(
        self, policy_id: str, default_attachment: Attachment, read_contexts: List[Tuple[str, Attachment]]
    ) -> None:
        """
        Set a binding of a data policy by ID

        :param policy_id: The ID of the data policy
        :param default_attachment: The default attachment for the data policy
        """
        self.authz.get_session().set_data_policy_binding(
            policy_id,
            openapi_client.SetDataPolicyBinding(
                default_attachment=default_attachment.value,
                read_contexts=[
                    openapi_client.SetDataPolicyBindingReadContextsInner(name=r[0], configuration=r[1].value)
                    for r in read_contexts
                ],
            ).to_json(),
        )
