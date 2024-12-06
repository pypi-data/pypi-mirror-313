from dataclasses import dataclass


@dataclass
class MessageHeader:
    """
    Represents the header information of a message.

    Attributes:
        exchange (str): The name of the exchange.
        timestamp (int): The timestamp of the message.
    """

    exchange: str
    timestamp: int
