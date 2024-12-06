from __future__ import annotations

import os
import typing

from pydantic import ValidationError

from digitalhub.stores._base.store import StoreParameters
from digitalhub.stores.local.store import LocalStore, LocalStoreConfig
from digitalhub.stores.remote.store import RemoteStore, RemoteStoreConfig
from digitalhub.stores.s3.store import S3Store, S3StoreConfig
from digitalhub.stores.sql.store import SqlStore, SQLStoreConfig
from digitalhub.utils.exceptions import StoreError
from digitalhub.utils.uri_utils import SchemeCategory, map_uri_scheme

if typing.TYPE_CHECKING:
    from digitalhub.stores._base.store import Store


REGISTRY_STORES = {
    "local": LocalStore,
    "s3": S3Store,
    "remote": RemoteStore,
    "sql": SqlStore,
}


class StoreBuilder:
    """
    Store builder class.
    """

    def __init__(self) -> None:
        self._instances: dict[str, Store] = {}
        self._default: Store | None = None
        self._def_scheme = "s3"

    def build(self, store_cfg: StoreParameters) -> None:
        """
        Build a store instance and register it.
        It overrides any existing instance.

        Parameters
        ----------
        store_cfg : StoreParameters
            Store configuration.

        Returns
        -------
        None
        """
        scheme = map_uri_scheme(store_cfg.type)
        self._instances[scheme] = self.build_store(store_cfg)

    def get(self, uri: str) -> Store:
        """
        Get a store instance by URI.

        Parameters
        ----------
        uri : str
            URI to parse.

        Returns
        -------
        Store
            The store instance.
        """
        scheme = map_uri_scheme(uri)
        if scheme not in self._instances:
            store_cfg = get_env_store_config(scheme)
            self._instances[scheme] = self.build_store(store_cfg)
        return self._instances[scheme]

    def default(self) -> Store:
        """
        Get the default store instance.

        Returns
        -------
        Store
            The default store instance.

        Raises
        ------
        StoreError
            If no default store is set.
        """
        if self._default is None:
            store_cfg = get_env_store_config(self._def_scheme)
            self._default = self.build_store(store_cfg)
        return self._default

    def build_store(self, cfg: StoreParameters) -> Store:
        """
        Build a store instance.

        Parameters
        ----------
        cfg : StoreParameters
            Store configuration.

        Returns
        -------
        Store
            The store instance.

        Raises
        ------
        NotImplementedError
            If the store type is not implemented.
        """
        try:
            obj = REGISTRY_STORES[cfg.type](cfg.name, cfg.type, cfg.config)
            if cfg.is_default and self._default is not None:
                raise StoreError("Only one default store!")
            return obj
        except KeyError as e:
            raise NotImplementedError from e

    @staticmethod
    def _check_config(config: StoreParameters | dict) -> StoreParameters:
        """
        Check the store configuration validity.

        Parameters
        ----------
        config : StoreParameters | dict
            The store configuration.

        Returns
        -------
        StoreParameters
            The store configuration.

        Raises
        ------
        TypeError
            If the config parameter is not a StoreParameters instance or a well-formed dictionary.
        """
        if not isinstance(config, StoreParameters):
            try:
                return StoreParameters(**config)
            except TypeError as e:
                raise StoreError("Invalid store configuration type.") from e
            except ValidationError as e:
                raise StoreError("Malformed store configuration parameters.") from e
        return config


def get_env_store_config(scheme: str) -> StoreParameters:
    """
    Get a store configuration from the environment.

    Parameters
    ----------
    scheme : str
        URI scheme.

    Returns
    -------
    StoreParameters
        The store configuration based on the scheme.

    Raises
    ------
    ValueError
        If the scheme is not supported.
    """
    if scheme == SchemeCategory.S3.value:
        return StoreParameters(
            name="s3",
            type="s3",
            config=S3StoreConfig(
                endpoint_url=os.getenv("S3_ENDPOINT_URL"),  # type: ignore
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),  # type: ignore
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),  # type: ignore
                bucket_name=os.getenv("S3_BUCKET_NAME"),  # type: ignore
            ),
        )
    if scheme == SchemeCategory.SQL.value:
        return StoreParameters(
            name="sql",
            type="sql",
            config=SQLStoreConfig(
                host=os.getenv("POSTGRES_HOST"),  # type: ignore
                port=os.getenv("POSTGRES_PORT"),  # type: ignore
                user=os.getenv("POSTGRES_USER"),  # type: ignore
                password=os.getenv("POSTGRES_PASSWORD"),  # type: ignore
                database=os.getenv("POSTGRES_DATABASE"),  # type: ignore
                pg_schema=os.getenv("POSTGRES_SCHEMA"),  # type: ignore
            ),
        )
    if scheme == SchemeCategory.REMOTE.value:
        return StoreParameters(
            name="remote",
            type="remote",
            config=RemoteStoreConfig(),
        )
    if scheme == SchemeCategory.LOCAL.value:
        return StoreParameters(
            name="local",
            type="local",
            config=LocalStoreConfig(
                path="tempsdk",
            ),
        )
    raise ValueError(f"Unsupported scheme {scheme}")


store_builder = StoreBuilder()
