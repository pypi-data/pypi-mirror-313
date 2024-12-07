from typing import List, Optional, Tuple, Union

import antimatter_api as openapi_client
from antimatter.constants import CapabilityOperator


class CapabilityRulesBuilder:
    """
    Builder class for creating a CapabilityRule.

    :param rules: A list of tuples containing the name, operator, and values of the match expression.
    """

    def __init__(self, *rules):
        self._rules: List[Tuple[str, CapabilityOperator, List[str]]] = list(rules)

    def with_rule(
        self,
        name: str,
        operator: Optional[Union[CapabilityOperator, str]],
        values: Optional[List[str]] = None,
    ) -> "CapabilityRulesBuilder":
        """
        Add a match expression to the rule.

        :param name: The name of the match expression.
        :param operator: The operator of the match expression.
        :param values: The values of the match expression.
        """
        if operator is not None:
            operator = CapabilityOperator(operator)
        if values is None:
            values = []
        self._rules.append((name, operator, values))
        return self

    def build(self) -> openapi_client.CapabilityRule:
        """
        Build the rule.

        :return: The CapabilityRule which can be used to create a new capability.
        """
        return openapi_client.CapabilityRule(
            match_expressions=[
                openapi_client.CapabilityRuleMatchExpressionsInner(
                    name=rule[0],
                    operator=rule[1] and rule[1].value,
                    values=rule[2],
                )
                for rule in self._rules
            ]
        )
