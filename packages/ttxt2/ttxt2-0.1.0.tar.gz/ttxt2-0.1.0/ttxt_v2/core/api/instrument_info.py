from dataclasses import dataclass

from .trading_pair import TradingPair

# TODO: (ivan needs refactoring with proper parameter taught)


@dataclass(frozen=True)
class InstrumentInfo:
    pair: TradingPair
    tradebale: bool = True
    base_precision: int = 0
    quote_precision: int = 0
    qty_precision: int = 0
    min_order_qty: float = 0.0
    max_order_qty: float = 0.0
    min_order_amt: float = 0.0
    max_order_amt: float = 0.0
    tick_size: float = 0.0
