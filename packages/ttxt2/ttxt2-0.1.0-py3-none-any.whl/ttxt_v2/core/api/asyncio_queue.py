import asyncio

from .base_queue import IQueue
from .event import BaseEvent


class AsyncioQueue(IQueue):
    """
    An asynchronous queue implementation using asyncio.Queue.

    Attributes:
        _queue (asyncio.Queue): The underlying asyncio queue with a specified capacity.
    """

    def __init__(self, capacity: int = 256):
        """
        Initializes the AsyncioQueue with a given capacity.

        Args:
            capacity (int): The maximum number of items the queue can hold. Defaults to 256.
        """
        self._queue = asyncio.Queue(maxsize=capacity)

    async def publish(self, item: BaseEvent):
        """
        Publishes an item to the queue.

        Args:
            item (BaseEvent): The event to be added to the queue.
        """
        await self._queue.put(item)

    async def poll(self) -> BaseEvent:
        """
        Polls an item from the queue.

        Returns:
            BaseEvent: The event retrieved from the queue.
        """
        return await self._queue.get()

    def put_nowait(self, item: "BaseEvent"):
        self._queue.put_nowait(item)
