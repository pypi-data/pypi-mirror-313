from typing import Optional, List
import antimatter_api as openapi_client
from antimatter.constants import Operator
from enum import Enum


class RuleEffect(Enum):
    DENYCAPSULE = openapi_client.DataPolicyRuleEffect.DENYCAPSULE
    DENYRECORD = openapi_client.DataPolicyRuleEffect.DENYRECORD
    REDACT = openapi_client.DataPolicyRuleEffect.REDACT
    TOKENIZE = openapi_client.DataPolicyRuleEffect.TOKENIZE
    ALLOW = openapi_client.DataPolicyRuleEffect.ALLOW


class TokenScope(Enum):
    UNIQUE = "unique"
    CAPSULE = "capsule"
    DOMAIN = "domain"


class TokenFormat(Enum):
    EXPLICIT = "explicit"
    SYNTHETIC = "synthetic"


class AssignPriority(Enum):
    FIRST = "first"
    LAST = "last"


class ClauseOperator(Enum):
    AllOf = "AllOf"
    NotAllOf = "NotAllOf"
    AnyOf = "AnyOf"
    NotAnyOf = "NotAnyOf"
    Always = "Always"


class Attachment(Enum):
    Inherit = "Inherit"
    NotAttached = "NotAttached"
    Attached = "Attached"


class ExpressionBuilder:
    def __init__(self):
        self.name = ""
        self.values = []
        self.operator = ""
        self.variables = []

    def set_name(self, name: str) -> "ExpressionBuilder":
        self.name = name
        return self

    def add_value(self, value: str) -> "ExpressionBuilder":
        self.values.append(value)
        return self

    def set_operator(self, operator: str) -> "ExpressionBuilder":
        self.operator = operator
        return self

    def add_variable(self, variable: "VariableBuilder") -> "ExpressionBuilder":
        self.variables.append(variable.build())
        return self


class TagExpressionBuilder(ExpressionBuilder):
    def build(self) -> openapi_client.TagExpression:
        return openapi_client.TagExpression(
            name=self.name, values=self.values, operator=self.operator, variables=self.variables
        )


class CapabilityExpressionBuilder(ExpressionBuilder):
    def build(self) -> openapi_client.CapabilityExpression:
        return openapi_client.CapabilityExpression(
            name=self.name, values=self.values, operator=self.operator, variables=self.variables
        )


class ReadParameterExpressionBuilder(ExpressionBuilder):
    def build(self) -> openapi_client.ReadParameterExpression:
        return openapi_client.ReadParameterExpression(
            name=self.name, values=self.values, operator=self.operator, variables=self.variables
        )


class FactExpressionBuilder:
    def __init__(self):
        self.type = ""
        self.operator = ""
        self.arguments = []
        self.variables = None

    def set_type(self, fact_type: str) -> "FactExpressionBuilder":
        self.type = fact_type
        return self

    def set_operator(self, operator: str) -> "FactExpressionBuilder":
        self.operator = operator
        return self

    def add_argument(self, operator: Operator, values: List[str] = []) -> "FactExpressionBuilder":
        self.arguments.append(
            openapi_client.FactExpressionArgumentsInner(operator=operator.value, values=values)
        )
        return self

    def add_variable(self, variable: "VariableBuilder") -> "FactExpressionBuilder":
        self.variables.append(variable.build())
        return self

    def build(self) -> openapi_client.FactExpression:
        return openapi_client.FactExpression(
            type=self.type, operator=self.operator, arguments=self.arguments, variables=self.variables
        )


class FactExpressionArgumentBuilder:
    def __init__(self):
        self.operator = ""
        self.values = []

    def set_operator(self, operator: str) -> "FactExpressionArgumentBuilder":
        self.operator = operator
        return self

    def add_value(self, value: str) -> "FactExpressionArgumentBuilder":
        self.values.append(value)
        return self

    def build(self) -> openapi_client.FactExpressionArgumentsInner:
        return openapi_client.FactExpressionArgumentsInner(operator=self.operator, values=self.values)


