from __future__ import annotations

from pathlib import Path
from typing import Any

import requests

from digitalhub.stores._base.store import Store, StoreConfig
from digitalhub.utils.exceptions import StoreError


class RemoteStoreConfig(StoreConfig):
    """
    Remote store configuration class.
    """


class RemoteStore(Store):
    """
    HTTP store class. It implements the Store interface and provides methods to fetch
    artifacts from remote HTTP based storage.
    """

    def __init__(self, name: str, store_type: str, config: RemoteStoreConfig) -> None:
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
        # Handle destination
        if dst is None:
            dst = self._build_temp()
        else:
            self._check_local_dst(str(dst))

        if dst.suffix == "":
            dst = dst / "data.file"

        self._check_overwrite(dst, overwrite)
        self._build_path(dst)

        return self._download_file(root, dst, overwrite)

    def upload(self, src: str | list[str], dst: str | None = None) -> list[tuple[str, str]]:
        """
        Upload an artifact to storage.

        Raises
        ------
        StoreError
            This method is not implemented.
        """
        raise StoreError("Remote HTTP store does not support upload.")

    def get_file_info(self, paths: list[str]) -> list[dict]:
        """
        Get file information from HTTP(s) storage.

        Parameters
        ----------
        paths : list[str]
            List of source paths.

        Returns
        -------
        list[dict]
            Returns files metadata.
        """
        return []

    ##############################
    # Datastore methods
    ##############################

    def write_df(self, df: Any, dst: str, extension: str | None = None, **kwargs) -> str:
        """
        Method to write a dataframe to a file. Note that this method is not implemented
        since the remote store is not meant to write dataframes.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("Remote store does not support write_df.")

    ##############################
    # Helper methods
    ##############################

    @staticmethod
    def _check_head(src) -> None:
        """
        Check if the source exists.

        Parameters
        ----------
        src : str
            The source location.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If an error occurs while checking the source.
        """
        r = requests.head(src, timeout=60)
        r.raise_for_status()

    def _download_file(self, url: str, dst: Path, overwrite: bool) -> str:
        """
        Method to download a file from a given url.

        Parameters
        ----------
        url : str
            The url of the file to download.
        dst : Path
            The destination of the file.
        overwrite : bool
            Whether to overwrite existing files.

        Returns
        -------
        str
            The path of the downloaded file.
        """
        self._check_head(url)
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return str(dst)
