import asyncio
import time
from typing import Any, Dict, List, Optional, cast

from ttxt_v2.connector import ConnectorBase, ConnectorConfig
from ttxt_v2.connector.connector_config import ConnectorConfig, StorageType
from ttxt_v2.connector.connector_urls import ConnectorURL
from ttxt_v2.core.api import (AmendOrder, BaseEvent, CancelOrder, CoinBalance,
                              CreateOrder, EAccountType, EAckType,
                              EOrderCategory, EOrderStatus, EOrderType, ESide,
                              ETimeInForce, EUpdateType, Event, EventType,
                              EWebSocketType, InstrumentInfo, IQueue, Kline,
                              MarketTrades, MarketTradesData, MessageHeader,
                              OrderAck, Orderbook, OrderbookEntry, OrderUpdate,
                              OrderUpdateItem, TradingPair, Wallet)
from ttxt_v2.core.web import (BaseAuth, WebAssitantFactory, WSJSONRequest,
                              WSRequest, WSResponse)
from ttxt_v2.core.web.data_types import RESTMethod, WSRequest
from ttxt_v2.utils.async_websocket_retrier import websocket_reconnect
from ttxt_v2.utils.logger import logger
from ttxt_v2.utils.math_utils import get_decimal_places

from .kucoin_auth import KucoinAuth