class VariableBuilder:
    def __init__(self):
        self.variable_name = ""
        self.source = ""
        self.tag_name = None
        self.capability_name = None
        self.fact_type = None
        self.fact_arguments = []
        self.variables = []

    def set_variable_name(self, name: str) -> "VariableBuilder":
        self.variable_name = name
        return self

    def set_source(self, source: str) -> "VariableBuilder":
        self.source = source
        return self

    def set_tag_name(self, tag_name: str) -> "VariableBuilder":
        self.tag_name = tag_name
        return self

    def set_capability_name(self, capability_name: str) -> "VariableBuilder":
        self.capability_name = capability_name
        return self

    def set_fact_type(self, fact_type: str) -> "VariableBuilder":
        self.fact_type = fact_type
        return self

    def add_fact_argument(self, argument: FactExpressionArgumentBuilder) -> "VariableBuilder":
        self.fact_arguments.append(argument.build())
        return self

    def add_variable(self, variable: "VariableBuilder") -> "VariableBuilder":
        self.variables.append(variable.build())
        return self

    def build(self) -> openapi_client.VariableDefinition:
        return openapi_client.VariableDefinition(
            variableName=self.variable_name,
            source=self.source,
            tagName=self.tag_name,
            capabilityName=self.capability_name,
            factType=self.fact_type,
            factArguments=self.fact_arguments,
            variables=self.variables,
        )


class DataPolicyClauseBuilder:
    def __init__(
        self,
        operator: ClauseOperator,
    ):
        self.operator = operator
        self.tags = []
        self.capabilities = []
        self.facts = []
        self.read_parameters = []

    def add_tag(self, tag: TagExpressionBuilder) -> "DataPolicyClauseBuilder":
        self.tags.append(tag.build())
        return self

    def add_capability(self, capability: CapabilityExpressionBuilder) -> "DataPolicyClauseBuilder":
        self.capabilities.append(capability.build())
        return self

    def add_fact(self, fact: FactExpressionBuilder) -> "DataPolicyClauseBuilder":
        self.facts.append(fact.build())
        return self

    def add_read_parameter(self, read_parameter: ReadParameterExpressionBuilder) -> "DataPolicyClauseBuilder":
        self.read_parameters.append(read_parameter.build())
        return self

    def build(self) -> openapi_client.DataPolicyClause:
        return openapi_client.DataPolicyClause(
            operator=self.operator.value,
            tags=self.tags,
            capabilities=self.capabilities,
            facts=self.facts,
            readParameters=self.read_parameters,
        )


class NewDataPolicyRuleBuilder:
    def __init__(
        self,
        effect: RuleEffect,
        comment: Optional[str] = None,
        token_scope: Optional[TokenScope] = None,
        token_format: Optional[TokenFormat] = None,
        assign_priority: Optional[AssignPriority] = None,
        priority: Optional[int] = None,
    ):
        self.clauses = []
        self.effect = effect
        self.token_scope = token_scope
        self.token_format = token_format
        self.assign_priority = assign_priority
        self.priority = priority
        self.comment = comment

        # either of priority or assign_priority should be set
        if priority is not None and assign_priority is not None:
            raise ValueError("Either of priority or assign_priority should be set")

    def add_clause(self, clause: DataPolicyClauseBuilder) -> "NewDataPolicyRuleBuilder":
        self.clauses.append(clause.build())
        return self

    def build(self) -> openapi_client.NewDataPolicyRule:
        return openapi_client.NewDataPolicyRule(
            clauses=self.clauses,
            effect=self.effect.value,
            comment=self.comment,
            tokenScope=self.token_scope.value if self.token_scope is not None else None,
            tokenFormat=self.token_format.value if self.token_format is not None else None,
            assignPriority=self.assign_priority.value if self.assign_priority is not None else None,
            priority=self.priority,
        )


class DataPolicyRuleChangesBuilder:
    def __init__(self):
        self.new_rules = []
        self.delete_rules = []

    def add_rule(self, rule: NewDataPolicyRuleBuilder) -> "DataPolicyRuleChangesBuilder":
        self.new_rules.append(rule.build())
        return self

    def delete_rules(self, rule_ids: List[str]) -> "DataPolicyRuleChangesBuilder":
        self.delete_rules.extend(rule_ids)
        return self

    def build(self) -> openapi_client.DataPolicyRuleChanges:
        return openapi_client.DataPolicyRuleChanges(new_rules=self.new_rules, delete_rules=self.delete_rules)
