from __future__ import annotations

import base64
import importlib.util as imputil
import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable
from zipfile import ZipFile

import numpy as np
import requests
from slugify import slugify

from digitalhub.utils.io_utils import read_text


def get_timestamp() -> str:
    """
    Get the current timestamp timezoned.

    Returns
    -------
    str
        The current timestamp.
    """
    return datetime.now().astimezone().isoformat()


def decode_base64_string(string: str) -> str:
    """
    Decode a string from base64.

    Parameters
    ----------
    string : str
        The string to decode.

    Returns
    -------
    str
        The string decoded from base64.
    """
    return base64.b64decode(string).decode()


def encode_string(string: str) -> str:
    """
    Encode a string in base64.

    Parameters
    ----------
    string : str
        The string to encode.

    Returns
    -------
    str
        The string encoded in base64.
    """
    return base64.b64encode(string.encode()).decode()


def encode_source(path: str) -> str:
    """
    Read a file and encode in base64 the content.

    Parameters
    ----------
    path : str
        The file path to read.

    Returns
    -------
    str
        The file content encoded in base64.
    """
    return encode_string(read_text(path))


def requests_chunk_download(source: str, filename: Path) -> None:
    """
    Download a file in chunks.

    Parameters
    ----------
    source : str
        URL to download the file.
    filename : Path
        Path where to save the file.

    Returns
    -------
    None
    """
    with requests.get(source, stream=True) as r:
        r.raise_for_status()
        with filename.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def extract_archive(path: Path, filename: Path) -> None:
    """
    Extract a zip archive.

    Parameters
    ----------
    path : Path
        Path where to extract the archive.
    filename : Path
        Path to the archive.

    Returns
    -------
    None
    """
    with ZipFile(filename, "r") as zip_file:
        zip_file.extractall(path)


class MyEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle numpy types.
    """

    def default(self, obj: Any) -> Any:
        """
        Convert numpy types to json.

        Parameters
        ----------
        obj : Any
            The object to convert.

        Returns
        -------
        Any
            The object converted to json.
        """
        if isinstance(obj, (int, str, float, list, dict)):
            return obj
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return str(obj)


def dict_to_json(struct: dict) -> str:
    """
    Convert a dict to json.

    Parameters
    ----------
    struct : dict
        The dict to convert.

    Returns
    -------
    str
        The json string.
    """
    return json.dumps(struct, cls=MyEncoder)


def slugify_string(filename: str) -> str:
    """
    Sanitize a filename.

    Parameters
    ----------
    filename : str
        The filename to sanitize.

    Returns
    -------
    str
        The sanitized filename.
    """
    return slugify(filename, max_length=255)


def import_function(path: Path, handler: str) -> Callable:
    """
    Import a function from a module.

    Parameters
    ----------
    path : Path
        Path where the function source is located.
    handler : str
        Function name.

    Returns
    -------
    Callable
        Function.
    """
    spec = imputil.spec_from_file_location(path.stem, path)
    mod = imputil.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, handler)


def list_enum(enum: Enum) -> list:
    """
    Get all values of an enum.

    Parameters
    ----------
    enum : Enum
        Enum to get values from.

    Returns
    -------
    list
        List of enum values.
    """
    return [e.value for e in enum]
