from __future__ import annotations

from pydantic import BaseModel

from digitalhub.client.dhcore.env import FALLBACK_USER


class AuthConfig(BaseModel):
    """Client configuration model."""

    user: str = FALLBACK_USER
    """Username."""


class BasicAuth(AuthConfig):
    """Basic authentication model."""

    password: str
    """Basic authentication password."""


class ClientParams(AuthConfig):
    """Client id authentication model."""

    client_id: str = None
    """OAuth2 client id."""

    client_scecret: str = None
    """OAuth2 client secret."""


class OAuth2TokenAuth(ClientParams):
    """OAuth2 token authentication model."""

    access_token: str
    """OAuth2 token."""

    refresh_token: str = None
    """OAuth2 refresh token."""


class TokenExchangeAuth(ClientParams):
    """Token exchange authentication model."""

    exchange_token: str
    """Exchange token."""
