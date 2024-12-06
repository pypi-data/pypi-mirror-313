from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

from boto3 import client as boto3_client


def get_bucket_and_key(path: str) -> tuple[str, str]:
    """
    Get bucket and key from path.

    Parameters
    ----------
    path : str
        The source path to get the key from.

    Returns
    -------
    tuple[str, str]
        The bucket and key.
    """
    parsed = urlparse(path)
    return parsed.netloc, parsed.path


def get_s3_source(bucket: str, key: str, filename: Path) -> None:
    """
    Get S3 source.

    Parameters
    ----------
    bucket : str
        S3 bucket name.
    key : str
        S3 object key.
    filename : Path
        Path where to save the function source.

    Returns
    -------
    None
    """
    s3 = boto3_client("s3", endpoint_url=os.getenv("S3_ENDPOINT_URL"))
    s3.download_file(bucket, key, filename)


def get_s3_bucket() -> str | None:
    """
    Function to get S3 bucket name.

    Returns
    -------
    str
        The S3 bucket name.
    """
    return os.getenv("S3_BUCKET_NAME", "datalake")
