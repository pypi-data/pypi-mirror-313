from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import List, Optional

from ttxt_v2.core.api.trading_pair import TradingPair


@dataclass
class OrderbookStreamConfig:
    """
    Configuration for the order book stream.

    Attributes:
        tickers (List[str]): List of ticker symbols to subscribe to.
        depth (int): Depth of the order book to fetch. Default is 50.
    """

    tickers: List[TradingPair]
    depth: int = 50


@dataclass
class MarketTradeStreamConfig:
    """
    Configuration for the market trade stream.

    Attributes:
        tickers (List[str]): List of ticker symbols to subscribe to.
    """

    tickers: List[TradingPair]


class KlineTime(str, Enum):
    """
    Enumeration for Kline time intervals.

    Attributes:
        ONE_MIN (str): 1 minute interval.
        FIVE_MIN (str): 5 minute interval.
        FIFTEEN_MIN (str): 15 minute interval.
        THIRTY_MIN (str): 30 minute interval.
    """

    ONE_MIN = "1"
    FIVE_MIN = "5"
    FIFTEEN_MIN = "15"
    THIRTY_MIN = "30"
    ONE_HOUR = "1h"
    FOUR_HOUR = "4h"
    ONE_DAY = "1d"


@dataclass
class KLineStreamConfig:
    """
    Configuration for the Kline stream.

    Attributes:
        tickers (List[str]): List of ticker symbols to subscribe to.
        timeframe (KlineTime): Timeframe for the Kline data. Default is 1 minute.
    """

    tickers: List[TradingPair]
    timeframe: KlineTime = KlineTime.ONE_MIN


class StorageType(StrEnum):
    NONE = "none"
    LOCAL = "local"


@dataclass
class StorageConfig:
    enable: bool = False
    storage_type: Optional[StorageType] = None


class OperationMode(Enum):
    SPOT = 0
    FUTURES = 1


class TradingMode(StrEnum):
    NONE = "None"
    TRADE = "trade"
    TEST = "test"


@dataclass
class ConnectorConfig:
    """
    Configuration for the connector.

    Attributes:
        exchange (str): Name of the exchange.
        ob_config (Optional[OrderbookStreamConfig]): Configuration for the order book stream.
        mt_config (Optional[MarketTradeStreamConfig]): Configuration for the market trade stream.
        kl_config (Optional[KLineStreamConfig]): Configuration for the Kline stream.
    """

    exchange: str
    trading_mode: TradingMode
    recording_config: StorageConfig
    ob_config: Optional[OrderbookStreamConfig]
    mt_config: Optional[MarketTradeStreamConfig]
    kl_config: Optional[KLineStreamConfig]
    operation_mode: OperationMode = OperationMode.SPOT
