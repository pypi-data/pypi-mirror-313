from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from digitalhub.readers.api import get_reader_by_object
from digitalhub.stores._base.store import Store, StoreConfig
from digitalhub.utils.exceptions import StoreError
from digitalhub.utils.file_utils import get_file_info_from_local


class LocalStoreConfig(StoreConfig):
    """
    Local store configuration class.
    """

    path: str
    """Local path."""


class LocalStore(Store):
    """
    Local store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on local filesystem based storage.
    """

    def __init__(self, name: str, store_type: str, config: LocalStoreConfig) -> None:
        super().__init__(name, store_type)
        self.config = config

    ##############################
    # I/O methods
    ##############################

    def download(
        self,
        root: str,
        dst: Path,
        src: list[str],
        overwrite: bool = False,
    ) -> str:
        """
        Download artifacts from storage.

        Parameters
        ----------
        root : str
            The root path of the artifact.
        dst : str
            The destination of the artifact on local filesystem.
        src : list[str]
            List of sources.
        overwrite : bool
            Specify if overwrite existing file(s).

        Returns
        -------
        str
            Destination path of the downloaded artifact.
        """
        raise StoreError("Local store does not support download.")

    def upload(self, src: str | list[str], dst: str | None = None) -> list[tuple[str, str]]:
        """
        Upload an artifact to storage.

        Raises
        ------
        StoreError
            This method is not implemented.
        """
        raise StoreError("Local store does not support upload.")

    def get_file_info(self, paths: list[str]) -> list[dict]:
        """
        Method to get file metadata.

        Parameters
        ----------
        paths : list
            List of source paths.

        Returns
        -------
        list[dict]
            Returns files metadata.
        """
        return [get_file_info_from_local(p) for p in paths]

    ##############################
    # Private I/O methods
    ##############################

    def _get_src_dst_files(self, src: Path, dst: Path) -> list[str]:
        """
        Copy files from source to destination.

        Parameters
        ----------
        src : Path
            The source path.
        dst : Path
            The destination path.

        Returns
        -------
        list[str]
            Returns the list of destination and source paths of the
            copied files.
        """
        return [self._get_src_dst_file(i, dst) for i in src.rglob("*") if i.is_file()]

    def _get_src_dst_file(self, src: Path, dst: Path) -> str:
        """
        Copy file from source to destination.

        Parameters
        ----------
        src : Path
            The source path.
        dst : Path
            The destination path.

        Returns
        -------
        str
        """
        dst_pth = self._copy_file(src, dst, True)
        return str(dst_pth), str(src)

    def _copy_dir(self, src: Path, dst: Path, overwrite: bool) -> list[str]:
        """
        Download file from source to destination.

        Parameters
        ----------
        src : Path
            The source path.
        dst : Path
            The destination path.

        Returns
        -------
        list[str]
        """
        dst = self._rebuild_path(dst, src)
        shutil.copytree(src, dst, dirs_exist_ok=overwrite)
        return [str(i) for i in dst.rglob("*") if i.is_file()]

    def _copy_file(self, src: Path, dst: Path, overwrite: bool) -> str:
        """
        Copy file from source to destination.

        Parameters
        ----------
        src : Path
            The source path.
        dst : Path
            The destination path.

        Returns
        -------
        str
        """
        dst = self._rebuild_path(dst, src)
        self._check_overwrite(dst, overwrite)
        return str(shutil.copy2(src, dst))

    def _rebuild_path(self, dst: Path, src: Path) -> Path:
        """
        Rebuild path.

        Parameters
        ----------
        dst : Path
            The destination path.
        src : Path
            The source path.

        Returns
        -------
        Path
            The rebuilt path.
        """
        if dst.is_dir():
            if src.is_absolute():
                raise StoreError("Source must be a relative path if the destination is a directory.")
            dst = dst / src
        self._build_path(dst)
        return dst

    ##############################
    # Datastore methods
    ##############################

    def write_df(self, df: Any, dst: str, extension: str | None = None, **kwargs) -> str:
        """
        Method to write a dataframe to a file. Kwargs are passed to df.to_parquet().
        If destination is not provided, the dataframe is written to the default
        store path with generated name.

        Parameters
        ----------
        df : Any
            The dataframe to write.
        dst : str
            The destination of the dataframe.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        str
            Path of written dataframe.
        """
        self.store._check_local_dst(dst)
        self._validate_extension(Path(dst).suffix.removeprefix("."))

        # Write dataframe
        reader = get_reader_by_object(df)
        reader.write_df(df, dst, extension=extension, **kwargs)

        return dst

    ##############################
    # Helper methods
    ##############################

    @staticmethod
    def is_partition_or_dir(path: str) -> bool:
        """
        Check if path is a directory or a partition.

        Parameters
        ----------
        path : str
            The path to check.

        Returns
        -------
        bool
        """
        return Path(path).is_dir()

    @staticmethod
    def build_object_path(root: str, paths: str | list[str]) -> list[str]:
        """
        Method to build object path.

        Parameters
        ----------
        root : str
            The root of the object path.
        paths : str | list[str]
            The path to build.

        Returns
        -------
        list[str]
            Returns the path of the object.
        """
        if isinstance(paths, str):
            paths = [paths]
        return [str(Path(root) / path) for path in paths]
