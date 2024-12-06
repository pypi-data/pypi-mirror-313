from ttxt_v2.core.api.event import BaseEvent
from .base_queue import IQueue


class IQueuePublisher:
    """
    An interface for a queue publisher that defines the behavior for writing to a queue.

    Methods:
        publish_to_queue(queue: IQueue, item: BaseEvent):
            Publishes an item to the specified queue.
    """

    async def publish_to_queue(self, queue: IQueue, item: BaseEvent):
        """
        Publishes an item to the specified queue.

        Args:
            queue (IQueue): The queue to which the item will be published.
            item (BaseEvent): The event to be published to the queue.
        """
        await queue.publish(item)
