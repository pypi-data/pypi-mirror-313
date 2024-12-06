from dataclasses import dataclass
from typing import List

from ttxt_v2.core.api.trading_pair import TradingPair

from .enums import ESide


@dataclass
class MarketTradesData:
    """
    Represents a single market trade data.

    Attributes:
        price (float): The price at which the trade was executed.
        qty (float): The quantity of the trade.
        side (ESide): The side of the trade (buy or sell).
    """

    price: float
    qty: float
    side: ESide


@dataclass
class MarketTrades:
    """
    Represents a collection of market trades for a specific symbol.

    Attributes:
        symbol (str): The trading pair symbol.
        trades (List[MarketTradesData]): A list of market trade data.
    """

    trading_pair: TradingPair
    trades: List[MarketTradesData]