class Kucoin(ConnectorBase):
    """
    Connector class for Bybit exchange.

    Methods:
        subscribe_to_public_stream():
            Subscribes to the public WebSocket stream.

        _process_market_data(response: WSResponse):
            Processes market data received from the WebSocket stream.

        authenticator() -> BaseAuth:
            Returns the authenticator for the connector.

        _create_web_assistant_factory() -> WebAssitantFactory:
            Creates a web assistant factory.

        get_spot_url() -> str:
            Returns the URL for the spot market.

        pinger():
            Sends periodic ping messages to keep the WebSocket connection alive.

        _create_public_ws_subscription_request() -> List[WSJSONRequest]:
            Creates subscription requests for the public WebSocket stream.
    """

    def __init__(
        self,
        config: Optional[ConnectorConfig] = None,
        public_queue: Optional[IQueue] = None,
        signal_queue: Optional[IQueue] = None,
        api_key: str = "",
        api_secret: str = "",
        api_passphrase: str = "",
        api_key_version: str = "3",
    ):
        """
        Initializes the Bybit connector with the given configuration, public queue, API key, and secret.

        Args:
            config (ConnectorConfig): Configuration for the connector.
            public_queue (IQueue): Queue for public data streams.
            api_key (str): The API key for authentication.
            api_secret (str): The secret key for authentication.
        """
        self._passphrase = api_passphrase
        self._api_key_version = api_key_version
        super().__init__(config, public_queue, signal_queue, api_key, api_secret)
        self._public_ws_url = ""
        self._private_ws_url = ""
        self._public_token = ""
        self._private_token = ""

    def is_ws_trading_enabled(self) -> bool:
        return False

    async def _subscribe_to_public_stream(self):
        """
        Subscribes to the public WebSocket stream by sending subscription requests.
        """
        assert (
            self._public_ws is not None and self._public_ws.connected
        ), "Public WS cannot be None and should be connected"

        # Create subscription requests
        reqs = self._create_public_ws_subscription_request()
        for req in reqs:
            await self._public_ws.send(req)

    async def _subscribe_to_trade_stream(self):
        """Not needed since we do not trade over websocket"""
        pass

    async def _subscribe_to_private_stream(self):
        assert (
            self._private_ws is not None and self._private_ws.connected
        ), "Private WS cannot be None and should be connected"

        # Create subscription requests
        reqs = self._create_private_ws_subscription_request()
        for req in reqs:
            await self._private_ws.send(req)
            res = await self._private_ws.receive()
            if res is not None:
                logger.debug(f"Private subscription response: {res.data}")

    async def _process_market_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Processes market data received from the WebSocket stream.

        Args:
            response (WSResponse): The WebSocket response containing market data.
        """
        assert (
            self._config is not None
        ), "Cannot process public market data. Config is None"
        msg_data = response.data

        if not isinstance(msg_data, dict):
            logger.debug(f"Public message: {msg_data}")
            return None

        msg_type = msg_data.get("type", "")
        msg_type_mapping = {
            "": "Empty message type",
            "ack": f"Acknowledgment: {msg_data}",
            "welcome": f"Welcome: {msg_data}",
        }

        mapped = msg_type_mapping.get(msg_type, "")
        if mapped != "":
            logger.info(mapped)
            return None

        if msg_data.get("type") == "message":
            topic = msg_data.get("topic", "")
            if topic.startswith("/market/match:"):
                event = self.convert_exchange_trades_to_trades(msg_data)
                if event:
                    return BaseEvent(
                        event_type=EventType.MT_EVENT,
                        payload=Event[MarketTrades](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=int(time.time()),
                            ),
                            data=event,
                        ),
                    )
            elif topic.startswith("/spotMarket/level2Depth5:"):
                orderbook = self.convert_exchange_orderbook_to_orderbook(msg_data)
                self._update_orderbooks(orderbook)
                if orderbook:
                    self._update_orderbooks(orderbook)
                    return BaseEvent(
                        event_type=EventType.OB_EVENT,
                        payload=Event[Orderbook](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=orderbook.timestamp,
                            ),
                            data=orderbook,
                        ),
                    )
            elif topic.startswith("/market/candles:"):
                kline = self.convert_exchange_klines_to_klines(msg_data)
                if kline:
                    return BaseEvent(
                        event_type=EventType.KL_EVENT,
                        payload=Event[Kline](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=kline.timestamp,
                            ),
                            data=kline,
                        ),
                    )
            else:
                logger.debug(f"Unhandled topic: {topic}")

        return None

    def _process_trade_data(self, response: WSResponse) -> Optional[BaseEvent]:
        assert self._config is not None, "Config cannot be None"
        """ Not required since we will not trade using websockets """

    def _process_private_data(self, response: WSResponse) -> Optional[List[BaseEvent]]:
        assert self._config is not None, "Config cannot be None"
        msg_data = response.data

        if not isinstance(msg_data, dict):
            logger.debug(f"Private message: {msg_data}")
            return None

        if msg_data.get("type") == "message":
            topic = msg_data.get("topic", "")
            if topic == "/spotMarket/tradeOrdersV2":
                order_update = self.convert_exchange_order_update_to_order_update(
                    msg_data
                )
                if order_update:
                    return [
                        BaseEvent(
                            event_type=EventType.ORDER_UPDATE_EVENT,
                            payload=Event[OrderUpdate](
                                header=MessageHeader(
                                    exchange=self._config.exchange,
                                    timestamp=order_update.timestamp,
                                ),
                                data=order_update,
                            ),
                        )
                    ]
            elif topic == "/account/balance":
                wallet_update = self.convert_exchange_wallet_update_to_wallet(msg_data)
                if wallet_update:
                    return [
                        BaseEvent(
                            event_type=EventType.WALLET_UPDATE_EVENT,
                            payload=Event[Wallet](
                                header=MessageHeader(
                                    exchange=self._config.exchange,
                                    timestamp=wallet_update.timestamp,
                                ),
                                data=wallet_update,
                            ),
                        )
                    ]
            else:
                logger.debug(f"Unhandled private topic: {topic}")

        return None

    def _process_signal_event(self, event: BaseEvent) -> List[WSRequest]:
        """
        Abstract method to process event from the signal event queue and return the WSRequest to send to the exchange.

        Returns:
            WSRequest: Request to be sent to the trade websocket connection.
        """
        """ not required since we will not trade using websockets """
        return NotImplemented

    async def _process_http_signals(self, event: BaseEvent) -> Optional[BaseEvent]:
        if event.event_type == EventType.CREATE_ORDER_EVENT:
            return await self._create_order_signal(
                cast(CreateOrder, event.payload.data)
            )
        elif event.event_type == EventType.CANCEL_ORDER_EVENT:
            return await self._cancel_order_signal(
                cast(CancelOrder, event.payload.data)
            )
        else:
            logger.warning(f"Received unsupported event type: {event.event_type}")
            return None

    async def _create_order_signal(
        self, create_order: CreateOrder
    ) -> Optional[BaseEvent]:
        assert self._config is not None, "Config cannot be None when placing orders"

        symbol = self._trading_pairs_to_symbols_table[create_order.trading_pair]

        data = {
            "clientOid": create_order.client_order_id,
            "side": self.convert_order_side_to_exchange_side(create_order.side),
            "symbol": symbol,
            "type": self.convert_order_type_to_exchange_order_type(
                create_order.order_type
            ),
        }

        if create_order.order_type == EOrderType.LIMIT:
            data["price"] = str(create_order.price)
            data["size"] = str(create_order.qty)
            data["timeInForce"] = self.convert_tif_to_exchange_tif(create_order.tif)
        elif create_order.order_type == EOrderType.MARKET:
            data["size"] = str(create_order.qty)

        response = await self.api_request(
            path_url="/api/v1/orders",
            method=RESTMethod.POST,
            data=data,
            is_auth_required=True,
        )

        def create_order_ack(response: Dict[str, Any]) -> Optional[OrderAck]:
            if response.get("code") != "200000":
                logger.error(f"Order creation failed: {response}")
                return None
            return OrderAck(
                order_id=create_order.client_order_id,
                ack_type=EAckType.CREATE,
                timestamp=int(time.time_ns() / 1_000_000),
            )

        order_ack = create_order_ack(response)
        if order_ack is None:
            return None

        return BaseEvent(
            event_type=EventType.ORDER_ACK_EVENT,
            payload=Event[OrderAck](
                header=MessageHeader(
                    exchange=self._config.exchange, timestamp=order_ack.timestamp
                ),
                data=order_ack,
            ),
        )

    async def _cancel_order_signal(
        self, cancel_order: CancelOrder
    ) -> Optional[BaseEvent]:
        assert self._config is not None, "Config cannot be None when cancelling orders"
        assert (
            cancel_order.client_order_id is not None
        ), "Client order id cannot be None for cancelling in Kucoin"

        if cancel_order.client_order_id:
            path_url = f"/api/v1/order/client-order/{cancel_order.client_order_id}"
        else:
            logger.error("Cancel order requires client_order_id")
            return None

        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.DELETE,
            is_auth_required=True,
        )

        def cancel_order_ack(response: Dict[str, Any]) -> Optional[OrderAck]:
            if response.get("code") != "200000":
                logger.error(f"Order cancellation failed: {response}")
                return None
            return OrderAck(
                order_id=cancel_order.client_order_id,
                ack_type=EAckType.CANCEL,
                timestamp=int(time.time_ns() / 1_000_000),
            )

        order_ack = cancel_order_ack(response)
        if order_ack is None:
            return None

        return BaseEvent(
            event_type=EventType.ORDER_ACK_EVENT,
            payload=Event[OrderAck](
                header=MessageHeader(
                    exchange=self._config.exchange, timestamp=order_ack.timestamp
                ),
                data=order_ack,
            ),
        )

    @property
    def authenticator(self) -> BaseAuth:
        """
        Returns the authenticator for the connector.

        Returns:
            BaseAuth: The authenticator for the connector.
        """
        assert self._api_key is not None, "API KEY cannot be None for auth"
        assert self._api_secret is not None, "API_SECRET cannot be None for auth"
        return KucoinAuth(
            api_key=self._api_key,
            api_secret=self._api_secret,
            api_passphrase=self._passphrase,
            api_key_version=self._api_key_version,
        )

    def _create_web_assistant_factory(self) -> WebAssitantFactory:
        """
        Creates a web assistant factory.

        Returns:
            WebAssitantFactory: The web assistant factory."""
        return WebAssitantFactory(auth=self._auth)

    def _get_connector_urls(self) -> ConnectorURL:
        return ConnectorURL(
            PUBLIC_SPOT="",  # Will be obtained dynamically
            PUBLIC_LINEAR="",
            PUBLIC_INVERSE="",
            TRADE="",
            BASE="https://api.kucoin.com",
            PRIVATE="",
        )

    async def pinger(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        assert (
            self._public_ws is not None and self._public_ws.connected
        ), "Public WS cannot be None and should be connected"
        try:
            while True:
                ping_msg = {
                    "id": str(int(time.time() * 1000)),
                    "type": "ping",
                }
                await self._public_ws.send(WSJSONRequest(payload=ping_msg))
                await asyncio.sleep(15)
        except asyncio.CancelledError:
            logger.info("Public WS pinger cancelled")

    async def pinger_trade(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        assert (
            self._trade_ws is not None and self._trade_ws.connected
        ), "Trade WS cannot be None and should be connected"

    async def pinger_private(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        assert (
            self._private_ws is not None and self._private_ws.connected
        ), "Private WS cannot be None and should be connected"
        try:
            while True:
                ping_msg = {
                    "id": str(int(time.time() * 1000)),
                    "type": "ping",
                }
                await self._private_ws.send(WSJSONRequest(payload=ping_msg))
                await asyncio.sleep(15)
        except asyncio.CancelledError:
            logger.info("Private WS pinger cancelled")

    def _create_public_ws_subscription_request(self) -> List[WSJSONRequest]:
        """
        Creates subscription requests for the public WebSocket stream.

        Returns:
            List[WSJSONRequest]: The list of WebSocket subscription requests.
        """
        assert self._config is not None, "Config cannot be None"

        reqs = []
        id_counter = int(time.time() * 1000)

        if self._config.ob_config:
            for ticker in self._config.ob_config.tickers:
                symbol = self._trading_pairs_to_symbols_table[ticker]
                req = {
                    "id": str(id_counter),
                    "type": "subscribe",
                    "topic": f"/spotMarket/level2Depth5:{symbol}",
                    "response": True,
                }
                reqs.append(WSJSONRequest(payload=req))
                id_counter += 1

        if self._config.mt_config:
            for ticker in self._config.mt_config.tickers:
                symbol = self._trading_pairs_to_symbols_table[ticker]
                req = {
                    "id": str(id_counter),
                    "type": "subscribe",
                    "topic": f"/market/match:{symbol}",
                    "response": True,
                }
                reqs.append(WSJSONRequest(payload=req))
                id_counter += 1

        if self._config.kl_config:
            for ticker in self._config.kl_config.tickers:
                symbol = self._trading_pairs_to_symbols_table[ticker]
                interval = self._config.kl_config.timeframe
                req = {
                    "id": str(id_counter),
                    "type": "subscribe",
                    "topic": f"/market/candles:{symbol}_{interval}",
                    "response": True,
                }
                reqs.append(WSJSONRequest(payload=req))
                id_counter += 1

        return reqs

    def _create_private_ws_subscription_request(self) -> List[WSJSONRequest]:
        """
        Creates subscription requests for the private WebSocket stream.

        Returns:
            List[WSJSONRequest]: The list of WebSocket subscription requests.
        """
        id_counter = int(time.time() * 1000)

        # Subscribe to order updates
        req_order_updates = {
            "id": str(id_counter),
            "type": "subscribe",
            "topic": "/spotMarket/tradeOrdersV2",
            "privateChannel": True,
            "response": True,
        }
        id_counter += 1

        # Subscribe to account balance updates
        req_balance_updates = {
            "id": str(id_counter),
            "type": "subscribe",
            "topic": "/account/balance",
            "privateChannel": True,
            "response": True,
        }

        return [
            WSJSONRequest(payload=req_order_updates),
            WSJSONRequest(payload=req_balance_updates),
        ]

    async def _get_ws_connection_info(self, private: bool) -> Dict[str, Any]:
        """
        Obtains WebSocket connection info (endpoint and token).
        """
        if private:
            path_url = "/api/v1/bullet-private"
            is_auth_required = True
        else:
            path_url = "/api/v1/bullet-public"
            is_auth_required = False

        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.POST,
            is_auth_required=is_auth_required,
        )

        if response.get("code") != "200000":
            logger.error(f"Failed to get websocket connection info: {response}")
            raise Exception("Failed to get websocket connection info")

        data = response["data"]
        instance_servers = data["instanceServers"]
        # We'll use the first server
        endpoint = instance_servers[0]["endpoint"]
        token = data["token"]
        return {"endpoint": endpoint, "token": token}

    def _generate_connect_id(self) -> str:
        """
        Generates a unique connection ID.
        """
        return str(int(time.time() * 1000))

    @websocket_reconnect(EWebSocketType.PRIVATE)
    async def _private_stream(self):
        """
        Listens to the private data stream and processes events.
        """
        assert (
            self._public_queue_stream is not None
        ), "Cannot listen to private stream with None public queue"

        # Get private websocket info
        ws_info = await self._get_ws_connection_info(private=True)
        self._urls.PRIVATE = ws_info["endpoint"]
        self._private_token = ws_info["token"]
        ws_url = f"{self._urls.PRIVATE}?token={self._private_token}&connectId={self._generate_connect_id()}"

        self._private_ws = await self._web_assistant_factory.get_ws_assistant()
        await self._private_ws.connect(ws_url)
        await self._on_websocket_connected(EWebSocketType.PRIVATE)
        await self._subscribe_to_private_stream()
        pinger = asyncio.create_task(self.pinger_private())
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
            await pinger

    @websocket_reconnect(EWebSocketType.PUBLIC)
    async def listen_public_stream(self):
        """
        Listens to the public data stream and processes market data.
        """
        assert self._config is not None, "Cannot listen to public stream without config"
        if not self._config.recording_config.enable:
            assert (
                self._public_queue_stream is not None
            ), "Cannot listen for public data if queue is None"

        # Get public websocket info
        ws_info = await self._get_ws_connection_info(private=False)
        self._urls.PUBLIC_SPOT = ws_info["endpoint"]
        self._public_token = ws_info["token"]
        ws_url = f"{self._urls.PUBLIC_SPOT}?token={self._public_token}&connectId={self._generate_connect_id()}"

        self._public_ws = await self._web_assistant_factory.get_ws_assistant()
        logger.info(f"Connecting on public URL: {ws_url}")
        await self._public_ws.connect(ws_url)
        await self._on_websocket_connected(EWebSocketType.PUBLIC)
        await self._subscribe_to_public_stream()
        self._clock_drift = await self._find_clock_drift()
        pinger = asyncio.create_task(self.pinger())
        if self._recorder:
            recording_task = asyncio.create_task(self._recorder.start())
        try:
            while True:
                resp = await self._public_ws.receive()
                if resp is not None and resp.data is not None:
                    event = await self._process_market_data(resp)
                    if event is not None:
                        if self._public_queue_stream is not None:
                            await self._public_queue_stream.publish(event)
                        if (
                            self._config.recording_config.enable
                            and self._config.recording_config.storage_type
                            != StorageType.NONE
                        ):
                            assert (
                                self._recorder is not None
                            ), "Cannot record without a recorder"
                            await self._recorder.queue.publish(event)
        except asyncio.CancelledError:
            logger.warn("Public stream listener cancelled.")
            raise
        finally:
            pinger.cancel()
            await pinger
            if self._recorder:
                await self._recorder.stop()
                await recording_task

    def _gen_symbols_table(self) -> Dict[str, TradingPair]:
        assert self._config is not None, "Config cannot be None"
        res = {}
        if self._config.ob_config:
            for ticker in self._config.ob_config.tickers:
                symbol = f"{ticker.base.upper()}-{ticker.quote.upper()}"
                res[symbol] = ticker
        return res

    def _gen_trading_pairs_table(self) -> Dict[TradingPair, str]:
        assert self._config is not None, "Config cannot be None"
        assert self._config.ob_config is not None, "Config cannot be None"
        assert self._config is not None, "Config cannot be None"
        res = {}
        if self._config.ob_config:
            for ticker in self._config.ob_config.tickers:
                symbol = f"{ticker.base.upper()}-{ticker.quote.upper()}"
                res[ticker] = symbol
        return res

    """
    REST API
    """

    async def get_server_time_ms(self) -> int:
        response = await self.api_request(path_url="/api/v1/timestamp")
        if response.get("code") != "200000":
            logger.error(f"Failed to get server time: {response}")
            return int(time.time() * 1000)
        return int(response["data"])

    async def fetch_wallet_balance(
        self, account_type: EAccountType = EAccountType.UNIFIED
    ) -> Wallet:
        """
        Fetches wallet balances from Kucoin for the user.

        Returns:
            Wallet: A dictionary mapping coin names to CoinBalance instances and a timestamp.
        """
        response = await self.api_request(
            path_url="/api/v1/accounts", is_auth_required=True
        )
        if response.get("code") != "200000":
            logger.error(f"Failed to fetch wallet balances: {response}")
            return Wallet()

        balances = Wallet()
        data = response.get("data", [])
        for item in data:
            currency = item["currency"]
            balance_type = item["type"]
            if balance_type != "trade":  # Only include trade account balances
                continue
            total = float(item["balance"])
            available = float(item["available"])
            balances.wallet[currency] = CoinBalance(
                total=total,
                available=available,
                realised_pnl=0.0,
                unrealised_pnl=0.0,
            )
        balances.timestamp = int(time.time() * 1000)
        return balances

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
        Fetch Kline data from Bybit for a given symbol, interval, and time range.

        :param symbol: Symbol name, e.g., BTCUSDT.
        :param interval: Kline interval, e.g., 1, 3, 5, etc.
        :param start_time: Start time in human-readable format, e.g., "2024-11-01 00:00".
        :param end_time: End time in human-readable format, e.g., "2024-11-15 00:00".
        :param category: Product type. Default is "spot".
        :param limit: Max results per request. Default is 1000.
        :return: List of Kline data.
        """
        return []

    async def fetch_instrument_info(
        self, pair: TradingPair, category: EOrderCategory = EOrderCategory.SPOT
    ) -> List[InstrumentInfo]:
        """
        Fetch instrument info for a given trading pair and category from Kucoin.
        """
        sym_mapping = {pair: f"{pair.base.upper()}-{pair.quote.upper()}"}
        symbol_str = sym_mapping[pair]
        response = await self.api_request(path_url=f"/api/v2/symbols/{symbol_str}")
        if response.get("code") != "200000":
            logger.error(f"Failed to fetch instrument info: {response}")
            return []

        data = response.get("data", {})
        instrument_info = InstrumentInfo(
            pair=pair,
            tradebale=data.get("enableTrading", False),
            qty_precision=get_decimal_places(data.get("baseMinSize", "0")),
            base_precision=get_decimal_places(data.get("baseIncrement", "0")),
            quote_precision=get_decimal_places(data.get("priceIncrement", "0")),
            min_order_qty=float(data.get("baseMinSize", "0")),
            max_order_qty=float(data.get("baseMaxSize", "0")),
        )

        return [instrument_info]

    async def cancel_all_orders(
        self,
        order_category: EOrderCategory = EOrderCategory.SPOT,
        symbol: Optional[TradingPair] = None,
    ) -> Dict[str, Any]:
        """
        Cancel all orders on Kucoin.
        """
        params = {}
        if symbol:
            sym_map = {symbol: self._trading_pairs_to_symbols_table[symbol]}
        if symbol:
            params["symbol"] = sym_map[symbol]

        response = await self.api_request(
            path_url="/api/v1/orders",
            method=RESTMethod.DELETE,
            params=params,
            is_auth_required=True,
        )
        return response

    """
    Normalizer API
    """

    def convert_exchange_orderbook_to_orderbook(self, data: Dict) -> Orderbook:
        topic = data.get("topic", "")
        symbol = topic.split(":")[1]
        pair = self._symbols_to_trading_pairs_table[symbol]
        orderbook_data = data.get("data", {})
        bids = [
            OrderbookEntry(price=float(bid[0]), qty=float(bid[1]))
            for bid in orderbook_data.get("bids", [])
        ]
        asks = [
            OrderbookEntry(price=float(ask[0]), qty=float(ask[1]))
            for ask in orderbook_data.get("asks", [])
        ]
        timestamp = int(orderbook_data.get("timestamp", time.time() * 1000))
        return Orderbook(
            update_type=EUpdateType.SNAPSHOT,
            trading_pair=pair,
            bids=bids,
            asks=asks,
            timestamp=timestamp,
            seq=0,
        )

    def convert_exchange_klines_to_klines(self, data: Dict) -> Kline:
        topic = data.get("topic", "")
        symbol, _ = topic.split(":")[1].split("_")
        pair = self._symbols_to_trading_pairs_table[symbol]
        kline_data = data.get("data", {})
        candles = kline_data.get("candles", [])
        timestamp = int(candles[0]) * 1000
        return Kline(
            trading_pair=pair,
            open=float(candles[1]),
            close=float(candles[2]),
            high=float(candles[3]),
            low=float(candles[4]),
            volume=float(candles[5]),
            start=timestamp,
            timestamp=int(time.time() * 1000),
            confirm=True,
        )

    def convert_exchange_trades_to_trades(self, data: Dict) -> MarketTrades:
        topic = data.get("topic", "")
        symbol = topic.split(":")[1]
        pair = self._symbols_to_trading_pairs_table[symbol]
        trade_data = data.get("data", {})
        trades = [
            MarketTradesData(
                price=float(trade_data.get("price", "0")),
                qty=float(trade_data.get("size", "0")),
                side=self.convert_exchange_side_to_side(trade_data.get("side", "")),
            )
        ]
        return MarketTrades(trading_pair=pair, trades=trades)

    def convert_exchange_order_ack_to_order_ack(self, data: dict) -> OrderAck:
        return NotImplemented

    def convert_exchange_wallet_update_to_wallet(self, data: dict) -> Wallet:
        data = data.get("data", {})
        currency = data.get("currency", "")
        total = float(data.get("total", "0"))
        available = float(data.get("available", "0"))
        timestamp = int(data.get("time", time.time() * 1000))
        wallet = Wallet()
        wallet.wallet[currency] = CoinBalance(
            total=total,
            available=available,
            realised_pnl=0.0,
            unrealised_pnl=0.0,
        )
        wallet.timestamp = timestamp
        return wallet

    def convert_exchange_order_update_to_order_update(self, data: dict) -> OrderUpdate:
        data = data.get("data", {})
        updates = []
        qty = 0
        if data.get("size", "") != "":
            qty = float(data.get("size", "0"))
        elif data.get("originSize", "") != "":
            qty = float(data.get("originSize", "0"))

        order_update_item = OrderUpdateItem(
            symbol=self._symbols_to_trading_pairs_table[data.get("symbol", "")],
            order_id=data.get("orderId", ""),
            side=self.convert_exchange_side_to_side(data.get("side", "")),
            order_type=self.convert_exchange_order_type_to_order_type(
                data.get("orderType", "")
            ),
            price=float(data.get("price", "0")),
            qty=qty,
            tif=self.convert_exchange_tif_to_tif(data.get("timeInForce", "")),
            order_status=self.convert_exchange_order_status_to_order_status(
                data.get("type", "")
            ),
            custom_order_id=data.get("clientOid", ""),
            cum_exec_qty=float(data.get("filledSize", "0")),
            cum_exec_fee=float(data.get("fee", "0")),
            cum_exec_value=float(data.get("filledValue", "0")),
            closed_pnl=0.0,
            take_profit=0.0,
            stop_loss=0.0,
            tp_limit_price=0.0,
            sl_limit_price=0.0,
            create_time=int(data.get("orderTime", time.time() * 1000)),
            update_time=int(data.get("ts", time.time() * 1000)),
        )
        updates.append(order_update_item)
        return OrderUpdate(timestamp=order_update_item.update_time, updates=updates)

    def convert_exchange_order_type_to_order_type(self, data: str) -> EOrderType:
        mapping = {
            "limit": EOrderType.LIMIT,
            "market": EOrderType.MARKET,
        }
        return mapping.get(data, EOrderType.UNKNOWN)

    def convert_exchange_order_status_to_order_status(self, data: str) -> EOrderStatus:
        mapping = {
            "received": EOrderStatus.UNKNOWN,
            "open": EOrderStatus.NEW,
            "match": EOrderStatus.UNKNOWN,
            "update": EOrderStatus.NEW,
            "filled": EOrderStatus.FILLED,
            "canceled": EOrderStatus.CANCELLED,
        }
        return mapping.get(data, EOrderStatus.UNKNOWN)

    def convert_exchange_order_category_to_order_category(
        self, data: str
    ) -> EOrderCategory:
        return NotImplemented

    def convert_exchange_tif_to_tif(self, data: str) -> ETimeInForce:
        mapping = {
            "GTC": ETimeInForce.GTC,
            "IOC": ETimeInForce.IOC,
            "FOK": ETimeInForce.FOK,
        }
        return mapping.get(data, ETimeInForce.UNKNOWN)

    def convert_exchange_side_to_side(self, data: str) -> ESide:
        mapping = {"sell": ESide.SELL, "buy": ESide.BUY}
        return mapping.get(data, ESide.SELL)

    """
    Denormalizer API
    """

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

    def convert_amend_order_to_ws_request(self, amend_order: AmendOrder) -> WSRequest:
        """Not needed since we do not trade over websockets"""
        return WSJSONRequest(payload={})

    def convert_order_type_to_exchange_order_type(self, order_type: EOrderType) -> str:
        mapping = {EOrderType.LIMIT: "limit", EOrderType.MARKET: "market"}
        return mapping.get(order_type, "limit")

    def convert_tif_to_exchange_tif(self, tif: ETimeInForce) -> str:
        mapping = {
            ETimeInForce.GTC: "GTC",
            ETimeInForce.IOC: "IOC",
            ETimeInForce.FOK: "FOK",
        }
        return mapping.get(tif, "GTC")

    def convert_order_category_to_exchange_category(
        self, order_category: EOrderCategory
    ) -> str:
        """Not needed for now for bitget"""
        return NotImplemented

    def convert_order_side_to_exchange_side(self, side: ESide) -> str:
        mapping = {ESide.BUY: "buy", ESide.SELL: "sell"}
        return mapping.get(side, "buy")
