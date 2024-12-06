import asyncio
import hashlib
import hmac
import time
from typing import Any, Dict, List, Mapping, Optional, cast

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
from ttxt_v2.core.web.data_types import RESTMethod, WSRequest
from ttxt_v2.utils.logger import logger

from .gate_auth import GateAuth


class GateIO(ConnectorBase):
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

    BOOK_CHAN = "spot.order_book_update"
    CANDLE_CHAN = "spot.candlesticks"
    TRADES_CHAN = "spot.trades"
    LOGIN_CHAN = "spot.login"
    USER_ORDERS_CHAN = "spot.orders"
    USER_TRADES_CHAN = "spot.usertrades"
    USER_BALANCE_CHAN = "spot.balances"
    ORDER_PLACE_CHAN = "spot.order_place"
    ORDER_CANCEL_CHAN = "spot.order_cancel"
    PING_CHAN = "spot.ping"
    SUBSCRIBE_OP = "subscribe"
    UNSUBSCRIBE_OP = "unsubscribe"
    API_OP = "api"
    EXCHANGE = "gate_io"

    def __init__(
        self,
        config: Optional[ConnectorConfig] = None,
        public_queue: Optional[IQueue] = None,
        signal_queue: Optional[IQueue] = None,
        api_key: str = "",
        api_secret: str = "",
    ):
        """
        Initializes the GateIO connector with the given configuration, public queue, API key, and secret.

        Args:
            config (ConnectorConfig): Configuration for the connector.
            public_queue (IQueue): Queue for public data streams.
            api_key (str): The API key for authentication.
            api_secret (str): The secret key for authentication.
        """
        super().__init__(config, public_queue, signal_queue, api_key, api_secret)

    def is_ws_trading_enabled(self) -> bool:
        return True

    async def _fetch_orderbook_and_send_for_processing(self, pair: TradingPair):
        ob = await self.fetch_orderbook(self._trading_pairs_to_symbols_table[pair])
        self._update_orderbooks(ob)
        ob_ev = BaseEvent(
            event_type=EventType.OB_EVENT,
            payload=Event[Orderbook](
                header=MessageHeader(
                    exchange=self.EXCHANGE, timestamp=int(time.time())
                ),
                data=ob,
            ),
        )
        if self._public_queue_stream is not None:
            await self.publish_to_queue(self._public_queue_stream, ob_ev)
        if self._recorder is not None:
            await self._recorder.queue.publish(ob_ev)

    async def _subscribe_to_public_stream(self):
        assert self._public_ws is not None, "Public WS cannot be None"

        # INFO: Subscribe to public ws streams for updates
        sub_reqs = self._create_public_ws_subscription_request()
        for req in sub_reqs:
            await self._public_ws.send(req)

        # INFO: Obtain orderbooks first and send them in the queue for processing
        for ticker in self._trading_pairs_to_symbols_table:
            await self._fetch_orderbook_and_send_for_processing(ticker)

    async def _subscribe_to_trade_stream(self):
        pass

    async def _subscribe_to_private_stream(self):
        assert (
            self._private_ws is not None and self._private_ws.connected
        ), "Private WS cannot be None and has to be connected"
        try:
            subscribe_user_orders_payload: WSJSONRequest = WSJSONRequest(
                payload={
                    "time": int(time.time()),
                    "channel": self.USER_ORDERS_CHAN,
                    "event": self.SUBSCRIBE_OP,
                    "payload": ["!all"],
                },
                is_auth_required=True,
            )
            subscribe_user_trades_payload: WSJSONRequest = WSJSONRequest(
                payload={
                    "time": int(time.time()),
                    "channel": self.USER_TRADES_CHAN,
                    "event": self.SUBSCRIBE_OP,
                    "payload": ["!all"],
                },
                is_auth_required=True,
            )
            subscribe_balance_payload: WSJSONRequest = WSJSONRequest(
                payload={
                    "time": int(time.time()),
                    "channel": self.USER_BALANCE_CHAN,
                    "event": self.SUBSCRIBE_OP,
                },
                is_auth_required=True,
            )

            await self._private_ws.send(subscribe_user_orders_payload)
            await self._private_ws.send(subscribe_user_trades_payload)
            await self._private_ws.send(subscribe_balance_payload)
        except Exception as e:
            logger.error(f"Error when subscribing to private stream: {e}")

    async def _process_market_data(self, response: WSResponse) -> Optional[BaseEvent]:
        try:
            message = response.data
            chan = message.get("channel", "")
            if self.BOOK_CHAN in chan:
                event_type = message.get("event", "")
                if event_type == "subscribe":
                    return None
                normalized_book = self.convert_exchange_orderbook_to_orderbook(message)

                active_ob = self._ob_map[normalized_book.trading_pair]

                # INFO: update sequence matches so just send the update
                end_seq = message.get("result", {}).get("u", 0)
                if normalized_book.seq <= active_ob.seq + 1:
                    normalized_book.seq = end_seq
                    active_ob.update(normalized_book)
                    event = BaseEvent(
                        event_type=EventType.OB_EVENT,
                        payload=Event[Orderbook](
                            header=MessageHeader(
                                exchange=self.EXCHANGE, timestamp=int(time.time())
                            ),
                            data=normalized_book,
                        ),
                    )
                else:
                    # INFO: refetch orderbook and send snapshot
                    self._ob_map[active_ob.trading_pair] = await self.fetch_orderbook(
                        self._trading_pairs_to_symbols_table[
                            normalized_book.trading_pair
                        ]
                    )
                    event = BaseEvent(
                        event_type=EventType.OB_EVENT,
                        payload=Event[Orderbook](
                            header=MessageHeader(
                                exchange=self.EXCHANGE, timestamp=int(time.time())
                            ),
                            data=active_ob,
                        ),
                    )
                return event
            elif self.CANDLE_CHAN in chan:
                event_type = message.get("event", "")
                if event_type == "subscribe":
                    return None
                normalized_candle = self.convert_exchange_klines_to_klines(message)
                event = BaseEvent(
                    event_type=EventType.KL_EVENT,
                    payload=Event[Kline](
                        header=MessageHeader(
                            exchange=self.EXCHANGE, timestamp=int(time.time())
                        ),
                        data=normalized_candle,
                    ),
                )
                return event
            elif self.TRADES_CHAN in chan:
                event_type = message.get("event", "")
                if event_type == "subscribe":
                    return None
                normalized_trades = self.convert_exchange_trades_to_trades(message)
                event = BaseEvent(
                    event_type=EventType.MT_EVENT,
                    payload=Event[MarketTrades](
                        header=MessageHeader(
                            exchange=self.EXCHANGE, timestamp=int(time.time())
                        ),
                        data=normalized_trades,
                    ),
                )
                return event
        except Exception as e:
            logger.error(f"Error when processing public market data: %s", str(e))
        return None

    async def _process_http_signals(self, event: BaseEvent) -> Optional[BaseEvent]:
        """No need to implement since exchange supports WS trading"""
        return None

    def _process_trade_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Processes trade data received from the WebSocket stream by converting order acknowledgments
        into the OrderAck dataclass and wrapping it into a BaseEvent.

        Args:
            response (WSResponse): The WebSocket response containing trade data.

        Returns:
            Optional[BaseEvent]: The converted BaseEvent containing the OrderAck, or None if processing fails.
        """
        assert self._config is not None, "Config cannot be None"
        try:
            msg_data = response.data
            hdrs = msg_data.get("header", {})
            event = hdrs.get("channel", "")
            if "spot.pong" in event or "spot.pong" in msg_data.get("channel", ""):
                logger.debug(f"Received pong: {msg_data}")
                return None

            if "spot.login" in event:
                return None

            if hdrs.get("status", "400") != "200":
                logger.error(f"Order ack error: {msg_data}")
                return None

            # Check if acknowledgment is present and true
            if not msg_data.get("ack", True):
                logger.warning(f"Trade response not acknowledged: {str(msg_data)}")
                return None

            # Use the converter to create OrderAck
            order_ack = self.convert_exchange_order_ack_to_order_ack(msg_data)
            # If order_id is empty, skip creating the event
            if not order_ack.order_id:
                logger.warning(f"Order ID is missing in trade data: {str(msg_data)}")
                return None

            event = BaseEvent(
                event_type=EventType.ORDER_ACK_EVENT,
                payload=Event[OrderAck](
                    header=MessageHeader(
                        exchange=self._config.exchange, timestamp=order_ack.timestamp
                    ),
                    data=order_ack,
                ),
            )

            return event

        except Exception as e:
            logger.error(
                f"Error processing trade data: {str(e)}. WSResponse: {str(response.data)}"
            )
            return None

    def _process_private_data(self, response: WSResponse) -> Optional[List[BaseEvent]]:
        assert self._config is not None, "Cannot process private data if config is None"
        try:
            msg_data = response.data
            chan = msg_data["channel"]
            event = msg_data.get("event", "")
            if "pong" in chan:
                logger.info(f"Receive a private pong: {msg_data}")
                return None

            if "subscribe" in event:
                logger.debug(f"Received private subscription response {msg_data}")
                return None

            if chan not in [
                self.USER_BALANCE_CHAN,
                self.USER_TRADES_CHAN,
                self.USER_ORDERS_CHAN,
            ]:
                logger.warning(
                    f"The channel: {chan} is not any of the known private channels"
                )
                return None

            if chan == self.USER_BALANCE_CHAN:
                wal_ev = self.convert_exchange_wallet_update_to_wallet(msg_data)
                return [
                    BaseEvent(
                        event_type=EventType.WALLET_UPDATE_EVENT,
                        payload=Event[Wallet](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=int(time.time()),
                            ),
                            data=wal_ev,
                        ),
                    )
                ]
            elif chan == self.USER_ORDERS_CHAN:
                order_up = self.convert_exchange_order_update_to_order_update(msg_data)
                return [
                    BaseEvent(
                        event_type=EventType.ORDER_UPDATE_EVENT,
                        payload=Event[OrderUpdate](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=int(time.time()),
                            ),
                            data=order_up,
                        ),
                    )
                ]
            elif chan == self.USER_TRADES_CHAN:
                logger.warning(f"Not implemented yet. Event: {msg_data}")
                return None
            else:
                return None
        except Exception as e:
            logger.error(f"Error processing private data: {e}")

        return None

    def _process_signal_event(self, event: BaseEvent) -> List[WSRequest]:
        try:
            login_req = self._convert_login_to_ws_request()
            if event.event_type == EventType.CREATE_ORDER_EVENT:
                create_req = self.convert_create_order_to_ws_request(
                    cast(CreateOrder, event.payload.data)
                )
                return [login_req, create_req]
            elif event.event_type == EventType.CANCEL_ORDER_EVENT:
                cancel_req = self.convert_cancel_order_to_ws_request(
                    cast(CancelOrder, event.payload.data)
                )
                return [login_req, cancel_req]
            else:
                raise RuntimeError("Ammend order is not implemented")
        except Exception as e:
            logger.error(f"Exception occured: {e}")
        return []

    @property
    def authenticator(self) -> BaseAuth:
        assert self._api_key is not None, "API KEY cannot be None for auth"
        assert self._api_secret is not None, "API_SECRET cannot be None for auth"
        return GateAuth(api_key=self._api_key, api_secret=self._api_secret)

    def _create_web_assistant_factory(self) -> WebAssitantFactory:
        return WebAssitantFactory(auth=self._auth)

    def _get_connector_urls(self) -> ConnectorURL:
        return ConnectorURL(
            PUBLIC_SPOT="wss://api.gateio.ws/ws/v4/",
            PUBLIC_LINEAR="",
            PUBLIC_INVERSE="",
            TRADE="wss://api.gateio.ws/ws/v4/",
            BASE="https://api.gateio.ws/api/v4",
            PRIVATE="wss://api.gateio.ws/ws/v4/",
        )

    async def pinger(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            await super().pinger()
            assert self._public_ws is not None, "Public WS cannot be none"
            await asyncio.sleep(3)
            while self._public_ws.connected:
                req = WSJSONRequest(
                    payload={"time": int(time.time()), "channel": self.PING_CHAN}
                )
                logger.debug("Sending public_ws ping: %s", str(req))
                await self._public_ws.send(req)
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.error(f"Stopping gate_io public ping coroutine")

    async def pinger_trade(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            await super().pinger()
            assert self._trade_ws is not None, "Trade WS cannot be none"
            await asyncio.sleep(3)
            while self._trade_ws.connected:
                req = WSJSONRequest(
                    payload={"time": int(time.time()), "channel": self.PING_CHAN}
                )
                logger.debug("Sending trade_ws ping: %s", str(req))
                await self._trade_ws.send(req)
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.error(f"Stopping gate_io trade ping coroutine")

    async def pinger_private(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            await super().pinger()
            assert self._private_ws is not None, "Private WS cannot be none"
            await asyncio.sleep(3)
            while self._private_ws.connected:
                req = WSJSONRequest(
                    payload={"time": int(time.time()), "channel": self.PING_CHAN}
                )
                logger.debug("Sending private_ws ping: %s", str(req))
                await self._private_ws.send(req)
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.error(f"Stopping gate_io private ping coroutine")

    def _create_public_ws_subscription_request(self) -> List[WSJSONRequest]:
        """
        Creates subscription requests for the public WebSocket stream.

        Returns:
            List[WSJSONRequest]: The list of WebSocket subscription requests.
        """
        assert self._config is not None, "Config cannot be None"
        ob_config = self._config.ob_config
        ws_reqs = []
        if ob_config is not None:
            for ticker in ob_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker]
                # HACK: for now 100ms is the best freqeuncy
                ws_reqs.append(
                    WSJSONRequest(
                        {
                            "time": int(time.time()),
                            "channel": self.BOOK_CHAN,
                            "event": self.SUBSCRIBE_OP,
                            "payload": [symb, "100ms"],
                        }
                    )
                )

        mt_config = self._config.mt_config
        if mt_config is not None:
            args: List[str] = []
            for ticker in mt_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker]
                args.append(symb)

            ws_reqs.append(
                WSJSONRequest(
                    {
                        "time": int(time.time()),
                        "channel": self.TRADES_CHAN,
                        "event": self.SUBSCRIBE_OP,
                        "payload": args,
                    }
                )
            )

        kl_config = self._config.kl_config
        if kl_config is not None:
            for ticker in kl_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker]
                ws_reqs.append(
                    WSJSONRequest(
                        {
                            "time": int(time.time()),
                            "channel": self.CANDLE_CHAN,
                            "event": self.SUBSCRIBE_OP,
                            "payload": ["1m", symb],
                        }
                    )
                )

        logger.debug(f"WS subscriptions reqs for GateIO: {str(ws_reqs)}")
        return ws_reqs

    def _gen_symbols_table(self) -> Dict[str, TradingPair]:
        res = {}
        for ticker in self._config.ob_config.tickers:
            symb = f"{ticker.base}_{ticker.quote}"
            res[symb] = ticker
        return res

    def _gen_trading_pairs_table(self) -> Dict[TradingPair, str]:
        res = {}
        for ticker in self._config.ob_config.tickers:
            res[ticker] = f"{ticker.base}_{ticker.quote}"
        return res

    def _gen_request_headers(self) -> Mapping[str, Any]:
        return NotImplemented

    """
    REST API
    """

    async def fetch_orderbook(self, ticker: str, depth: int = 50) -> Orderbook:
        response = await self.api_request(
            path_url="/spot/order_book",
            method=RESTMethod.GET,
            params={"currency_pair": ticker, "limit": depth, "with_id": "true"},
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        ob = self._convert_http_spot_ob_to_ob(
            self._symbols_to_trading_pairs_table[ticker], response
        )
        return ob

    async def get_server_time_ms(self) -> int:
        res = await self.api_request("/spot/time")
        return res.get("server_time", 0)

    async def fetch_wallet_balance(
        self, account_type: EAccountType = EAccountType.UNIFIED
    ) -> Wallet:
        # HACK: for now only spot
        res = await self.api_request(
            path_url="/spot/accounts", method=RESTMethod.GET, is_auth_required=True
        )
        wallet: Wallet = Wallet()
        for bal in res["res"]:
            assert isinstance(bal, Dict), "Balance should be a dictionary"
            coin_bal = CoinBalance(
                total=float(bal.get("available", "0")),
                available=float(bal.get("available", "0")),
            )
            wallet.wallet[bal.get("currency", "")] = coin_bal
        wallet.timestamp = int(time.time())
        return wallet

    async def fetch_klines(
        self,
        symbol: TradingPair,
        interval: str,
        start_time: str,
        end_time: str,
        category: EOrderCategory = EOrderCategory.SPOT,
        limit: int = 1000,
    ) -> List[Kline]:
        return await super().fetch_klines(
            symbol, interval, start_time, end_time, category, limit
        )

    async def fetch_instrument_info(
        self, pair: TradingPair, category: EOrderCategory = EOrderCategory.SPOT
    ) -> List[InstrumentInfo]:
        return []

    async def cancel_all_orders(
        self,
        order_category: EOrderCategory = EOrderCategory.SPOT,
        symbol: Optional[TradingPair] = None,
    ) -> Dict[str, Any]:

        return NotImplemented

    """
    Normalizer API
    """

    def _convert_login_to_ws_request(self) -> WSRequest:
        """
        Creates a WebSocket login request for Gate.io.

        Returns:
            WSRequest: The login request to be sent to the exchange.
        """
        data_time = int(time.time())
        param_json = ""
        message = "%s\n%s\n%s\n%d" % ("api", "spot.login", param_json, data_time)
        req_id = f"{int(time.time() * 1000)}-1"

        data_param = {
            "time": data_time,
            "channel": "spot.login",
            "event": "api",
            "payload": {
                "req_id": req_id,
                "api_key": self._api_key,
                "timestamp": f"{data_time}",
                "signature": hmac.new(
                    self._api_secret.encode("utf8"),
                    message.encode("utf8"),
                    hashlib.sha512,
                ).hexdigest(),
            },
        }

        ws_request = WSJSONRequest(payload=data_param)
        return ws_request

    def _convert_http_spot_ob_to_ob(self, ticker: TradingPair, data: Dict) -> Orderbook:
        update_type = EUpdateType.SNAPSHOT
        trading_pair = ticker
        bids = [
            OrderbookEntry(price=float(bid[0]), qty=float(bid[1]))
            for bid in data.get("bids", [])
        ]
        asks = [
            OrderbookEntry(price=float(ask[0]), qty=float(ask[1]))
            for ask in data.get("asks", [])
        ]
        seq = data.get("id", 1)
        timestamp = data.get("update", 1)
        return Orderbook(
            update_type=update_type,
            trading_pair=trading_pair,
            bids=bids,
            asks=asks,
            timestamp=timestamp,
            seq=seq,
        )

    def convert_exchange_orderbook_to_orderbook(self, data: Dict) -> Orderbook:
        res_obj = data.get("result", {})
        symbol = res_obj.get("s", "")

        update_type = EUpdateType.DELTA
        pair = self._symbols_to_trading_pairs_table[symbol]

        bids = [
            OrderbookEntry(price=float(bid[0]), qty=float(bid[1]))
            for bid in res_obj.get("b", [])
        ]
        asks = [
            OrderbookEntry(price=float(ask[0]), qty=float(ask[1]))
            for ask in res_obj.get("a", [])
        ]
        timestamp = res_obj.get("t", 1)
        seq = res_obj.get("U", 1)
        return Orderbook(
            update_type=update_type,
            trading_pair=pair,
            bids=bids,
            asks=asks,
            timestamp=timestamp,
            seq=seq,
        )

    def convert_exchange_klines_to_klines(self, data: Dict) -> Kline:
        res_obj = data.get("result", {})
        symb = res_obj.get("n", "")
        for ticker in self._symbols_to_trading_pairs_table:
            if ticker in symb:
                symb = ticker
                break
        confirm = res_obj["w"]

        pair = self._symbols_to_trading_pairs_table[symb]
        open = float(res_obj.get("o", 0.0))
        close = float(res_obj.get("c", 0.0))
        high = float(res_obj.get("h", 0.0))
        low = float(res_obj.get("l", 0.0))
        volume = float(res_obj.get("v", 0.0))
        start = int(res_obj.get("t", 0))
        time = int(data.get("time_ms", 0))
        return Kline(
            trading_pair=pair,
            open=open,
            close=close,
            high=high,
            low=low,
            volume=volume,
            start=start,
            timestamp=time,
            confirm=confirm,
        )

    def convert_exchange_trades_to_trades(self, data: Dict) -> MarketTrades:
        # INFO: Always has only 1 trade not an array
        res_obj = data.get("result", {})
        exch_side = res_obj.get("side", "")

        price = float(res_obj.get("price", 0.0))
        qty = float(res_obj.get("amount", 0.0))
        side = self.convert_exchange_side_to_side(exch_side)
        trades = [MarketTradesData(price=price, qty=qty, side=side)]
        pair = self._symbols_to_trading_pairs_table[res_obj.get("currency_pair", "")]
        return MarketTrades(trading_pair=pair, trades=trades)

    def convert_exchange_order_ack_to_order_ack(self, data: dict) -> OrderAck:
        """
        Converts the exchange's order acknowledgment response to the internal OrderAck dataclass.

        Args:
            data (dict): The order acknowledgment response from Bybit.

        Returns:
            OrderAck: The internal representation of the order acknowledgment.
        """
        operation = data.get("header", {}).get("channel", "")
        order_ack = OrderAck(order_id="", ack_type=EAckType.UNKNOWN, timestamp=0)

        if operation == "spot.order_place":
            # Order Creation Acknowledgment
            order_ack.ack_type = EAckType.CREATE
            order_ack.order_id = (
                data.get("data", {})
                .get("result", {})
                .get("req_param", {})
                .get("text", "")
            )
            if order_ack.order_id == "":
                order_ack.order_id = (
                    data.get("data", {}).get("result", {}).get("text", "")
                )

            timestamp_str = data.get("header", {}).get("response_time", "0")
            order_ack.timestamp = int(timestamp_str) if timestamp_str.isdigit() else 0

        elif operation == "spot.order_cancel":
            # Order Cancellation Acknowledgment
            order_ack.ack_type = EAckType.CANCEL
            order_ack.order_id = data.get("data", {}).get("result", {}).get("text", "")
            if order_ack.order_id == "":
                order_ack.order_id = (
                    data.get("data", {}).get("result", {}).get("text", "")
                )
            timestamp_str = data.get("header", {}).get("response_time", "0")
            order_ack.timestamp = int(timestamp_str) if timestamp_str.isdigit() else 0

        else:
            logger.warning(f"Unidentified operation type: {operation}")
            order_ack.ack_type = EAckType.UNKNOWN
            order_ack.order_id = ""
            order_ack.timestamp = int(time.time() * 1000)  # Current time in ms

        return order_ack

    def convert_exchange_wallet_update_to_wallet(self, data: dict) -> Wallet:
        """
        Converts the exchange's wallet update response to the internal Wallet dataclass.

        Args:
            data (dict): The wallet update response from Gate.io.

        Returns:
            Wallet: The internal representation of the wallet.
        """
        try:
            timestamp = int(data.get("time", 0))  # Unix timestamp in seconds
            wallet_dict: Dict[str, CoinBalance] = {}

            for balance in data.get("result", []):
                currency = balance.get("currency")
                if not currency:
                    logger.warning("Missing currency in balance update.")
                    continue

                try:
                    total = float(balance.get("total", "0"))
                    available = float(balance.get("available", "0"))
                    # Gate.io does not provide PnL in the balance update
                    realised_pnl = 0.0
                    unrealised_pnl = 0.0

                    wallet_dict[currency] = CoinBalance(
                        total=total,
                        available=available,
                        realised_pnl=realised_pnl,
                        unrealised_pnl=unrealised_pnl,
                    )
                except ValueError as ve:
                    logger.error(f"Error parsing balance for {currency}: {ve}")
                    continue

            return Wallet(wallet=wallet_dict, timestamp=timestamp)

        except Exception as e:
            logger.error(f"Failed to convert wallet update: {e}")
            raise

    def convert_exchange_order_update_to_order_update(self, data: dict) -> OrderUpdate:
        """
        Converts the exchange's order update response to the internal OrderUpdate dataclass.

        Args:
            data (dict): The order update response from Gate.io.

        Returns:
            OrderUpdate: The internal representation of the order updates.
        """
        try:
            timestamp = int(data.get("time", 0))  # Unix timestamp in seconds
            updates: List[OrderUpdateItem] = []

            for order in data.get("result", []):
                try:
                    symbol = order.get("currency_pair")
                    if not symbol:
                        logger.warning("Missing currency_pair in order update.")
                        continue

                    order_id = order.get("id")
                    if not order_id:
                        logger.warning("Missing order ID in order update.")
                        continue

                    side = self.convert_exchange_side_to_side(
                        order.get("side", "").lower()
                    )
                    order_type = self.convert_exchange_order_type_to_order_type(
                        order.get("type", "").lower()
                    )
                    price = float(order.get("price", "0"))
                    qty = float(order.get("amount", "0"))
                    tif = self.convert_exchange_tif_to_tif(
                        order.get("time_in_force", "").lower()
                    )
                    order_status = self.convert_exchange_order_status_to_order_status(
                        order.get("finish_as", "").lower()
                    )
                    custom_order_id = order.get("text", "")
                    cum_exec_qty = float(order.get("filled_total", "0"))
                    avg_deal_price = float(order.get("avg_deal_price", "0"))
                    cum_exec_value = avg_deal_price * cum_exec_qty
                    cum_exec_fee = float(order.get("fee", "0"))

                    # The following fields are not provided by Gate.io's order update response
                    # Set them to default values or handle accordingly
                    closed_pnl = 0.0
                    take_profit = 0.0
                    stop_loss = 0.0
                    tp_limit_price = 0.0
                    sl_limit_price = 0.0

                    create_time = int(order.get("create_time", "0"))
                    update_time = int(order.get("update_time", "0"))

                    update_item = OrderUpdateItem(
                        symbol=self._symbols_to_trading_pairs_table[symbol],
                        order_id=order_id,
                        side=side,
                        order_type=order_type,
                        price=price,
                        qty=qty,
                        tif=tif,
                        order_status=order_status,
                        custom_order_id=custom_order_id,
                        cum_exec_qty=cum_exec_qty,
                        cum_exec_value=cum_exec_value,
                        cum_exec_fee=cum_exec_fee,
                        closed_pnl=closed_pnl,
                        take_profit=take_profit,
                        stop_loss=stop_loss,
                        tp_limit_price=tp_limit_price,
                        sl_limit_price=sl_limit_price,
                        create_time=create_time,
                        update_time=update_time,
                    )

                    updates.append(update_item)

                except Exception as order_exc:
                    logger.error(f"Error processing order update: {order_exc}")
                    continue

            return OrderUpdate(timestamp=timestamp, updates=updates)

        except Exception as e:
            logger.error(f"Failed to convert order update: {e}")
            raise

    def convert_exchange_order_type_to_order_type(self, data: str) -> EOrderType:
        mapping = {
            "limit": EOrderType.LIMIT,
            "market": EOrderType.MARKET,
        }
        order_type = mapping.get(data.lower())
        if order_type is None:
            raise RuntimeError(f"Unknown order type: {data}")
        return order_type

    def convert_exchange_order_status_to_order_status(self, data: str) -> EOrderStatus:
        mapping = {
            "open": EOrderStatus.NEW,
            "filled": EOrderStatus.FILLED,
            "cancelled": EOrderStatus.CANCELLED,
        }
        status = mapping.get(data.lower())
        if status is None:
            raise RuntimeError(f"Unknown order status: {data}")
        return status

    def convert_exchange_order_category_to_order_category(
        self, data: str
    ) -> EOrderCategory:
        return NotImplemented

    def convert_exchange_tif_to_tif(self, data: str) -> ETimeInForce:
        mapping = {
            "gtc": ETimeInForce.GTC,
            "ioc": ETimeInForce.IOC,
        }
        tif = mapping.get(data.lower())
        if tif is None:
            raise RuntimeError(f"Unknown time in force: {data}")
        return tif

    def convert_exchange_side_to_side(self, data: str) -> ESide:
        if data == "buy":
            return ESide.BUY
        if data == "sell":
            return ESide.SELL
        raise RuntimeError(f"Unknown side argument: {data}")

    """
    Denormalizer API
    """

    def convert_create_order_to_ws_request(
        self, create_order: CreateOrder
    ) -> WSRequest:
        """
        Converts a CreateOrder signal into Gate.io WebSocket requests, including login.

        Args:
            create_order (CreateOrder): The create order signal.

        Returns:
            WSRequest: The create order request.
        """

        # Create Order Request
        event = "api"
        channel = self.ORDER_PLACE_CHAN  # e.g., "spot.order_place"
        req_id = f"create-{int(time.time() * 1000)}"

        if (
            create_order.client_order_id[:2] != "t-"
            and len(create_order.client_order_id) > 28
        ):
            raise RuntimeError(
                "Invalid order id should start with t- and be less than or equal to 28 bytes"
            )
        req_param = {
            "text": create_order.client_order_id,  # Must start with 't-'
            "currency_pair": self._trading_pairs_to_symbols_table[
                create_order.trading_pair
            ],
            "type": self.convert_order_type_to_exchange_order_type(
                create_order.order_type
            ),
            "account": "spot",  # Assumes spot account
            "side": self.convert_order_side_to_exchange_side(create_order.side),
            "amount": str(create_order.qty),  # Quantity as string
            "price": (
                str(create_order.price) if create_order.price is not None else ""
            ),
        }

        if create_order.order_type == EOrderType.LIMIT:
            req_param.update(
                {"time_in_force": self.convert_tif_to_exchange_tif(create_order.tif)}
            )
        # Ensure that 'price' is provided for limit orders
        if create_order.order_type == EOrderType.LIMIT and not create_order.price:
            raise ValueError("Price must be provided for limit orders.")

        timestamp = int(time.time())

        order_request_payload = {
            "time": timestamp,
            "channel": channel,
            "event": event,
            "payload": {"req_id": req_id, "req_param": req_param, "req_header": {}},
        }

        order_request = WSJSONRequest(payload=order_request_payload)

        return order_request

    def convert_cancel_order_to_ws_request(
        self, cancel_order: CancelOrder
    ) -> WSRequest:
        """
        Converts a CancelOrder signal into Gate.io WebSocket requests, including login.

        Args:
            cancel_order (CancelOrder): The cancel order signal.

        Returns:
            List[WSRequest]: A list containing the login request and the cancel order request.
        """

        # Create Cancel Order Request
        event = "api"
        channel = self.ORDER_CANCEL_CHAN
        req_id = f"cancel-{int(time.time()*1000)}"
        req_param = {
            "id": cancel_order.client_order_id,
            "currency_pair": self._trading_pairs_to_symbols_table[
                cancel_order.trading_pair
            ],
        }

        timestamp = int(time.time())

        cancel_request_payload = {
            "time": timestamp,
            "id": req_id,  # Optional request id
            "channel": channel,
            "event": event,
            "payload": {
                "req_id": req_id,
                "req_param": req_param,
            },
        }

        cancel_request = WSJSONRequest(payload=cancel_request_payload)
        return cancel_request

    def convert_amend_order_to_ws_request(self, amend_order: AmendOrder) -> WSRequest:
        return NotImplemented

    def convert_order_type_to_exchange_order_type(self, order_type: EOrderType) -> str:
        if order_type == EOrderType.LIMIT:
            return "limit"
        if order_type == EOrderType.MARKET:
            return "market"
        raise RuntimeError("UNKNOWN order type")

    def convert_tif_to_exchange_tif(self, tif: ETimeInForce) -> str:
        if tif == ETimeInForce.GTC:
            return "gtc"
        if tif == ETimeInForce.IOC:
            return "ioc"
        raise RuntimeError("Unsupported time in force")

    def convert_order_category_to_exchange_category(
        self, order_category: EOrderCategory
    ) -> str:
        return NotImplemented

    def convert_order_side_to_exchange_side(self, side: ESide) -> str:
        if side == ESide.BUY:
            return "buy"
        if side == ESide.SELL:
            return "sell"
