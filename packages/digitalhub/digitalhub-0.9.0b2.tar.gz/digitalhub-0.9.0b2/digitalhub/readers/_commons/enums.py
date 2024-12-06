from __future__ import annotations

from enum import Enum


class Extensions(Enum):
    """
    Supported file extensions.
    """

    CSV = "csv"
    PARQUET = "parquet"
    FILE = "file"
