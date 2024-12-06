from typing import Optional

import aiohttp

from ttxt_v2.core.web.rest_connection import RESTConnection
from ttxt_v2.utils.logger import logger

from .ws_connection import WSConnection


class ConnectionFactory:
    """
    Factory class for managing WebSocket and shared HTTP connections.

    Methods:
        get_ws_connection() -> WSConnection:
            Returns a WebSocket connection using a shared client session.

        _get_shared_client() -> aiohttp.ClientSession:
            Returns a shared aiohttp client session.

        close():
            Closes the shared and WebSocket client sessions.
    """

    def __init__(self):
        """
        Initializes the ConnectionFactory with optional aiohttp client sessions.
        """
        self._ws_session: Optional[aiohttp.ClientSession] = None
        self._shared_session: Optional[aiohttp.ClientSession] = None

    async def get_ws_connection(self) -> WSConnection:
        """
        Returns a WebSocket connection using a shared client session.

        Returns:
            WSConnection: The WebSocket connection.
        """
        shared_client = self._ws_session or await self._get_shared_client()
        connection = WSConnection(aiohttp_session=shared_client)
        return connection

    async def get_rest_connection(self) -> RESTConnection:
        shared_client = await self._get_shared_client()
        connection = RESTConnection(aiohttp_client_session=shared_client)
        return connection

    async def _get_shared_client(self) -> aiohttp.ClientSession:
        """
        Returns a shared aiohttp client session. If the session does not exist, it creates a new one.

        Returns:
            aiohttp.ClientSession: The shared aiohttp client session.
        """
        self._shared_session = self._shared_session or aiohttp.ClientSession()
        return self._shared_session

    async def close(self):
        """
        Closes the shared and WebSocket client sessions if they are open.
        """
        logger.info("Cleaning up the connection factory")
        if self._shared_session and not self._shared_session.closed:
            await self._shared_session.close()
        if self._ws_session and not self._ws_session.closed:
            await self._ws_session.close()
