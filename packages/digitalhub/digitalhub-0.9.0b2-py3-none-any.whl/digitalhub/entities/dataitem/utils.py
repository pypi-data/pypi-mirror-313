from __future__ import annotations

import shutil
import typing
from typing import Any

from digitalhub.context.api import get_context
from digitalhub.entities._base.entity._constructors.uuid import build_uuid
from digitalhub.entities._base.material.utils import build_log_path_from_source, eval_local_source
from digitalhub.entities._commons.enums import EntityKinds, EntityTypes
from digitalhub.readers._commons.enums import Extensions
from digitalhub.readers.api import get_reader_by_object
from digitalhub.utils.generic_utils import slugify_string

if typing.TYPE_CHECKING:
    from digitalhub.entities.dataitem._base.entity import Dataitem


def eval_source(
    source: str | list[str] | None = None,
    data: Any | None = None,
    kind: str | None = None,
    name: str | None = None,
    project: str | None = None,
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
    if (source is None) == (data is None):
        raise ValueError("You must provide source or data.")

    if source is not None:
        return eval_local_source(source)

    if kind == EntityKinds.DATAITEM_TABLE.value:
        ctx = get_context(project)
        pth = ctx.root / f"{slugify_string(name)}.{Extensions.PARQUET.value}"
        reader = get_reader_by_object(data)
        reader.write_parquet(data, pth)
        return str(pth)

    raise NotImplementedError


def process_kwargs(
    project: str,
    name: str,
    kind: str,
    source: str | list[str],
    data: Any | None = None,
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
    kind : str
        Kind the object.
    source : str
        Source(s).
    data : Any
        Dataframe to log. Alternative to source.
    path : str
        Destination path of the entity. If not provided, it's generated.
    **kwargs : dict
        Spec parameters.

    Returns
    -------
    dict
        Kwargs updated.
    """
    if data is not None:
        if kind == EntityKinds.DATAITEM_TABLE.value:
            reader = get_reader_by_object(data)
            kwargs["schema"] = reader.get_schema(data)
    if path is None:
        uuid = build_uuid()
        kwargs["uuid"] = uuid
        kwargs["path"] = build_log_path_from_source(project, EntityTypes.DATAITEM.value, name, uuid, source)
    else:
        kwargs["path"] = path
    return kwargs


def clean_tmp_path(pth: str) -> None:
    """
    Clean temporary path.

    Parameters
    ----------
    pth : str
        Path to clean.

    Returns
    -------
    None
    """
    shutil.rmtree(pth, ignore_errors=True)


def post_process(obj: Dataitem, data: Any) -> Dataitem:
    """
    Post process object.

    Parameters
    ----------
    obj : Dataitem
        The object.
    data : Any
        The data.

    Returns
    -------
    Dataitem
        The object.
    """
    if obj.kind == EntityKinds.DATAITEM_TABLE.value:
        reader = get_reader_by_object(data)
        obj.status.preview = reader.get_preview(data)
        obj.save(update=True)
    return obj
