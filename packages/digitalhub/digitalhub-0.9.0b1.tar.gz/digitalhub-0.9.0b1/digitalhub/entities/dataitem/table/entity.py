from __future__ import annotations

import shutil
import typing
from pathlib import Path
from typing import Any

from digitalhub.entities.dataitem._base.entity import Dataitem
from digitalhub.stores.api import get_store
from digitalhub.utils.uri_utils import has_local_scheme

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities.dataitem.table.spec import DataitemSpecTable
    from digitalhub.entities.dataitem.table.status import DataitemStatusTable


class DataitemTable(Dataitem):
    """
    DataitemTable class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: DataitemSpecTable,
        status: DataitemStatusTable,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: DataitemSpecTable
        self.status: DataitemStatusTable

    def as_df(
        self,
        file_format: str | None = None,
        engine: str | None = None,
        clean_tmp_path: bool = True,
        **kwargs,
    ) -> Any:
        """
        Read dataitem file (csv or parquet) as a DataFrame from spec.path.
        If the dataitem is not local, it will be downloaded to a temporary
        folder named tmp_dir in the project context folder.
        If clean_tmp_path is True, the temporary folder will be deleted after the
        method is executed.
        It's possible to pass additional arguments to the this function. These
        keyword arguments will be passed to the DataFrame reader function such as
        pandas's read_csv or read_parquet.

        Parameters
        ----------
        file_format : str
            Format of the file. (Supported csv and parquet).
        engine : str
            Dataframe framework, by default pandas.
        clean_tmp_path : bool
            If True, the temporary folder will be deleted.
        **kwargs : dict
            Keyword arguments passed to the read_df function.

        Returns
        -------
        Any
            DataFrame.
        """
        try:
            if has_local_scheme(self.spec.path):
                tmp_dir = None
                data_path = self.spec.path
            else:
                tmp_dir = self._context().root / "tmp_data"
                tmp_dir.mkdir(parents=True, exist_ok=True)
                data_path = self.download(destination=str(tmp_dir), overwrite=True)

            if Path(data_path).is_dir():
                files = [str(i) for i in Path(data_path).rglob("*") if i.is_file()]
                checker = files[0]
            else:
                checker = data_path

            extension = self._get_extension(checker, file_format)
            return get_store("").read_df(data_path, extension, engine, **kwargs)

        except Exception as e:
            raise e

        finally:
            # Delete tmp folder
            self._clean_tmp_path(tmp_dir, clean_tmp_path)

    def write_df(
        self,
        df: Any,
        extension: str | None = None,
        **kwargs,
    ) -> str:
        """
        Write DataFrame as parquet/csv/table into dataitem spec.path.
        keyword arguments will be passed to the DataFrame reader function such as
        pandas's to_csv or to_parquet.

        Parameters
        ----------
        df : Any
            DataFrame to write.
        extension : str
            Extension of the file.
        **kwargs : dict
            Keyword arguments passed to the write_df function.

        Returns
        -------
        str
            Path to the written dataframe.
        """
        return get_store(self.spec.path).write_df(df, self.spec.path, extension=extension, **kwargs)

    @staticmethod
    def _clean_tmp_path(pth: Path | None, clean: bool) -> None:
        """
        Clean temporary path.

        Parameters
        ----------
        pth : Path | None
            Path to clean.
        clean : bool
            If True, the path will be cleaned.

        Returns
        -------
        None
        """
        if pth is not None and clean:
            shutil.rmtree(pth)
