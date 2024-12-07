import pytest

from antimatter.location.infer import infer_location
from antimatter.location.locations import Location


class TestInferLocation:
    @pytest.mark.parametrize(
        ("path", "expected_location"),
        (
            ("/Users/bob/Capsules/capsule", Location.File),
            ("s3://mybucket/capsule", Location.S3),
            ("S3://mybucket/capsule", Location.S3),
            ("gs://mybucket/capsule", Location.GCS),
            ("GS://mybucket/capsule", Location.GCS),
        ),
    )
    def test_infer_location(self, path: str, expected_location: Location):
        loc = infer_location(path)
        assert loc is expected_location
