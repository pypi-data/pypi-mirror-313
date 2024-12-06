from abc import ABC, abstractmethod

from ttxt_v2.core.api import (
    Kline,
    MarketTrades,
    OrderAck,
    Orderbook,
    OrderUpdate,
    Wallet,
)
from ttxt_v2.core.api.enums import (
    EOrderCategory,
    EOrderStatus,
    EOrderType,
    ESide,
    ETimeInForce,
)


class NormalizerBase(ABC):
    """
    Abstract base class for normalizing exchange data into standard formats.

    Methods:
        convert_exchange_orderbook_to_orderbook(data: dict) -> Orderbook:
            Converts exchange-specific order book data to a standard Orderbook format.

        convert_exchange_klines_to_klines(data: dict) -> Kline:
            Converts exchange-specific Kline data to a standard Kline format.

        convert_exchange_trades_to_trades(data: dict) -> MarketTrades:
            Converts exchange-specific trade data to a standard MarketTrades format.
    """

    @abstractmethod
    def convert_exchange_orderbook_to_orderbook(self, data: dict) -> Orderbook:
        """
        Converts exchange-specific order book data to a standard Orderbook format.

        Args:
            data (dict): The exchange-specific order book data.

        Returns:
            Orderbook: The standardized order book data.
        """
        pass

    @abstractmethod
    def convert_exchange_klines_to_klines(self, data: dict) -> Kline:
        """
        Converts exchange-specific Kline data to a standard Kline format.

        Args:
            data (dict): The exchange-specific Kline data.

        Returns:
            Kline: The standardized Kline data.
        """
        pass

    @abstractmethod
    def convert_exchange_trades_to_trades(self, data: dict) -> MarketTrades:
        """
        Converts exchange-specific trade data to a standard MarketTrades format.

        Args:
            data (dict): The exchange-specific trade data.

        Returns:
            MarketTrades: The standardized trade data.
        """
        pass

    @abstractmethod
    def convert_exchange_order_ack_to_order_ack(self, data: dict) -> OrderAck:
        """
        Converts exchange-specific order acknowledgment to a standard OrderAck format.

        Args:
            data (dict): The exchange-specific order acknowledgment.

        Returns:
            OrderAck: The standardized order acknowledgment.
        """
        pass

    @abstractmethod
    def convert_exchange_wallet_update_to_wallet(self, data: dict) -> Wallet:
        """
        Converts exchange-specific wallet update to a standard Wallet format.

        Args:
            data (dict): The exchange-specific wallet update.

        Returns:
            Wallet: The standardized wallet.
        """
        pass

    @abstractmethod
    def convert_exchange_order_update_to_order_update(self, data: dict) -> OrderUpdate:
        """
        Converts exchange-specific order update to a standard OrderUpdate format.

        Args:
            data (dict): The exchange-specific order update.

        Returns:
            OrderUpdate: The standardized order update.
        """
        pass

    @abstractmethod
    def convert_exchange_order_type_to_order_type(self, data: str) -> EOrderType:
        """
        Converts exchange-specific order type to standardized EOrderType enum.

        Args:
            data (str): The exchange-specific order type.

        Returns:
            EOrderType: The standardized order type enum.
        """
        pass

    @abstractmethod
    def convert_exchange_order_status_to_order_status(self, data: str) -> EOrderStatus:
        """
        Converts exchange-specific order status string to standardized EOrderStatus enum.

        Args:
            data (str): The exchange specific order status.

        Returns:
            EOrderStatus: The standardized order status enum.
        """
        pass

    @abstractmethod
    def convert_exchange_order_category_to_order_category(
        self, data: str
    ) -> EOrderCategory:
        """
        Converts exchange-specific order category string to standardized EOrderCategory enum.

        Args:
            data (str): The exchange-specific order category.

        Returns:
            EOrderCategory: The standardized order category enum.
        """
        pass

    @abstractmethod
    def convert_exchange_tif_to_tif(self, data: str) -> ETimeInForce:
        """
        Converts exchange-specific time in force string to standardized ETimeInForce enum.

        Args:
            data (str): The exchange-specific time in force.

        Returns:
            ETimeInForce: The standardized time in force enum.
        """
        pass

    @abstractmethod
    def convert_exchange_side_to_side(self, data: str) -> ESide:
        """
        Converts exchange-specific order side to standardized ESide enum.

        Args:
            data (str): The exchange-specific order side.

        Returns:
            ESide: The standardized order side enum.
        """
        pass
