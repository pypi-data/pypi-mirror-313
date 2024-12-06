import asyncio
import time
from typing import Any, Dict, List, Optional, Union, cast

from ttxt_v2.connector import ConnectorBase, ConnectorConfig
from ttxt_v2.connector.connector_urls import ConnectorURL
from ttxt_v2.core.api import (
    AmendOrder,
    BaseEvent,
    CancelOrder,
    CoinBalance,
    CreateOrder,
    EAccountType,
    EAckType,
    EOrderCategory,
    EOrderStatus,
    EOrderType,
    ESide,
    ETimeInForce,
    EUpdateType,
    Event,
    EventType,
    InstrumentInfo,
    IQueue,
    Kline,
    MarketTrades,
    MarketTradesData,
    MessageHeader,
    OrderAck,
    Orderbook,
    OrderbookEntry,
    OrderUpdate,
    OrderUpdateItem,
    TradingPair,
    Wallet,
)
from ttxt_v2.core.api.enums import EWebSocketType
from ttxt_v2.core.web import (
    BaseAuth,
    WebAssitantFactory,
    WSJSONRequest,
    WSRequest,
    WSResponse,
)
from ttxt_v2.core.web.data_types import RESTMethod
from ttxt_v2.utils.async_websocket_retrier import websocket_reconnect
from ttxt_v2.utils.logger import logger
from ttxt_v2.utils.math_utils import get_decimal_places

from .mexc_auth import MexcAuth


