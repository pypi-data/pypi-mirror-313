from __future__ import annotations

from pathlib import Path

from digitalhub.utils.file_utils import eval_zip_type
from digitalhub.utils.s3_utils import get_s3_bucket
from digitalhub.utils.uri_utils import S3Schemes, has_local_scheme


def eval_local_source(source: str | list[str]) -> None:
    """
    Evaluate if source is local.

    Parameters
    ----------
    source : str | list[str]
        Source(s).

    Returns
    -------
    None
    """
    if isinstance(source, list):
        if not source:
            raise ValueError("Empty list of sources.")
        source_is_local = all(has_local_scheme(s) for s in source)
        for s in source:
            if Path(s).is_dir():
                raise ValueError(f"Invalid source path: {s}. List of paths must be list of files, not directories.")
    else:
        source_is_local = has_local_scheme(source)

    if not source_is_local:
        raise ValueError("Invalid source path. Source must be a local path.")


def eval_zip_sources(source: str | list[str]) -> str:
    """
    Evaluate zip sources.

    Parameters
    ----------
    source : str | list[str]
        Source(s).

    Returns
    -------
    str
        S3Schemes.
    """
    if isinstance(source, list):
        if len(source) > 1:
            return S3Schemes.S3.value
        path = source[0]
    else:
        if Path(source).is_dir():
            return S3Schemes.S3.value
        path = source

    if not eval_zip_type(path):
        return S3Schemes.S3.value
    return S3Schemes.ZIP_S3.value


def build_log_path_from_source(
    project: str,
    entity_type: str,
    name: str,
    uuid: str,
    source: str | list[str],
) -> str:
    """
    Build log path.

    Parameters
    ----------
    project : str
        Project name.
    entity_type : str
        Entity type.
    name : str
        Object name.
    uuid : str
        Object UUID.
    source : str | list[str]
        Source(s).

    Returns
    -------
    str
        Log path.
    """
    scheme = eval_zip_sources(source)
    path = f"{scheme}://{get_s3_bucket()}/{project}/{entity_type}/{name}/{uuid}"

    if isinstance(source, list) and len(source) >= 1:
        if len(source) > 1:
            path += "/"
        else:
            path += f"/{Path(source[0]).name}"
    elif Path(source).is_dir():
        path += "/"
    elif Path(source).is_file():
        path += f"/{Path(source).name}"

    return path
