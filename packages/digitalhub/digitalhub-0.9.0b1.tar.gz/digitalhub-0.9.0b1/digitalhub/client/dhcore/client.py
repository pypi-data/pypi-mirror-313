from __future__ import annotations

import datetime
import json
import os
import typing
from warnings import warn

from dotenv import get_key, set_key
from requests import request
from requests.exceptions import HTTPError, JSONDecodeError, RequestException

from digitalhub.client._base.client import Client
from digitalhub.client.dhcore.api_builder import ClientDHCoreApiBuilder
from digitalhub.client.dhcore.enums import AuthType, DhcoreEnvVar
from digitalhub.client.dhcore.env import ENV_FILE, FALLBACK_USER, LIB_VERSION, MAX_API_LEVEL, MIN_API_LEVEL
from digitalhub.client.dhcore.models import BasicAuth, OAuth2TokenAuth
from digitalhub.utils.exceptions import (
    BackendError,
    BadRequestError,
    EntityAlreadyExistsError,
    EntityNotExistsError,
    ForbiddenError,
    MissingSpecError,
    UnauthorizedError,
)
from digitalhub.utils.uri_utils import has_remote_scheme

if typing.TYPE_CHECKING:
    from requests import Response


class ClientDHCore(Client):
    """
    DHCore client.

    The DHCore client is used to communicate with the Digitalhub Core
    backendAPI via REST. The client supports basic authentication and
    OAuth2 token authentication with token refresh.
    At creation, the client tries to get the endpoint and authentication
    parameters from the .dhcore file and the environment variables. In
    case the user incours into an authentication/endpoint error during
    the client creation, the user has the possibility to update the
    correct parameters using the `set_dhcore_env` function. If the DHCore
    client is already initialized, this function will override the
    configuration, otherwise it simply set the environment variables.
    """

    def __init__(self, config: dict | None = None) -> None:
        super().__init__()

        # API builder
        self._api_builder = ClientDHCoreApiBuilder()

        # Endpoints
        self._endpoint_core: str | None = None
        self._endpoint_issuer: str | None = None

        # Authentication
        self._auth_type: str | None = None

        # Basic
        self._user: str | None = None
        self._password: str | None = None

        # OAuth2
        self._access_token: str | None = None
        self._refresh_token: str | None = None

        self._configure(config)

    ##############################
    # CRUD methods
    ##############################

    def create_object(self, api: str, obj: dict, **kwargs) -> dict:
        """
        Create an object in DHCore.

        Parameters
        ----------
        api : str
            Create API.
        obj : dict
            Object to create.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Content-Type"] = "application/json"
        kwargs["data"] = json.dumps(obj, default=ClientDHCore._json_serialize)
        return self._prepare_call("POST", api, **kwargs)

    def read_object(self, api: str, **kwargs) -> dict:
        """
        Get an object from DHCore.

        Parameters
        ----------
        api : str
            Read API.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        return self._prepare_call("GET", api, **kwargs)

    def update_object(self, api: str, obj: dict, **kwargs) -> dict:
        """
        Update an object in DHCore.

        Parameters
        ----------
        api : str
            Update API.
        obj : dict
            Object to update.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Content-Type"] = "application/json"
        kwargs["data"] = json.dumps(obj, default=ClientDHCore._json_serialize)
        return self._prepare_call("PUT", api, **kwargs)

    def delete_object(self, api: str, **kwargs) -> dict:
        """
        Delete an object from DHCore.

        Parameters
        ----------
        api : str
            Delete API.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        resp = self._prepare_call("DELETE", api, **kwargs)
        if isinstance(resp, bool):
            resp = {"deleted": resp}
        return resp

    def list_objects(self, api: str, **kwargs) -> list[dict]:
        """
        List objects from DHCore.

        Parameters
        ----------
        api : str
            List API.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        list[dict]
            Response objects.
        """
        if kwargs is None:
            kwargs = {}

        if "params" not in kwargs:
            kwargs["params"] = {}

        start_page = 0
        if "page" not in kwargs["params"]:
            kwargs["params"]["page"] = start_page

        objects = []
        while True:
            resp = self._prepare_call("GET", api, **kwargs)
            contents = resp["content"]
            total_pages = resp["totalPages"]
            if not contents or kwargs["params"]["page"] >= total_pages:
                break
            objects.extend(contents)
            kwargs["params"]["page"] += 1

        return objects

    def list_first_object(self, api: str, **kwargs) -> dict:
        """
        List first objects.

        Parameters
        ----------
        api : str
            The api to list the objects with.
        **kwargs : dict
            Keyword arguments passed to the request.

        Returns
        -------
        dict
            The list of objects.
        """
        try:
            return self.list_objects(api, **kwargs)[0]
        except IndexError:
            raise BackendError("No object found.")

    def search_objects(self, api: str, **kwargs) -> list[dict]:
        """
        Search objects from DHCore.

        Parameters
        ----------
        api : str
            Search API.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        list[dict]
            Response objects.
        """
        if kwargs is None:
            kwargs = {}

        if "params" not in kwargs:
            kwargs["params"] = {}

        start_page = 0
        if "page" not in kwargs["params"]:
            kwargs["params"]["page"] = start_page

        if "size" not in kwargs["params"]:
            kwargs["params"]["size"] = 10

        # Add sorting
        if "sort" not in kwargs["params"]:
            kwargs["params"]["sort"] = "metadata.updated,DESC"

        objects_with_highlights = []
        while True:
            resp = self._prepare_call("GET", api, **kwargs)
            contents = resp["content"]
            total_pages = resp["totalPages"]
            if not contents or kwargs["params"]["page"] >= total_pages:
                break
            objects_with_highlights.extend(contents)
            kwargs["params"]["page"] += 1

        objects = []
        for obj in objects_with_highlights:
            obj.pop("highlights", None)
            objects.append(obj)

        return objects

    ##############################
    # Call methods
    ##############################

    @staticmethod
    def _json_serialize(obj: dict) -> dict:
        """
        JSON datetime to ISO format serializer.

        Parameters
        ----------
        obj : dict
            The object to serialize.

        Returns
        -------
        dict
            The serialized object.
        """
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    def _prepare_call(self, call_type: str, api: str, **kwargs) -> dict:
        """
        Prepare a call to the DHCore API.

        Parameters
        ----------
        call_type : str
            The type of call to prepare.
        api : str
            The api to call.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        if kwargs is None:
            kwargs = {}
        url = self._endpoint_core + api
        kwargs = self._set_auth(kwargs)
        return self._make_call(call_type, url, **kwargs)

    def _set_auth(self, kwargs: dict) -> dict:
        """
        Set the authentication type.

        Parameters
        ----------
        kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Keyword arguments with the authentication parameters.
        """
        if self._auth_type == AuthType.BASIC.value:
            kwargs["auth"] = self._user, self._password
        elif self._auth_type == AuthType.OAUTH2.value:
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            kwargs["headers"]["Authorization"] = f"Bearer {self._access_token}"
        return kwargs

    def _make_call(self, call_type: str, url: str, refresh_token: bool = True, **kwargs) -> dict:
        """
        Make a call to the DHCore API.

        Parameters
        ----------
        call_type : str
            The type of call to make.
        url : str
            The URL to call.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Response object.
        """
        # Call the API
        response = request(call_type, url, timeout=60, **kwargs)

        # Evaluate DHCore API version
        self._check_core_version(response)

        # Handle token refresh
        if response.status_code in [401] and refresh_token:
            self._get_new_access_token()
            kwargs = self._set_auth(kwargs)
            return self._make_call(call_type, url, refresh_token=False, **kwargs)

        self._raise_for_error(response)
        return self._parse_response(response)

    def _check_core_version(self, response: Response) -> None:
        """
        Raise an exception if DHCore API version is not supported.

        Parameters
        ----------
        response : Response
            The response object.

        Returns
        -------
        None
        """
        if "X-Api-Level" in response.headers:
            core_api_level = int(response.headers["X-Api-Level"])
            if not (MIN_API_LEVEL <= core_api_level <= MAX_API_LEVEL):
                raise BackendError("Backend API level not supported.")
            if LIB_VERSION < core_api_level:
                warn("Backend API level is higher than library version. You should consider updating the library.")

    def _raise_for_error(self, response: Response) -> None:
        """
        Handle DHCore API errors.

        Parameters
        ----------
        response : Response
            The response object.

        Returns
        -------
        None
        """
        try:
            response.raise_for_status()

        # Backend errors
        except RequestException as e:
            # Handle timeout
            if isinstance(e, TimeoutError):
                msg = "Request to DHCore backend timed out."
                raise TimeoutError(msg)

            # Handle connection error
            elif isinstance(e, ConnectionError):
                msg = "Unable to connect to DHCore backend."
                raise ConnectionError(msg)

            # Handle HTTP errors
            elif isinstance(e, HTTPError):
                txt_resp = f"Response: {response.text}."

                # Bad request
                if response.status_code == 400:
                    # Missing spec in backend
                    if "missing spec" in response.text:
                        msg = f"Missing spec in backend. {txt_resp}"
                        raise MissingSpecError(msg)

                    # Duplicated entity
                    elif "Duplicated entity" in response.text:
                        msg = f"Entity already exists. {txt_resp}"
                        raise EntityAlreadyExistsError(msg)

                    # Other errors
                    else:
                        msg = f"Bad request. {txt_resp}"
                        raise BadRequestError(msg)

                # Unauthorized errors
                elif response.status_code == 401:
                    msg = f"Unauthorized. {txt_resp}"
                    raise UnauthorizedError(msg)

                # Forbidden errors
                elif response.status_code == 403:
                    msg = f"Forbidden. {txt_resp}"
                    raise ForbiddenError(msg)

                # Entity not found
                elif response.status_code == 404:
                    # Put with entity not found
                    if "No such EntityName" in response.text:
                        msg = f"Entity does not exists. {txt_resp}"
                        raise EntityNotExistsError(msg)

                    # Other cases
                    else:
                        msg = f"Not found. {txt_resp}"
                        raise BackendError(msg)

                # Other errors
                else:
                    msg = f"Backend error. {txt_resp}"
                    raise BackendError(msg) from e

            # Other requests errors
            else:
                msg = f"Some error occurred. {e}"
                raise BackendError(msg) from e

        # Other generic errors
        except Exception as e:
            msg = f"Some error occurred: {e}"
            raise RuntimeError(msg) from e

    def _parse_response(self, response: Response) -> dict:
        """
        Parse the response object.

        Parameters
        ----------
        response : Response
            The response object.

        Returns
        -------
        dict
            The parsed response object.
        """
        try:
            return response.json()
        except JSONDecodeError:
            if response.text == "":
                return {}
            raise BackendError("Backend response could not be parsed.")

    ##############################
    # Configuration methods
    ##############################

    def _configure(self, config: dict | None = None) -> None:
        """
        Configure the client attributes with config (given or from
        environment).
        Regarding authentication parameters, the config parameter
        takes precedence over the env variables, and the token
        over the basic auth. Furthermore, the config parameter is
        validated against the proper pydantic model.

        Parameters
        ----------
        config : dict
            Configuration dictionary.

        Returns
        -------
        None
        """
        self._get_endpoints_from_env()

        if config is not None:
            if config.get("access_token") is not None:
                config = OAuth2TokenAuth(**config)
                self._user = config.user
                self._access_token = config.access_token
                self._refresh_token = config.refresh_token
                self._client_id = config.client_id
                self._auth_type = AuthType.OAUTH2.value

            elif config.get("user") is not None and config.get("password") is not None:
                config = BasicAuth(**config)
                self._user = config.user
                self._password = config.password
                self._auth_type = AuthType.BASIC.value

            return

        self._get_auth_from_env()

        # Propagate access and refresh token to env file
        self._write_env()

    def _get_endpoints_from_env(self) -> None:
        """
        Get the DHCore endpoint and token issuer endpoint from env.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the endpoint of DHCore is not set in the env variables.
        """
        core_endpt = os.getenv(DhcoreEnvVar.ENDPOINT.value)
        if core_endpt is None:
            raise BackendError("Endpoint not set as environment variables.")
        self._endpoint_core = self._sanitize_endpoint(core_endpt)

        issr_endpt = os.getenv(DhcoreEnvVar.ISSUER.value)
        if issr_endpt is not None:
            self._endpoint_issuer = self._sanitize_endpoint(issr_endpt)

    def _sanitize_endpoint(self, endpoint: str) -> str:
        """
        Sanitize the endpoint.

        Returns
        -------
        None
        """
        if not has_remote_scheme(endpoint):
            raise BackendError("Invalid endpoint scheme. Must start with http:// or https://.")

        endpoint = endpoint.strip()
        return endpoint.removesuffix("/")

    def _get_auth_from_env(self) -> None:
        """
        Get authentication parameters from the env.

        Returns
        -------
        None
        """
        self._user = os.getenv(DhcoreEnvVar.USER.value, FALLBACK_USER)
        self._refresh_token = os.getenv(DhcoreEnvVar.REFRESH_TOKEN.value)
        self._client_id = os.getenv(DhcoreEnvVar.CLIENT_ID.value)

        token = os.getenv(DhcoreEnvVar.ACCESS_TOKEN.value)
        if token is not None and token != "":
            self._auth_type = AuthType.OAUTH2.value
            self._access_token = token
            return

        password = os.getenv(DhcoreEnvVar.PASSWORD.value)
        if self._user is not None and password is not None:
            self._auth_type = AuthType.BASIC.value
            self._password = password
            return

    def _get_new_access_token(self) -> None:
        """
        Get a new access token.

        Returns
        -------
        None
        """
        # Call issuer and get endpoint for
        # refreshing access token
        url = self._get_refresh_endpoint()

        # Call refresh token endpoint
        # Try token from env
        refresh_token = os.getenv(DhcoreEnvVar.REFRESH_TOKEN.value)
        response = self._call_refresh_token_endpoint(url, refresh_token)

        # Otherwise try token from file
        if response.status_code in (400, 401, 403):
            refresh_token = get_key(ENV_FILE, DhcoreEnvVar.REFRESH_TOKEN.value)
            response = self._call_refresh_token_endpoint(url, refresh_token)

        response.raise_for_status()
        dict_response = response.json()

        # Read new access token and refresh token
        self._access_token = dict_response["access_token"]
        self._refresh_token = dict_response["refresh_token"]

        # Propagate new access token to env
        self._write_env()

    def _get_refresh_endpoint(self) -> str:
        """
        Get the refresh endpoint.

        Returns
        -------
        str
            Refresh endpoint.
        """
        # Get issuer endpoint
        if self._endpoint_issuer is None:
            raise BackendError("Issuer endpoint not set.")

        # Standard issuer endpoint path
        url = self._endpoint_issuer + "/.well-known/openid-configuration"

        # Call
        r = request("GET", url, timeout=60)
        self._raise_for_error(r)
        return r.json().get("token_endpoint")

    def _call_refresh_token_endpoint(self, url: str, refresh_token: str) -> Response:
        """
        Call the refresh token endpoint.

        Parameters
        ----------
        url : str
            Refresh token endpoint.
        refresh_token : str
            Refresh token.

        Returns
        -------
        Response
            Response object.
        """
        # Send request to get new access token
        payload = {
            "grant_type": "refresh_token",
            "client_id": self._client_id,
            "refresh_token": refresh_token,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return request("POST", url, data=payload, headers=headers, timeout=60)

    def _write_env(self) -> None:
        """
        Write the env variables to the .dhcore file.
        It will overwrite any existing env variables.

        Returns
        -------
        None
        """
        keys = {}
        if self._access_token is not None:
            keys[DhcoreEnvVar.ACCESS_TOKEN.value] = self._access_token
        if self._refresh_token is not None:
            keys[DhcoreEnvVar.REFRESH_TOKEN.value] = self._refresh_token

        for k, v in keys.items():
            set_key(dotenv_path=ENV_FILE, key_to_set=k, value_to_set=v)

    ##############################
    # Interface methods
    ##############################

    @staticmethod
    def is_local() -> bool:
        """
        Declare if Client is local.

        Returns
        -------
        bool
            False
        """
        return False
