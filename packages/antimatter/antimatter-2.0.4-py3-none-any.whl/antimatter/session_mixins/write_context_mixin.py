from typing import Any, Callable, Dict, List, Optional

import antimatter_api as openapi_client
from antimatter_api.models import (
    LLMClassifierConfig,
    RegexClassifierConfig,
    ClassifierRule,
    WriteContextClassifierTag,
    TagTypeField,
)
from antimatter.builders import (
    WriteContextBuilder,
    WriteContextConfigurationBuilder,
    WriteContextClassifierRuleBuilder,
)
from antimatter.session_mixins.base import BaseMixin
from antimatter.converters import TagConverter
from antimatter.tags import TagType


class WriteContextMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for write contexts.
    """

    def add_write_context(
        self,
        name: str,
        builder: WriteContextBuilder,
    ) -> None:
        """
        Upserts a write context for the current domain and auth

        :param name: The name of the write context to add or update
        :param builder: The builder containing write context configuration
        """
        if builder is None:
            raise ValueError("Write context builder is required")
        self.authz.get_session().add_write_context(name, builder.build().to_json())

    def list_write_context(self) -> List[openapi_client.WriteContextDetails]:
        """
        Returns a list of write contexts available for the current domain and auth
        """
        return openapi_client.WriteContextList.from_json(
            self.authz.get_session().list_write_context()
        ).write_contexts

    def describe_write_context(self, name: str) -> openapi_client.WriteContextDetails:
        """
        Returns the write context with the given name for the current domain and auth

        :param name: The name of the write context to describe
        :return: The full details of the write context
        """
        return openapi_client.WriteContextDetails.from_json(
            self.authz.get_session().describe_write_context(name)
        )

    def upsert_write_context_configuration(
        self,
        name: str,
        builder: WriteContextConfigurationBuilder,
    ) -> None:
        """
        Update a write context configuration. The write context must already exist.

        :param name: The name of the write context to update the configuration for
        :param builder: The builder containing write context configuration
        """
        if builder is None:
            raise ValueError("Write context configuration builder is required")
        self.authz.get_session().upsert_write_context_configuration(name, builder.build().to_json())

    def delete_write_context(self, name: str) -> None:
        """
        Delete a write context. All configuration associated with this write
        context will also be deleted. Domain policy rules referencing this write
        context will be left as-is.

        :param name: The name of the write context to delete
        """
        self.authz.get_session().delete_write_context(name)

    def list_write_context_classifier_rules(self, context_name: str) -> List[openapi_client.ClassifierRule]:
        """
        List all regex rules for the write context.

        :param context_name: The name of the write context
        :return: The list of rules
        """
        return openapi_client.DomainGetWriteContextClassifierRules200Response.from_json(
            self.authz.get_session().list_write_context_classifier_rules(context_name)
        ).rules

    def insert_write_context_classifier_rule(
        self,
        context_name: str,
        comment: Optional[str] = None,
        span_tags: List[str] = [],
        capsule_tags: List[str] = [],
        llm_model: Optional[str] = None,
        llm_prompt: Optional[str] = None,
        regex_pattern: Optional[str] = None,
        regex_match_on_key: Optional[bool] = None,
    ) -> str:
        """
        Insert a classifier rule for the context.

        :param context_name: The name of the write context
        :param comment: The comment for the classifier rule
        :param span_tags: The span tags for the classifier rule
        :param capsule_tags: The capsule tags for the classifier rule
            Span tags and capsule tags can be of the form:
            - A list of unary tags, like ['tag.antimatter.io/pii/email', 'tag.antimatter.io/pii/name']
            - A list of key-value pairs, like ["tag.antimatter.io/pii/date=24/12/2021", "tag.antimatter.io/pii/credit_card=1234"]
            - A list of dictionaries, like [{"tag.antimatter.io/pii/email": ""}, {"tag.antimatter.io/pii/date": "24/12/2021"}]
            - A list of dictionaries as a name/value pair, like [{"name": "tag.antimatter.io/pii/email", "value": ""}, {"name": "tag.antimatter.io/pii/date", "value": "24/12/2021"}]
            - Any combination of the above
        :param llm_model: The LLM model for the classifier rule. One of: 'openai', 'bedrock'
            One of the following must be provided: llm classifier rules or regex classifier rules
        :param llm_prompt: The LLM prompt for the classifier rule
        :param regex_pattern: A regex pattern for the classifier rule
            One of the following must be provided: llm classifier rules or regex classifier rules
        :param regex_match_on_key: A regex match on key for the classifier rule
        """

        def get_tag(tag: TagType) -> TagTypeField:
            if tag.name == "Unary":
                return TagTypeField.UNARY
            elif tag.name == "Boolean":
                return TagTypeField.BOOLEAN
            elif tag.name == "String":
                return TagTypeField.STRING
            elif tag.name == "Number":
                return TagTypeField.NUMBER
            elif tag.name == "Date":
                return TagTypeField.DATE
            raise ValueError(f"Invalid tag type: {tag.name}")

        span_tags = [
            WriteContextClassifierTag(
                name=tag.name,
                value=tag.tag_value,
                # convert tag type to string to the tagtype enum.
                type=get_tag(tag.tag_type),
            )
            for tag in TagConverter.convert_tags(span_tags)
        ]
        capsule_tags = [
            WriteContextClassifierTag(
                name=tag.name,
                value=tag.tag_value,
                type=get_tag(tag.tag_type),
            )
            for tag in TagConverter.convert_tags(capsule_tags)
        ]

        if llm_model is None and llm_prompt is None and regex_pattern is None:
            raise ValueError("Either llm_model, llm_prompt, or regex_pattern must be provided")
        if llm_model is not None and llm_prompt is None:
            raise ValueError("llm_prompt is required when llm_model is provided")
        if regex_pattern is not None and regex_match_on_key is None:
            raise ValueError("regex_match_on_key is required when regex_pattern is provided")
        llm_config, regex_config = None, None
        if llm_model is not None:
            llm_config = LLMClassifierConfig(
                model=llm_model,
                prompt=llm_prompt,
            )
        if regex_pattern is not None:
            regex_config = RegexClassifierConfig(
                pattern=regex_pattern,
                match_on_key=regex_match_on_key,
            )

        if llm_config is not None and regex_config is not None:
            raise ValueError("Only one of llm_model or regex_pattern can be provided at a time")

        return openapi_client.DomainInsertWriteContextClassifierRule200Response.from_json(
            self.authz.get_session().insert_write_context_classifier_rule(
                context_name,
                ClassifierRule(
                    comment=comment,
                    span_tags=span_tags,
                    capsule_tags=capsule_tags,
                    llm_config=llm_config,
                    regex_config=regex_config,
                ).to_json(),
            )
        ).rule_id

    def delete_write_context_classifier_rule(self, context_name: str, rule_id: str) -> None:
        """
        Delete a regex classifier rule for the context.

        :param context_name: The name of the write context
        :param rule_id: The ID of the rule to delete
        """
        self.authz.get_session().delete_write_context_classifier_rule(context_name, rule_id)

    def delete_write_context_classifier_rules(self, context_name: str) -> None:
        """
        Delete the regex classifier rules for the context.

        :param context_name: The name of the write context
        """
        self.authz.get_session().delete_write_context_classifier_rules(context_name)
