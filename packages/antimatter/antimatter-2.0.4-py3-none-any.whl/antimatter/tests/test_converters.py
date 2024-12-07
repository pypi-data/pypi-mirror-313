import pytest
import datetime
from antimatter.converters import CapabilityConverter, TagConverter
from antimatter.tags import SpanTag, TagType


@pytest.mark.parametrize(
    "capabilities,expected,expected_span_tags,error_expected",
    [
        # Test with empty capabilities
        ([], {}, [], False),
        # Test with capabilities as a list of dictionaries containing name, value pairs
        (
            [{"name": "capability1", "value": "value1"}],
            {"capability1": "value1"},
            [SpanTag(name="capability1", tag_type=TagType.String, tag_value="value1")],
            False,
        ),
        # Test with capabilities as a list of dictionaries containing key:value pairs
        (
            [{"capability1": "value1"}],
            {"capability1": "value1"},
            [SpanTag(name="capability1", tag_type=TagType.String, tag_value="value1")],
            False,
        ),
        # Test with capabilities as a list of strings containing equal signs
        (
            ["capability1=value1"],
            {"capability1": "value1"},
            [SpanTag(name="capability1", tag_type=TagType.String, tag_value="value1")],
            False,
        ),
        # Test with capabilities as a list of strings containing unary keys
        (
            ["capability1"],
            {"capability1": None},
            [SpanTag(name="capability1", tag_type=TagType.Unary, tag_value=None)],
            False,
        ),
        # Test with mixed capabilities
        (
            [{"name": "capability1", "value": "value1"}, "capability2=value2", "capability3"],
            {"capability1": "value1", "capability2": "value2", "capability3": None},
            [
                SpanTag(name="capability1", tag_type=TagType.String, tag_value="value1"),
                SpanTag(name="capability2", tag_type=TagType.String, tag_value="value2"),
                SpanTag(name="capability3", tag_type=TagType.Unary, tag_value=None),
            ],
            False,
        ),
        # Test with capabilities as a list of dictionaries
        (
            [{"name": "capability1", "value": "value1"}, {"name": "capability2", "value": "value2"}],
            {"capability1": "value1", "capability2": "value2"},
            [
                SpanTag(name="capability1", tag_type=TagType.String, tag_value="value1"),
                SpanTag(name="capability2", tag_type=TagType.String, tag_value="value2"),
            ],
            False,
        ),
        # Test with capabilities as a list of strings with "="
        (
            ["capability1=value1", "capability2=value2"],
            {"capability1": "value1", "capability2": "value2"},
            [
                SpanTag(name="capability1", tag_type=TagType.String, tag_value="value1"),
                SpanTag(name="capability2", tag_type=TagType.String, tag_value="value2"),
            ],
            False,
        ),
        # Test with capabilities as a list of strings without "="
        (
            ["capability1", "capability2"],
            {"capability1": None, "capability2": None},
            [
                SpanTag(name="capability1", tag_type=TagType.Unary, tag_value=None),
                SpanTag(name="capability2", tag_type=TagType.Unary, tag_value=None),
            ],
            False,
        ),
        # Test with capabilities as a list of strings with multiple "="
        (
            ["capability1=value1=value2"],
            {"capability1": "value1=value2"},
            [SpanTag(name="capability1", tag_type=TagType.String, tag_value="value1=value2")],
            False,
        ),
        # Invalid test case, list of dicts with name, value pairs but name is missing, or misspelled
        (
            [
                {"value": "value1"},
                {"name": "capability2", "value": "value2"},
                {"name": "capability"},
                {"name"},
                {"name": "capability4", "values": "value"},
            ],
            {},
            [],
            True,
        ),
        # Invalid case, set
        ([{"capability1"}], {}, [], True),
        # Invalid case, dict with no value
        ([{"name": "capability1"}], {}, [], True),
        # Valid case, integer value
        (
            [{"name": "capability1", "value": 123}],
            {"capability1": 123},
            [SpanTag(name="capability1", tag_type=TagType.Number, tag_value=123)],
            False,
        ),
        # Invalid case, tuples
        ([("name", "value"), ("name2", 4)], {}, [], True),
        # Add unary capability with None as dict value
        (
            [{"name": "capability1", "value": None}, {"capability2": None}],
            {"capability1": None, "capability2": None},
            [
                SpanTag(name="capability1", tag_type=TagType.Unary, tag_value=None),
                SpanTag(name="capability2", tag_type=TagType.Unary, tag_value=None),
            ],
            False,
        ),
        # Add tagtype bool
        (
            [{"name": "capability1", "value": True}],
            {"capability1": True},
            [SpanTag(name="capability1", tag_type=TagType.Boolean, tag_value=True)],
            False,
        ),
        # Add tagtype date
        (
            [{"name": "capability1", "value": datetime.date(2021, 1, 1)}],
            {"capability1": datetime.date(2021, 1, 1)},
            [SpanTag(name="capability1", tag_type=TagType.Date, tag_value=datetime.date(2021, 1, 1))],
            False,
        ),
        # Tag value = None in string
        (
            ["capability1="],
            {"capability1": ""},
            [SpanTag(name="capability1", tag_type=TagType.String, tag_value="")],
            False,
        ),
        # Empty dict
        ([{}], {}, [], True),
    ],
    ids=[
        "empty",
        "dict containing name, value pairs",
        "dict containing key:value pairs",
        "str containing unary key",
        "str_no_value",
        "mixed",
        "list of dicts with name, value pairs",
        "list of str with =",
        "list of str without =",
        "str with multiple =",
        "list of dicts with name, value pairs missing name or misspelled",
        "set",
        "dict with no value",
        "int value",
        "tuples",
        "unary capability with None as dict value",
        "tagtype bool",
        "tagtype date",
        "tag value = None in string",
        "empty dict",
    ],
)
def test_convertor(capabilities, expected, expected_span_tags, error_expected):
    if error_expected:
        with pytest.raises(ValueError):
            CapabilityConverter.convert_capabilities(capabilities)
    else:
        assert CapabilityConverter.convert_capabilities(capabilities) == expected

    if error_expected:
        with pytest.raises(ValueError):
            TagConverter.convert_tags(capabilities)
    else:
        assert TagConverter.convert_tags(capabilities, unary_value=None) == expected_span_tags
