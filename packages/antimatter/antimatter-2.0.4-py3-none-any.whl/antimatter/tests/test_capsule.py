import datetime

import pytest

from antimatter.tags import ColumnTag, SpanTag, TagType
from antimatter.capsule import Capsule, CapsuleBindings, AnnotatedData, _markup_bytes
import antimatter_engine as ae


@pytest.fixture
def mock_capsule_bindings(
    monkeypatch, capsule_tags, column_names, column_tags, redacted_data, data_span_tags, extra_info
):
    mock_capsule_bindings = CapsuleBindings(None)

    # mock the read_all_with_tags method
    monkeypatch.setattr(
        mock_capsule_bindings,
        "read_all_with_tags",
        lambda tags: (capsule_tags, column_names, column_tags, redacted_data, data_span_tags, extra_info),
    )

    return mock_capsule_bindings


@pytest.mark.parametrize(
    "capsule_tags, column_names, column_tags, redacted_data, data_span_tags, extra_info",
    [
        # Test case 1
        (
            [],  # capsule_tags
            [
                "email",
                "bytes",
                "fname",
                "bio",
                "duration",
                "dt",
                "float",
                "age",
                "status",
                "id",
            ],  # column_names
            [
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [
                    ae.PyTag("tag.antimatter.io/pii/age", 0, "", "manual", (1, 0, 0)),
                    ae.PyTag("tag.antimatter.io/pii/other", 0, "", "manual", (1, 0, 0)),
                ],
                [],
                [],
            ],  # column_tags
            [
                [
                    b"allen@gmail.com",
                    b"fdsa",
                    b"Allen",
                    b"{redacted} on {redacted} 9 1974 in Cheverly, MD",
                    b"{redacted}",
                    b"{redacted}",
                    b"3.14",
                    b"{redacted}",
                    b"True",
                    b"44",
                ],
                [
                    b"this is an email address: {redacted}",
                    b"asdf",
                    b"Bob",
                    b"Born on November 1 1985 in Pittsburg, PA.",
                    b"{redacted}",
                    b"2024-01-10T14:44:07.625505",
                    b"6.28",
                    b"{redacted}",
                    b"False",
                    b"33",
                ],
            ],  # redacted_data
            [
                [
                    [],
                    [],
                    [],
                    [
                        ae.PySpanTag(
                            start=0,
                            end=4,
                            tag=ae.PyTag("tag.antimatter.io/pii/first_name", 1, "", "manual", (1, 0, 0)),
                        ),
                        ae.PySpanTag(
                            start=8,
                            end=16,
                            tag=ae.PyTag("tag.antimatter.io/pii/first_name", 1, "", "manual", (1, 0, 0)),
                        ),
                    ],
                    [
                        ae.PySpanTag(
                            start=0,
                            end=7,
                            tag=ae.PyTag("tag.antimatter.io/pii/id", 1, "", "manual", (1, 0, 0)),
                        )
                    ],
                    [
                        ae.PySpanTag(
                            start=0,
                            end=26,
                            tag=ae.PyTag("tag.antimatter.io/pii/date_of_birth", 1, "", "manual", (1, 0, 0)),
                        )
                    ],
                    [],
                    [],
                    [],
                    [],
                ],
                [
                    [
                        ae.PySpanTag(
                            start=26,
                            end=39,
                            tag=ae.PyTag("tag.antimatter.io/pii/email_address", 1, "", "manual", (1, 0, 0)),
                        )
                    ],
                    [],
                    [],
                    [],
                    [
                        ae.PySpanTag(
                            start=0,
                            end=7,
                            tag=ae.PyTag("tag.antimatter.io/pii/id", 1, "", "manual", (1, 0, 0)),
                        )
                    ],
                    [],
                    [],
                    [],
                    [],
                    [],
                ],
            ],  # data_span_tags
            '{"dict_list": {}, "_coltype": {"email": "string", "bytes": "bytes", "fname": "string", "bio": "string", "duration": "timedelta", "dt": "date_time", "float": "float", "age": "int", "status": "bool", "id": "int"}, "_metadtype": "dict_list"}',  # extra_info
        ),
        # Additional test cases can be added here
    ],
)
def test_data_with_tags(mock_capsule_bindings):
    capsule = Capsule(mock_capsule_bindings)
    result = capsule.data_with_tags(column_major=False, inline=False)

    # validate expected list lengths for result
    assert len(result) == 2
    assert len(result[0]) == 10
    assert len(result[1]) == 10

    # validate span tags were created
    assert len(result[0][3].span_tags) == 2
    spans = result[0][3].span_tags
    assert spans[0].__class__ == SpanTag and spans[1].__class__ == SpanTag
    assert spans[0].start == 0 and spans[0].end == 4
    assert spans[1].start == 8 and spans[1].end == 16
    assert len(result[0][4].span_tags) == 1

    # validate column tags were created
    assert len(result[0][7].column_tags) == 2
    assert result[0][7].column_tags[0].__class__ == ColumnTag
    assert result[0][7].column_tags[1].__class__ == ColumnTag

    # sanity check on unmolested bytes
    assert result[1][0].bytes == b"this is an email address: {redacted}"
    assert result[1][1].bytes == b"asdf"
    assert result[1][2].bytes == b"Bob"
    assert result[1][3].bytes == b"Born on November 1 1985 in Pittsburg, PA."
    assert result[1][4].bytes == b"{redacted}"
    assert result[1][5].bytes == b"2024-01-10T14:44:07.625505"
    assert result[1][6].bytes == b"6.28"
    assert result[1][7].bytes == b"{redacted}"
    assert result[1][8].bytes == b"False"
    assert result[1][9].bytes == b"33"

    # validate the data conversions for redacted and unredacted data
    assert result[1][0].data == "this is an email address: {redacted}"
    assert result[1][1].data == b"asdf"
    assert result[1][2].data == "Bob"
    assert result[1][3].data == "Born on November 1 1985 in Pittsburg, PA."
    assert result[1][4].data == datetime.timedelta(0)
    assert result[1][5].data == datetime.datetime.strptime(
        "2024-01-10 14:44:07.625505", "%Y-%m-%d %H:%M:%S.%f"
    )
    assert result[1][6].data == 6.28
    assert result[1][7].data == 0
    assert result[1][8].data is False
    assert result[1][9].data == 33

    v = repr(result[0][0])
    assert isinstance(v, str)


