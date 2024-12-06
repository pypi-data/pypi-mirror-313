from dataclasses import dataclass
from typing import Optional

from ttxt_v2.core.api.enums import EOrderCategory
from ttxt_v2.core.api.trading_pair import TradingPair


@dataclass
class CancelOrder:
    trading_pair: TradingPair
    category: EOrderCategory
    client_order_id: Optional[str] = None
