from dataclasses import dataclass
from typing import List

from .trading_pair import TradingPair


@dataclass
class Position:
    symbol: TradingPair
    amount: float
    entry_price: float
    unrealized_pnl: float
    margin_type: str
    isolated_wallet: float
    position_side: str


@dataclass
class PositionUpdate:
    positions: List[Position]
    timestamp: int
