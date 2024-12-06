from dataclasses import dataclass, field
from typing import Optional

from ttxt_v2.core.api.trading_pair import TradingPair

from .enums import EOrderCategory, EOrderType, ESide, ETimeInForce


@dataclass
class CreateOrder:
    trading_pair: TradingPair
    category: EOrderCategory
    side: ESide
    order_type: EOrderType
    qty: float
    client_order_id: str
    price: Optional[float] = None
    tif: ETimeInForce = ETimeInForce.GTC
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None
    extra_params: Optional[dict] = field(
        default_factory=dict
    )  # INFO: can be used for exchange specific parameters
