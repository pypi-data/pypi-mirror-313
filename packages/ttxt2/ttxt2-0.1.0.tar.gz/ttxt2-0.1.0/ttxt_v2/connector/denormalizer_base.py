from abc import ABC, abstractmethod

from ttxt_v2.core.api import (
    AmendOrder,
    CancelOrder,
    CreateOrder,
    EOrderCategory,
    EOrderType,
    ESide,
    ETimeInForce,
)
from ttxt_v2.core.web.data_types import WSRequest


class DenormalizerBase(ABC):
    """
    Abstract base class for denormalizing standardized types into WSRequest
    for trade websocket to send to exchanges.

    Methods:
        convert_create_order_to_ws_request(self,create_order: CreateOrder) -> WSRequest:
            Convert standardized CreateOrder object into an exchange specific
            websocket request for order creation.

        convert_cancel_order_to_ws_request(self,cancel_order: CancelOrder) -> WSRequest:
            Convert standardized CancelOrder object into an exchange specific
            websocket request for order cancellation.

        convert_cancel_all_orders_to_ws_request(self,cancel_all_orders: CancelAllOrders) -> WSRequest:
            Convert standardized CancelAllOrders object into an exchange specific
            websocket request for cancellation of all orders (either all or all for a trading pair)

        convert_amend_order_to_ws_request(self,amend_order: AmendOrder) -> WSRequest:
            Convert standardized AmendOrder object into an exchange specific
            websocket request for updating exiting order.
    """

    @abstractmethod
    def convert_create_order_to_ws_request(
        self, create_order: CreateOrder
    ) -> WSRequest:
        """
        Converts CreateOrder object into exchange specific websocket request.

        Args:
            create_order (CreateOrder): The CreateOrder event sent by the user.

        Returns:
            WSRequest: the exchange specific web socket request
        """
        pass

    @abstractmethod
    def convert_cancel_order_to_ws_request(
        self, cancel_order: CancelOrder
    ) -> WSRequest:
        """
        Converts CancelOrder object into exchange specific websocket request.

        Args:
            cancel_order (CancelOrder): The CancelOrder event sent by the user.

        Returns:
            WSRequest: the exchange specific web socket request
        """
        pass

    @abstractmethod
    def convert_amend_order_to_ws_request(self, amend_order: AmendOrder) -> WSRequest:
        """
        Converts AmendOrder object into exchange specific websocket request.

        Args:
            amend_order (AmendOrder): The AmendOrder event sent by the user.

        Returns:
            WSRequest: the exchange specific web socket request
        """
        pass

    @abstractmethod
    def convert_order_type_to_exchange_order_type(self, order_type: EOrderType) -> str:
        pass

    @abstractmethod
    def convert_tif_to_exchange_tif(self, tif: ETimeInForce) -> str:
        pass

    @abstractmethod
    def convert_order_category_to_exchange_category(
        self, order_category: EOrderCategory
    ) -> str:
        pass

    @abstractmethod
    def convert_order_side_to_exchange_side(self, side: ESide) -> str:
        pass
