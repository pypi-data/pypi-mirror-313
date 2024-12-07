from typing import Optional, Union

import antimatter_api as openapi_client
from antimatter.tags import TagType


class WriteContextClassifierRuleBuilder:
    """
    Builder class for creating a WriteContextRegexRule
    """

    def __init__(self):
        """
        Initialize a new instance of WriteContextClassifierRuleBuilder.
        """
        self._match_on_key = False
        self._span_tags = []
        self._capsule_tags = []
        self._regex_pattern = None
        self._llm_config = None

    def add_regex_rule(self, pattern: str, match_on_key: bool = False) -> "WriteContextClassifierRuleBuilder":
        """
        Create a new regex rule builder.

        :param pattern: The regex pattern for matching
        :param match_on_key: If True, match against the key instead of the field
        :return: The builder instance
        """
        if self._llm_config is not None:
            raise ValueError("Cannot add a regex rule when an LLM config is already set")

        self._regex_pattern = openapi_client.RegexClassifierConfig(
            pattern=pattern,
            match_on_key=match_on_key,
        )
        return self

    def add_llm_config(self, model: str, prompt: str) -> "WriteContextClassifierRuleBuilder":
        """
        Add LLM config to the rule

        :param model: The LLM model to use
        :param prompt: The prompt to use
        :return: The builder instance
        """
        if self._regex_pattern is not None:
            raise ValueError("Cannot add an LLM config when a regex rule is already set")

        self._llm_config = openapi_client.LLMClassifierConfig(
            model=model,
            prompt=prompt,
        )

    def add_span_tag(
        self,
        name: str,
        tag_type: Union[str, TagType] = TagType.Unary,
        value: Optional[str] = None,
    ) -> "WriteContextClassifierRuleBuilder":
        """
        The span tag to add when the regex rule matches

        :param name: The span tag name
        :param tag_type: The span tag type; default 'unary'
        :param value: The span tag value, if the tag_type is not 'unary'
        :return: The builder instance
        """
        tag_type = TagType(tag_type).name.lower()
        self._span_tags.append(
            openapi_client.WriteContextClassifierTag(
                name=name,
                value=value,
                type=openapi_client.TagTypeField(tag_type),
            )
        )
        return self

    def add_capsule_tag(
        self,
        name: str,
        tag_type: Union[str, TagType] = TagType.Unary,
        value: Optional[str] = None,
    ) -> "WriteContextClassifierRuleBuilder":
        """
        The capsule tag to add when the regex rule matches

        :param name: The capsule tag name
        :param tag_type: The capsule tag type; default 'unary'
        :param value: The capsule tag value, if the tag_type is not 'unary'
        :return: The builder instance
        """
        tag_type = TagType(tag_type).name.lower()
        self._capsule_tags.append(
            openapi_client.WriteContextClassifierTag(
                name=name,
                value=value,
                type=openapi_client.TagTypeField(tag_type),
            )
        )
        return self

    def build(self) -> openapi_client.ClassifierRule:
        """
        Build the rule.

        :return: The built rule
        """
        return openapi_client.ClassifierRule(
            span_tags=self._span_tags,
            capsule_tags=self._capsule_tags,
            regexConfig=self._regex_pattern,
            llmConfig=self._llm_config,
        )
