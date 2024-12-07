from typing import Dict, List

import antimatter_engine as am

from antimatter.tags import SpanTag
from antimatter.fieldtype import converters
from antimatter.fieldtype.fieldtypes import FieldType

TAG_SOURCE = "manual"
TAG_VERSION = (0, 0, 0)


class SpanTagApplicator:
    """
    SpanTagApplicator wraps user-provided span tags into intermediary form span
    tags when the tag applies to cell data.
    """

    _tags: Dict[str, List[SpanTag]]

    def __init__(self, span_tags: List[SpanTag]):
        """
        Initialize a SpanTagApplicator with a list of user-provided span tags.

        :param span_tags: User-provided span tags
        """
        tags = {}
        for tag in span_tags or []:
            if tag.cell_path not in tags:
                tags[tag.cell_path] = []
            tags[tag.cell_path].append(tag)
        self._tags = tags

    def span_tags_for_cell(
        self, cell_path: str, cell_val: bytes, field_type: FieldType
    ) -> List[am.PySpanTag]:
        """
        Given the path to a cell, provide a list of intermediary form span tags
        that apply to the cell. The cell's value and field type are used to ensure
        span tags are applied properly across various types of data. For example,
        when a user specifies start and end indices for a string, they likely intend
        to index it based on rune, not on byte.

        :param cell_path: The name of the path to a cell
        :param cell_val: The value in generic form of the cell pointed to in the cell path
        :param field_type: The original type of data in the cell
        :return: A list of span tags that apply to the cell pointed to in the cell path
        """
        tags = []
        if span_tags := self._tags.get(cell_path):
            for st in span_tags:
                start = st.start
                end = st.end

                # If the start isn't specified, assume it means the start of the value
                if start is None:
                    start = 0

                # If the end isn't specified, assume it means the end of the value
                if end is None:
                    end = len(cell_val)

                if field_type is FieldType.String and end != len(cell_val):
                    # Caller shouldn't have to know that the underlying type is
                    # bytes. Convert back to string, so we can index by rune and
                    # find the byte positioning
                    data = converters.Standard.field_converter_from_generic(FieldType.String)(cell_val)
                    converter = converters.Standard.field_converter_to_generic(FieldType.String)
                    b_idx = 0
                    for i, rune in enumerate(data):
                        if i == st.start:
                            start = b_idx
                        b = converter(rune)
                        b_idx += len(b)
                        if i + 1 == st.end:
                            end = b_idx

                tags.append(
                    am.PySpanTag(
                        am.PyTag(st.name, st.tag_type.value, st.tag_value, TAG_SOURCE, TAG_VERSION),
                        start,
                        end,
                    )
                )
        return tags
