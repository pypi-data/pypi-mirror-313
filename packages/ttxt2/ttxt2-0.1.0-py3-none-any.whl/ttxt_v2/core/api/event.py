from dataclasses import dataclass
from typing import Generic, TypeVar, Union

from .amend_order import AmendOrder
from .cancel_order import CancelOrder
from .connector_status import ConnectorStatus
from .create_order import CreateOrder
from .enums import EventType
from .header import MessageHeader
from .kline import Kline
from .market_trades import MarketTrades
from .order_ack import OrderAck
from .order_update import OrderUpdate
from .orderbook import Orderbook
from .position_update import PositionUpdate
from .wallet import Wallet

T = TypeVar(
    "T",
    Orderbook,
    MarketTrades,
    Kline,
    CreateOrder,
    CancelOrder,
    AmendOrder,
    OrderAck,
    Wallet,
    OrderUpdate,
    ConnectorStatus,
    PositionUpdate,
)


@dataclass
class Event(Generic[T]):
    """
    Represents a generic event with a header and data payload.

    Attributes:
        header (MessageHeader): The header information of the message.
        data (T): The data payload of the event, which can be of type Orderbook, MarketTrades, or Kline.
    """

    header: MessageHeader
    data: T


EventLike = Union[
    Event[Orderbook],
    Event[MarketTrades],
    Event[Kline],
    Event[CreateOrder],
    Event[CancelOrder],
    Event[AmendOrder],
    Event[OrderAck],
    Event[PositionUpdate],
    Event[Wallet],
    Event[OrderUpdate],
    Event[ConnectorStatus],
]


@dataclass
class BaseEvent:
    """
    Represents a base event with an event type and payload.

    Attributes:
        event_type (EventType): The type of the event.
        payload (EventLike): The payload of the event, which can be an Event of type Orderbook, MarketTrades, or Kline.
    """

    event_type: EventType
    payload: EventLike
