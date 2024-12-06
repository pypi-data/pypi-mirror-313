from copy import deepcopy
from typing import Dict, Optional

from .base_auth import BaseAuth
from .ws_connection import WSConnection, WSRequest, WSResponse


class WSAssistant:
    """
    WebSocket assistant class for managing WebSocket connections and requests.

    Methods:
        connect(ws_url: str, *, ping_timeout: float = 10, message_timeout: Optional[float] = None, ws_header: Optional[Dict] = {}, max_msg_size: Optional[int] = None):
            Connects to the WebSocket server with the given URL and parameters.

        disconnect():
            Disconnects from the WebSocket server.

        subscribe(request: WSRequest):
            Subscribes to a WebSocket stream using the given request.

        send(request: WSRequest):
            Sends a WebSocket request.

        ping():
            Sends a ping message to the WebSocket server.

        receive() -> Optional[WSResponse]:
            Receives a message from the WebSocket server.

        _authenticate(request: WSRequest) -> WSRequest:
            Authenticates the WebSocket request if authentication is required.
    """

    def __init__(self, connection: WSConnection, auth: Optional[BaseAuth]):
        """
        Initializes the WSAssistant with the given WebSocket connection and optional authenticator.

        Args:
            connection (WSConnection): The WebSocket connection to use.
            auth (Optional[BaseAuth]): The authenticator for the WebSocket connection. Default is None.
        """
        self._connection = connection
        self._auth = auth

    @property
    def connected(self):
        return self._connection.connected

    @property
    def last_recv_time(self) -> float:
        """
        Returns the timestamp of the last received message.

        Returns:
            float: The timestamp of the last received message.
        """
        return self._connection.last_recv_time

    async def connect(
        self,
        ws_url: str,
        *,
        ping_timeout: float = 10,
        message_timeout: Optional[float] = None,
        ws_header: Optional[Dict] = {},
        max_msg_size: Optional[int] = None,
    ):
        """
        Connects to the WebSocket server with the given URL and parameters.

        Args:
            ws_url (str): The WebSocket server URL.
            ping_timeout (float): The timeout for ping messages. Default is 10 seconds.
            message_timeout (Optional[float]): The timeout for receiving messages. Default is None.
            ws_header (Optional[Dict]): The headers to include in the WebSocket connection. Default is an empty dictionary.
            max_msg_size (Optional[int]): The maximum message size. Default is None.
        """
        await self._connection.connect(
            ws_url=ws_url,
            ws_headers=ws_header,
            ping_timeout=ping_timeout,
            message_timeout=message_timeout,
            max_msg_size=max_msg_size,
        )

    async def disconnect(self):
        """
        Disconnects from the WebSocket server.
        """
        await self._connection.disconnect()

    async def subscribe(self, request: WSRequest):
        """
        Subscribes to a WebSocket stream using the given request.

        Args:
            request (WSRequest): The WebSocket request to subscribe to.
        """
        await self.send(request)

    async def send(self, request: WSRequest):
        """
        Sends a WebSocket request.

        Args:
            request (WSRequest): The WebSocket request to send.
        """
        request = deepcopy(request)
        request = await self._authenticate(request)
        await self._connection.send(request)

    async def ping(self):
        """
        Sends a ping message to the WebSocket server.
        """
        await self._connection.ping()

    async def receive(self) -> Optional[WSResponse]:
        """
        Receives a message from the WebSocket server.

        Returns:
            Optional[WSResponse]: The received WebSocket response, or None if no message is received.
        """
        response = await self._connection.receive()
        return response

    async def _authenticate(self, request: WSRequest) -> WSRequest:
        """
        Authenticates the WebSocket request if authentication is required.

        Args:
            request (WSRequest): The WebSocket request to authenticate.

        Returns:
            WSRequest: The authenticated WebSocket request.
        """
        if self._auth is not None and request.is_auth():
            request = await self._auth.ws_authenticate(request)
        return request
