from dataclasses import dataclass, field
from typing import List, Tuple

from .enums import EUpdateType
from .trading_pair import TradingPair


@dataclass
class OrderbookEntry:
    """
    Represents a single entry in the order book.

    Attributes:
        price (float): The price level of the order.
        qty (float): The quantity available at the price level.
    """

    price: float = 0.0
    qty: float = 0.0

    def __eq__(self, other):
        if isinstance(other, OrderbookEntry):
            return self.price == other.price
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, OrderbookEntry):
            return self.price < other.price
        return NotImplemented


Bids = List[OrderbookEntry]
Asks = List[OrderbookEntry]


@dataclass
class Orderbook:
    """
    Represents the order book for a specific trading pair.

    Attributes:
        update_type (EUpdateType): The type of update (e.g., snapshot, delta).
        symbol (str): The trading pair symbol.
        bids (Bids): A list of bid entries in the order book.
        asks (Asks): A list of ask entries in the order book.
        timestamp (int): The timestamp of the order book update.
    """

    update_type: EUpdateType = EUpdateType.SNAPSHOT
    trading_pair: TradingPair = TradingPair(base="", quote="")
    bids: Bids = field(default_factory=list)
    asks: Asks = field(default_factory=list)
    timestamp: int = 0
    seq: int = 0

    def update(self, ob):
        if not isinstance(ob, Orderbook):
            return NotImplemented
        if ob.update_type == EUpdateType.SNAPSHOT:
            self = ob
        else:
            self._update_from_delta(ob)

        # HACK: maybe it should be configurable
        self.bids = self.bids[:50]
        self.asks = self.asks[:50]
        self.timestamp = ob.timestamp
        self.seq = ob.seq

    def get_mid_price(self) -> float:
        return (self.bids[0].price + self.asks[0].price) / 2

    def get_vwap_price(self) -> float:
        vwap_bid, vwap_ask = self.get_vwap()
        return (vwap_bid + vwap_ask) / 2

    def get_vwap(self, depth: int = 10) -> Tuple[float, float]:
        if not self.bids or not self.asks:
            return 0.0, 0.0
        """
        Calculates the Volume-Weighted Average Price (VWAP) for both bids and asks.

        Args:
            depth (int): The depth to which VWAP should be calculated. Defaults to 10.

        Returns:
            Tuple[float, float]: The VWAP for bids and asks as a tuple (vwap_bids, vwap_asks).
        """

        def calculate_vwap(side: List[OrderbookEntry]) -> float:
            total_volume = sum(entry.qty for entry in side[:depth])
            total_price_volume = sum(entry.price * entry.qty for entry in side[:depth])
            return total_price_volume / total_volume if total_volume > 0 else 0.0

        vwap_bids = calculate_vwap(self.bids)
        vwap_asks = calculate_vwap(self.asks)

        return vwap_bids, vwap_asks

    def get_volume_within_percentage(self, percentage: float) -> Tuple[float, float]:
        """
        Calculates the volume within a given percentage range from the best bid and ask prices.

        Args:
            percentage (float): The percentage range within which to calculate volume.

        Returns:
            Tuple[float, float]: The cumulative volumes within the percentage range
                                 for bids and asks as (volume_bids, volume_asks).
        """
        if not self.bids or not self.asks:
            return 0.0, 0.0

        mid_price = self.get_mid_price()
        bid_limit = mid_price * (1 + percentage / 100)
        ask_limit = mid_price * (1 - percentage / 100)

        volume_bids = sum(entry.qty for entry in self.bids if entry.price <= bid_limit)
        volume_asks = sum(entry.qty for entry in self.asks if entry.price >= ask_limit)

        return volume_bids, volume_asks

    def _update_from_delta(self, delta):
        """
        Updates the orderbook from a delta. The rules for updating the orderbook are as follows:
            1. If update price level is not found in the orderbook then add it
            2. If the price level is found
                - if the qty is 0 delete the price level
                - if the qty does not match update the level
        """
        if not isinstance(delta, Orderbook):
            return NotImplemented
        if (
            delta.trading_pair.base != self.trading_pair.base
            or delta.trading_pair.quote != self.trading_pair.quote
        ):
            return NotImplemented

        def bisect_left_custom(a, x, reverse=False):
            lo, hi = 0, len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                if reverse:
                    # For descending order
                    if a[mid].price > x.price:
                        lo = mid + 1
                    else:
                        hi = mid
                else:
                    # For ascending order
                    if a[mid].price < x.price:
                        lo = mid + 1
                    else:
                        hi = mid
            return lo

        def insort_left_custom(a, x, reverse=False):
            idx = bisect_left_custom(a, x, reverse)
            a.insert(idx, x)

        def update_side(
            side: List[OrderbookEntry], delta_side: List[OrderbookEntry], reverse: bool
        ):
            for entry in delta_side:
                index = bisect_left_custom(side, entry, reverse)
                if index < len(side) and abs(side[index].price - entry.price) < 1e-8:
                    # Remove from book
                    if entry.qty == 0:
                        side.pop(index)
                    else:
                        side[index].qty = entry.qty  # Update quantity if different
                elif entry.qty > 0:
                    # Insert new price level while maintaining sorted order
                    insort_left_custom(side, entry, reverse)

        # Update bids and asks
        update_side(self.bids, delta.bids, reverse=True)
        update_side(self.asks, delta.asks, reverse=False)
        self.timestamp = delta.timestamp


Delta = Orderbook
