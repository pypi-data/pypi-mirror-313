import asyncio
from abc import ABC, abstractmethod
from typing import Optional, cast

from ttxt_v2.core.api.order_update import OrderUpdate
from ttxt_v2.utils.logger import logger

from .base_queue import IQueue
from .connector_status import ConnectorStatus
from .event import Event, Kline, MarketTrades, Orderbook
from .event_handler import IEventHandler
from .order_ack import OrderAck
from .queue_actor import IQueueActor
from .wallet import Wallet


class BaseClient(IEventHandler, IQueueActor, ABC):
    """
    Base class for a client that handles events from a queue and publishes events to a queue.

    This class implements the `IEventHandler` and `IQueueActor` interfaces and provides
    methods for listening to market data and publishing events to a queue.
    """

    def __init__(self, pub_queue: IQueue, sig_queue: Optional[IQueue] = None):
        """
        Initialize the BaseClient with public and optional signal queues.

        Args:
            pub_queue (IQueue): The public queue to listen to for market data.
            sig_queue (Optional[IQueue]): An optional signal queue for additional events.
        """
        self._public_queue = pub_queue
        self._signal_queue = sig_queue
        IQueueActor.__init__(self)

    async def listen_market_data(self):
        """
        Listen to market data from the public queue.

        This method starts the queue reader to process events from the public queue.
        """
        await self.queue_reader(self._public_queue)

    async def queue_reader(self, queue: IQueue):
        """
        Read and process events from the given queue.

        This method continuously polls the queue for events and processes them based on their type.
        It handles `Orderbook`, `MarketTrades`, and `Kline` events specifically, and logs a warning
        for unknown event types.

        Args:
            queue (IQueue): The queue to read events from.
        """
        try:
            while True:
                event = await queue.poll()
                if isinstance(event.payload.data, Orderbook):
                    self.on_orderbook(cast(Event[Orderbook], event.payload))
                elif isinstance(event.payload.data, MarketTrades):
                    self.on_market_trades(cast(Event[MarketTrades], event.payload))
                elif isinstance(event.payload.data, Kline):
                    self.on_kline(cast(Event[Kline], event.payload))
                elif isinstance(event.payload.data, OrderAck):
                    self.on_order_ack(cast(Event[OrderAck], event.payload))
                elif isinstance(event.payload.data, ConnectorStatus):
                    self.on_connector_status(
                        cast(Event[ConnectorStatus], event.payload)
                    )
                elif isinstance(event.payload.data, OrderUpdate):
                    self.on_order_update(cast(Event[OrderUpdate], event.payload))
                elif isinstance(event.payload.data, Wallet):
                    self.on_wallet_update(cast(Event[Wallet], event.payload))
                else:
                    logger.warning(
                        f"Received unknown type from the queue: {event.event_type}"
                    )
        except asyncio.CancelledError:
            logger.warning("BaseClient::queue_reader got cancelled")

    @abstractmethod
    async def run(self):
        pass
