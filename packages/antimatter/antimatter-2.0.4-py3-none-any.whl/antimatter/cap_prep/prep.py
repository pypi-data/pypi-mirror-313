from collections import defaultdict
from typing import Any, Dict, List, Tuple

import antimatter_engine as am

from antimatter.cap_prep.applicator import SpanTagApplicator, TAG_SOURCE, TAG_VERSION
from antimatter.tags import ColumnTag, SpanTag, RowTag
from antimatter.cell_utils import cell_path
from antimatter.extra_helper import get_field_type


class Preparer:
    """
    Preparer is a helper class to prepare data for encapsulation, packing it in
    the intermediary data formats.
    """

    @classmethod
    def prepare(
        cls,
        col_names: List[str],
        col_tags: List[ColumnTag],
        row_tags: List[RowTag],
        skip_classify_col_names: List[str],
        raw_data: List[List[bytes]],
        span_tags: List[SpanTag],
        extra_dict: Dict[str, Any],
    ) -> Tuple[List[am.PyColumnDefinition], List[am.PyDataRow]]:
        """
        Prepare the columns, raw data, and tags, packing into the intermediary
        data formats.

        :param col_names: The names of the columns in the data set
        :param col_tags: User-provided tags for entire columns of data
        :param row_tags: User-provided tags for rows of data
        :param skip_classify_col_names: List of columns to skip classification on
        :param raw_data: The data set in generic format
        :param span_tags: User-provided span tags to bundle with the data
        :param extra_dict: Dictionary containing metadata for data handling and formatting
        :return: Wrapped column definitions and data elements
        """
        return (
            column_definitions(col_names, col_tags, skip_classify_col_names),
            data_elements(col_names, raw_data, span_tags, row_tags, extra_dict),
        )


def column_definitions(
    col_names: List[str], col_tags: List[ColumnTag], skip_classify_col_names: List[str]
) -> List[am.PyColumnDefinition]:
    """
    Helper function for packaging column definitions.

    :param col_names: The names of the columns in the data set
    :param col_tags: User-provided tags for entire columns of data
    :param skip_classify_col_names: List of columns to skip classification on
    :return: Wrapped column definitions
    """
    tags = defaultdict(list)
    for tag in col_tags:
        for tag_name in tag.tag_names:
            tags[tag.column_name].append(
                am.PyTag(tag_name, tag.tag_type.value, tag.tag_value, TAG_SOURCE, TAG_VERSION)
            )

    return [
        am.PyColumnDefinition(
            col_name, tags.get(col_name, []), True if col_name in skip_classify_col_names else False
        )
        for col_name in col_names
    ]


def pack_row_tags(idx: int, tags: List[RowTag]) -> List[am.PyTag]:
    """
    Helper function to group row tags for a given row
    """
    row_tags = []
    if tags is None:
        return row_tags
    for tag in tags:
        if tag.row_idx == idx:
            for tag_name in tag.tag_names:
                row_tags.append(
                    am.PyTag(tag_name, tag.tag_type.value, tag.tag_value, TAG_SOURCE, TAG_VERSION)
                )

    return row_tags


def data_elements(
    col_names: List[str],
    raw_data: List[List[bytes]],
    span_tags: List[SpanTag],
    row_tags: List[RowTag],
    extra_dict: Dict[str, Any],
) -> List[am.PyDataRow]:
    """
    Helper function for packaging data elements into rows. Applies span tags to matching
    cell data where applicable.

    :param col_names: The names of the columns in the data set
    :param raw_data: The data set in generic format
    :param span_tags: User-provided span tags to bundle with the data
    :param row_tags: User-provided row tags to bundle with the data
    :param extra_dict: Dictionary containing metadata for data handling and formatting
    :return: Wrapped data elements
    """
    elems = []

    span_applicator = SpanTagApplicator(span_tags)
    for i, raw_row in enumerate(raw_data):
        elems_row = []
        for col, field in zip(col_names, raw_row):
            p = cell_path(col, i)
            elems_row.append(
                am.PyDataElement(
                    field,
                    span_applicator.span_tags_for_cell(p, field, get_field_type(col, extra_dict)),
                )
            )
        elems.append(am.PyDataRow(elems_row, pack_row_tags(i, row_tags)))

    return elems
