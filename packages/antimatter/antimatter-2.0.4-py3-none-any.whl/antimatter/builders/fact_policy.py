from typing import List, Optional, Tuple, Union

import antimatter_api as openapi_client
from antimatter.constants import FactArgumentSource, FactOperator


class FactPolicyArgumentBuilder:
    """
    Builder class for creating a FactPolicyRulesInnerArgumentsInner.

    :param source: The source of the argument.
    :param capability: The capability of the argument.
    :param any_value: Whether the argument can be any value.
    :param value: The value of the argument.
    """

    def __init__(
        self,
        source: Union[str, FactArgumentSource],
        capability: Optional[str] = None,
        any_value: Optional[bool] = None,
        value: Optional[str] = None,
    ):
        self._source = FactArgumentSource(source)
        self._capability = capability
        self._any = any_value
        self._value = value

    def build(self) -> openapi_client.FactPolicyRulesInnerArgumentsInner:
        """
        Build the argument.

        :return: The built argument.
        """
        return openapi_client.FactPolicyRulesInnerArgumentsInner(
            any=self._any,
            source=self._source.value,
            capability=self._capability,
            value=self._value,
        )


class FactPoliciesBuilder:
    """
    Builder class for creating a list of FactPolicyRulesInner.
    """

    def __init__(self):
        self._policies: List[Tuple[FactOperator, str, List[FactPolicyArgumentBuilder]]] = []

    def with_policy(
        self,
        name: str,
        operator: Union[FactOperator, str],
        *policies: FactPolicyArgumentBuilder,
    ) -> "FactPoliciesBuilder":
        """
        Add a policy to the list.

        :param name: The name of the policy.
        :param operator: The operator of the policy.
        :param policies: The arguments of the policy.
        :return: The builder instance.
        """
        self._policies.append((FactOperator(operator), name, list(policies)))
        return self

    def build(self) -> List[openapi_client.FactPolicyRulesInner]:
        """
        Build the list of policies.

        :return: The built list of policies.
        """
        return [
            openapi_client.FactPolicyRulesInner(
                operator=policy[0].value,
                name=policy[1],
                arguments=[arg.build() for arg in policy[2]],
            )
            for policy in self._policies
        ]
