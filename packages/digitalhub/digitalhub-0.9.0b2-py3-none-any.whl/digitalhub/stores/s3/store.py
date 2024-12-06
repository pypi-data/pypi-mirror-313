from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any, Type
from urllib.parse import urlparse

import boto3
import botocore.client  # pylint: disable=unused-import
from botocore.exceptions import ClientError

from digitalhub.readers.api import get_reader_by_object
from digitalhub.stores._base.store import Store, StoreConfig
from digitalhub.utils.exceptions import StoreError
from digitalhub.utils.file_utils import get_file_info_from_s3, get_file_mime_type

# Type aliases
S3Client = Type["botocore.client.S3"]


class S3StoreConfig(StoreConfig):
    """
    S3 store configuration class.
    """

    endpoint_url: str
    """S3 endpoint URL."""

    aws_access_key_id: str
    """AWS access key ID."""

    aws_secret_access_key: str
    """AWS secret access key."""

    bucket_name: str
    """S3 bucket name."""


class S3Store(Store):
    """
    S3 store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on S3 based storage.
    """

    def __init__(self, name: str, store_type: str, config: S3StoreConfig) -> None:
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
        client, bucket = self._check_factory()

        # Build destination directory
        if dst.suffix == "":
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)

        # Handle src and tree destination
        if self.is_partition(root):
            if not src:
                keys = self._list_objects(client, bucket, root)
                strip_root = self._get_key(root)
                trees = [k.removeprefix(strip_root) for k in keys]
            else:
                keys = self._build_key_from_root(root, src)
                trees = [s for s in src]
        else:
            keys = [self._get_key(root)]
            if not src:
                trees = [Path(self._get_key(root)).name]
            else:
                trees = [s for s in src]

        if len(keys) != len(trees):
            raise StoreError("Keys and trees must have the same length.")

        # Download files
        for elements in zip(keys, trees):
            key = elements[0]
            tree = elements[1]

            # Build destination path
            if dst.suffix == "":
                dst_pth = Path(dst, tree)
            else:
                dst_pth = dst

            # Check if destination path already exists
            self._check_overwrite(dst_pth, overwrite)

            self._build_path(dst_pth.parent)

            self._download_file(key, dst_pth, client, bucket)

        if len(trees) == 1:
            if dst.suffix == "":
                return str(Path(dst, trees[0]))
        return str(dst)

    def upload(self, src: str | list[str], dst: str | None = None) -> list[tuple[str, str]]:
        """
        Upload an artifact to storage.

        Parameters
        ----------
        src : str
            List of sources.
        dst : str
            The destination of the artifact on storage.

        Returns
        -------
        list[tuple[str, str]]
            Returns the list of destination and source paths of the uploaded artifacts.
        """
        # Destination handling

        # If no destination is provided, build key from source
        # Otherwise build key from destination
        if dst is None:
            raise StoreError(
                "Destination must be provided. If source is a list of files or a directory, destination must be a partition, e.g. 's3://bucket/partition/' otherwise a destination key, e.g. 's3://bucket/key'"
            )
        else:
            dst = self._get_key(dst)

        # Source handling
        if not isinstance(src, list):
            self._check_local_src(src)
            src_is_dir = Path(src).is_dir()
        else:
            for s in src:
                self._check_local_src(s)
            src_is_dir = False
            if len(src) == 1:
                src = src[0]

        # If source is a directory, destination must be a partition
        if (src_is_dir or isinstance(src, list)) and not dst.endswith("/"):
            raise StoreError("Destination must be a partition if the source is a directory or a list of files.")

        # Directory
        if src_is_dir:
            return self._upload_dir(src, dst)

        # List of files
        elif isinstance(src, list):
            return self._upload_file_list(src, dst)

        # Single file
        return self._upload_single_file(src, dst)

    def upload_fileobject(self, src: BytesIO, dst: str) -> str:
        """
        Upload an BytesIO to S3 based storage.

        Parameters
        ----------
        src : BytesIO
            The source object to be persisted.
        dst : str
            The destination partition for the artifact.

        Returns
        -------
        str
            S3 key of the uploaded artifact.
        """
        client, bucket = self._check_factory()
        self._upload_fileobject(src, dst, client, bucket)
        return f"s3://{bucket}/{dst}"

    def get_file_info(self, paths: list[tuple[str, str]]) -> list[dict]:
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
        client, bucket = self._check_factory()

        infos = []
        for i in paths:
            key, src_path = i

            # Rebuild key in case here arrive an s3://bucket prefix
            key = self._get_key(key)

            # Get metadata
            metadata = client.head_object(Bucket=bucket, Key=key)

            # Get file info
            info = get_file_info_from_s3(src_path, metadata)
            infos.append(info)

        return infos

    ##############################
    # Private I/O methods
    ##############################

    def _download_file(
        self,
        key: str,
        dst_pth: Path,
        client: S3Client,
        bucket: str,
    ) -> list[str]:
        """
        Download files from S3 partition.

        Parameters
        ----------
        keys : str
            The list of keys to be downloaded.
        dst_pth : str
            The destination of the files on local filesystem.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        list[str]
            The list of paths of the downloaded files.
        """
        # Download file
        client.download_file(bucket, key, dst_pth)

    def _upload_dir(self, src: str, dst: str) -> list[tuple[str, str]]:
        """
        Upload directory to storage.

        Parameters
        ----------
        src : str
            List of sources.
        dst : str
            The destination of the artifact on storage.

        Returns
        -------
        list[tuple[str, str]]
            Returns the list of destination and source paths of the uploaded artifacts.
        """
        client, bucket = self._check_factory()

        # Get list of files
        src_pth = Path(src)
        files = [i for i in src_pth.rglob("*") if i.is_file()]

        # Build keys
        keys = []
        for i in files:
            i = i.relative_to(src_pth)
            keys.append(f"{dst}{i}")

        # Upload files
        paths = []
        for f, k in zip(files, keys):
            self._upload_file(f, k, client, bucket)
            paths.append((k, str(f.relative_to(src_pth))))
        return paths

    def _upload_file_list(self, src: list[str], dst: str) -> list[tuple[str, str]]:
        """
        Upload list of files to storage.

        Parameters
        ----------
        src : list
            List of sources.
        dst : str
            The destination of the artifact on storage.

        Returns
        -------
        list[tuple[str, str]]
            Returns the list of destination and source paths of the uploaded artifacts.
        """
        client, bucket = self._check_factory()
        files = src
        keys = []
        for i in files:
            keys.append(f"{dst}{Path(i).name}")
        if len(set(keys)) != len(keys):
            raise StoreError("Keys must be unique (Select files with different names, otherwise upload a directory).")

        # Upload files
        paths = []
        for f, k in zip(files, keys):
            self._upload_file(f, k, client, bucket)
            paths.append((k, Path(f).name))
        return paths

    def _upload_single_file(self, src: str, dst: str) -> str:
        """
        Upload a single file to storage.

        Parameters
        ----------
        src : str
            List of sources.
        dst : str
            The destination of the artifact on storage.

        Returns
        -------
        str
            Returns the list of destination and source paths of the uploaded artifacts.
        """
        client, bucket = self._check_factory()

        if dst.endswith("/"):
            dst = f"{dst.removeprefix('/')}{Path(src).name}"

        # Upload file
        self._upload_file(src, dst, client, bucket)
        name = Path(self._get_key(dst)).name
        return [(dst, name)]

    @staticmethod
    def _upload_file(src: str, key: str, client: S3Client, bucket: str) -> None:
        """
        Upload a file to S3 based storage. The function checks if the
        bucket is accessible.

        Parameters
        ----------
        src : str
            The source path of the file on local filesystem.
        key : str
            The key of the file on S3 based storage.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        None
        """
        extra_args = {}
        mime_type = get_file_mime_type(src)
        if mime_type is not None:
            extra_args["ContentType"] = mime_type
        client.upload_file(Filename=src, Bucket=bucket, Key=key, ExtraArgs=extra_args)

    @staticmethod
    def _upload_fileobject(fileobj: BytesIO, key: str, client: S3Client, bucket: str) -> None:
        """
        Upload a fileobject to S3 based storage. The function checks if the bucket is accessible.

        Parameters
        ----------
        fileobj : BytesIO
            The fileobject to be uploaded.
        key : str
            The key of the file on S3 based storage.
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        None
        """
        client.put_object(Bucket=bucket, Key=key, Body=fileobj.getvalue())

    ##############################
    # Datastore methods
    ##############################

    def write_df(self, df: Any, dst: str, extension: str | None = None, **kwargs) -> str:
        """
        Write a dataframe to S3 based storage. Kwargs are passed to df.to_parquet().

        Parameters
        ----------
        df : Any
            The dataframe.
        dst : str
            The destination path on S3 based storage.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        str
            The S3 path where the dataframe was saved.
        """
        fileobj = BytesIO()
        reader = get_reader_by_object(df)
        reader.write_df(df, fileobj, extension=extension, **kwargs)

        key = self._get_key(dst)
        return self.upload_fileobject(fileobj, key)

    ##############################
    # Helper methods
    ##############################

    def _get_bucket(self) -> str:
        """
        Get the name of the S3 bucket from the URI.

        Returns
        -------
        str
            The name of the S3 bucket.
        """
        return str(self.config.bucket_name)

    def _get_client(self) -> S3Client:
        """
        Get an S3 client object.

        Returns
        -------
        S3Client
            Returns a client object that interacts with the S3 storage service.
        """
        cfg = {
            "endpoint_url": self.config.endpoint_url,
            "aws_access_key_id": self.config.aws_access_key_id,
            "aws_secret_access_key": self.config.aws_secret_access_key,
        }
        return boto3.client("s3", **cfg)

    def _check_factory(self) -> tuple[S3Client, str]:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Returns
        -------
        tuple[S3Client, str]
            A tuple containing the S3 client object and the name of the S3 bucket.
        """
        client = self._get_client()
        bucket = self._get_bucket()
        self._check_access_to_storage(client, bucket)
        return client, bucket

    def _check_access_to_storage(self, client: S3Client, bucket: str) -> None:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Parameters
        ----------
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        None

        Raises
        ------
        ClientError:
            If access to the specified bucket is not available.
        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError as e:
            raise ClientError("No access to s3 bucket!") from e

    @staticmethod
    def _get_key(path: str) -> str:
        """
        Build key.

        Parameters
        ----------
        path : str
            The source path to get the key from.

        Returns
        -------
        str
            The key.
        """
        key = urlparse(path).path.replace("\\", "/")
        if key.startswith("/"):
            key = key[1:]
        return key

    def _build_key_from_root(self, root: str, paths: list[str]) -> list[str]:
        """
        Method to build object path.

        Parameters
        ----------
        root : str
            The root of the object path.
        paths : list[str]
            The path to build.

        Returns
        -------
        list[str]
            List of keys.
        """
        keys = []
        for path in paths:
            clean_path = self._get_key(path)
            key = self._get_key(f"{root}{clean_path}")
            keys.append(key)
        return keys

    def _list_objects(self, client: S3Client, bucket: str, partition: str) -> list[str]:
        """
        List objects in a S3 partition.

        Parameters
        ----------
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.
        partition : str
            The partition.

        Returns
        -------
        list[str]
            The list of keys under the partition.
        """
        key = self._get_key(partition)
        file_list = client.list_objects_v2(Bucket=bucket, Prefix=key).get("Contents", [])
        return [f["Key"] for f in file_list]

    @staticmethod
    def is_partition(path: str) -> bool:
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
        if path.endswith("/"):
            return True
        return False
