import pathlib
import re

import regex

from antimatter.location.locations import Location

s3_reg = regex.compile(r"^s3://.*$", re.IGNORECASE)
gcs_reg = regex.compile(r"^gs://.*$", re.IGNORECASE)


def infer_location(p: str) -> Location:
    """
    Convenience handler for inferring the Location from a path. Supported
    locations include local file, S3 bucket, and GCS bucket.

    :param p: The path name, pointing to a location.
    :return: The inferred location.
    """
    p = str(p)
    loc = Location.Unknown
    if s3_reg.fullmatch(p):
        return Location.S3
    if gcs_reg.fullmatch(p):
        return Location.GCS
    try:
        v = pathlib.Path(p)
        if v:
            return Location.File
    except Exception:  # Gotta catch 'em all
        pass
    return loc
