from antimatter.tags import TagType, SpanTag, ColumnTag, RowTag, CapsuleTag


def test_span_tag_repr():
    span_tag = SpanTag(
        name="example", start=0, end=5, cell_path="name[9]", tag_type=TagType.String, tag_value="value"
    )
    expected_repr = "SpanTag(name='example', start=0, end=5, cell_path='name[9]', tag_type=TagType.String, tag_value='value')"
    assert repr(span_tag) == expected_repr
    assert str(span_tag) == expected_repr

    span_tag_unary = SpanTag(name="example_unary")
    expected_repr_unary = (
        "SpanTag(name='example_unary', start=None, end=None, cell_path='', tag_type=TagType.Unary)"
    )
    assert repr(span_tag_unary) == expected_repr_unary
    assert str(span_tag_unary) == expected_repr_unary


def test_column_tag_repr():
    column_tag = ColumnTag(
        column_name="column1", tag_names=["tag1", "tag2"], tag_type=TagType.Number, tag_value="123"
    )
    expected_repr = "ColumnTag(column_name='column1', tag_names=['tag1', 'tag2'], tag_type=TagType.Number, tag_value='123')"
    assert repr(column_tag) == expected_repr
    assert str(column_tag) == expected_repr

    column_tag_unary = ColumnTag(column_name="column1", tag_names=["tag1", "tag2"])
    expected_repr_unary = (
        "ColumnTag(column_name='column1', tag_names=['tag1', 'tag2'], tag_type=TagType.Unary)"
    )
    assert repr(column_tag_unary) == expected_repr_unary
    assert str(column_tag_unary) == expected_repr_unary


def test_row_tag_repr():
    column_tag = RowTag(row_idx=1, tag_names=["tag1", "tag2"], tag_type=TagType.Number, tag_value="123")
    expected_repr = "RowTag(row_idx=1, tag_names=['tag1', 'tag2'], tag_type=TagType.Number, tag_value='123')"
    assert repr(column_tag) == expected_repr
    assert str(column_tag) == expected_repr

    row_tag_unary = RowTag(row_idx=5, tag_names=["tag1", "tag2"])
    expected_repr_unary = "RowTag(row_idx=5, tag_names=['tag1', 'tag2'], tag_type=TagType.Unary)"
    assert repr(row_tag_unary) == expected_repr_unary
    assert str(row_tag_unary) == expected_repr_unary


def test_capsule_tag_repr():
    capsule_tag = CapsuleTag(name="capsule1", tag_type=TagType.Boolean, tag_value="true")
    expected_repr = "CapsuleTag(name='capsule1', tag_type=TagType.Boolean, tag_value='true')"
    assert repr(capsule_tag) == expected_repr
    assert str(capsule_tag) == expected_repr

    capsule_tag_unary = CapsuleTag(name="capsule1")
    expected_repr_unary = "CapsuleTag(name='capsule1', tag_type=TagType.Unary)"
    assert repr(capsule_tag_unary) == expected_repr_unary
    assert str(capsule_tag_unary) == expected_repr_unary
