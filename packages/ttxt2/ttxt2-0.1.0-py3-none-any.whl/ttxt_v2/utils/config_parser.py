import json
from abc import ABC, abstractmethod
from pathlib import Path

from ttxt_v2.connector.connector_config import (
    ConnectorConfig,
    KLineStreamConfig,
    KlineTime,
    MarketTradeStreamConfig,
    OperationMode,
    OrderbookStreamConfig,
    StorageConfig,
    StorageType,
    TradingMode,
)
from ttxt_v2.core.api import TradingPair


class IConfigParser(ABC):
    def __init__(self, path: str):
        self._path = path

    @abstractmethod
    def parse_config(self) -> ConnectorConfig:
        pass


class JSONConfigParser(IConfigParser):
    def __init__(self, path: str):
        super().__init__(path)

    def parse_config(self) -> ConnectorConfig:
        """
        Parses the configuration file and returns a ConnectorConfig object.

        Returns:
            ConnectorConfig: The parsed configuration object.

        Raises:
            FileNotFoundError: If the configuration file is not found.
        """
        config_file = Path(self._path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self._path}")

        with open(config_file, "r") as file:
            config_data = json.load(file)

        trading = config_data.get("trading_mode", "none")
        trading_mode_mapping = {
            "none": TradingMode.NONE,
            "test": TradingMode.TEST,
            "live": TradingMode.TRADE,
        }

        tickers = config_data["tickers"]
        pairs = [
            TradingPair(tick.split("/")[0], tick.split("/")[1]) for tick in tickers
        ]
        market_recorder = config_data.get("recording_config")
        recording_type = StorageType.NONE
        if market_recorder["enable"]:
            recording_type = (
                StorageType.LOCAL
                if market_recorder["storage_type"] == "local"
                else StorageType.NONE
            )
        recording_config = StorageConfig(
            enable=market_recorder["enable"], storage_type=recording_type
        )
        # HACK: For now only spot and futures later also options
        operations_mode = config_data.get("operation_mode", "spot")
        op_mode_en = (
            OperationMode.SPOT if operations_mode == "spot" else OperationMode.FUTURES
        )
        kline_mapping = {
            "1m": KlineTime.ONE_MIN,
            "5m": KlineTime.FIVE_MIN,
            "15m": KlineTime.FIFTEEN_MIN,
            "30m": KlineTime.THIRTY_MIN,
            "1h": KlineTime.ONE_HOUR,
            "4h": KlineTime.FOUR_HOUR,
            "1d": KlineTime.ONE_DAY,
        }
        kline_time = config_data.get("kline_timeframe", "1m")
        return ConnectorConfig(
            exchange=config_data["exchange"],
            trading_mode=trading_mode_mapping[trading],
            recording_config=recording_config,
            ob_config=OrderbookStreamConfig(tickers=pairs),
            mt_config=MarketTradeStreamConfig(tickers=pairs),
            kl_config=KLineStreamConfig(
                tickers=pairs, timeframe=kline_mapping[kline_time]
            ),
            operation_mode=op_mode_en,
        )
