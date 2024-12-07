import os
import pytest

from antimatter.filetype.infer import infer_by_extension, infer_by_magic

fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")


class TestInferFiletype:
    has_libmagic = False

    @classmethod
    def setup_class(cls):
        """Setup method to check for libmagic availability"""
        try:
            import magic

            cls.has_libmagic = True
        except ImportError:
            cls.has_libmagic = False

    @pytest.mark.parametrize(
        ("path", "expected_filetype"),
        (
            (os.path.join(fixtures_dir, "data.json"), "json"),
            (os.path.join(fixtures_dir, "data.txt"), "txt"),
            (os.path.join(fixtures_dir, "data.csv"), "csv"),
            (os.path.join(fixtures_dir, "data.parquet"), "parquet"),
        ),
    )
    def test_infer_by_extension(self, path: str, expected_filetype: str):
        assert infer_by_extension(path) == expected_filetype

    @pytest.mark.parametrize(
        ("path", "expected_filetype"),
        (
            (os.path.join(fixtures_dir, "data.json"), "json"),
            (os.path.join(fixtures_dir, "data.txt"), "txt"),
            (os.path.join(fixtures_dir, "data.csv"), "csv"),
        ),
    )
    def test_infer_by_magic(self, path: str, expected_filetype: str):
        if not self.has_libmagic:
            pytest.skip("libmagic is not installed")

        assert infer_by_magic(path) == expected_filetype
