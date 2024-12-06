from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .event import BaseEvent


class IQueue(ABC):
    """
    Interface for a queue that handles publishing and polling of events.

    This abstract base class defines the methods that must be implemented
    by any concrete queue class. It uses the `abc` module to enforce the
    implementation of the `publish` and `poll` methods.
    """

    @abstractmethod
    async def publish(self, item: "BaseEvent"):
        """
        Publish an event to the queue.

        This method should be implemented by subclasses to provide the
        specific logic for publishing an event to the queue.

        Args:
            item (BaseEvent): The event to publish.
        """
        pass

    @abstractmethod
    async def poll(self) -> "BaseEvent":
        """
        Poll an event from the queue.

        This method should be implemented by subclasses to provide the
        specific logic for polling an event from the queue.

        Returns:
            BaseEvent: The event polled from the queue.
        """
        pass

    def put_nowait(self, item: "BaseEvent"):
        pass
