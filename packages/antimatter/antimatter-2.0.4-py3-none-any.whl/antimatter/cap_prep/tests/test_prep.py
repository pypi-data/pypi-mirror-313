from collections import defaultdict

import pytest

from antimatter.tags import ColumnTag, RowTag, SpanTag
import antimatter.handlers as handlers
from antimatter.cap_prep.prep import Preparer
from antimatter.cell_utils import cell_path
from antimatter.datatype.infer import infer_datatype
from antimatter.extra_helper import extra_for_session

some_col = "some"
name_col = "name"
std_data = [
    {some_col: "data", name_col: "The name is Adam Smith"},
    {some_col: "other data", name_col: "Joe Joseph"},
    {some_col: "données en français", name_col: "Monsieur Pierre Cousteau"},
]


class TestPreparer:
    @pytest.mark.parametrize(
        ("data", "span_tags", "col_tags", "row_tags"),
        (
            (std_data, [], [], []),
            (
                std_data,
                [
                    SpanTag("tag.antimatter.io/manual", cell_path=cell_path(some_col, 1), start=0, end=5),
                    SpanTag("tag.antimatter.io/manual", cell_path=cell_path(some_col, 2), start=8, end=10),
                ],
                [],
                [],
            ),
            (
                std_data,
                [],
                [ColumnTag(name_col, tag_names=["pii/name"])],
                [],
            ),
            (
                std_data,
                [
                    SpanTag("tag.antimatter.io/manual", cell_path=cell_path(some_col, 1), start=0, end=5),
                    SpanTag("tag.antimatter.io/manual", cell_path=cell_path(some_col, 2), start=8, end=10),
                ],
                [ColumnTag(name_col, tag_names=["pii/name"])],
                [],
            ),
            (
                std_data,
                [
                    SpanTag("tag.antimatter.io/manual", cell_path=cell_path(some_col, 1), start=0, end=5),
                    SpanTag("tag.antimatter.io/manual", cell_path=cell_path(some_col, 2), start=8, end=10),
                ],
                [ColumnTag(name_col, tag_names=["pii/name"])],
                [
                    RowTag(row_idx=0, tag_names=["user_a"]),
                    RowTag(row_idx=0, tag_names=["user_f"]),
                    RowTag(row_idx=1, tag_names=["user_b"]),
                    RowTag(row_idx=2, tag_names=["user_c"]),
                ],
            ),
        ),
        ids=(
            "data with no tags",
            "data with only span tags",
            "data with only column tag",
            "data with span tags and column tag",
            "data with span tags, row tags, and column tag",
        ),
    )
    def test_prepare(self, data, span_tags, col_tags, row_tags):
        dt = infer_datatype(data)
        h = handlers.factory(dt)
        col_names, raw, extra = h.to_generic(data)
        extra = extra_for_session(dt, {})

        cols, elems = Preparer.prepare(col_names, col_tags, row_tags, [], raw, span_tags, extra)
        assert len(cols) == len(data[0])
        assert len(elems) == len(data)

        expected_col_tags = defaultdict(lambda: 0)
        for tag in col_tags:
            expected_col_tags[tag.column_name] += len(tag.tag_names)

        for col in cols:
            assert len(col.tags) == expected_col_tags[col.name]

        span_tag_cnt = 0
        for row in elems:
            for elem in row.cells:
                span_tag_cnt += len(elem.span_tags)
        assert span_tag_cnt == len(span_tags)
