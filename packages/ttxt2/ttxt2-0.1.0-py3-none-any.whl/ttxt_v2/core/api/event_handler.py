from abc import ABC, abstractmethod

from ttxt_v2.core.api.connector_status import ConnectorStatus
from ttxt_v2.core.api.order_ack import OrderAck
from ttxt_v2.core.api.order_update import OrderUpdate
from ttxt_v2.core.api.wallet import Wallet

from .event import Event, Kline, MarketTrades, Orderbook


class IEventHandler(ABC):
    """
    Interface for handling different types of events.

    This abstract base class defines the methods that must be implemented
    by any concrete event handler class. It uses the `abc` module to enforce
    the implementation of the `on_orderbook`, `on_market_trades`, and `on_kline` methods.
    """

    @abstractmethod
    def on_orderbook(self, ob_ev: Event[Orderbook]):
        """
        Handle an orderbook event.

        This method should be implemented by subclasses to provide the
        specific logic for handling an orderbook event.

        Args:
            ob_ev (Event[Orderbook]): The orderbook event to handle.
        """
        pass

    @abstractmethod
    def on_market_trades(self, mt_ev: Event[MarketTrades]):
        """
        Handle a market trades event.

        This method should be implemented by subclasses to provide the
        specific logic for handling a market trades event.

        Args:
            mt_ev (Event[MarketTrades]): The market trades event to handle.
        """
        pass

    @abstractmethod
    def on_kline(self, kl_ev: Event[Kline]):
        """
        Handle a kline event.

        This method should be implemented by subclasses to provide the
        specific logic for handling a kline event.

        Args:
            kl_ev (Event[Kline]): The kline event to handle.
        """
        pass

    @abstractmethod
    def on_order_ack(self, order_ack_ev: Event[OrderAck]):
        """
        Handle a order acknowledgment event.

        This method should be implemented by subclasses to provide the
        specific logic for handling a order_ack.

        Args:
            order_ack_ev (Event[OrderAck]): The acknowledgement event to handle.
        """
        pass

    @abstractmethod
    def on_order_update(self, order_update_ev: Event[OrderUpdate]):
        """
        Handle an order update event from the exchange.

        This method should be implemented by subclasses to provide the
        specific logic for handling a order updates.

        Args:
            order_update_ev (Event[OrderUpdate]): The payload with the updated order
        """
        pass

    @abstractmethod
    def on_wallet_update(self, wallet_update_ev: Event[Wallet]):
        """
        Handle an wallet update event from the exchange.

        This method should be implemented by subclasses to provide the
        specific logic for handling a wallet update

        Args:
            wallet_update_ev (Event[WalletUpdate]): The payload with the wallet update event.
        """
        pass

    @abstractmethod
    def on_connector_status(self, status: Event[ConnectorStatus]):
        """
        Handle incoming change of status from the connector.

        This method should be implemented by subclasses to provide the
        specific logic for handling a connector status changes

        Args:
            status (Event[ConnectorStatus]): The new connector status
        """
        pass
