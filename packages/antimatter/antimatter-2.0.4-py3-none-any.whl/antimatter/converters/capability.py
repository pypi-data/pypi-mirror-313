from typing import List, Dict, Any, Union
from antimatter.converters.tags import TagConverter


class CapabilityConverter:
    @staticmethod
    def convert_capabilities(capabilities: List[Union[str, Dict[str, Any]]]) -> Dict[str, str]:
        """
        Convert a list of capabilities into a dictionary.
        """
        tags = TagConverter.convert_tags(capabilities, unary_value=None)
        capability_dict = {}
        for tag in tags:
            capability_dict[tag.name] = tag.tag_value
        return capability_dict
