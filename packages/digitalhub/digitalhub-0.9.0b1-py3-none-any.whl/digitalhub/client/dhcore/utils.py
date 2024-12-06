from __future__ import annotations

import os
import typing

from digitalhub.client.api import get_client
from digitalhub.client.dhcore.enums import AuthType, DhcoreEnvVar

if typing.TYPE_CHECKING:
    from digitalhub.client.dhcore.client import ClientDHCore


def set_dhcore_env(
    endpoint: str | None = None,
    user: str | None = None,
    password: str | None = None,
    access_token: str | None = None,
    refresh_token: str | None = None,
    client_id: str | None = None,
) -> None:
    """
    Function to set environment variables for DHCore config.
    Note that if the environment variable is already set, it
    will be overwritten. It also ovverides the remote client
    configuration.

    Parameters
    ----------
    endpoint : str
        The endpoint of DHCore.
    user : str
        The user of DHCore.
    password : str
        The password of DHCore.
    access_token : str
        The access token of DHCore.
    refresh_token : str
        The refresh token of DHCore.
    client_id : str
        The client id of DHCore.

    Returns
    -------
    None
    """
    if endpoint is not None:
        os.environ[DhcoreEnvVar.ENDPOINT.value] = endpoint
    if user is not None:
        os.environ[DhcoreEnvVar.USER.value] = user
    if password is not None:
        os.environ[DhcoreEnvVar.PASSWORD.value] = password
    if access_token is not None:
        os.environ[DhcoreEnvVar.ACCESS_TOKEN.value] = access_token
    if refresh_token is not None:
        os.environ[DhcoreEnvVar.REFRESH_TOKEN.value] = refresh_token
    if client_id is not None:
        os.environ[DhcoreEnvVar.CLIENT_ID.value] = client_id

    update_client_from_env()


def update_client_from_env() -> None:
    """
    Function to update client from environment variables.

    Returns
    -------
    None
    """
    client: ClientDHCore = get_client(local=False)

    # Update endpoint
    endpoint = os.getenv(DhcoreEnvVar.ENDPOINT.value)
    if endpoint is not None:
        client._endpoint_core = endpoint

    # Update auth

    # If token is set, it will override the other auth options
    access_token = os.getenv(DhcoreEnvVar.ACCESS_TOKEN.value)
    refresh_token = os.getenv(DhcoreEnvVar.REFRESH_TOKEN.value)
    client_id = os.getenv(DhcoreEnvVar.CLIENT_ID.value)

    if access_token is not None:
        if refresh_token is not None:
            client._refresh_token = refresh_token
        if client_id is not None:
            client._client_id = client_id
        client._access_token = access_token
        client._auth_type = AuthType.OAUTH2.value
        return

    # Otherwise, if user and password are set, basic auth will be used
    username = os.getenv(DhcoreEnvVar.USER.value)
    password = os.getenv(DhcoreEnvVar.PASSWORD.value)
    if username is not None and password is not None:
        client._user = username
        client._password = password
        client._auth_type = AuthType.BASIC.value


def refresh_token() -> None:
    """
    Function to refresh token.

    Returns
    -------
    None
    """
    client: ClientDHCore = get_client(local=False)
    client._get_new_access_token()
