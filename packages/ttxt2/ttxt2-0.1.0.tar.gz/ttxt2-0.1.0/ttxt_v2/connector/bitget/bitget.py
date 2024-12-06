import asyncio
import time
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
from ttxt_v2.core.web.data_types import RESTMethod, WSPlainTextRequest, WSRequest
from ttxt_v2.core.web.ws_assistant import WSAssistant
from ttxt_v2.utils.logger import logger

from .bitget_auth import BitgetAuth


class Bitget(ConnectorBase):
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

    LOGIN_OP = "login"

    # INFO: public chans
    BOOK_CHAN = "books15"
    PUBLIC_TRADES_CHAN = "trade"
    KLINE_CHAN = "candle1m"
    SUBSCRIBE_OP = "subscribe"

    # INFO: private chans
    ORDERS_CHAN = "orders"
    ACCOUNT_CHAN = "account"

    def __init__(
        self,
        config: Optional[ConnectorConfig] = None,
        public_queue: Optional[IQueue] = None,
        signal_queue: Optional[IQueue] = None,
        api_key: str = "",
        api_secret: str = "",
        api_passphrase: str = "",
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
        super().__init__(config, public_queue, signal_queue, api_key, api_secret)

    def is_ws_trading_enabled(self) -> bool:
        return False

    async def _login(self, ws: WSAssistant):
        login = WSJSONRequest(payload={}, is_auth_required=True)
        await ws.send(login)
        res = await ws.receive()
        assert res is not None, "Failed to get login response"
        res_data = res.data
        code = int(res_data["code"])
        if code != 0:
            logger.error(f"Error msg: {res_data}")
            raise RuntimeError("failed to login")

    async def _subscribe_to_public_stream(self):
        """
        Subscribes to the public WebSocket stream by sending subscription requests.
        """
        assert (
            self._public_ws is not None and self._public_ws.connected
        ), "Public WS cannot be None and should be connected"
        # await self._login(self._public_ws)
        reqs = self._create_public_ws_subscription_request()
        for req in reqs:
            await self._public_ws.send(req)
            res = await self._public_ws.receive()
            assert res is not None, "response cannot be None"
            msg_data = res.data
            logger.debug(f"Public subscription response: {msg_data}")

    async def _subscribe_to_trade_stream(self):
        """Not needed since we do not trade over websocket"""
        pass

    async def _subscribe_to_private_stream(self):
        assert (
            self._private_ws is not None and self._private_ws.connected
        ), "Private WS cannot be None and should be connected"
        await self._login(self._private_ws)
        reqs = self._create_private_ws_subscription_request()
        for req in reqs:
            await self._private_ws.send(req)
            res = await self._private_ws.receive()
            assert res is not None, "response cannot be None"
            msg_data = res.data
            logger.debug(f"Private subscription response: {msg_data}")

    async def _process_market_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Processes market data received from the WebSocket stream.

        Args:
            response (WSResponse): The WebSocket response containing market data.
        """
        assert (
            self._config is not None
        ), "Cannot process public market data. Config is None"
        try:
            msg_data = response.data
            if not isinstance(msg_data, dict):
                logger.debug(f"resp: {msg_data}")
                return None
            exch_ev = msg_data.get("event", "")
            if len(exch_ev) != 0 and exch_ev == "subscribe":
                logger.debug(f"Subscribed: {response.data}")
                return None

            arg = msg_data.get("arg", {})
            chan = arg.get("channel", "")
            if chan == "":
                logger.error(f"Unknown response: {msg_data}")
                return None

            if chan == self.BOOK_CHAN:
                normalized_orderbook = self.convert_exchange_orderbook_to_orderbook(
                    msg_data
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
            elif chan == self.PUBLIC_TRADES_CHAN:
                normalized_trades = self.convert_exchange_trades_to_trades(msg_data)
                event = BaseEvent(
                    event_type=EventType.MT_EVENT,
                    payload=Event[MarketTrades](
                        header=MessageHeader(
                            exchange=self._config.exchange, timestamp=int(time.time())
                        ),
                        data=normalized_trades,
                    ),
                )
                return event
            elif chan == self.KLINE_CHAN:
                normalized_kline = self.convert_exchange_klines_to_klines(msg_data)
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
            else:
                logger.error(f"Unknown channel: {chan}, data: {msg_data}")
                return None

        except Exception as e:
            logger.error(
                f"Error processing public market data. Exception: {str(e)}, Data: {response.data}"
            )

    def _process_trade_data(self, response: WSResponse) -> Optional[BaseEvent]:
        assert self._config is not None, "Config cannot be None"
        """ Not required since we will not trade using websockets """

    def _process_private_data(self, response: WSResponse) -> Optional[List[BaseEvent]]:
        assert self._config is not None, "Config cannot be None"
        try:
            msg_data = response.data
            if not isinstance(msg_data, dict):
                logger.debug(f"Private resp: {msg_data}")
                return None
            exch_ev = msg_data.get("event", "")
            if len(exch_ev) != 0 and exch_ev == "subscribe":
                logger.debug(f"Subscribed: {response.data}")
                return None

            chan = msg_data.get("arg").get("channel")
            if chan not in [self.ORDERS_CHAN, self.ACCOUNT_CHAN]:
                logger.warning(f"Unknown chanel: {chan}, data: {msg_data}")
                return None

            if chan == self.ORDERS_CHAN:
                order_up = self.convert_exchange_order_update_to_order_update(msg_data)
                return [
                    BaseEvent(
                        event_type=EventType.ORDER_UPDATE_EVENT,
                        payload=Event[OrderUpdate](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=order_up.timestamp,
                            ),
                            data=order_up,
                        ),
                    )
                ]
            else:
                wal_ev = self.convert_exchange_wallet_update_to_wallet(msg_data)
                return [
                    BaseEvent(
                        event_type=EventType.WALLET_UPDATE_EVENT,
                        payload=Event[Wallet](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=wal_ev.timestamp,
                            ),
                            data=wal_ev,
                        ),
                    )
                ]

        except Exception as e:
            logger.error(f"Error processing private market data: {str(e)}")

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
        assert self._config is not None, "Config cannot be None when placing orders"

        # NOTE: for now we do not use any stop loss / take profit params
        data = {
            "symbol": self._trading_pairs_to_symbols_table[create_order.trading_pair],
            "side": self.convert_order_side_to_exchange_side(create_order.side),
            "orderType": self.convert_order_type_to_exchange_order_type(
                create_order.order_type
            ),
            "force": self.convert_tif_to_exchange_tif(create_order.tif),
            "size": str(round(create_order.qty, 4)),
            "clientOid": create_order.client_order_id,
        }
        if create_order.order_type == EOrderType.LIMIT:
            assert (
                create_order.price is not None
            ), "Price cannot be None for limit orders"
            data["price"] = str(round(create_order.price, 5))

        response = await self.api_request(
            path_url="/api/v2/spot/trade/place-order",
            method=RESTMethod.POST,
            data=data,
            is_auth_required=True,
        )

        def create_order_ack(response: Dict[str, Any]) -> Optional[OrderAck]:
            if response["msg"] != "success":
                logger.error(f"Could not send order: {response}")
                return None
            data = response["data"]
            return OrderAck(
                order_id=data["clientOid"],
                ack_type=EAckType.CREATE,
                timestamp=int(time.time_ns() / 1_000_000),
            )

        order_ack = create_order_ack(response)
        assert order_ack is not None, "Order ack cannot be None, error occured"
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
        self, create_order: CancelOrder
    ) -> Optional[BaseEvent]:
        assert self._config is not None, "Config cannot be None when placing orders"

        # NOTE: for now we do not use any stop loss / take profit params
        data = {
            "symbol": self._trading_pairs_to_symbols_table[create_order.trading_pair],
            "clientOid": create_order.client_order_id,
        }
        response = await self.api_request(
            path_url="/api/v2/spot/trade/cancel-order",
            method=RESTMethod.POST,
            data=data,
            is_auth_required=True,
        )

        def cancel_order_ack(response: Dict[str, Any]) -> Optional[OrderAck]:
            if response["msg"] != "success":
                logger.error(f"Could not send order: {response}")
                return None
            data = response["data"]
            return OrderAck(
                order_id=data["clientOid"],
                ack_type=EAckType.CANCEL,
                timestamp=int(time.time_ns() / 1_000_000),
            )

        order_ack = cancel_order_ack(response)
        if order_ack == None:
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
        return BitgetAuth(
            api_key=self._api_key,
            api_secret=self._api_secret,
            api_passphrase=self._passphrase,
        )

    def _create_web_assistant_factory(self) -> WebAssitantFactory:
        """
        Creates a web assistant factory.

        Returns:
            WebAssitantFactory: The web assistant factory."""
        return WebAssitantFactory(auth=self._auth)

    def _get_connector_urls(self) -> ConnectorURL:
        return ConnectorURL(
            PUBLIC_SPOT="wss://ws.bitget.com/v2/ws/public",
            PUBLIC_LINEAR="",
            PUBLIC_INVERSE="",
            TRADE="",
            BASE="https://api.bitget.com",
            PRIVATE="wss://ws.bitget.com/v2/ws/private",
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
                await self._public_ws.send(WSPlainTextRequest(payload="ping"))
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.info("Public WS pinger cancelled")

    async def pinger_trade(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        assert (
            self._trade_ws is not None and self._trade_ws.connected
        ), "Trade WS cannot be None and should be connected"
        try:
            while True:
                await self._trade_ws.send(WSPlainTextRequest(payload="ping"))
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.info("Public WS pinger cancelled")

    async def pinger_private(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        assert (
            self._private_ws is not None and self._private_ws.connected
        ), "Private WS cannot be None and should be connected"
        try:
            while True:
                await self._private_ws.send(WSPlainTextRequest(payload="ping"))
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.info("Public WS pinger cancelled")

    def _create_public_ws_subscription_request(self) -> List[WSJSONRequest]:
        """
        Creates subscription requests for the public WebSocket stream.

        Returns:
            List[WSJSONRequest]: The list of WebSocket subscription requests.
        """
        assert self._config is not None, "Config cannot be None"
        # HACK: for now only SPOT
        msgs = []
        ob_config = self._config.ob_config
        if ob_config is not None:
            for ticker in ob_config.tickers:
                msgs.append(
                    {
                        "instType": "SPOT",
                        "channel": self.BOOK_CHAN,
                        "instId": self._trading_pairs_to_symbols_table[ticker],
                    }
                )

        mt_config = self._config.mt_config
        if mt_config is not None:
            for ticker in mt_config.tickers:
                msgs.append(
                    {
                        "instType": "SPOT",
                        "channel": self.PUBLIC_TRADES_CHAN,
                        "instId": self._trading_pairs_to_symbols_table[ticker],
                    }
                )

        kl_config = self._config.kl_config
        if kl_config is not None:
            for ticker in kl_config.tickers:
                msgs.append(
                    {
                        "instType": "SPOT",
                        "channel": self.KLINE_CHAN,
                        "instId": self._trading_pairs_to_symbols_table[ticker],
                    }
                )

        return [WSJSONRequest(payload={"op": self.SUBSCRIBE_OP, "args": msgs})]

    def _create_private_ws_subscription_request(self) -> List[WSJSONRequest]:
        msgs = []
        for _, ticker in self._trading_pairs_to_symbols_table.items():
            msgs.append(
                {"instType": "SPOT", "channel": self.ORDERS_CHAN, "instId": ticker}
            )
        msgs.append(
            {"instType": "SPOT", "channel": self.ACCOUNT_CHAN, "coin": "default"}
        )
        return [WSJSONRequest(payload={"op": self.SUBSCRIBE_OP, "args": msgs})]

    def _gen_symbols_table(self) -> Dict[str, TradingPair]:
        assert self._config is not None, "Config cannot be None"
        assert self._config.ob_config is not None, "Config cannot be None"
        ob_config = self._config.ob_config
        res = {}
        for ticker in ob_config.tickers:
            symb = f"{ticker.base.upper()}{ticker.quote.upper()}"
            res[symb] = ticker
        return res

    def _gen_trading_pairs_table(self) -> Dict[TradingPair, str]:
        assert self._config is not None, "Config cannot be None"
        assert self._config.ob_config is not None, "Config cannot be None"
        ob_config = self._config.ob_config
        res = {}
        for ticker in ob_config.tickers:
            res[ticker] = f"{ticker.base.upper()}{ticker.quote.upper()}"
        return res

    """
    REST API
    """

    async def get_server_time_ms(self) -> int:
        response = await self.api_request(path_url="/api/v2/public/time")
        code = response["code"]
        if code != "00000":
            logger.error(f"Could not get server time: {response}, returning 0")
            return 0

        return int(response["data"]["serverTime"])

    async def fetch_wallet_balance(
        self, account_type: EAccountType = EAccountType.UNIFIED
    ) -> Wallet:
        """
        Fetches wallet balances from Bybit for the user.

        Returns:
            Wallet: A dictionary mapping coin names to CoinBalance instances and a timestamp.
        """
        # HACK: for now spot only
        response = await self.api_request(
            path_url="/api/v2/spot/account/assets", is_auth_required=True
        )
        if response["code"] != "00000":
            logger.error(
                f"Could not fetch balanced: {response}\nReturning empty balances."
            )
            return Wallet()

        data = response["data"]
        balances = Wallet()
        for bal in data:
            balances.wallet[bal["coin"]] = CoinBalance(
                total=float(bal["available"]) + float(bal["frozen"]),
                available=float(bal["available"]),
                realised_pnl=0.0,
                unrealised_pnl=0.0,
            )

        balances.timestamp = int(response["requestTime"])
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
        return NotImplemented

    async def fetch_instrument_info(
        self, pair: TradingPair, category: EOrderCategory = EOrderCategory.SPOT
    ) -> List[InstrumentInfo]:
        """
        Fetch instrument info for a given trading pair and category from Bybit.

        :param pair: The trading pair (base and quote coin).
        :param category: The product type (spot, linear, inverse, option). Default is "spot".
        :return: A list of InstrumentInfo objects.
        """
        symb = f"{pair.base.upper()}{pair.quote.upper()}"
        mapping = {pair: symb}
        reverse_mapping = {symb: pair}
        # TODO: make it return all symbols with optional pair parameter

        # HACK: for now spot only
        response = await self.api_request(
            path_url="/api/v2/spot/public/symbols", params={"symbol": mapping[pair]}
        )
        if response["code"] != "00000":
            logger.error(
                f"Cannot get instrument info: {response}. Returning default one"
            )
            return [InstrumentInfo(pair=TradingPair(base="", quote=""))]

        msg_data = response["data"][0]

        status = msg_data["status"]
        trade_on = True if status == "online" else False
        return [
            InstrumentInfo(
                pair=reverse_mapping[msg_data["symbol"]],
                tradebale=trade_on,
                base_precision=int(msg_data["pricePrecision"]),
                quote_precision=int(msg_data["quotePrecision"]),
                qty_precision=int(msg_data["quantityPrecision"]),
                min_order_qty=float(msg_data["minTradeAmount"]),
                max_order_qty=float(msg_data["maxTradeAmount"]),
            )
        ]

    async def cancel_all_orders(
        self,
        order_category: EOrderCategory = EOrderCategory.SPOT,
        symbol: Optional[TradingPair] = None,
    ) -> Dict[str, Any]:
        """
        Bitget does not provide such functionality
        """
        return NotImplemented

    """
    Normalizer API
    """

    def convert_exchange_orderbook_to_orderbook(self, data: Dict) -> Orderbook:
        symbol = data["arg"]["instId"]
        pair = self._symbols_to_trading_pairs_table[symbol]

        assert len(data["data"]) == 1, "Weird why more than 1 snapshot"
        bids = data["data"][0]["bids"]
        asks = data["data"][0]["asks"]
        return Orderbook(
            update_type=EUpdateType.SNAPSHOT,  # since we get depth channel its always snapshot
            trading_pair=pair,
            bids=[
                OrderbookEntry(price=float(bid[0]), qty=float(bid[1])) for bid in bids
            ],
            asks=[
                OrderbookEntry(price=float(ask[0]), qty=float(ask[1])) for ask in asks
            ],
            timestamp=int(data["data"][0]["ts"]),
            seq=0,  # since we always get snapshot no sequence number
        )

    def convert_exchange_klines_to_klines(self, data: Dict) -> Kline:
        symbol = data["arg"]["instId"]
        pair = self._symbols_to_trading_pairs_table[symbol]
        payload = data["data"][0]
        return Kline(
            trading_pair=pair,
            open=float(payload[1]),
            close=float(payload[4]),
            high=float(payload[2]),
            low=float(payload[3]),
            volume=float(payload[7]),  # in USDT
            start=int(payload[0]),
            timestamp=int(data["ts"]),
            confirm=True,  # NOTE: weird API says index[7] twice aka this field should not exist will research
        )

    def convert_exchange_trades_to_trades(self, data: Dict) -> MarketTrades:
        symbol = data["arg"]["instId"]
        pair = self._symbols_to_trading_pairs_table[symbol]
        msg_data = data["data"]
        entries: List[MarketTradesData] = []
        for item in msg_data:
            entries.append(
                MarketTradesData(
                    price=float(item["price"]),
                    qty=float(item["size"]),
                    side=self.convert_exchange_side_to_side(item["side"]),
                )
            )
        return MarketTrades(trading_pair=pair, trades=entries)

    def convert_exchange_order_ack_to_order_ack(self, data: dict) -> OrderAck:
        return NotImplemented

    def convert_exchange_wallet_update_to_wallet(self, data: dict) -> Wallet:
        msg_data = data["data"]
        balances = Wallet()
        for item in msg_data:
            balances.wallet[item["coin"]] = CoinBalance(
                total=float(item["available"]) + float(item["frozen"]),
                available=float(item["available"]),
                realised_pnl=0.0,
                unrealised_pnl=0.0,
            )

        balances.timestamp = int(data["ts"])
        return balances

    def convert_exchange_order_update_to_order_update(self, data: dict) -> OrderUpdate:
        msg_data = data["data"]
        ts_raw = data.get("ts")
        if isinstance(ts_raw, (int, float)):
            ts = int(ts_raw)
        elif isinstance(ts_raw, str):
            ts = int(
                float(ts_raw)
            )  # Handles strings like '3.000128167' by converting to float first
        else:
            raise ValueError(f"Unexpected type for 'ts': {type(ts_raw)}")

        updates: List[OrderUpdateItem] = []
        for _, item in enumerate(msg_data):
            try:
                # Parse and validate 'size' and 'newSize'
                size_str = item.get("size")
                new_size_str = item.get("newSize", "0")
                size = float(size_str) if size_str else 0.0
                new_size = float(new_size_str) if new_size_str else 0.0
                true_size = new_size if new_size != 0.0 else size

                # Parse 'fillPrice' if available
                fill_price_str = item.get("fillPrice")
                fill_price = (
                    float(fill_price_str) if fill_price_str else 0.0
                )  # Default to 0.0 if missing

                # Parse other numerical fields with validation
                acc_base_volume_str = item.get("accBaseVolume", "0.0")
                acc_base_volume = float(acc_base_volume_str)

                fill_fee_str = item.get("fillFee", "0.0")
                fill_fee = float(fill_fee_str)

                base_volume_str = item.get("baseVolume", "0.0")
                base_volume = float(base_volume_str)

                # Calculate cumulative execution value
                cum_exec_value = fill_price * base_volume

                # Parse and validate 'cTime' and 'uTime'
                cTime_raw = item.get("cTime")
                uTime_raw = item.get("uTime")

                cTime = int(float(cTime_raw)) if cTime_raw else 0
                uTime = int(float(uTime_raw)) if uTime_raw else 0

                # Convert order type and status
                order_type = self.convert_exchange_order_type_to_order_type(
                    item["orderType"]
                )
                order_status = self.convert_exchange_order_status_to_order_status(
                    item["status"]
                )

                # Convert 'force' to ETimeInForce enum
                force_str = item.get(
                    "force", "gtc"
                ).lower()  # Default to 'gtc' if missing
                tif = self.convert_exchange_tif_to_tif(force_str)

                # Convert 'side' to ESide enum
                side_str = item.get(
                    "side", "buy"
                ).lower()  # Default to 'buy' if missing
                side = self.convert_exchange_side_to_side(side_str)

                # Append the order update item
                updates.append(
                    OrderUpdateItem(
                        symbol=self._symbols_to_trading_pairs_table[item["instId"]],
                        order_id=item["orderId"],
                        side=side,
                        order_type=order_type,
                        price=fill_price,
                        qty=true_size,
                        tif=tif,
                        order_status=order_status,
                        custom_order_id=item.get("clientOid", ""),
                        cum_exec_qty=acc_base_volume,
                        cum_exec_fee=fill_fee,
                        cum_exec_value=cum_exec_value,
                        closed_pnl=0.0,
                        take_profit=0.0,
                        stop_loss=0.0,
                        tp_limit_price=0.0,
                        sl_limit_price=0.0,
                        create_time=cTime,
                        update_time=uTime,
                    )
                )
            except KeyError as e:
                logger.error(f"Missing key {e} in order update item: {item}")
            except ValueError as e:
                logger.error(f"Value error {e} in order update item: {item}")
            except TypeError as e:
                logger.error(f"Type error {e} in order update item: {item}")
            except Exception as e:
                logger.error(f"Unexpected error {e} in order update item: {item}")

        return OrderUpdate(timestamp=ts, updates=updates)

    def convert_exchange_order_type_to_order_type(self, data: str) -> EOrderType:
        mapping = {
            "limit": EOrderType.LIMIT,
            "market": EOrderType.MARKET,
        }
        return mapping[data]

    def convert_exchange_order_status_to_order_status(self, data: str) -> EOrderStatus:
        mapping = {
            "partially_filled": EOrderStatus.PARTIALLY_FILLED,
            "filled": EOrderStatus.FILLED,
            "cancelled": EOrderStatus.CANCELLED,
            "live": EOrderStatus.NEW,
        }
        return mapping.get(data, EOrderStatus.UNKNOWN)

    def convert_exchange_order_category_to_order_category(
        self, data: str
    ) -> EOrderCategory:
        return NotImplemented

    def convert_exchange_tif_to_tif(self, data: str) -> ETimeInForce:
        mapping = {
            "gtc": ETimeInForce.GTC,
            "ioc": ETimeInForce.IOC,
            "fok": ETimeInForce.FOK,
        }
        return mapping[data]

    def convert_exchange_side_to_side(self, data: str) -> ESide:
        mapping = {"sell": ESide.SELL, "buy": ESide.BUY}
        return mapping[data]

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
        return mapping[order_type]

    def convert_tif_to_exchange_tif(self, tif: ETimeInForce) -> str:
        mapping = {
            ETimeInForce.GTC: "gtc",
            ETimeInForce.IOC: "ioc",
            ETimeInForce.FOK: "fok",
        }
        return mapping[tif]

    def convert_order_category_to_exchange_category(
        self, order_category: EOrderCategory
    ) -> str:
        """Not needed for now for bitget"""
        return NotImplemented

    def convert_order_side_to_exchange_side(self, side: ESide) -> str:
        mapping = {ESide.BUY: "buy", ESide.SELL: "sell"}
        return mapping[side]
