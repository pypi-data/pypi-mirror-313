from abc import ABC

from .queue_consumer import IQueueConsumer
from .queue_publisher import IQueuePublisher


class IQueueActor(IQueueConsumer, IQueuePublisher, ABC):
    """
    An interface for a queue actor that combines both consumer and publisher behaviors.

    This class inherits from IQueueConsumer, IQueuePublisher, and ABC (Abstract Base Class).

    Methods:
        This interface does not define any additional methods, but requires implementation of methods
        from IQueueConsumer and IQueuePublisher.
    """

    pass
