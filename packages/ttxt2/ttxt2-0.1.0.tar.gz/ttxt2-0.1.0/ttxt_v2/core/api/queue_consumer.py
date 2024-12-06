from abc import ABC, abstractmethod

from .base_queue import IQueue


class IQueueConsumer(ABC):
    """
    An interface for a queue consumer that defines the behavior for reading from a queue.

    Methods:
        queue_reader(queue: IQueue):
            An abstract method that must be implemented to read items from the specified queue.
    """

    @abstractmethod
    async def queue_reader(self, queue: IQueue):
        """
        Reads items from the specified queue.

        Args:
            queue (IQueue): The queue from which to read items.
        """
        pass
