from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union


class TagType(Enum):
    """
    The span tag types
    """

    Unary = 0
    String = 1
    Number = 2
    Boolean = 3
    Date = 4


@dataclass
class SpanTag:
    """
    Defines a span tag manually to the data contained in the cell path. The tag
    is applied to the subset of data contained between start (inclusive) and end
    (exclusive).

    The cell path describes which cell to apply this tag to. Cell paths can be
    created using the antimatter.cell_utils.cell_path(cname, rnum) helper function,
    which takes the name of the column and the row number. As an example, if the
    cell to apply this span tag to was in a column named "name" and was in row 10
    of the data, the cell path would be "name[9]" (the first row would be number 0).
    """

    name: str
    start: Optional[int] = None
    end: Optional[int] = None
    cell_path: str = ""
    tag_type: TagType = TagType.Unary
    tag_value: str = ""

    def __repr__(self) -> str:
        output = (
            f"SpanTag(name={self.name!r}, start={self.start!r}, end={self.end!r}"
            f", cell_path={self.cell_path!r}"
            f", tag_type={self.tag_type}"
        )

        if self.tag_type != TagType.Unary:
            output += f", tag_value={self.tag_value!r}"

        output += ")"
        return output


@dataclass
class ColumnTag:
    """
    Defines a column tag manually set to apply a rule to a particular column of data.
    """

    column_name: str
    tag_names: List[str]
    tag_type: TagType = TagType.Unary
    tag_value: str = ""

    def __repr__(self) -> str:
        output = (
            f"ColumnTag(column_name={self.column_name!r}, tag_names={self.tag_names!r}"
            f", tag_type={self.tag_type}"
        )

        if self.tag_type != TagType.Unary:
            output += f", tag_value={self.tag_value!r}"

        output += ")"
        return output


@dataclass
class RowTag:
    """
    Defines a row tag manually set to apply a rule to all cells in a data row.
    """

    row_idx: int
    tag_names: List[str]
    tag_type: TagType = TagType.Unary
    tag_value: str = ""

    def __repr__(self) -> str:
        output = f"RowTag(row_idx={self.row_idx}, tag_names={self.tag_names!r}, tag_type={self.tag_type}"

        if self.tag_type != TagType.Unary:
            output += f", tag_value={self.tag_value!r}"

        output += ")"
        return output


@dataclass
class CapsuleTag:
    """
    Defines a capsule tag manually set to apply a rule to a capsule.
    """

    name: str
    tag_type: TagType = TagType.Unary
    tag_value: str = ""

    def __repr__(self) -> str:
        output = f"CapsuleTag(name={self.name!r}" f", tag_type={self.tag_type}"

        if self.tag_type != TagType.Unary:
            output += f", tag_value={self.tag_value!r}"

        output += ")"
        return output


def get_tag_name(tag: Optional[Union[str, CapsuleTag, ColumnTag, SpanTag]] = None) -> str:
    if tag:
        if isinstance(tag, CapsuleTag):
            tag = tag.name
        elif isinstance(tag, ColumnTag):
            if len(tag.tag_names) > 0:
                tag = tag.tag_names[0]
        elif isinstance(tag, SpanTag):
            tag = tag.name
    return tag
