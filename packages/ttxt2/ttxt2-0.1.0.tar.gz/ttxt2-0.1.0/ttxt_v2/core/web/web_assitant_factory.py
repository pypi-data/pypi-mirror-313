from typing import Optional

from ttxt_v2.core.web.rest_assistant import RESTAssistant

from .base_auth import BaseAuth
from .connection_factory import ConnectionFactory
from .ws_assistant import WSAssistant


class WebAssitantFactory:
    """
    Factory class for creating WebSocket assistants.

    Methods:
        get_ws_assistant() -> WSAssistant:
            Returns a WebSocket assistant using a connection from the connection factory.

        close():
            Closes the connection factory.
    """

    def __init__(self, auth: Optional[BaseAuth] = None):
        """
        Initializes the WebAssitantFactory with an optional authenticator.

        Args:
            auth (Optional[BaseAuth]): The authenticator for the WebSocket assistant. Default is None.
        """
        self._connection_factory = ConnectionFactory()
        self._auth = auth

    @property
    def auth(self):
        return self._auth

    async def get_rest_assistant(self) -> RESTAssistant:
        connection = await self._connection_factory.get_rest_connection()
        assistant = RESTAssistant(connection=connection, auth=self._auth)
        return assistant

    async def get_ws_assistant(self) -> WSAssistant:
        """
        Returns a WebSocket assistant using a connection from the connection factory.

        Returns:
            WSAssistant: The WebSocket assistant.
        """
        connection = await self._connection_factory.get_ws_connection()
        assistant = WSAssistant(connection, self._auth)
        return assistant

    async def close(self):
        """
        Closes the connection factory.
        """
        await self._connection_factory.close()
