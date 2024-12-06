from __future__ import annotations

import typing

from digitalhub.client.builder import client_builder

if typing.TYPE_CHECKING:
    from digitalhub.client._base.client import Client


def get_client(local: bool = False, config: dict | None = None) -> Client:
    """
    Wrapper around ClientBuilder.build.

    Parameters
    ----------
    local : bool
        Whether to create a local client or not.
    config : dict
        DHCore environment configuration.

    Returns
    -------
    Client
        The client instance.
    """
    return client_builder.build(local, config)
