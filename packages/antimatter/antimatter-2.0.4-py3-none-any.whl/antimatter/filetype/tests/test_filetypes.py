import os
import pandas as pd
import pytest
from antimatter.filetype.extract import (
    extract_from_file,
    extract_from_csv,
    extract_from_json,
    extract_from_ndjson,
    extract_from_parquet,
    extract_from_txt,
)
from antimatter import errors

fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")


class TestExtractFromFile:
    def test_invalid_hint(self):
        with pytest.raises(errors.DataFormatError):
            extract_from_file(os.path.join(fixtures_dir, "data.txt"), "invalid")

    def test_extract_from_csv(self):
        data = extract_from_csv(os.path.join(fixtures_dir, "data.csv"))
        assert len(data) == 3
        assert isinstance(data, list)
        assert all(isinstance(row, dict) for row in data)

    def test_extract_from_json(self):
        data = extract_from_json(os.path.join(fixtures_dir, "data.json"))
        assert isinstance(data, list)
        assert len(data) == 3

    def test_extract_from_ndjson(self):
        data = extract_from_ndjson(os.path.join(fixtures_dir, "data-ndjson.json"))
        assert isinstance(data, list)
        assert len(data) == 3

    def test_extract_from_parquet(self):
        data = extract_from_parquet(os.path.join(fixtures_dir, "data.parquet"))
        assert isinstance(data, pd.DataFrame)
        assert data.shape == (3, 3)

    def test_extract_from_txt(self):
        data = extract_from_txt(os.path.join(fixtures_dir, "data.txt"))
        assert isinstance(data, str)
        assert len(data) == 179
