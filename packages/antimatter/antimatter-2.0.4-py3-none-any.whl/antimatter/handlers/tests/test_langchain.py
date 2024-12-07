import pytest

from antimatter.handlers import LangchainHandler


class TestLangchain:
    @pytest.mark.parametrize(
        "data",
        (
            LangchainHandler.Retriever([{"a": "1", "b": "2", "c": "4"}]),
            LangchainHandler.Retriever([{}]),
            LangchainHandler.Retriever(
                [
                    {"a": "1", "b": "2", "c": "4", "d": "6"},
                    {"a": "5", "b": "3", "c": "1", "d": "8"},
                    {"a": "0", "b": "7", "c": "6", "d": "9"},
                ]
            ),
        ),
        ids=(
            "retriever data embeddings of list with one dictionary with values",
            # "retriever data embeddings of list with dictionaries having variations in keys",
            "retriever data embeddings of one list containing one empty dict",
            "retriever data embeddings of multiples dictionaries with string values",
        ),
    )
    def test_lossless_conversions(self, data):
        handler = LangchainHandler()
        cols, rows, extra = handler.to_generic(data)
        generic = handler.from_generic(cols, rows, extra)
        assert list(generic.vectors.values())[0].content == list(data.vectors.values())[0].content
