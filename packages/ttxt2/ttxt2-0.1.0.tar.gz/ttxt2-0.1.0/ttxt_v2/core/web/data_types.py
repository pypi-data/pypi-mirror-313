import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Mapping, Optional

import aiohttp
from attr import dataclass

if TYPE_CHECKING:
    from .ws_connection import WSConnection


class RESTMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    def __str__(self):
        obj_str = repr(self)
        return obj_str

    def __repr__(self):
        return self.value


@dataclass
class RESTRequest:
    method: RESTMethod
    url: Optional[str] = None
    endpoint_url: Optional[str] = None
    params: Optional[Mapping[str, str]] = None
    data: Any = None
    headers: Optional[Mapping[str, str]] = None
    is_auth_required: bool = False


@dataclass
class EndpointRESTRequest(RESTRequest, ABC):
    endpoint: Optional[str] = None

    def __post_init__(self):
        self._ensure_url()
        self._ensure_params()
        self._ensure_data()

    @property
    @abstractmethod
    def base_url(self) -> str: ...

    def _ensure_url(self):
        if self.url is None and self.endpoint is None:
            raise ValueError("Either the full url or the endpoint must be specified")

        if self.url is None:
            assert self.endpoint is not None, "Endpoint cannot be None"
            if self.endpoint.startswith("/"):
                self.url = f"{self.base_url}{self.endpoint}"
            else:
                self.url = f"{self.base_url}/{self.endpoint}"

    def _ensure_params(self):
        if self.method == RESTMethod.POST:
            if self.params is not None:
                raise ValueError(
                    "POST requests should not use `params`. Use `data` instead."
                )

    def _ensure_data(self):
        if self.method == RESTMethod.POST:
            if self.data is not None:
                self.data = json.dumps(self.data)
        elif self.data is not None:
            raise ValueError(
                "The `data` field should be used only for POST requests. Use `params` instead"
            )


class RESTResponse:
    def __init__(self, aiohttp_response: aiohttp.ClientResponse):
        self._aiohttp_resp = aiohttp_response
        self.url = str(aiohttp_response.url)
        self.method = RESTMethod(aiohttp_response.method.upper())
        self.status = aiohttp_response.status
        self.headers = dict(aiohttp_response.headers)

    async def json(self) -> Any:
        return await self._aiohttp_resp.json()

    async def text(self) -> str:
        return await self._aiohttp_resp.text()


class WSRequest(ABC):
    """
    Abstract base class for WebSocket requests.

    Methods:
        send_with_conn(connection: "WSConnection"):
            Sends the request using the provided WebSocket connection.

        is_auth() -> bool:
            Checks if the request requires authentication.
    """

    @abstractmethod
    async def send_with_conn(self, connection: "WSConnection"):
        """
        Sends the request using the provided WebSocket connection.

        Args:
            connection (WSConnection): The WebSocket connection to use for sending the request.
        """
        pass

    @abstractmethod
    def is_auth(self) -> bool:
        """
        Checks if the request requires authentication.

        Returns:
            bool: True if the request requires authentication, False otherwise.
        """
        pass


@dataclass
class WSJSONRequest(WSRequest):
    """
    WebSocket request class for sending JSON payloads.

    Attributes:
        payload (Mapping[str, Any]): The JSON payload to send.
        is_auth_required (bool): Indicates if the request requires authentication. Default is False.
    """

    payload: Mapping[str, Any]
    is_auth_required: bool = False

    async def send_with_conn(self, connection: "WSConnection"):
        """
        Sends the JSON payload using the provided WebSocket connection.

        Args:
            connection (WSConnection): The WebSocket connection to use for sending the request.
        """
        return await connection._send_json(payload=self.payload)

    def is_auth(self) -> bool:
        """
        Checks if the request requires authentication.

        Returns:
            bool: True if the request requires authentication, False otherwise.
        """
        return self.is_auth_required


@dataclass
class WSPlainTextRequest(WSRequest):
    """
    WebSocket request class for sending plain text payloads.

    Attributes:
        payload (str): The plain text payload to send.
        is_auth_required (bool): Indicates if the request requires authentication. Default is False.
    """

    payload: str
    is_auth_required: bool = False

    async def send_with_conn(self, connection: "WSConnection"):
        """
        Sends the plain text payload using the provided WebSocket connection.

        Args:
            connection (WSConnection): The WebSocket connection to use for sending the request.
        """
        return await connection._send_plain_text(payload=self.payload)

    def is_auth(self) -> bool:
        """
        Checks if the request requires authentication.

        Returns:
            bool: True if the request requires authentication, False otherwise.
        """
        return self.is_auth_required


@dataclass
class WSBinaryRequest(WSRequest):
    """
    WebSocket request class for sending binary payloads.

    Attributes:
        payload (bytes): The binary payload to send.
        is_auth_required (bool): Indicates if the request requires authentication. Default is False.
    """

    payload: bytes
    is_auth_required: bool = False

    async def send_with_conn(self, connection: "WSConnection"):
        """
        Sends the binary payload using the provided WebSocket connection.

        Args:
            connection (WSConnection): The WebSocket connection to use for sending the request.
        """
        return await connection._send_binary(self.payload)

    def is_auth(self) -> bool:
        """
        Checks if the request requires authentication.

        Returns:
            bool: True if the request requires authentication, False otherwise.
        """
        return self.is_auth_required


@dataclass
class WSResponse:
    """
    Class representing a WebSocket response.

    Attributes:
        data (Any): The data received in the WebSocket response.
    """

    data: Any
