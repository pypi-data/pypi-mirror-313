from __future__ import annotations

from typing import Any

from digitalhub.entities._base.entity._constructors.uuid import build_uuid
from digitalhub.entities._base.material.utils import build_log_path_from_source, eval_local_source
from digitalhub.entities._commons.enums import EntityTypes


def eval_source(
    source: str | list[str] | None = None,
) -> Any:
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
    return eval_local_source(source)


def process_kwargs(
    project: str,
    name: str,
    source: str | list[str],
    path: str | None = None,
    **kwargs,
) -> dict:
    """
    Process spec kwargs.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    source : str
        Source(s).
    path : str
        Destination path of the entity. If not provided, it's generated.
    **kwargs : dict
        Spec parameters.

    Returns
    -------
    dict
        Kwargs updated.
    """
    if path is None:
        uuid = build_uuid()
        kwargs["uuid"] = uuid
        kwargs["path"] = build_log_path_from_source(project, EntityTypes.MODEL.value, name, uuid, source)
    else:
        kwargs["path"] = path
    return kwargs