test_data = [
    # Basic non-overlapping
    (
        b"the {redacted} {redacted}",
        [
            SpanTag(name="foo", start=4, end=14, cell_path=""),
            SpanTag(name="bar", start=15, end=25, cell_path=""),
        ],
        b"the <span tags=['foo']>{redacted}</span> <span tags=['bar']>{redacted}</span>",
    ),
    # Exact overlap example 1
    (
        b"it is {redacted}",
        [
            SpanTag(name="foo", start=6, end=16, cell_path=""),
            SpanTag(name="bar", start=6, end=16, cell_path=""),
        ],
        b"it is <span tags=['foo', 'bar']>{redacted}</span>",
    ),
    # Overlap with start and end
    (
        b"Bob is {redacted} again",
        [
            SpanTag(name="name", start=0, end=3, cell_path=""),
            SpanTag(name="foo", start=0, end=17, cell_path=""),
            SpanTag(name="bar", start=7, end=17, cell_path=""),
        ],
        b"<span tags=['name', 'foo']>Bob</span> is <span tags=['bar']>{redacted}</span> again",
    ),
    # Non-overlapping tags
    (
        b"{redacted} morning, {redacted} night",
        [
            SpanTag(name="time1", start=0, end=10, cell_path=""),
            SpanTag(name="time2", start=20, end=30, cell_path=""),
        ],
        b"<span tags=['time1']>{redacted}</span> morning, <span tags=['time2']>{redacted}</span> night",
    ),
    # Exact overlap example 2
    (
        b"Welcome to the {redacted} world",
        [
            SpanTag(name="adj1", start=15, end=25, cell_path=""),
            SpanTag(name="adj2", start=15, end=25, cell_path=""),
        ],
        b"Welcome to the <span tags=['adj1', 'adj2']>{redacted}</span> world",
    ),
    # Partially overlapping tags
    (
        b"{redacted} morning and {redacted} night",
        [
            SpanTag(name="time1", start=0, end=10, cell_path=""),
            SpanTag(name="time2", start=6, end=16, cell_path=""),
            SpanTag(name="time3", start=23, end=33, cell_path=""),
        ],
        b"<span tags=['time1']>{redac<span tags=['time2']>ted}</span> morni</span>ng and <span tags=['time3']>{redacted}</span> night",
    ),
    # Nested overlaps with different starts and ends
    (
        b"Data {redacted} is {redacted} for analysis",
        [
            SpanTag(name="data", start=5, end=15, cell_path=""),
            SpanTag(name="status", start=19, end=29, cell_path=""),
            SpanTag(name="purpose", start=5, end=42, cell_path=""),
        ],
        b"Data <span tags=['data', 'purpose']>{redacted}</span> is <span tags=['status']>{redacted}</span> for analysis</span>",
    ),
    # Test case with invalid UTF-8 byte
    (
        b"Invalid \xff byte here",
        [SpanTag(name="foo", start=15, end=19, cell_path="")],
        b"Invalid \xff byte <span tags=['foo']>here</span>",
    ),
]
test_ids = [
    "Basic non-overlapping",
    "Exact overlap example 1",
    "Overlap with start and end",
    "Non-overlapping tags",
    "Exact overlap example 2",
    "Partially overlapping tags",
    "Nested overlaps with different starts and ends",
    "Test case with invalid UTF-8 byte",
]


@pytest.mark.parametrize("input_bytes, span_tags, expected_output", test_data, ids=test_ids)
def test_markup_bytes(input_bytes, span_tags, expected_output):
    assert _markup_bytes(input_bytes, span_tags) == expected_output


