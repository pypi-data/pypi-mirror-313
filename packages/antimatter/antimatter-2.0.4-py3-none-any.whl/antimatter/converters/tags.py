from typing import List, Dict, Any, Union
from antimatter.tags import SpanTag, TagType
from antimatter.fieldtype.infer import infer_fieldtype
from antimatter.fieldtype.fieldtypes import FieldType


class TagConverter:
    """
    Supports parsing tags from strings and dictionaries.
    Tags can be of the following format:
    - A list of unary tags, like ['tag.antimatter.io/pii/email', 'tag.antimatter.io/pii/name', 'name', 'admin']
    - A list of key-value pairs, like ["tag.antimatter.io/pii/date=24/12/2021", "tag.antimatter.io/pii/credit_card=1234", 'admin=True']
    - A list of dictionaries, like [{"tag.antimatter.io/pii/email": ""}, {"tag.antimatter.io/pii/date": "24/12/2021"}]
    - A list of dictionaries as a name/value pair, like [{"name": "tag.antimatter.io/pii/email", "value": ""}, {"name": "tag.antimatter.io/pii/date", "value": "24/12/2021"}]
    - Any combination of the above
    """

    @staticmethod
    def infer_type(tag: str) -> FieldType:
        """
        Infer the field type of the tag value.
        """
        if tag is None:
            return TagType.Unary
        tag_type = TagType.String
        cls_type = infer_fieldtype(tag)
        if cls_type in [FieldType.Int, FieldType.Float, FieldType.Decimal]:
            tag_type = TagType.Number
        elif cls_type is FieldType.Bool:
            tag_type = TagType.Boolean
        elif cls_type in [FieldType.Date, FieldType.DateTime, FieldType.Time]:
            tag_type = TagType.Date
        return tag_type

    @staticmethod
    def _process_string_tag(tag: str, unary_value: Any) -> SpanTag:
        """
        Process a tag provided as a string and return it as a dictionary.
        String tags can be unary or key-value pairs separated by an equal sign. Construct a SpanTag object from the string.
        """
        if "=" in tag:
            split_pairs = tag.split("=", maxsplit=1)
            return SpanTag(
                name=split_pairs[0],
                tag_type=TagConverter.infer_type(split_pairs[1]),
                tag_value=split_pairs[1],
            )
        else:
            return SpanTag(name=tag, tag_type=TagType.Unary, tag_value=unary_value)

    @staticmethod
    def _process_dict_tag(tag: Dict[str, Any], unary_value: Any) -> SpanTag:
        """
        Process a tag provided as a dictionary and return it as a dictionary.
        Dictionary tags can be unary or key-value pairs. Construct a SpanTag object from the dictionary.
        """
        if "name" in tag and "value" in tag:
            return SpanTag(
                name=tag["name"], tag_type=TagConverter.infer_type(tag["value"]), tag_value=tag["value"]
            )
        elif "name" in tag or "value" in tag:
            raise ValueError("Capability dictionary must have both 'name' and 'value' fields")
        else:
            if len(tag) == 0:
                raise ValueError("Tag dictionary must have at least one key-value pair")
            key = list(tag.keys())[0]
            value = tag[key]

            return SpanTag(name=key, tag_type=TagConverter.infer_type(value), tag_value=value)

    @staticmethod
    def convert_tags(tags: List[Union[str, Dict[str, Any]]], unary_value: Any = "") -> List[SpanTag]:
        """
        Convert a list of tags into a dictionary.
        """
        span_tags = []
        for tag in tags:
            if isinstance(tag, dict):
                span_tags.append(TagConverter._process_dict_tag(tag, unary_value))
            elif isinstance(tag, str):
                span_tags.append(TagConverter._process_string_tag(tag, unary_value))
            else:
                raise ValueError("Tag must be a string or dictionary")
        return span_tags
