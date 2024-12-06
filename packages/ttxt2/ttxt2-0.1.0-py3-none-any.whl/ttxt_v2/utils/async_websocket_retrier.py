import asyncio
from functools import wraps
from typing import Callable

from ttxt_v2.core.api import EWebSocketType
from ttxt_v2.utils.logger import logger


def websocket_reconnect(websocket_type: EWebSocketType):
    """
    Decorator to ensure that a WebSocket connection is re-established in case of disconnection.

    Args:
        websocket_type (EWebsocketType): The type of WebSocket (PUBLIC, PRIVATE, TRADE).
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            while True:
                try:
                    await func(self, *args, **kwargs)
                except asyncio.CancelledError:
                    logger.error(f"WebSocket {websocket_type.name} stream cancelled.")
                    break
                except Exception as e:
                    logger.error(
                        f"WebSocket {websocket_type.name} connection error: {str(e)}"
                    )
                    await self._on_websocket_disconnected(e, websocket_type)
                    logger.info(
                        f"Attempting to reconnect {websocket_type.name} WebSocket in 5 seconds..."
                    )
                    await asyncio.sleep(5)
                    await self._on_websocket_reconnecting(e, websocket_type)

        return wrapper

    return decorator
