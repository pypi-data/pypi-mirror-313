import asyncio
import time
from json import JSONDecodeError
from typing import Any, Dict, Mapping, Optional

import aiohttp
from aiohttp import WebSocketError, WSCloseCode, WSMessage

from ttxt_v2.utils.logger import logger

from .data_types import WSRequest, WSResponse


class WSConnection:
    """
    WebSocket connection class for managing WebSocket connections and communication.

    Attributes:
        CONFIG_MAX_MSG_SIZE (int): The default maximum message size for aiohttp WebSocket connections.

    Methods:
        connect(ws_url: str, ping_timeout: float = 10, message_timeout: Optional[float] = None, ws_headers: Optional[Dict] = {}, max_msg_size: Optional[int] = None):
            Connects to the WebSocket server with the given URL and parameters.

        disconnect():
            Disconnects from the WebSocket server.

        send(request: WSRequest):
            Sends a WebSocket request.

        ping():
            Sends a ping message to the WebSocket server.

        receive() -> Optional[WSResponse]:
            Receives a message from the WebSocket server.

        _ensure_connected():
            Ensures that the WebSocket connection is established.

        _ensure_not_connected():
            Ensures that the WebSocket connection is not established.

        _read_message() -> aiohttp.WSMessage:
            Reads a message from the WebSocket server.

        _process_message(msg: aiohttp.WSMessage) -> Optional[aiohttp.WSMessage]:
            Processes a received WebSocket message.

        _check_msg_types(msg: Optional[WSMessage]) -> Optional[aiohttp.WSMessage]:
            Checks the type of the received WebSocket message for errors.

        _check_msg_closed_type(msg: Optional[aiohttp.WSMessage]) -> Optional[aiohttp.WSMessage]:
            Checks if the received WebSocket message indicates a closed connection.

        _check_msg_ping_type(msg: Optional[aiohttp.WSMessage]) -> Optional[aiohttp.WSMessage]:
            Checks if the received WebSocket message is a ping message and responds with a pong.

        _check_msg_pong_type(msg: Optional[aiohttp.WSMessage]) -> Optional[aiohttp.WSMessage]:
            Checks if the received WebSocket message is a pong message.

        _update_last_recv_time(_: aiohttp.WSMessage):
            Updates the timestamp of the last received message.

        _send_json(payload: Mapping[str, Any]):
            Sends a JSON payload through the WebSocket connection.

        _send_plain_text(payload: str):
            Sends a plain text payload through the WebSocket connection.

        _send_binary(payload: bytes):
            Sends a binary payload through the WebSocket connection.

        _build_resp(msg: aiohttp.WSMessage) -> WSResponse:
            Builds a WSResponse object from the received WebSocket message.
    """

    CONFIG_MAX_MSG_SIZE = 4 * 1024 * 1024  # Default aiohttp

    def __init__(self, aiohttp_session: aiohttp.ClientSession):
        """
        Initializes the WSConnection with the given aiohttp client session.

        Args:
            aiohttp_session (aiohttp.ClientSession): The aiohttp client session to use for the WebSocket connection.
        """
        self._client_session = aiohttp_session
        self._connection: Optional[aiohttp.ClientWebSocketResponse] = None
        self._connected = False
        self._message_timeout: Optional[float] = None
        self._last_recv_time = 0

    @property
    def last_recv_time(self) -> float:
        """
        Returns the timestamp of the last received message.

        Returns:
            float: The timestamp of the last received message.
        """
        return self._last_recv_time

    @property
    def connected(self) -> bool:
        """
        Checks if the WebSocket connection is established.

        Returns:
            bool: True if the WebSocket connection is established, False otherwise.
        """
        return self._connected

    async def connect(
        self,
        ws_url: str,
        ping_timeout: float = 10,
        message_timeout: Optional[float] = None,
        ws_headers: Optional[Dict] = {},
        max_msg_size: Optional[int] = None,
    ):
        """
        Connects to the WebSocket server with the given URL and parameters.

        Args:
            ws_url (str): The WebSocket server URL.
            ping_timeout (float): The timeout for ping messages. Default is 10 seconds.
            message_timeout (Optional[float]): The timeout for receiving messages. Default is None.
            ws_headers (Optional[Dict]): The headers to include in the WebSocket connection. Default is an empty dictionary.
            max_msg_size (Optional[int]): The maximum message size. Default is None.
        """
        if max_msg_size is None:
            max_msg_size = self.CONFIG_MAX_MSG_SIZE
        self._ensure_not_connected()
        self._connection = await self._client_session.ws_connect(
            ws_url,
            headers=ws_headers,
            max_msg_size=max_msg_size,
        )
        self._message_timeout = message_timeout
        self._connected = True

    async def disconnect(self):
        """
        Disconnects from the WebSocket server.
        """
        if self._connection is not None and not self._connection.closed:
            await self._connection.close()
        self._connection = None
        self._connected = False

    async def send(self, request: WSRequest):
        """
        Sends a WebSocket request.

        Args:
            request (WSRequest): The WebSocket request to send.
        """
        try:
            self._ensure_connected()
            await request.send_with_conn(connection=self)
        except asyncio.CancelledError:
            logger.error("Send cancelled...")
            raise

    async def ping(self):
        """
        Sends a ping message to the WebSocket server.
        """
        self._ensure_connected()
        assert self._connection is not None, "Connection cannot be None"
        await self._connection.ping()

    async def receive(self) -> Optional[WSResponse]:
        """
        Receives a message from the WebSocket server.

        Returns:
            Optional[WSResponse]: The received WebSocket response, or None if no message is received.
        """
        try:
            self._ensure_connected()
            response = None
            while self._connected:
                msg = await self._read_message()
                msg = await self._process_message(msg)
                if msg is not None:
                    response = self._build_resp(msg)
                    break
            return response
        except asyncio.CancelledError:
            logger.error("Receive cancelled...")
            raise

    def _ensure_connected(self):
        """
        Ensures that the WebSocket connection is established.

        Raises:
            RuntimeError: If the WebSocket connection is not established.
        """
        if not self._connected:
            raise RuntimeError("WS is not connected")

    def _ensure_not_connected(self):
        """
        Ensures that the WebSocket connection is not established.

        Raises:
            RuntimeError: If the WebSocket connection is already established.
        """
        if self._connected:
            raise RuntimeError("WS is connected")

    async def _read_message(self) -> aiohttp.WSMessage:
        """
        Reads a message from the WebSocket server.

        Returns:
            aiohttp.WSMessage: The received WebSocket message.

        Raises:
            asyncio.TimeoutError: If the message receive operation times out.
        """
        self._ensure_connected()
        assert self._connection is not None, "Connection cannot be None"
        try:
            msg = await self._connection.receive(self._message_timeout)
            return msg
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError("Message receive timed out")

    async def _process_message(
        self, msg: aiohttp.WSMessage
    ) -> Optional[aiohttp.WSMessage]:
        """
        Processes a received WebSocket message.

        Args:
            msg (aiohttp.WSMessage): The received WebSocket message.

        Returns:
            Optional[aiohttp.WSMessage]: The processed WebSocket message, or None if the message is not valid.
        """
        data = await self._check_msg_types(msg)
        if data is not None:
            msg = data
        self._update_last_recv_time(msg)
        return msg

    async def _check_msg_types(
        self, msg: Optional[WSMessage]
    ) -> Optional[aiohttp.WSMessage]:
        """
        Checks the type of the received WebSocket message for errors.

        Args:
            msg (Optional[WSMessage]): The received WebSocket message.

        Returns:
            Optional[aiohttp.WSMessage]: The WebSocket message if it is valid, or None if it is not valid.

        Raises:
            WebSocketError: If the WebSocket message indicates an error.
            ConnectionError: If the WebSocket connection is closed unexpectedly.
        """
        if msg is not None and msg.type in [aiohttp.WSMsgType.ERROR]:
            if (
                isinstance(msg.data, WebSocketError)
                and msg.data.code == WSCloseCode.MESSAGE_TOO_BIG
            ):
                await self.disconnect()
                raise WebSocketError(
                    msg.data.code, f"The WS message is too big: {msg.data}"
                )
            else:
                await self.disconnect()
                raise ConnectionError(f"WS error: {msg.data}")
        return msg

    async def _check_msg_closed_type(
        self, msg: Optional[aiohttp.WSMessage]
    ) -> Optional[aiohttp.WSMessage]:
        """
        Checks if the received WebSocket message indicates a closed connection.

        Args:
            msg (Optional[aiohttp.WSMessage]): The received WebSocket message.

        Returns:
            Optional[aiohttp.WSMessage]: The WebSocket message if it is valid, or None if the connection is closed.

        Raises:
            ConnectionError: If the WebSocket connection is closed unexpectedly.
        """
        if msg is not None and msg.type in [
            aiohttp.WSMsgType.CLOSED,
            aiohttp.WSMsgType.CLOSE,
        ]:
            if self._connected:
                assert self._connection is not None, "Connection cannot be None"
                close_code = self._connection.close_code
                await self.disconnect()
                raise ConnectionError(
                    f"The WS connection was closed unexpectedly. Close code {close_code} msg data {msg.data}"
                )
            msg = None
        return msg

    async def _check_msg_ping_type(
        self, msg: Optional[aiohttp.WSMessage]
    ) -> Optional[aiohttp.WSMessage]:
        """
        Checks if the received WebSocket message is a ping message and responds with a pong.

        Args:
            msg (Optional[aiohttp.WSMessage]): The received WebSocket message.

        Returns:
            Optional[aiohttp.WSMessage]: None if the message is a ping message, or the original message if it is not.
        """
        if msg is not None and msg.type == aiohttp.WSMsgType.PING:
            assert self._connection is not None, "Connection cannot be None"
            await self._connection.pong()
            msg = None
        return msg

    async def _check_msg_pong_type(
        self, msg: Optional[aiohttp.WSMessage]
    ) -> Optional[aiohttp.WSMessage]:
        """
        Checks if the received WebSocket message is a pong message.

        Args:
            msg (Optional[aiohttp.WSMessage]): The received WebSocket message.

        Returns:
            Optional[aiohttp.WSMessage]: None if the message is a pong message, or the original message if it is not.
        """
        if msg is not None and msg.type == aiohttp.WSMsgType.PONG:
            msg = None
        return msg

    def _update_last_recv_time(self, _: aiohttp.WSMessage):
        """
        Updates the timestamp of the last received message.

        Args:
            _ (aiohttp.WSMessage): The received WebSocket message.
        """
        self._last_recv_time = time.time()

    async def _send_json(self, payload: Mapping[str, Any]):
        """
        Sends a JSON payload through the WebSocket connection.

        Args:
            payload (Mapping[str, Any]): The JSON payload to send.
        """
        assert self._connection is not None, "Connection cannot be None"
        await self._connection.send_json(payload)

    async def _send_plain_text(self, payload: str):
        """
        Sends a plain text payload through the WebSocket connection.

        Args:
            payload (str): The plain text payload to send.
        """
        assert self._connection is not None, "Connection cannot be None"
        await self._connection.send_str(payload)

    async def _send_binary(self, payload: bytes):
        """
        Sends a binary payload through the WebSocket connection.

        Args:
            payload (bytes): The binary payload to send.
        """
        assert self._connection is not None, "Connection cannot be None"
        await self._connection.send_bytes(payload)

    @staticmethod
    def _build_resp(msg: aiohttp.WSMessage) -> WSResponse:
        """
        Builds a WSResponse object from the received WebSocket message.

        Args:
            msg (aiohttp.WSMessage): The received WebSocket message.

        Returns:
            WSResponse: The built WSResponse object.
        """
        if msg.type == aiohttp.WSMsgType.BINARY:
            data = msg.data
        elif msg.type == aiohttp.WSMsgType.PONG:
            data = None
        else:
            try:
                data = msg.json()
            except JSONDecodeError as je:
                logger.debug(f"JSONDecode error on receive: {je}, msg: {msg}")
                data = msg.data
        response = WSResponse(data)
        return response
