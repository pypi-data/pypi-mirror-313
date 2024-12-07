from enum import Enum


class Hook(str, Enum):
    """
    Enum representing the available hooks.
    """

    Fast = "fast-pii"
    Accurate = "accurate-pii"
    Regex = "regex-classifier"
    Datastructure = "data-structure-classifier"
    LLM = "llm-classifier"