@pytest.mark.parametrize(
    ("col_names", "data", "expected_output"),
    (
        (["content"], [[b"hello antimatter"]], "hello antimatter"),
        (["data"], [[b"hello antimatter"]], {"data": "hello antimatter"}),
        (["data"], [[b"hello"], [b"antimatter"]], [{"data": "hello"}, {"data": "antimatter"}]),
    ),
    ids=(
        "Scalar value",
        "Dict value",
        "DictList value",
    ),
)
def test_capsule_data_no_extra_info(col_names, data, expected_output):
    # Be aware that this tests assumes only one column. To support extra columns,
    # the 'column_tags' and 'data_span_tags' will need to have their shape adjusted
    # to match
    cb = CapsuleBindings(None)
    cb.capsule_tags = []
    cb.column_names = col_names
    cb.column_tags = [[]]
    cb.redacted_data = data
    cb.data_span_tags = [[[]] for _ in data]
    cb.extra_info = ""

    cap = Capsule(cb)
    output = cap.data()

    assert output == expected_output


@pytest.mark.parametrize(
    ("data", "expected_repr", "expected_str"),
    (
        (
            AnnotatedData(
                capsule_tags=[],
                column="age",
                column_tags=[],
                data="19",
                bytes=b"19",
                span_tags=[
                    SpanTag(
                        name="tag.antimatter.io/pii/age",
                        start=0,
                        end=2,
                        cell_path="age[0]",
                        tag_type=TagType.Unary,
                    )
                ],
                row=0,
            ),
            "AnnotatedData(column='age', column_tags=[], bytes_with_tags=b\"<span tags=['tag.antimatter.io/pii/age']>19</span>\", row=0)",
            "AnnotatedData(capsule_tags=[], column='age', column_tags=[], data='19', bytes=b'19', bytes_with_tags=b\"<span tags=['tag.antimatter.io/pii/age']>19</span>\", span_tags=[SpanTag(name='tag.antimatter.io/pii/age', start=0, end=2, cell_path='age[0]', tag_type=TagType.Unary)], row=0)",
        ),
        (
            AnnotatedData(
                capsule_tags=[],
                column="name",
                column_tags=[],
                data="The name is Adam Smith smith@gmail.com",
                bytes=b"The name is Adam Smith smith@gmail.com",
                span_tags=[
                    SpanTag(
                        name="tag.antimatter.io/pii/name",
                        start=12,
                        end=22,
                        cell_path="name[0]",
                        tag_type=TagType.Unary,
                    ),
                    SpanTag(
                        name="tag.antimatter.io/pii/email_address",
                        start=23,
                        end=38,
                        cell_path="name[0]",
                        tag_type=TagType.Unary,
                    ),
                ],
                row=0,
            ),
            "AnnotatedData(column='name', column_tags=[], bytes_with_tags=b\"The name is <span tags=['tag.antimatter.io/pii/name']>Adam Smith</span> <span tags=['tag.antimatter.io/pii/email_address']>smith@gmail.com</span>\", row=0)",
            "AnnotatedData(capsule_tags=[], column='name', column_tags=[], data='The name is Adam Smith smith@gmail.com', bytes=b'The name is Adam Smith smith@gmail.com', bytes_with_tags=b\"The name is <span tags=['tag.antimatter.io/pii/name']>Adam Smith</span> <span tags=['tag.antimatter.io/pii/email_address']>smith@gmail.com</span>\", span_tags=[SpanTag(name='tag.antimatter.io/pii/name', start=12, end=22, cell_path='name[0]', tag_type=TagType.Unary), SpanTag(name='tag.antimatter.io/pii/email_address', start=23, end=38, cell_path='name[0]', tag_type=TagType.Unary)], row=0)",
        ),
        (
            AnnotatedData(
                capsule_tags=[],
                column="email",
                column_tags=[],
                data="smith@gmail.com",
                bytes=b"smith@gmail.com",
                span_tags=[
                    SpanTag(
                        name="tag.antimatter.io/pii/email_address",
                        start=0,
                        end=15,
                        cell_path="email[0]",
                        tag_type=TagType.Unary,
                    )
                ],
                row=0,
            ),
            "AnnotatedData(column='email', column_tags=[], bytes_with_tags=b\"<span tags=['tag.antimatter.io/pii/email_address']>smith@gmail.com</span>\", row=0)",
            "AnnotatedData(capsule_tags=[], column='email', column_tags=[], data='smith@gmail.com', bytes=b'smith@gmail.com', bytes_with_tags=b\"<span tags=['tag.antimatter.io/pii/email_address']>smith@gmail.com</span>\", span_tags=[SpanTag(name='tag.antimatter.io/pii/email_address', start=0, end=15, cell_path='email[0]', tag_type=TagType.Unary)], row=0)",
        ),
    ),
)
def test_rep_str(data, expected_repr, expected_str):
    assert repr(data) == expected_repr
    assert str(data) == expected_str
