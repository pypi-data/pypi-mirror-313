from dataclasses import dataclass, field
from typing import Optional

from ttxt_v2.core.api.trading_pair import TradingPair


@dataclass
class AmendOrder:
    trading_pair: TradingPair
    order_id: str
    new_qty: Optional[float] = None
    new_price: Optional[float] = None
    new_stop_loss: Optional[float] = None
    new_take_profit: Optional[float] = None
    extra_params: Optional[dict] = field(default_factory=dict)
