from __future__ import annotations

import typing
from pathlib import Path

from digitalhub.entities._base.material.entity import MaterialEntity
from digitalhub.entities._commons.enums import EntityTypes
from digitalhub.readers._commons.enums import Extensions
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.uri_utils import has_sql_scheme

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities.dataitem._base.spec import DataitemSpec
    from digitalhub.entities.dataitem._base.status import DataitemStatus


class Dataitem(MaterialEntity):
    """
    A class representing a dataitem.
    """

    ENTITY_TYPE = EntityTypes.DATAITEM.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: DataitemSpec,
        status: DataitemStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)
        self.spec: DataitemSpec
        self.status: DataitemStatus

    ##############################
    #  Helper methods
    ##############################

    @staticmethod
    def _get_extension(path: str, file_format: str | None = None) -> str:
        """
        Get extension of path.

        Parameters
        ----------
        path : str
            Path to get extension from.
        file_format : str
            File format.

        Returns
        -------
        str
            File extension.

        Raises
        ------
        EntityError
            If file format is not supported.
        """
        if file_format is not None:
            return file_format

        if has_sql_scheme(path):
            return Extensions.PARQUET.value

        ext = Path(path).suffix[1:]
        if ext is not None:
            return ext
        raise EntityError("Unknown file format. Only csv and parquet are supported.")
