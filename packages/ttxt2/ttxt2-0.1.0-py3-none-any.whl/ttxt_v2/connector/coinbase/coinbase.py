import asyncio
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, cast

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
from ttxt_v2.core.web import (
    BaseAuth,
    WebAssitantFactory,
    WSJSONRequest,
    WSRequest,
    WSResponse,
)
from ttxt_v2.core.web.data_types import RESTMethod
from ttxt_v2.utils.logger import logger
from ttxt_v2.utils.math_utils import get_decimal_places

from .coinbase_auth import CoinbaseAuth


def parse_timestamp_to_millis(timestamp_str: str) -> int:
    """
    Parses a timestamp string like '2023-02-09T20:32:50.714964855Z'
    and returns the Unix timestamp in milliseconds.
    """
    # Remove 'Z' timezone indicator and ensure UTC timezone
    if timestamp_str.endswith("Z"):
        timestamp_str = timestamp_str[:-1]
    else:
        raise ValueError("Timestamp must end with 'Z' indicating UTC timezone")

    # Parse the datetime and fractional seconds
    if "." in timestamp_str:
        datetime_part, frac_part = timestamp_str.split(".")
        frac_part = frac_part.ljust(9, "0")  # Ensure nanoseconds precision
        timestamp_format = "%Y-%m-%dT%H:%M:%S"
        dt = datetime.strptime(datetime_part, timestamp_format)
        dt = dt.replace(tzinfo=timezone.utc)
        timestamp = dt.timestamp()
        nanoseconds = int(frac_part)
        timestamp += nanoseconds / 1e9
    else:
        timestamp_format = "%Y-%m-%dT%H:%M:%S"
        dt = datetime.strptime(timestamp_str, timestamp_format)
        dt = dt.replace(tzinfo=timezone.utc)
        timestamp = dt.timestamp()

    return int(timestamp * 1000)  # Convert to milliseconds


