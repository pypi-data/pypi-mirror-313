from dataclasses import dataclass
from typing import List

from .enums import EOrderStatus, EOrderType, ESide, ETimeInForce
from .trading_pair import TradingPair


@dataclass
class OrderUpdateItem:
    symbol: TradingPair
    order_id: str
    side: ESide
    order_type: EOrderType
    price: float
    qty: float
    tif: ETimeInForce
    order_status: EOrderStatus
    custom_order_id: str
    cum_exec_qty: float
    cum_exec_value: float
    cum_exec_fee: float
    closed_pnl: float
    take_profit: float
    stop_loss: float
    tp_limit_price: float
    sl_limit_price: float
    create_time: int
    update_time: int


@dataclass
class OrderUpdate:
    timestamp: int
    updates: List[OrderUpdateItem]
