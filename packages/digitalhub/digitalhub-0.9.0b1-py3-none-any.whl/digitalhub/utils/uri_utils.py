from __future__ import annotations

from enum import Enum
from urllib.parse import urlparse

from digitalhub.utils.generic_utils import list_enum


class S3Schemes(Enum):
    """
    S3 schemes.
    """

    S3 = "s3"
    S3A = "s3a"
    S3N = "s3n"
    ZIP_S3 = "zip+s3"


class LocalSchemes(Enum):
    """
    Local schemes.
    """

    LOCAL = ""


class InvalidLocalSchemes(Enum):
    """
    Local schemes.
    """

    FILE = "file"
    LOCAL = "local"


class RemoteSchemes(Enum):
    """
    Remote schemes.
    """

    HTTP = "http"
    HTTPS = "https"


class SqlSchemes(Enum):
    """
    Sql schemes.
    """

    SQL = "sql"
    POSTGRESQL = "postgresql"


class GitSchemes(Enum):
    """
    Git schemes.
    """

    GIT = "git"
    GIT_HTTP = "git+http"
    GIT_HTTPS = "git+https"


class SchemeCategory(Enum):
    """
    Scheme types.
    """

    S3 = "s3"
    LOCAL = "local"
    REMOTE = "remote"
    SQL = "sql"
    GIT = "git"


def map_uri_scheme(uri: str) -> str:
    """
    Map an URI scheme to a common scheme.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        Mapped scheme type.

    Raises
    ------
    ValueError
        If the scheme is unknown.
    """
    scheme = urlparse(uri).scheme
    if scheme in list_enum(LocalSchemes):
        return SchemeCategory.LOCAL.value
    if scheme in list_enum(InvalidLocalSchemes):
        raise ValueError("For local path, do not use any scheme.")
    if scheme in list_enum(RemoteSchemes):
        return SchemeCategory.REMOTE.value
    if scheme in list_enum(S3Schemes):
        return SchemeCategory.S3.value
    if scheme in list_enum(SqlSchemes):
        return SchemeCategory.SQL.value
    if scheme in list_enum(GitSchemes):
        return SchemeCategory.GIT.value
    raise ValueError(f"Unknown scheme '{scheme}'!")


def has_local_scheme(path: str) -> bool:
    """
    Check if path is local.

    Parameters
    ----------
    path : str
        Path of some source.

    Returns
    -------
    bool
        True if path is local.
    """
    return map_uri_scheme(path) == SchemeCategory.LOCAL.value


def has_remote_scheme(path: str) -> bool:
    """
    Check if path is remote.

    Parameters
    ----------
    path : str
        Path of some source.

    Returns
    -------
    bool
        True if path is remote.
    """
    return map_uri_scheme(path) == SchemeCategory.REMOTE.value


def has_s3_scheme(path: str) -> bool:
    """
    Check if path is s3.

    Parameters
    ----------
    path : str
        Path of some source.

    Returns
    -------
    bool
        True if path is s3.
    """
    return map_uri_scheme(path) == SchemeCategory.S3.value


def has_sql_scheme(path: str) -> bool:
    """
    Check if path is sql.

    Parameters
    ----------
    path : str
        Path of some source.

    Returns
    -------
    bool
        True if path is sql.
    """
    return map_uri_scheme(path) == SchemeCategory.SQL.value


def has_git_scheme(path: str) -> bool:
    """
    Check if path is git.

    Parameters
    ----------
    path : str
        Path of some source.

    Returns
    -------
    bool
        True if path is git.
    """
    return map_uri_scheme(path) == SchemeCategory.GIT.value