class Coinbase(ConnectorBase):
    """
    Connector class for Coinbase exchange.
    """

    CREATE_OP = ""
    CANCEL_OP = ""
    AUTH_OP = ""
    PONG_OP = ""
    SUBSCRIBE_OP = "subscribe"
    HEARTBEAT_CHANNEL = "heartbeats"
    KLINE_CHANNEL = "candles"
    MARKET_TRADES_CHANNEL = "market_trades"
    ORDERBOOK_CHANNEL = "level2"
    USER_CHANNEL = "user"

    def __init__(
        self,
        config: Optional[ConnectorConfig] = None,
        public_queue: Optional[IQueue] = None,
        signal_queue: Optional[IQueue] = None,
        api_key: str = "",
        api_secret: str = "",
    ):
        super().__init__(config, public_queue, signal_queue, api_key, api_secret)

    def is_ws_trading_enabled(self) -> bool:
        return False  # Coinbase does not support WS trading for now

    @property
    def authenticator(self) -> BaseAuth:
        """
        Returns the authenticator for the connector.
        """
        return CoinbaseAuth(api_key=self._api_key, api_secret=self._api_secret)

    def _create_web_assistant_factory(self) -> WebAssitantFactory:
        """
        Creates a web assistant factory.
        """
        return WebAssitantFactory(auth=self._auth)

    def _get_connector_urls(self) -> ConnectorURL:
        return ConnectorURL(
            PUBLIC_SPOT="wss://advanced-trade-ws.coinbase.com",
            PUBLIC_LINEAR="",
            PUBLIC_INVERSE="",
            TRADE="",  # Coinbase does not support WS trading
            BASE="https://api.coinbase.com",
            PRIVATE="wss://advanced-trade-ws-user.coinbase.com",
        )

    async def _subscribe_to_public_stream(self):
        """
        Subscribes to the public WebSocket stream by sending subscription requests.
        """
        subscription_reqs = await self._create_public_ws_subscription_request()
        assert self._public_ws is not None, "Public ws cannot be None"
        for req in subscription_reqs:
            logger.debug(f"Public WS sub req: {req}")
            await self._public_ws.send(req)

    async def _subscribe_to_trade_stream(self):
        pass  # Not needed as we don't support WS trading

    async def _subscribe_to_private_stream(self):
        """
        Subscribes to the private WebSocket stream.
        """
        assert (
            self._private_ws is not None and self._private_ws.connected
        ), "Private WS cannot be None and should be connected"

        subscription_request = WSJSONRequest(
            payload={
                "type": self.SUBSCRIBE_OP,
                "channel": self.USER_CHANNEL,
            },
            is_auth_required=True,
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
            channel = data.get("channel", "")
            if not channel:
                return None
            if channel == "l2_data":
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
            elif channel == self.KLINE_CHANNEL:
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
            elif channel == self.MARKET_TRADES_CHANNEL:
                # Market trades data
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
            elif channel == self.HEARTBEAT_CHANNEL:
                # Heartbeats data
                # Process heartbeats if needed
                pass
            else:
                logger.warning(f"Unknown message channel: {channel}")
                return None
        except Exception as e:
            logger.error(
                f"Error processing market data response: {str(e)}. WSResponse: {str(response.data)}"
            )
            return None

    def _process_trade_data(self, response: WSResponse) -> Optional[BaseEvent]:
        pass  # Not needed as we don't support WS trading

    def _process_private_data(self, response: WSResponse) -> Optional[List[BaseEvent]]:
        """
        Processes private data received from the WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        data = response.data
        logger.debug(f"Coinbase private data: {data}")
        if data is None:
            return None
        events = data.get("events", [])
        if not events:
            return None
        event_list = []
        for event in events:
            if "orders" in event:
                # Order updates
                order_update = self.convert_exchange_order_update_to_order_update(event)
                event_list.append(
                    BaseEvent(
                        event_type=EventType.ORDER_UPDATE_EVENT,
                        payload=Event[OrderUpdate](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=int(time.time() * 1000),
                            ),
                            data=order_update,
                        ),
                    )
                )
            if "account" in event:
                # Wallet updates
                wallet_update = self.convert_exchange_wallet_update_to_wallet(event)
                event_list.append(
                    BaseEvent(
                        event_type=EventType.WALLET_UPDATE_EVENT,
                        payload=Event[Wallet](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=int(time.time() * 1000),
                            ),
                            data=wallet_update,
                        ),
                    )
                )
        return event_list

    def _process_signal_event(self, event: BaseEvent) -> List[WSRequest]:
        """No need to implement since exchange does not support WS trading"""
        return []

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
        assert self._config is not None, "Config cannot be None"

        path_url = "/api/v3/brokerage/orders"

        trading_pair = create_order.trading_pair
        trading_pairs_table = self._trading_pairs_to_symbols_table
        product_id = trading_pairs_table[trading_pair]

        side = self.convert_order_side_to_exchange_side(create_order.side)
        client_order_id = create_order.client_order_id

        order_configuration = {}
        if create_order.order_type == EOrderType.MARKET:
            # For market orders, we need to specify base_size or quote_size
            if create_order.side == ESide.BUY:
                # For BUY market orders, we can specify quote_size
                order_configuration["market_market_ioc"] = {
                    "quote_size": str(create_order.qty),
                }
            else:
                # For SELL market orders, we specify base_size
                order_configuration["market_market_ioc"] = {
                    "base_size": str(create_order.qty),
                }
        elif create_order.order_type == EOrderType.LIMIT:
            # For limit orders, we need to specify base_size and limit_price
            limit_price = str(create_order.price)
            base_size = str(create_order.qty)

            tif = create_order.tif
            if tif == ETimeInForce.GTC:
                order_configuration["limit_limit_gtc"] = {
                    "base_size": base_size,
                    "limit_price": limit_price,
                    "post_only": False,  # Set based on create_order parameters
                }
            elif tif == ETimeInForce.IOC:
                order_configuration["sor_limit_ioc"] = {
                    "base_size": base_size,
                    "limit_price": limit_price,
                }
            elif tif == ETimeInForce.FOK:
                order_configuration["limit_limit_fok"] = {
                    "base_size": base_size,
                    "limit_price": limit_price,
                }
            else:
                # Default to GTC
                order_configuration["limit_limit_gtc"] = {
                    "base_size": base_size,
                    "limit_price": limit_price,
                    "post_only": False,
                }
        else:
            # Unsupported order type
            logger.error(f"Unsupported order type: {create_order.order_type}")
            return None

        data = {
            "client_order_id": client_order_id,
            "product_id": product_id,
            "side": side,
            "order_configuration": order_configuration,
        }

        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.POST,
            data=data,
            is_auth_required=True,
        )

        # Parse the response and return an OrderAck event
        if response.get("success", False):
            success_response = response.get("success_response", {})
            order_ack = self.convert_create_order_response_to_order_ack(
                success_response
            )
            event = BaseEvent(
                event_type=EventType.ORDER_ACK_EVENT,
                payload=Event[OrderAck](
                    header=MessageHeader(
                        exchange=self._config.exchange,
                        timestamp=int(time.time() * 1000),
                    ),
                    data=order_ack,
                ),
            )
            return event
        else:
            error_response = response.get("error_response", {})
            logger.error(f"Order creation failed: {error_response}")
            return None

    async def _cancel_order_signal(
        self, cancel_order: CancelOrder
    ) -> Optional[BaseEvent]:
        assert self._config is not None, "Config cannot be None"
        path_url = "/api/v3/brokerage/orders/batch_cancel"
        data = {
            "order_ids": [cancel_order.client_order_id],
        }
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.POST,
            data=data,
            is_auth_required=True,
        )
        # Parse the response and return an OrderAck event
        results = response.get("results", [])
        if results:
            result = results[0]
            if result.get("success", False):
                order_ack = self.convert_cancel_order_response_to_order_ack(result)
                event = BaseEvent(
                    event_type=EventType.ORDER_ACK_EVENT,
                    payload=Event[OrderAck](
                        header=MessageHeader(
                            exchange=self._config.exchange,
                            timestamp=int(time.time() * 1000),
                        ),
                        data=order_ack,
                    ),
                )
                return event
            else:
                logger.error(f"Order cancellation failed: {result}")
                return None
        else:
            logger.error(f"Order cancellation failed: {response}")
            return None

    async def pinger(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            assert self._public_ws is not None, "Public WS cannot be none"
            while self._public_ws.connected:
                # No specific ping message required by Coinbase, but maintain connection
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            logger.error("Stopping Coinbase public WS ping coroutine")

    async def pinger_private(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            assert self._private_ws is not None, "Private WS cannot be none"
            while self._private_ws.connected:
                # No specific ping message required by Coinbase, but maintain connection
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            logger.error("Stopping Coinbase private WS ping coroutine")

    async def _create_public_ws_subscription_request(self) -> List[WSJSONRequest]:
        """
        Creates subscription requests for the public WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        ws_reqs = []
        trading_pairs_table = self._trading_pairs_to_symbols_table

        # Subscription parameters for each stream
        channels = []

        # Orderbook subscriptions
        if self._config.ob_config is not None:
            ob_config = self._config.ob_config
            product_ids = [trading_pairs_table[ticker] for ticker in ob_config.tickers]
            channels.append(
                {
                    "type": self.SUBSCRIBE_OP,
                    "channel": self.ORDERBOOK_CHANNEL,
                    "product_ids": product_ids,
                }
            )

        # Market trades subscriptions
        if self._config.mt_config is not None:
            mt_config = self._config.mt_config
            product_ids = [trading_pairs_table[ticker] for ticker in mt_config.tickers]
            channels.append(
                {
                    "type": self.SUBSCRIBE_OP,
                    "channel": self.MARKET_TRADES_CHANNEL,
                    "product_ids": product_ids,
                }
            )

        # Kline subscriptions
        if self._config.kl_config is not None:
            kl_config = self._config.kl_config
            product_ids = [trading_pairs_table[ticker] for ticker in kl_config.tickers]
            channels.append(
                {
                    "type": self.SUBSCRIBE_OP,
                    "channel": self.KLINE_CHANNEL,
                    "product_ids": product_ids,
                }
            )

        # Heartbeats subscription
        channels.append(
            {
                "type": self.SUBSCRIBE_OP,
                "channel": self.HEARTBEAT_CHANNEL,
            }
        )

        for channel_payload in channels:
            req = WSJSONRequest(payload=channel_payload, is_auth_required=True)
            ws_reqs.append(req)

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
            symbol = f"{base_asset}-{quote_asset}".upper()
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
            symbol = f"{base_asset}-{quote_asset}".upper()
            trading_pairs_table[trading_pair] = symbol
        return trading_pairs_table

    """
    REST API
    """

    async def get_server_time_ms(self) -> int:
        path_url = "/api/v3/brokerage/time"
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.GET,
            is_auth_required=False,
        )
        epochMillis = int(response.get("epochMillis", int(time.time() * 1000)))
        return epochMillis

    async def fetch_wallet_balance(
        self, account_type: EAccountType = EAccountType.UNIFIED
    ) -> Wallet:
        path_url = "/api/v3/brokerage/accounts"
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.GET,
            is_auth_required=True,
        )
        timestamp = int(time.time() * 1000)
        wallet = {}
        accounts = response.get("accounts", [])
        for account in accounts:
            currency = account.get("currency")
            available_balance = account.get("available_balance", {})
            hold_balance = account.get("hold", {})
            available = float(available_balance.get("value", "0"))
            hold = float(hold_balance.get("value", "0"))
            total = available + hold
            coin_balance = CoinBalance(
                total=total,
                available=available,
                realised_pnl=0.0,
                unrealised_pnl=0.0,
            )
            wallet[currency] = coin_balance
        return Wallet(wallet=wallet, timestamp=timestamp)

    async def fetch_open_orders(
        self, symbol: Optional[TradingPair] = None
    ) -> List[Dict]:
        path_url = "/api/v3/brokerage/orders/historical/batch"
        params = {
            "order_status": "OPEN",
            "limit": 100,  # Maximum limit per request
        }
        if symbol:
            trading_pairs_table = self._trading_pairs_to_symbols_table
            product_id = trading_pairs_table[symbol]
            params["product_id"] = product_id

        orders = []
        has_next = True
        cursor = None

        while has_next:
            if cursor:
                params["cursor"] = cursor
            response = await self.api_request(
                path_url=path_url,
                method=RESTMethod.GET,
                params=params,
                is_auth_required=True,
            )
            orders.extend(response.get("orders", []))
            has_next = response.get("has_next", False)
            cursor = response.get("cursor")

        return orders

    async def cancel_all_orders(
        self,
        order_category: EOrderCategory = EOrderCategory.SPOT,
        symbol: Optional[TradingPair] = None,
    ) -> Dict[str, Any]:
        # Fetch open orders
        open_orders = await self.fetch_open_orders(symbol=symbol)
        order_ids = [order.get("order_id") for order in open_orders]

        # Batch cancel orders
        path_url = "/api/v3/brokerage/orders/batch_cancel"
        data = {
            "order_ids": order_ids[:100],  # Max 100 per request
        }

        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.POST,
            data=data,
            is_auth_required=True,
        )

        return response

    async def fetch_instrument_info(
        self, pair: TradingPair, category: EOrderCategory = EOrderCategory.SPOT
    ) -> List[InstrumentInfo]:
        """
        Fetches instrument information for a given trading pair.
        """
        symbol = self._trading_pairs_to_symbols_table.get(pair)
        if not symbol:
            raise Exception(f"Trading pair {pair} not found in symbol table")
        path_url = f"/api/v3/brokerage/market/products/{symbol}"
        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.GET,
            is_auth_required=False,
        )
        product_info = response
        base_asset = product_info.get("base_currency_id")
        quote_asset = product_info.get("quote_currency_id")
        if base_asset != pair.base or quote_asset != pair.quote:
            raise Exception("Mismatch in base or quote asset")
        trade_on = not product_info.get("trading_disabled", True)
        min_order_size = float(product_info.get("base_min_size", "0"))
        max_order_size = float(product_info.get("base_max_size", "0"))
        tick_size = float(product_info.get("price_increment", "0"))
        instrument_info = InstrumentInfo(
            pair=pair,
            tradebale=trade_on,
            base_precision=get_decimal_places(product_info.get("base_increment", "0")),
            quote_precision=get_decimal_places(
                product_info.get("quote_increment", "0")
            ),
            qty_precision=get_decimal_places(product_info.get("base_increment", "0")),
            min_order_qty=min_order_size,
            max_order_qty=max_order_size,
            tick_size=tick_size,
            min_order_amt=float(product_info.get("quote_min_size", "0")),
        )
        return [instrument_info]

    async def fetch_klines(
        self,
        symbol: TradingPair,
        interval: str,
        start_time: str,
        end_time: str,
        category: EOrderCategory = EOrderCategory.SPOT,
        limit: int = 1000,
    ) -> List[Kline]:
        return []

    """
    Normalizer API
    """

    def convert_exchange_orderbook_to_orderbook(self, data: Dict) -> Orderbook:
        """
        Converts exchange-specific orderbook data to a standardized Orderbook instance.
        """
        events = data.get("events", [])
        event = events[0]
        update_type_str = event.get("type", "snapshot")
        update_type = (
            EUpdateType.SNAPSHOT if update_type_str == "snapshot" else EUpdateType.DELTA
        )

        product_id = event.get("product_id", "")
        trading_pair = self._symbols_to_trading_pairs_table.get(product_id)
        assert trading_pair is not None, "Unidentified trading pair"

        updates = event.get("updates", [])
        bids = []
        asks = []

        for update in updates:
            side = update.get("side", "")
            price = float(update.get("price_level", "0"))
            qty = float(update.get("new_quantity", "0"))
            entry = OrderbookEntry(price=price, qty=qty)
            if side == "bid":
                bids.append(entry)
            elif side == "offer":  # Coinbase uses 'offer' instead of 'ask'
                asks.append(entry)

        timestamp_str = parse_timestamp_to_millis(data.get("timestamp", ""))

        seq = data.get("sequence_num", 0)

        orderbook = Orderbook(
            update_type=update_type,
            trading_pair=trading_pair,
            bids=bids,
            asks=asks,
            timestamp=timestamp_str,
            seq=seq,
        )
        return orderbook

    def convert_exchange_klines_to_klines(self, data: Dict) -> Kline:
        """
        Converts exchange-specific kline data to a standardized Kline instance.
        """
        events = data.get("events", [])
        event = events[0]
        candles_list = event.get("candles", [])
        candle_data = candles_list[0]
        product_id = candle_data.get("product_id", "")
        trading_pair = self._symbols_to_trading_pairs_table.get(product_id)
        assert trading_pair is not None, "Unidentified trading pair"

        kline = Kline(
            trading_pair=trading_pair,
            open=float(candle_data.get("open", "0")),
            close=float(candle_data.get("close", "0")),
            high=float(candle_data.get("high", "0")),
            low=float(candle_data.get("low", "0")),
            volume=float(candle_data.get("volume", "0")),
            start=int(candle_data.get("start", "0")) * 1000,
            timestamp=int(time.time() * 1000),
            confirm=True,
        )
        return kline

    def convert_exchange_trades_to_trades(self, data: Dict) -> MarketTrades:
        """
        Converts exchange-specific trade data to a standardized MarketTrades instance.
        """
        events = data.get("events", [])
        event = events[0]
        trades_list = event.get("trades", [])
        product_id = trades_list[0].get("product_id", "")
        trading_pair = self._symbols_to_trading_pairs_table.get(product_id)
        assert trading_pair is not None, "Unidentified trading pair"
        trades_data = []
        for trade in trades_list:
            price = float(trade.get("price", "0"))
            qty = float(trade.get("size", "0"))
            side_str = trade.get("side", "BUY")
            side = ESide.BUY if side_str.upper() == "BUY" else ESide.SELL
            trades_data.append(MarketTradesData(price=price, qty=qty, side=side))
        market_trades = MarketTrades(
            trading_pair=trading_pair,
            trades=trades_data,
        )
        return market_trades

    def convert_create_order_response_to_order_ack(
        self, data: Dict[str, Any]
    ) -> OrderAck:
        """
        Converts the exchange's create order response to an OrderAck.
        """
        order_id = data.get("order_id", "")
        timestamp = int(
            time.time() * 1000
        )  # Use current time, as no timestamp is provided
        order_ack = OrderAck(
            order_id=order_id,
            ack_type=EAckType.CREATE,
            timestamp=timestamp,
        )
        return order_ack

    def convert_cancel_order_response_to_order_ack(
        self, data: Dict[str, Any]
    ) -> OrderAck:
        """
        Converts the exchange's cancel order response to an OrderAck.
        """
        order_id = data.get("order_id", "")
        timestamp = int(time.time() * 1000)  # Use current time
        order_ack = OrderAck(
            order_id=order_id,
            ack_type=EAckType.CANCEL,
            timestamp=timestamp,
        )
        return order_ack

    def convert_exchange_wallet_update_to_wallet(self, data: Dict) -> Wallet:
        """
        Converts exchange-specific wallet update data to a standardized Wallet instance.
        """
        account_data = data.get("account", {})
        currency = account_data.get("currency")
        available_balance = account_data.get("available_balance", {})
        hold_balance = account_data.get("hold", {})
        available = float(available_balance.get("value", "0"))
        hold = float(hold_balance.get("value", "0"))
        total = available + hold
        coin_balance = CoinBalance(
            total=total,
            available=available,
            realised_pnl=0.0,
            unrealised_pnl=0.0,
        )
        wallet = Wallet(
            wallet={currency: coin_balance}, timestamp=int(time.time() * 1000)
        )
        return wallet

    def convert_exchange_order_update_to_order_update(self, data: Dict) -> OrderUpdate:
        """
        Converts exchange-specific order update data to a standardized OrderUpdate instance.
        """
        events = data.get("events", [])
        event = events[0]
        orders = event.get("orders", [])
        updates = []
        for order in orders:
            product_id = order.get("product_id", "")
            trading_pair = self._symbols_to_trading_pairs_table.get(product_id)
            if not trading_pair:
                continue
            order_id = order.get("order_id", "")
            side_str = order.get("order_side", "BUY")
            side = ESide.BUY if side_str.upper() == "BUY" else ESide.SELL
            order_type_str = order.get("order_type", "LIMIT_ORDER_TYPE")
            order_type = self.convert_exchange_order_type_to_order_type(order_type_str)
            price = float(order.get("limit_price", "0"))
            qty = float(order.get("base_size", "0"))
            status_str = order.get("status", "NEW")
            status = self.convert_exchange_order_status_to_order_status(status_str)
            cum_exec_qty = float(order.get("cumulative_quantity", "0"))
            cum_exec_value = float(order.get("filled_value", "0"))
            create_time_str = order.get("creation_time")
            create_time = int(
                time.mktime(time.strptime(create_time_str, "%Y-%m-%dT%H:%M:%S.%fZ"))
                * 1000
            )
            update_time = int(time.time() * 1000)
            order_update_item = OrderUpdateItem(
                symbol=trading_pair,
                order_id=order_id,
                side=side,
                order_type=order_type,
                price=price,
                qty=qty,
                tif=ETimeInForce.GTC,  # Adjust based on actual TIF
                order_status=status,
                custom_order_id=order.get("client_order_id", ""),
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
            updates.append(order_update_item)
        order_update = OrderUpdate(timestamp=int(time.time() * 1000), updates=updates)
        return order_update

    def convert_exchange_order_type_to_order_type(self, data: str) -> EOrderType:
        """
        Converts exchange-specific order type code to EOrderType.
        """
        order_type_mapping = {
            "LIMIT_ORDER_TYPE": EOrderType.LIMIT,
            "MARKET_ORDER_TYPE": EOrderType.MARKET,
        }
        return order_type_mapping.get(data, EOrderType.UNKNOWN)

    def convert_exchange_order_status_to_order_status(self, data: str) -> EOrderStatus:
        """
        Converts exchange-specific order status to EOrderStatus.
        """
        status_mapping = {
            "OPEN": EOrderStatus.NEW,
            "FILLED": EOrderStatus.FILLED,
            "CANCELLED": EOrderStatus.CANCELLED,
            "FAILED": EOrderStatus.REJECTED,
        }
        return status_mapping.get(data, EOrderStatus.UNKNOWN)

    """
    Denormalizer API
    """

    def convert_order_type_to_exchange_order_type(self, order_type: EOrderType) -> str:
        # Not needed as we map order types in _create_order_signal
        return NotImplemented

    def convert_tif_to_exchange_tif(self, tif: ETimeInForce) -> str:
        # Not needed as we map TIF in _create_order_signal
        return NotImplemented

    def convert_order_side_to_exchange_side(self, side: ESide) -> str:
        """
        Converts our ESide to Coinbase's side ('BUY' or 'SELL').
        """
        side_mapping = {
            ESide.BUY: "BUY",
            ESide.SELL: "SELL",
        }
        return side_mapping.get(side, "BUY")

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

    def convert_order_category_to_exchange_category(
        self, order_category: EOrderCategory
    ) -> str:
        return NotImplemented

    def convert_exchange_side_to_side(self, data: str) -> ESide:
        return NotImplemented

    def convert_exchange_tif_to_tif(self, data: str) -> ETimeInForce:
        return NotImplemented