class Mexc(ConnectorBase):
    """
    Connector class for Mexc exchange.
    """

    CREATE_OP = ""
    CANCEL_OP = ""
    AUTH_OP = ""
    PONG_OP = "PONG"
    SUBSCRIBE_OP = "SUBSCRIPTION"
    ORDER_CHAN = "spot@private.orders.v3.api"
    WALLET_CHAN = "spot@private.account.v3.api"

    def __init__(
        self,
        config: Optional[ConnectorConfig] = None,
        public_queue: Optional[IQueue] = None,
        signal_queue: Optional[IQueue] = None,
        api_key: str = "",
        api_secret: str = "",
    ):
        super().__init__(config, public_queue, signal_queue, api_key, api_secret)
        self._listen_key = None
        self._keep_alive_task = None

    def is_ws_trading_enabled(self) -> bool:
        return False

    async def _subscribe_to_public_stream(self):
        """
        Subscribes to the public WebSocket stream by sending subscription requests.
        """
        subscription_reqs = self._create_public_ws_subscription_request()
        assert self._public_ws is not None, "Public ws cannot be None"
        for req in subscription_reqs:
            await self._public_ws.send(req)

    async def _subscribe_to_trade_stream(self):
        pass

    async def _subscribe_to_private_stream(self):
        """
        Subscribes to the private WebSocket stream.
        """
        assert (
            self._private_ws is not None and self._private_ws.connected
        ), "Private WS cannot be None and should be connected"

        subscription_request = WSJSONRequest(
            payload={
                "method": "SUBSCRIPTION",
                "params": [
                    "spot@private.account.v3.api",
                    "spot@private.orders.v3.api",
                ],
            }
        )
        logger.debug(
            f"Sending subscription request for private streams: {subscription_request}"
        )
        await self._private_ws.send(subscription_request)

    async def _process_market_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Processes market data received from the WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        try:
            data = response.data
            if data is None:
                return None
            channel = data.get("c", "")
            if not channel:
                return None
            if "spot@public.limit.depth.v3.api" in channel:
                # Orderbook data
                normalized_orderbook = self.convert_exchange_orderbook_to_orderbook(
                    data
                )
                self._update_orderbooks(normalized_orderbook)
                event = BaseEvent(
                    event_type=EventType.OB_EVENT,
                    payload=Event[Orderbook](
                        header=MessageHeader(
                            exchange=self._config.exchange,
                            timestamp=normalized_orderbook.timestamp,
                        ),
                        data=normalized_orderbook,
                    ),
                )
                return event
            elif "spot@public.kline.v3.api" in channel:
                # Kline data
                normalized_kline = self.convert_exchange_klines_to_klines(data)
                event = BaseEvent(
                    event_type=EventType.KL_EVENT,
                    payload=Event[Kline](
                        header=MessageHeader(
                            exchange=self._config.exchange,
                            timestamp=normalized_kline.timestamp,
                        ),
                        data=normalized_kline,
                    ),
                )
                return event
            elif "spot@public.deals.v3.api" in channel:
                # Trade data
                normalized_trades = self.convert_exchange_trades_to_trades(data)
                event = BaseEvent(
                    event_type=EventType.MT_EVENT,
                    payload=Event[MarketTrades](
                        header=MessageHeader(
                            exchange=self._config.exchange,
                            timestamp=int(time.time() * 1000),
                        ),
                        data=normalized_trades,
                    ),
                )
                return event
            else:
                logger.warning(f"Unknown message channel: {channel}")
                return None
        except Exception as e:
            logger.error(
                f"Error processing market data response: {str(e)}. WSResponse: {str(response.data)}"
            )
            return None

    def _process_trade_data(self, response: WSResponse) -> Optional[BaseEvent]:
        assert self._config is not None, "Config cannot be None"
        pass

    def _process_private_data(self, response: WSResponse) -> Optional[List[BaseEvent]]:
        """
        Processes private data received from the WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        try:
            data = response.data
            if data is None:
                return None

            channel = data.get("c", "")
            if not channel:
                msg = data.get("msg", "")
                if msg == "PONG":
                    logger.warning(f"Received pong: {data}")
                else:
                    logger.warning(f"Unknown message to process: {data}. Skipping...")
                return None

            if channel == self.WALLET_CHAN:
                wallet_event = self.convert_exchange_wallet_update_to_wallet(data)
                return [
                    BaseEvent(
                        event_type=EventType.WALLET_UPDATE_EVENT,
                        payload=Event[Wallet](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=wallet_event.timestamp,
                            ),
                            data=wallet_event,
                        ),
                    )
                ]
            elif channel == self.ORDER_CHAN:
                order_update_event = self.convert_exchange_order_update_to_order_update(
                    data
                )
                return [
                    BaseEvent(
                        event_type=EventType.ORDER_UPDATE_EVENT,
                        payload=Event[OrderUpdate](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=order_update_event.timestamp,
                            ),
                            data=order_update_event,
                        ),
                    )
                ]
            else:
                logger.warning(f"Unknown private channel: {channel}")
                return None
        except Exception as e:
            logger.error(f"Error processing private response: {str(e)}")
            return None

    def _process_signal_event(self, event: BaseEvent) -> List[WSRequest]:
        """No need to implement since exchange does not support WS trading"""
        return [WSJSONRequest(payload={})]

    async def _process_http_signals(self, event: BaseEvent) -> Optional[BaseEvent]:
        if event.event_type == EventType.CREATE_ORDER_EVENT:
            # Process create order
            return await self._create_order_signal(
                cast(CreateOrder, event.payload.data)
            )
        elif event.event_type == EventType.CANCEL_ORDER_EVENT:
            # Process cancel order
            return await self._cancel_order_signal(
                cast(CancelOrder, event.payload.data)
            )
        else:
            logger.warning(f"Received unsupported event type: {event.event_type}")
            return None

    async def _create_order_signal(
        self, create_order: CreateOrder
    ) -> Optional[BaseEvent]:
        try:
            assert self._config is not None, "Config cannot be None"
            # Build the request data
            data = {
                "symbol": self._trading_pairs_to_symbols_table[
                    create_order.trading_pair
                ],
                "side": self.convert_order_side_to_exchange_side(create_order.side),
                "type": self.convert_order_type_to_exchange_order_type(
                    create_order.order_type
                ),
            }

            # Add additional parameters based on order type
            if create_order.order_type == EOrderType.LIMIT:
                data["quantity"] = str(create_order.qty)
                if create_order.price is not None:
                    data["price"] = str(create_order.price)
                else:
                    raise ValueError("Price must be specified for LIMIT orders.")
            elif create_order.order_type == EOrderType.MARKET:
                if create_order.qty:
                    data["quantity"] = str(create_order.qty)
                else:
                    raise ValueError(
                        "Quantity or quoteOrderQty must be specified for MARKET orders."
                    )

            if create_order.client_order_id:
                data["newClientOrderId"] = create_order.client_order_id

            # Send the API request
            response = await self.api_request(
                path_url="/api/v3/order",
                method=RESTMethod.POST,
                data=data,
                is_auth_required=True,
            )

            # Process the response and create OrderAck
            order_ack = self.convert_create_order_response_to_order_ack(response)

            # Return the OrderAck event
            return BaseEvent(
                event_type=EventType.ORDER_ACK_EVENT,
                payload=Event[OrderAck](
                    header=MessageHeader(
                        exchange=self._config.exchange, timestamp=order_ack.timestamp
                    ),
                    data=order_ack,
                ),
            )
        except Exception as e:
            logger.error(f"Error processing create order signal: {str(e)}")
            return None

    async def _cancel_order_signal(
        self, cancel_order: CancelOrder
    ) -> Optional[BaseEvent]:
        """
        Processes a cancel order event, sends the HTTP request to cancel the order,
        and returns an OrderAck event.
        """
        try:
            assert self._config is not None, "Config cannot be None"
            # Build the request parameters
            data = {
                "symbol": self._trading_pairs_to_symbols_table[
                    cancel_order.trading_pair
                ]
            }

            # Either orderId or origClientOrderId must be sent.
            if cancel_order.client_order_id:
                data["origClientOrderId"] = cancel_order.client_order_id
            else:
                raise ValueError("Either client_order_id or orderId must be specified.")

            # Send the API request
            response = await self.api_request(
                path_url="/api/v3/order",
                method=RESTMethod.DELETE,
                data=data,
                is_auth_required=True,
            )

            # Process the response and create OrderAck
            order_ack = self.convert_cancel_order_response_to_order_ack(response)

            # Return the OrderAck event
            return BaseEvent(
                event_type=EventType.ORDER_ACK_EVENT,
                payload=Event[OrderAck](
                    header=MessageHeader(
                        exchange=self._config.exchange, timestamp=order_ack.timestamp
                    ),
                    data=order_ack,
                ),
            )
        except Exception as e:
            logger.error(f"Error processing cancel order signal: {str(e)}")
            return None

    @property
    def authenticator(self) -> BaseAuth:
        """
        Returns the authenticator for the connector.
        """
        assert self._api_key is not None, "API KEY cannot be None for auth"
        assert self._api_secret is not None, "API_SECRET cannot be None for auth"
        return MexcAuth(api_key=self._api_key, api_secret=self._api_secret)

    def _create_web_assistant_factory(self) -> WebAssitantFactory:
        """
        Creates a web assistant factory.
        """
        return WebAssitantFactory(auth=self._auth)

    def _get_connector_urls(self) -> ConnectorURL:
        return ConnectorURL(
            PUBLIC_SPOT="wss://wbs.mexc.com/ws",
            PUBLIC_LINEAR="",
            PUBLIC_INVERSE="",
            TRADE="",
            BASE="https://api.mexc.com",
            PRIVATE="wss://wbs.mexc.com/ws",  # Same base URL for private WS
        )

    async def pinger(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            assert self._public_ws is not None, "Public WS cannot be none"
            while self._public_ws.connected:
                req = WSJSONRequest(payload={"method": "ping"})
                logger.debug("Sending public_ws ping")
                await self._public_ws.send(req)
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            logger.error("Stopping Mexc public WS ping coroutine")

    async def pinger_private(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            assert self._private_ws is not None, "Private WS cannot be none"
            while self._private_ws.connected:
                req = WSJSONRequest(payload={"method": "ping"})
                logger.debug("Sending private_ws ping")
                await self._private_ws.send(req)
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            logger.error("Stopping Mexc private WS ping coroutine")

    def _create_public_ws_subscription_request(self) -> List[WSJSONRequest]:
        """
        Creates subscription requests for the public WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        ws_reqs = []
        trading_pairs_table = self._trading_pairs_to_symbols_table

        # Subscription parameters for each stream
        params = []

        # Orderbook subscriptions
        if self._config.ob_config is not None:
            ob_config = self._config.ob_config
            for ticker in ob_config.tickers:
                symbol = trading_pairs_table[ticker]
                depth = ob_config.depth
                # Ensure depth is one of the valid levels (5, 10, or 20)
                if depth not in [5, 10, 20]:
                    depth = 20  # Default to 20
                # Orderbook stream
                params.append(f"spot@public.limit.depth.v3.api@{symbol}@{depth}")

        # Market trades subscriptions
        if self._config.mt_config is not None:
            mt_config = self._config.mt_config
            for ticker in mt_config.tickers:
                symbol = trading_pairs_table[ticker]
                # Trade stream
                params.append(f"spot@public.deals.v3.api@{symbol}")

        # Kline subscriptions
        if self._config.kl_config is not None:
            kl_config = self._config.kl_config
            for ticker in kl_config.tickers:
                symbol = trading_pairs_table[ticker]
                params.append(f"spot@public.kline.v3.api@{symbol}@Min1")

        if params:
            payload = {"method": self.SUBSCRIBE_OP, "params": params}
            ws_reqs.append(WSJSONRequest(payload=payload))

        return ws_reqs

    def _gen_symbols_table(self) -> Dict[str, TradingPair]:
        """
        Generates a mapping from exchange symbols to TradingPair instances.
        """
        assert self._config is not None, "Config cannot be None"
        symbols_table = {}
        trading_pairs = []
        if self._config.ob_config is not None:
            trading_pairs.extend(self._config.ob_config.tickers)
        if self._config.mt_config is not None:
            trading_pairs.extend(self._config.mt_config.tickers)
        if self._config.kl_config is not None:
            trading_pairs.extend(self._config.kl_config.tickers)
        trading_pairs = list(set(trading_pairs))  # Remove duplicates
        for trading_pair in trading_pairs:
            base_asset = trading_pair.base
            quote_asset = trading_pair.quote
            symbol = f"{base_asset}{quote_asset}".upper()
            symbols_table[symbol] = trading_pair
        return symbols_table

    def _gen_trading_pairs_table(self) -> Dict[TradingPair, str]:
        """
        Generates a mapping from TradingPair instances to exchange symbols.
        """
        assert self._config is not None, "Config cannot be None"
        trading_pairs_table = {}
        trading_pairs = []
        if self._config.ob_config is not None:
            trading_pairs.extend(self._config.ob_config.tickers)
        if self._config.mt_config is not None:
            trading_pairs.extend(self._config.mt_config.tickers)
        if self._config.kl_config is not None:
            trading_pairs.extend(self._config.kl_config.tickers)
        trading_pairs = list(set(trading_pairs))  # Remove duplicates
        for trading_pair in trading_pairs:
            base_asset = trading_pair.base
            quote_asset = trading_pair.quote
            symbol = f"{base_asset}{quote_asset}".upper()
            trading_pairs_table[trading_pair] = symbol
        return trading_pairs_table

    """
    REST API
    """

    async def get_server_time_ms(self) -> int:
        path_url = "/api/v3/time"
        response = await self.api_request(path_url=path_url)
        return response.get("serverTime", int(time.time() * 1000))

    async def fetch_wallet_balance(
        self, account_type: EAccountType = EAccountType.UNIFIED
    ) -> Wallet:
        """
        Fetches wallet balances from MEXC for the user.
        """
        path_url = "/api/v3/account"
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.GET,
            is_auth_required=True,
        )
        timestamp = int(time.time() * 1000)
        wallet = {}
        balances = response.get("balances", [])
        for balance in balances:
            asset = balance["asset"]
            free = float(balance["free"])
            locked = float(balance["locked"])
            total = free + locked
            coin_balance = CoinBalance(
                total=total,
                available=free,
                realised_pnl=0.0,
                unrealised_pnl=0.0,
            )
            wallet[asset] = coin_balance
        return Wallet(wallet=wallet, timestamp=timestamp)

    async def fetch_instrument_info(
        self, pair: TradingPair, category: EOrderCategory = EOrderCategory.SPOT
    ) -> List[InstrumentInfo]:
        """
        Fetches instrument information for a given trading pair.
        """
        symbol = f"{pair.base.upper()}{pair.quote.upper()}"
        path_url = "/api/v3/exchangeInfo"
        params = {
            "symbol": symbol.upper(),
        }
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.GET,
            params=params,
            headers={"Content-Type": "application/json"},
            is_auth_required=False,
        )
        symbols_info = response.get("symbols", [])
        if not symbols_info:
            raise Exception(f"No instrument info found for symbol {symbol}")
        symbol_info = symbols_info[0]  # Assuming only one symbol returned
        trade_on = symbol_info["status"] == "ENABLED"
        filters = symbol_info.get("filters", [])
        max_o_q = 0.0
        min_o_q = 0.0
        tick_s = 0.0
        min_o_a = 0.0
        for f in filters:
            if f["filterType"] == "LOT_SIZE":
                min_o_q = float(f["minQty"])
                max_o_q = float(f["maxQty"])
            elif f["filterType"] == "PRICE_FILTER":
                tick_s = float(f["tickSize"])
            elif f["filterType"] == "MIN_NOTIONAL":
                min_o_a = float(f["minNotional"])

        instrument_info = InstrumentInfo(
            pair=pair,
            tradebale=trade_on,
            base_precision=int(symbol_info["baseAssetPrecision"]),
            quote_precision=int(symbol_info.get("quotePrecision", "0")),
            qty_precision=get_decimal_places(symbol_info.get("baseSizePrecision", "0")),
            min_order_qty=min_o_q,
            max_order_qty=max_o_q,
            tick_size=tick_s,
            min_order_amt=min_o_a,
        )
        return [instrument_info]

    async def cancel_all_orders(
        self,
        order_category: EOrderCategory = EOrderCategory.SPOT,
        symbol: Optional[TradingPair] = None,
    ) -> Dict[str, Any]:
        """
        Cancels all open orders for the specified category and symbol.
        """
        path_url = "/api/v3/openOrders"
        data = {
            "timestamp": int(time.time() * 1000),
        }
        if symbol:
            data["symbol"] = f"{symbol.base.upper()}{symbol.quote.upper()}"
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.DELETE,
            data=data,
            is_auth_required=True,
        )
        return response

    async def fetch_klines(
        self,
        symbol: TradingPair,
        interval: str,
        start_time: str,
        end_time: str,
        category: EOrderCategory = EOrderCategory.SPOT,
        limit: int = 1000,
    ) -> List[Kline]:
        """
        Fetch Kline data from MEXC for a given symbol, interval, and time range.
        """
        return []

    """
    Normalizer API
    """

    def convert_exchange_orderbook_to_orderbook(self, data: Dict) -> Orderbook:
        """
        Converts exchange-specific orderbook data to a standardized Orderbook instance.
        """
        symbol = data.get("s", "")
        event_time = data.get("t", int(time.time() * 1000))
        data_content = data.get("d", {})
        asks = data_content.get("asks", [])
        bids = data_content.get("bids", [])
        # Build bids and asks lists
        bid_entries = [
            OrderbookEntry(price=float(bid["p"]), qty=float(bid["v"])) for bid in bids
        ]
        ask_entries = [
            OrderbookEntry(price=float(ask["p"]), qty=float(ask["v"])) for ask in asks
        ]
        trading_pair = self._symbols_to_trading_pairs_table[symbol]
        return Orderbook(
            update_type=EUpdateType.SNAPSHOT,  # Since it's partial book depth
            trading_pair=trading_pair,
            bids=bid_entries,
            asks=ask_entries,
            timestamp=event_time,
            seq=int(data_content.get("r", 0)),
        )

    def convert_exchange_klines_to_klines(self, data: Dict) -> Kline:
        """
        Converts exchange-specific kline data to a standardized Kline instance.
        """
        data_content = data.get("d", {}).get("k", {})
        symbol = data.get("s", "")
        trading_pair = self._symbols_to_trading_pairs_table[symbol]
        kline = Kline(
            trading_pair=trading_pair,
            open=float(data_content.get("o", 0)),
            close=float(data_content.get("c", 0)),
            high=float(data_content.get("h", 0)),
            low=float(data_content.get("l", 0)),
            volume=float(data_content.get("v", 0)),
            start=int(data_content.get("t", 0)),
            timestamp=int(data.get("t", int(time.time() * 1000))),
            confirm=False,  # does not send this data
        )
        return kline

    def convert_exchange_trades_to_trades(self, data: Dict) -> MarketTrades:
        """
        Converts exchange-specific trade data to a standardized MarketTrades instance.
        """
        symbol = data.get("s", "")
        trading_pair = self._symbols_to_trading_pairs_table[symbol]
        deals = data.get("d", {}).get("deals", [])
        trades_data = []
        for deal in deals:
            trade_type = deal.get("S")
            price = deal.get("p")
            quantity = deal.get("v")
            side = ESide.BUY if trade_type == 1 else ESide.SELL
            trades_data.append(
                MarketTradesData(price=float(price), qty=float(quantity), side=side)
            )
        return MarketTrades(trading_pair=trading_pair, trades=trades_data)

    def convert_create_order_response_to_order_ack(
        self, data: Dict[str, Any]
    ) -> OrderAck:
        """
        Converts the exchange's create order response to an OrderAck.
        """
        order_ack = OrderAck(
            order_id=data.get("clientOrderId", ""),
            ack_type=EAckType.CREATE,
            timestamp=data.get("transactTime", int(time.time() * 1000)),
        )
        return order_ack

    def convert_cancel_order_response_to_order_ack(
        self, data: Dict[str, Any]
    ) -> OrderAck:
        """
        Converts the exchange's cancel order response to an OrderAck.
        """
        order_ack = OrderAck(
            order_id=data.get("origClientOrderId", ""),
            ack_type=EAckType.CANCEL,
            timestamp=int(time.time() * 1000),  # Use current timestamp
        )
        return order_ack

    def convert_exchange_wallet_update_to_wallet(self, data: Dict) -> Wallet:
        """
        Converts exchange-specific wallet update data to a standardized Wallet instance.
        """
        account_data = data.get("d", {})
        asset = account_data.get("a")
        change_time = int(account_data.get("c", int(time.time() * 1000)))
        free_balance = float(account_data.get("f", "0"))
        frozen_balance = float(account_data.get("l", "0"))
        total_balance = free_balance + frozen_balance

        coin_balance = CoinBalance(
            total=total_balance,
            available=free_balance,
            realised_pnl=0.0,
            unrealised_pnl=0.0,
        )

        wallet = Wallet(wallet={asset: coin_balance}, timestamp=change_time)
        return wallet

    def convert_exchange_order_update_to_order_update(self, data: Dict) -> OrderUpdate:
        """
        Converts exchange-specific order update data to a standardized OrderUpdate instance.
        """
        d = data.get("d", {})
        event_time = int(data.get("t", int(time.time() * 1000)))
        symbol = data.get("s", "")

        order_type_code = int(d.get("o", 0))
        order_type_enum = self.convert_exchange_order_type_to_order_type(
            str(order_type_code)
        )
        tif_enum = self.convert_exchange_tif_to_tif(str(order_type_code))

        side_code = int(d.get("S", 0))
        side_enum = self.convert_exchange_side_to_side(str(side_code))

        status = d.get("s")
        status_enum = self._mexc_order_status(status)

        order_id = d.get("i", "")
        client_order_id = d.get("c", "")

        price = float(d.get("p", 0))
        quantity = float(d.get("v", 0))

        cum_exec_qty = float(d.get("cv", 0)) if "cv" in d else 0.0
        cum_exec_value = float(d.get("ca", 0)) if "ca" in d else 0.0

        create_time = int(d.get("O", int(time.time() * 1000)))
        update_time = event_time

        order_update_item = OrderUpdateItem(
            symbol=self._symbols_to_trading_pairs_table[symbol],
            order_id=order_id,
            side=side_enum,
            order_type=order_type_enum,
            price=price,
            qty=quantity,
            tif=tif_enum,
            order_status=status_enum,
            custom_order_id=client_order_id,
            cum_exec_qty=cum_exec_qty,
            cum_exec_value=cum_exec_value,
            cum_exec_fee=0.0,  # Not provided
            closed_pnl=0.0,  # Not provided
            take_profit=0.0,  # Not provided
            stop_loss=0.0,  # Not provided
            tp_limit_price=0.0,  # Not provided
            sl_limit_price=0.0,  # Not provided
            create_time=create_time,
            update_time=update_time,
        )

        order_update = OrderUpdate(timestamp=event_time, updates=[order_update_item])
        return order_update

    def convert_exchange_order_type_to_order_type(self, data: str) -> EOrderType:
        """
        Converts exchange-specific order type code to EOrderType.
        """
        order_type_mapping = {
            "1": EOrderType.LIMIT,
            "5": EOrderType.MARKET,
            # Add other mappings if necessary
        }
        return order_type_mapping.get(data.upper(), EOrderType.UNKNOWN)

    def convert_exchange_side_to_side(self, data: str) -> ESide:
        """
        Converts exchange-specific side code to ESide.
        """
        side_mapping = {
            "1": ESide.BUY,
            "2": ESide.SELL,
        }
        return side_mapping.get(data, ESide.SELL)

    def convert_exchange_tif_to_tif(self, data: str) -> ETimeInForce:
        tif_mapping = {
            "3": ETimeInForce.IOC,
            "4": ETimeInForce.FOK,
        }
        return tif_mapping.get(data, ETimeInForce.GTC)

    def _mexc_order_status(self, data: Union[int, str]) -> EOrderStatus:
        """
        Converts exchange-specific order status to EOrderStatus.
        """
        status_mapping = {
            "NEW": EOrderStatus.NEW,
            "PARTIALLY_FILLED": EOrderStatus.PARTIALLY_FILLED,
            "FILLED": EOrderStatus.FILLED,
            "CANCELED": EOrderStatus.CANCELLED,
            "REJECTED": EOrderStatus.REJECTED,
        }

        status_mapping_int = {
            1: EOrderStatus.NEW,
            3: EOrderStatus.PARTIALLY_FILLED,
            2: EOrderStatus.FILLED,
            4: EOrderStatus.CANCELLED,
        }
        if isinstance(data, str):
            return status_mapping.get(data.upper(), EOrderStatus.UNKNOWN)
        else:
            return status_mapping_int.get(data, EOrderStatus.UNKNOWN)

    """
    Denormalizer API
    """

    def convert_order_type_to_exchange_order_type(self, order_type: EOrderType) -> str:
        order_type_mapping = {
            EOrderType.LIMIT: "LIMIT",
            EOrderType.MARKET: "MARKET",
            # Add other mappings if necessary
        }
        return order_type_mapping.get(order_type, "LIMIT")

    def convert_tif_to_exchange_tif(self, tif: ETimeInForce) -> str:
        tif_mapping = {
            ETimeInForce.GTC: "GTC",
            ETimeInForce.IOC: "IOC",
            ETimeInForce.FOK: "FOK",
        }
        return tif_mapping.get(tif, "GTC")

    def convert_order_side_to_exchange_side(self, side: ESide) -> str:
        side_mapping = {
            ESide.BUY: "BUY",
            ESide.SELL: "SELL",
        }
        return side_mapping.get(side, "BUY")

    @websocket_reconnect(EWebSocketType.PRIVATE)
    async def _private_stream(self):
        """
        Listens to the private data stream and processes events.
        """
        assert (
            self._public_queue_stream is not None
        ), "Cannot listen to private stream with None public queue"
        self._private_ws = await self._web_assistant_factory.get_ws_assistant()
        self._listen_key = await self._get_listen_key()
        ws_url = f"{self._urls.PRIVATE}?listenKey={self._listen_key}"
        await self._private_ws.connect(ws_url)
        await self._on_websocket_connected(EWebSocketType.PRIVATE)
        await self._subscribe_to_private_stream()
        pinger = asyncio.create_task(self.pinger_private())
        keep_alive_task = asyncio.create_task(self._keep_alive_listen_key())
        try:
            while True:
                resp = await self._private_ws.receive()
                if resp is not None and resp.data is not None:
                    events = self._process_private_data(resp)
                    if events is not None and len(events) > 0:
                        for event in events:
                            await self._public_queue_stream.publish(event)
        except asyncio.CancelledError:
            logger.warning("Cancelling private stream")
            raise
        finally:
            pinger.cancel()
            keep_alive_task.cancel()
            await pinger
            await keep_alive_task

    async def _get_listen_key(self) -> str:
        """
        Obtains a listenKey by making a POST request to /api/v3/userDataStream.
        """
        path_url = "/api/v3/userDataStream"
        headers = {"Content-Type": "application/json"}
        logger.debug("Requesting new listenKey from MEXC")
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.POST,
            headers=headers,
            is_auth_required=True,
        )
        listen_key = response.get("listenKey")
        if not listen_key:
            raise RuntimeError("Failed to obtain listenKey from MEXC")
        logger.debug(f"Obtained listenKey: {listen_key}")
        return listen_key

    async def _keep_alive_listen_key(self):
        """
        Coroutine that keeps the listenKey alive by sending a PUT request every 30 minutes.
        """
        try:
            while True:
                await asyncio.sleep(30 * 60)  # Sleep for 30 minutes
                await self._extend_listen_key()
        except asyncio.CancelledError:
            logger.debug("Keep-alive listenKey coroutine has been cancelled.")
        except Exception as e:
            logger.error(f"Error in keep-alive listenKey coroutine: {str(e)}")

    async def _extend_listen_key(self):
        """
        Sends a PUT request to extend the listenKey's validity.
        """
        path_url = "/api/v3/userDataStream"
        headers = {"Content-Type": "application/json"}
        params = {"listenKey": self._listen_key}
        logger.debug(f"Extending listenKey: {self._listen_key}")
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.PUT,
            params=params,
            headers=headers,
            is_auth_required=True,
        )
        success_key = response.get("listenKey")
        if success_key != self._listen_key:
            logger.warning("ListenKey extension failed or returned a different key.")

    def convert_amend_order_to_ws_request(self, amend_order: AmendOrder) -> WSRequest:
        """Not needed since we do not trade over websockets"""
        return WSJSONRequest(payload={})

    def convert_create_order_to_ws_request(
        self, create_order: CreateOrder
    ) -> WSRequest:
        """Not needed since we do not trade over websockets"""
        return WSJSONRequest(payload={})

    def convert_cancel_order_to_ws_request(
        self, cancel_order: CancelOrder
    ) -> WSRequest:
        """Not needed since we do not trade over websockets"""
        return WSJSONRequest(payload={})

    def convert_exchange_order_ack_to_order_ack(self, data: dict) -> OrderAck:
        return NotImplemented

    def convert_exchange_order_category_to_order_category(
        self, data: str
    ) -> EOrderCategory:
        return NotImplemented

    def convert_exchange_order_status_to_order_status(self, data: str) -> EOrderStatus:
        mapping = {
            "partially_filled": EOrderStatus.PARTIALLY_FILLED,
            "filled": EOrderStatus.FILLED,
            "cancelled": EOrderStatus.CANCELLED,
            "live": EOrderStatus.NEW,
        }
        return mapping.get(data, EOrderStatus.UNKNOWN)

    def convert_order_category_to_exchange_category(
        self, order_category: EOrderCategory
    ) -> str:
        """Not needed for now for bitget"""
        return NotImplemented
