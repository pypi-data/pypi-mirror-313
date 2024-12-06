from dataclasses import dataclass

from .enums import EAckType


@dataclass
class OrderAck:
    order_id: str
    ack_type: EAckType
    timestamp: int
