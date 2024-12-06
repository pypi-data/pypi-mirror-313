from dataclasses import dataclass

from .trading_pair import TradingPair


@dataclass
class Kline:
    """
    Represents a Kline (candlestick) data structure.

    Attributes:
        symbol (str): The trading pair symbol.
        open (float): The opening price of the Kline.
        close (float): The closing price of the Kline.
        high (float): The highest price of the Kline.
        low (float): The lowest price of the Kline.
        volume (float): The trading volume during the Kline period.
        start (int): The start time of the Kline period.
        timestamp (int): The timestamp of the Kline.
    """

    trading_pair: TradingPair
    open: float
    close: float
    high: float
    low: float
    volume: float
    start: int
    timestamp: int
    confirm: bool
