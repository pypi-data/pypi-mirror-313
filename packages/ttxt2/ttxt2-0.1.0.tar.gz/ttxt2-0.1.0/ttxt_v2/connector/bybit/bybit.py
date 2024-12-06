import asyncio
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
from ttxt_v2.utils.date_time import (
    convert_date_to_utc_timestamp,
    timestamp_to_human_readable,
)
from ttxt_v2.utils.logger import logger
from ttxt_v2.utils.math_utils import get_decimal_places

from .bybit_auth import BybitAuth


class Bybit(ConnectorBase):
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

    CREATE_OP = "order.create"
    CANCEL_OP = "order.cancel"
    AUTH_OP = "auth"
    PONG_OP = "pong"
    SUBSCRIBE_OP = "subscribe"
    ORDER_CHAN = "order"
    WALLET_CHAN = "wallet"
    EXECUTION_CHAN = "execution.fast"
    POSITION_CHAN = "position"

    def __init__(
        self,
        config: Optional[ConnectorConfig] = None,
        public_queue: Optional[IQueue] = None,
        signal_queue: Optional[IQueue] = None,
        api_key: str = "",
        api_secret: str = "",
    ):
        """
        Initializes the Bybit connector with the given configuration, public queue, API key, and secret.

        Args:
            config (ConnectorConfig): Configuration for the connector.
            public_queue (IQueue): Queue for public data streams.
            api_key (str): The API key for authentication.
            api_secret (str): The secret key for authentication.
        """
        super().__init__(config, public_queue, signal_queue, api_key, api_secret)

    def is_ws_trading_enabled(self) -> bool:
        return True

    async def _subscribe_to_public_stream(self):
        """
        Subscribes to the public WebSocket stream by sending subscription requests.
        """
        subscription_reqs = self._create_public_ws_subscription_request()
        assert self._public_ws is not None, "Public ws cannot be None"
        for req in subscription_reqs:
            await self._public_ws.send(req)

    async def _subscribe_to_trade_stream(self):
        empty_req = WSJSONRequest(payload={"": ""})
        req = await self._auth.ws_authenticate(empty_req)
        assert self._trade_ws is not None, "Trade WS cannot be NONE"
        await self._trade_ws.send(req)

    async def _subscribe_to_private_stream(self):
        empty_req = WSJSONRequest(payload={"": ""})
        req = await self._auth.ws_authenticate(empty_req)
        assert self._private_ws is not None, "Private WS cannot be NONE"
        await self._private_ws.send(req)
        args = [
            self.ORDER_CHAN,
            self.WALLET_CHAN,
            self.POSITION_CHAN,
            self.EXECUTION_CHAN,
        ]
        await self._private_ws.send(
            WSJSONRequest({"op": self.SUBSCRIBE_OP, "args": args})
        )

    async def _process_market_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Processes market data received from the WebSocket stream.

        Args:
            response (WSResponse): The WebSocket response containing market data.
        """
        assert self._config is not None, "Config cannot be None"
        try:
            message = response.data
            op = message.get("op", "")
            if len(op) > 0 and op == self.SUBSCRIBE_OP:
                logger.debug(f"Subscription response: {str(op)}")
                return
            topic = message.get("topic", "")

            if "orderbook" in topic:
                normalized_orderbook = self.convert_exchange_orderbook_to_orderbook(
                    message
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
            elif "kline" in topic:
                normalized_kline = self.convert_exchange_klines_to_klines(message)
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
            elif "publicTrade" in topic:
                normalized_trades = self.convert_exchange_trades_to_trades(message)
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
            else:
                logger.warning(f"Unknown message topic: {topic}")
                return None
        except Exception as e:
            logger.error(
                f"Error processing market data response: {str(e)}. WSResponse: {str(response.data)}"
            )

    def _process_trade_data(self, response: WSResponse) -> Optional[BaseEvent]:
        assert self._config is not None, "Config cannot be None"
        try:
            msg_data = response.data
            if msg_data["retCode"] != 0:
                logger.warning(f"Trade response contains an error: {str(msg_data)}")
                return None

            operation = msg_data["op"]
            if operation == self.AUTH_OP:
                logger.info(f"Authentication successful: {str(msg_data)}")
                return None
            if operation == self.PONG_OP:
                logger.info(f"Received pong: {str(msg_data)}")
                return None

            if operation in ["order.create", "order.cancel"]:
                order_ack = self.convert_exchange_order_ack_to_order_ack(msg_data)
                return BaseEvent(
                    event_type=EventType.ORDER_ACK_EVENT,
                    payload=Event[OrderAck](
                        header=MessageHeader(
                            exchange=self._config.exchange,
                            timestamp=order_ack.timestamp,
                        ),
                        data=order_ack,
                    ),
                )
            else:
                logger.info(f"Unknown operation: {operation}")

        except Exception as e:
            logger.error(f"Error processing trade response: {str(e)}")

    def _process_private_data(self, response: WSResponse) -> Optional[List[BaseEvent]]:
        assert self._config is not None, "Config cannot be None"
        try:
            msg_data = response.data
            topic = msg_data.get("topic", "")
            if len(topic) == 0:
                logger.warning(f"Unknown message to process: {msg_data}")
                return None

            if topic not in [
                self.ORDER_CHAN,
                self.WALLET_CHAN,
                self.EXECUTION_CHAN,
                self.POSITION_CHAN,
            ]:
                logger.warning(
                    f"The topic: {topic} is not in any of the known channels"
                )
                return None

            if topic == self.WALLET_CHAN:
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
            elif topic == self.ORDER_CHAN:
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
            elif topic == self.EXECUTION_CHAN or topic == self.POSITION_CHAN:
                logger.warning(
                    f"Execution and position channels are not implemented yet. Event{msg_data}"
                )
                return None

        except Exception as e:
            logger.error(f"Error processing private response: {str(e)}")

        return None

    def _process_signal_event(self, event: BaseEvent) -> List[WSRequest]:
        """
        Abstract method to process event from the signal event queue and return the WSRequest to send to the exchange.

        Returns:
            WSRequest: Request to be sent to the trade websocket connection.
        """
        if event.event_type == EventType.CREATE_ORDER_EVENT:
            return [
                self.convert_create_order_to_ws_request(
                    cast(CreateOrder, event.payload.data)
                )
            ]
        elif event.event_type == EventType.CANCEL_ORDER_EVENT:
            return [
                self.convert_cancel_order_to_ws_request(
                    cast(CancelOrder, event.payload.data)
                )
            ]
        elif event.event_type == EventType.AMEND_ORDER_EVENT:
            raise RuntimeError("Amend order not implemented yet")

        return [WSJSONRequest(payload={})]

    async def _process_http_signals(self, event: BaseEvent) -> Optional[BaseEvent]:
        """No need to implement since exchange supports WS trading"""
        return None

    @property
    def authenticator(self) -> BaseAuth:
        """
        Returns the authenticator for the connector.

        Returns:
            BaseAuth: The authenticator for the connector.
        """
        assert self._api_key is not None, "API KEY cannot be None for auth"
        assert self._api_secret is not None, "API_SECRET cannot be None for auth"
        return BybitAuth(api_key=self._api_key, api_secret=self._api_secret)

    def _create_web_assistant_factory(self) -> WebAssitantFactory:
        """
        Creates a web assistant factory.

        Returns:
            WebAssitantFactory: The web assistant factory."""
        return WebAssitantFactory(auth=self._auth)

    def _get_connector_urls(self) -> ConnectorURL:
        return ConnectorURL(
            PUBLIC_SPOT="wss://stream.bybit.com/v5/public/spot",
            PUBLIC_LINEAR="wss://stream.bybit.com/v5/public/linear",
            PUBLIC_INVERSE="wss://stream.bybit.com/v5/public/inverse",
            TRADE="wss://stream.bybit.com/v5/trade",
            BASE="https://api.bybit.com",
            PRIVATE="wss://stream.bybit.com/v5/private",
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
                req = WSJSONRequest(payload={"op": "ping"})
                logger.debug("Sending public_ws ping: %s", str(req))
                await self._public_ws.send(req)
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.error(f"Stopping bybit ping coroutine")

    async def pinger_trade(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            await super().pinger_trade()
            assert self._trade_ws is not None, "Trade WS cannot be none"
            await asyncio.sleep(3)
            while self._trade_ws.connected:
                req = WSJSONRequest(payload={"op": "ping"})
                logger.debug("Sending trade_ws ping: %s", str(req))
                await self._trade_ws.send(req)
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.error("Stopping bybit trade WS ping coroutine...")

    async def pinger_private(self):
        """
        Sends periodic ping messages to keep the WebSocket connection alive.
        """
        try:
            await super().pinger_private()
            assert self._private_ws is not None, "Trade WS cannot be none"
            while self._private_ws.connected:
                req = WSJSONRequest(payload={"op": "ping"})
                await self._private_ws.send(req)
                logger.debug("Sending private_ws ping: %s", str(req))
                await asyncio.sleep(20)
        except asyncio.CancelledError:
            logger.error("Stopping bybit trade WS ping coroutine...")

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
            args: List[str] = []
            for ticker in ob_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker]
                arg_str = f"orderbook.{ob_config.depth}.{symb}"
                args.append(arg_str)
            ws_reqs.append(WSJSONRequest({"op": self.SUBSCRIBE_OP, "args": args}))

        mt_config = self._config.mt_config
        if mt_config is not None:
            args: List[str] = []
            for ticker in mt_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker]
                arg_str = f"publicTrade.{symb}"
                args.append(arg_str)
            ws_reqs.append(WSJSONRequest({"op": self.SUBSCRIBE_OP, "args": args}))

        kl_config = self._config.kl_config
        if kl_config is not None:
            args: List[str] = []
            for ticker in kl_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker]
                arg_str = f"kline.{kl_config.timeframe}.{symb}"
                args.append(arg_str)
            ws_reqs.append(WSJSONRequest({"op": self.SUBSCRIBE_OP, "args": args}))

        logger.debug(f"ws subscriptions reqs for bybit: {str(ws_reqs)}")
        return ws_reqs

    def _gen_symbols_table(self) -> Dict[str, TradingPair]:
        assert self._config is not None, "Config cannot be None"
        assert self._config.ob_config is not None, "Config cannot be None"
        res = {}
        # HACK: tickers should be global this is simply stupid
        for ticker in self._config.ob_config.tickers:
            symb = ticker.base + ticker.quote
            res[symb] = ticker
        return res

    def _gen_trading_pairs_table(self) -> Dict[TradingPair, str]:
        assert self._config is not None, "Config cannot be None"
        assert self._config.ob_config is not None, "Config cannot be None"
        res = {}
        for ticker in self._config.ob_config.tickers:
            res[ticker] = ticker.base + ticker.quote
        return res

    def _gen_request_headers(self) -> Mapping[str, Any]:
        # Get current time fix clock drift and remove 1 sec to be sure
        time_cur = time.time_ns() // 1_000_000 - self._clock_drift - 1000
        headers = {
            "X-BAPI-TIMESTAMP": str(time_cur),
            "X-BAPI-RECV-WINDOW": "8000",
        }
        return headers

    """
    REST API
    """

    async def get_server_time_ms(self) -> int:
        res = await self.api_request("/v5/market/time")
        if res["retCode"] != 0:
            logger.error("Error getting server time: %s", str(res))
        return int(res["result"]["timeNano"]) // (1000 * 1000)  # convert Nano to Ms

    async def fetch_wallet_balance(
        self, account_type: EAccountType = EAccountType.UNIFIED
    ) -> Wallet:
        """
        Fetches wallet balances from Bybit for the user.

        Returns:
            Wallet: A dictionary mapping coin names to CoinBalance instances and a timestamp.
        """
        a_type = "UNIFIED"
        if account_type == EAccountType.SPOT:
            a_type = "SPOT"
        elif account_type == EAccountType.CONTRACT:
            a_type = "CONTRACT"

        path_url = "/v5/account/wallet-balance"
        params = {"accountType": a_type}

        response = await self.api_request(
            path_url=path_url, params=params, is_auth_required=True
        )

        timestamp = int(time.time() * 1000)
        wallet_data = response.get("result", {}).get("list", [])
        wallet = {}
        for item in wallet_data:
            coin_data = item["coin"]
            for coin in coin_data:
                wallet[coin["coin"]] = CoinBalance(
                    total=float(coin["walletBalance"]),
                    available=float(coin["availableToWithdraw"]),
                    realised_pnl=float(coin.get("cumRealisedPnl", 0)),
                    unrealised_pnl=float(coin.get("unrealisedPnl", 0)),
                )

        return Wallet(wallet=wallet, timestamp=timestamp)

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
        bybit_symb = f"{symbol.base.upper()}{symbol.quote.upper()}"
        symb_mapping = {symbol: bybit_symb}
        pair_mapping = {bybit_symb: symbol}
        cat = "spot"
        if category == EOrderCategory.LINEAR:
            cat = "linear"

        start_timestamp: int = int(convert_date_to_utc_timestamp(start_time) * 1000)
        end_timestamp: int = int(convert_date_to_utc_timestamp(end_time) * 1000)

        all_klines: List[Kline] = []
        current_start: int = start_timestamp
        interval_ms = int(interval) * 60 * 1000  # interval in milliseconds

        def to_klines(symbol: str, arr: list) -> List[Kline]:
            lines: List[Kline] = []
            for kline in arr:
                lines.append(
                    Kline(
                        trading_pair=pair_mapping[symbol],
                        open=float(kline[1]),
                        close=float(kline[4]),
                        high=float(kline[2]),
                        low=float(kline[3]),
                        volume=float(kline[5]),
                        start=int(kline[0]),
                        timestamp=int(kline[0]),
                        confirm=True,
                    )
                )
            return lines

        logger.debug(
            "Start: %s\tEndTime:%s",
            timestamp_to_human_readable(current_start),
            timestamp_to_human_readable(end_timestamp),
        )
        while current_start < end_timestamp:
            max_end_ts = current_start + limit * interval_ms
            end_ts = min(max_end_ts, end_timestamp)

            params = {
                "category": cat,
                "symbol": symb_mapping[symbol],
                "interval": interval,
                "start": current_start,
                "end": end_ts,
                "limit": limit,
            }
            logger.debug(
                "Start: %s\tEnd:%s\tSymbol:%s",
                timestamp_to_human_readable(current_start),
                timestamp_to_human_readable(end_ts),
                symbol,
            )

            response = await self.api_request(
                path_url="/v5/market/kline",
                params=params,
                is_auth_required=False,
            )

            if response["retCode"] != 0:
                logger.error(
                    "Error occurred. Returning partial results...\nError: %s",
                    str(response),
                )
                return all_klines

            res_symb = response.get("result", {}).get("symbol", "")
            klines = response.get("result", {}).get("list", [])
            lines = to_klines(res_symb, klines)
            all_klines.extend(lines)

            if not klines or len(klines) < limit:
                break

            current_start = lines[0].timestamp + interval_ms

            await asyncio.sleep(0.1)

        return all_klines

    async def fetch_instrument_info(
        self, pair: TradingPair, category: EOrderCategory = EOrderCategory.SPOT
    ) -> List[InstrumentInfo]:
        """
        Fetch instrument info for a given trading pair and category from Bybit.

        :param pair: The trading pair (base and quote coin).
        :param category: The product type (spot, linear, inverse, option). Default is "spot".
        :return: A list of InstrumentInfo objects.
        """
        cat = "spot"
        if category == EOrderCategory.LINEAR:
            cat = "linear"
        elif category == EOrderCategory.INVERSE:
            cat = "inverse"

        symb = f"{pair.base.upper()}{pair.quote.upper()}"
        mapping = {pair: symb}

        reverse_mapping = {symb: pair}

        params = {"category": cat, "symbol": mapping[pair]}

        response = await self.api_request(
            path_url="/v5/market/instruments-info",
            params=params,
        )

        if response["retCode"] != 0:
            logger.error(
                f"Error fetching instrument info: {response.get('retMsg', 'Unknown error')}"
            )
            return NotImplemented

        instruments = response.get("result", {}).get("list", [])
        instrument_info_list: List[InstrumentInfo] = []

        # TODO: ivan(fix this since it is not correct)
        for instrument in instruments:
            try:
                lot_size_filter = instrument.get("lotSizeFilter", {})
                price_filter = instrument.get("priceFilter", {})

                status = instrument["status"]
                status_r = True if status == "Trading" else False
                info = InstrumentInfo(
                    pair=reverse_mapping[instrument["symbol"]],
                    tradebale=status_r,
                    base_precision=int(
                        get_decimal_places(lot_size_filter["basePrecision"])
                    ),
                    quote_precision=int(
                        get_decimal_places(lot_size_filter["quotePrecision"])
                    ),
                    qty_precision=int(get_decimal_places(price_filter["tickSize"])),
                    min_order_qty=float(lot_size_filter["minOrderQty"]),
                    max_order_qty=float(lot_size_filter["maxOrderQty"]),
                    min_order_amt=float(lot_size_filter["minOrderAmt"]),
                    max_order_amt=float(lot_size_filter["maxOrderAmt"]),
                    tick_size=float(price_filter["tickSize"]),
                )
                instrument_info_list.append(info)
            except KeyError as e:
                logger.warning(f"Missing key in instrument data: {e}")
                continue

        return instrument_info_list

    async def cancel_all_orders(
        self,
        order_category: EOrderCategory = EOrderCategory.SPOT,
        symbol: Optional[TradingPair] = None,
    ) -> Dict[str, Any]:
        """
        Cancels all open orders for the specified category and symbol.

        Args:
            category (str): The product category to cancel orders for (e.g., 'spot', 'linear').
            symbol (Optional[str]): The trading symbol to cancel orders for.

        Returns:
            Dict[str, Any]: Acknowledgment of cancellation request.
        """
        if symbol:
            sym_map = {symbol: f"{symbol.base.upper()}{symbol.quote.upper()}"}

        a_type = "spot"
        data = {"category": a_type}

        if order_category == EOrderCategory.LINEAR:
            a_type = "linear"
            if symbol is None:
                raise ValueError(
                    "For 'linear' category, 'symbol', 'baseCoin', or 'settleCoin' must be specified."
                )
            else:
                data["symbol"] = sym_map[symbol]

        elif order_category == EOrderCategory.INVERSE:
            a_type = "inverse"
            if symbol is None:
                raise ValueError(
                    "For 'inverse' category, 'symbol', 'baseCoin', or 'settleCoin' must be specified."
                )
            else:
                data["symbol"] = sym_map[symbol]

        elif order_category == EOrderCategory.SPOT:
            # For spot category, you can cancel all spot open orders without passing other params.
            data["orderFilter"] = "Order"
            if symbol:
                data["symbol"] = sym_map[symbol]

        logger.debug(f"API cancel_all_orders data: {data}")
        response = await self.api_request(
            path_url="/v5/order/cancel-all",
            method=RESTMethod.POST,
            data=data,  # Pass data here instead of params
            is_auth_required=True,
        )
        return response

    """
    Normalizer API
    """

    def convert_exchange_orderbook_to_orderbook(self, data: Dict) -> Orderbook:
        d = data.get("data", {})
        bids = [
            OrderbookEntry(price=float(bid[0]), qty=float(bid[1]))
            for bid in d.get("b", [])
        ]
        asks = [
            OrderbookEntry(price=float(ask[0]), qty=float(ask[1]))
            for ask in d.get("a", [])
        ]
        timestamp = data.get("ts", 0)
        type = (
            EUpdateType.SNAPSHOT
            if data.get("type", "snapshot") == "snapshot"
            else EUpdateType.DELTA
        )
        symb = d.get("s", "")
        seq = d.get("u", 1)

        return Orderbook(
            update_type=type,
            trading_pair=self._symbols_to_trading_pairs_table[symb],
            bids=bids,
            asks=asks,
            timestamp=timestamp,
            seq=seq,
        )

    def convert_exchange_klines_to_klines(self, data: Dict) -> Kline:
        kline_data = data["data"][0]  # Assuming one element per message for now
        ksymb = data.get("topic", "").split(".")[2]
        confirm = data["data"][0]["confirm"]

        return Kline(
            trading_pair=self._symbols_to_trading_pairs_table[ksymb],
            open=float(kline_data["open"]),
            close=float(kline_data["close"]),
            high=float(kline_data["high"]),
            low=float(kline_data["low"]),
            volume=float(kline_data["volume"]),
            start=int(kline_data["start"]),
            timestamp=int(kline_data["timestamp"]),
            confirm=confirm,
        )

    def convert_exchange_trades_to_trades(self, data: Dict) -> MarketTrades:
        trades = [
            MarketTradesData(
                price=float(trade["p"]),
                qty=float(trade["v"]),
                side=ESide.BUY if trade["S"].lower() == "buy" else ESide.SELL,
            )
            for trade in data["data"]
        ]
        tsymb = ""
        if len(data["data"]) > 0:
            tsymb = data["data"][0]["s"]

        return MarketTrades(
            trading_pair=self._symbols_to_trading_pairs_table[tsymb], trades=trades
        )

    def convert_exchange_order_ack_to_order_ack(self, data: dict) -> OrderAck:
        operation = data["op"]
        order_ack = OrderAck(order_id="", ack_type=EAckType.CREATE, timestamp=0)
        order_ack.order_id = data["data"]["orderLinkId"]
        order_ack.timestamp = int(data["header"]["Timenow"])
        if operation == self.CREATE_OP:
            order_ack.ack_type = EAckType.CREATE
        elif operation == self.CANCEL_OP:
            order_ack.ack_type = EAckType.CANCEL
        else:
            raise RuntimeError(f"Unidentified operation type: {operation}")
        return order_ack

    def convert_exchange_wallet_update_to_wallet(self, data: dict) -> Wallet:
        time = int(data.get("creationTime", 0))
        wal_ev = Wallet(wallet={}, timestamp=time)
        coins = data["data"][0]["coin"]
        for coin_data in coins:
            wal_ev.wallet[coin_data["coin"]] = CoinBalance(
                total=float(coin_data["walletBalance"]),
                available=float(coin_data["availableToWithdraw"]),
                realised_pnl=float(coin_data["cumRealisedPnl"]),
                unrealised_pnl=float(coin_data["unrealisedPnl"]),
            )
        return wal_ev

    def convert_exchange_order_update_to_order_update(self, data: dict) -> OrderUpdate:
        time = data["creationTime"]
        order_up = OrderUpdate(timestamp=time, updates=[])
        updates = data["data"]
        for update in updates:
            cum_exec_qty = (
                float(update.get("cumExecQty", "0"))
                if update.get("cumExecQty", "0") != ""
                else 0.0
            )
            cum_exec_value = (
                float(update.get("cumExecValue", "0"))
                if update.get("cumExecValue", "0") != ""
                else 0.0
            )

            cum_exec_fee = (
                float(update.get("cumExecFee", "0"))
                if update.get("cumExecFee", "0") != ""
                else 0.0
            )

            closed_pnl = (
                float(update.get("closedPnl", "0"))
                if update.get("closedPnl", "0") != ""
                else 0.0
            )

            take_profit = (
                float(update.get("takeProfit", "0"))
                if update.get("takeProfit", "0") != ""
                else 0.0
            )

            stop_loss = (
                float(update.get("stopLoss", "0"))
                if update.get("stopLoss", "0") != ""
                else 0.0
            )

            tp_limit_price = (
                float(update.get("tpLimitPrice", "0"))
                if update.get("tpLimitPrice", "0") != ""
                else 0.0
            )

            sl_limit_price = (
                float(update.get("slLimitPrice", "0"))
                if update.get("slLimitPrice", "0") != ""
                else 0.0
            )

            order_up.updates.append(
                OrderUpdateItem(
                    symbol=self._symbols_to_trading_pairs_table[update["symbol"]],
                    order_id=update["orderId"],
                    side=self.convert_exchange_side_to_side(update["side"]),
                    order_type=self.convert_exchange_order_type_to_order_type(
                        update["orderType"]
                    ),
                    price=float(update["price"]),
                    qty=float(update["qty"]),
                    tif=self.convert_exchange_tif_to_tif(update["timeInForce"]),
                    order_status=self.convert_exchange_order_status_to_order_status(
                        update["orderStatus"]
                    ),
                    custom_order_id=update["orderLinkId"],
                    cum_exec_qty=cum_exec_qty,
                    cum_exec_value=cum_exec_value,
                    cum_exec_fee=cum_exec_fee,
                    closed_pnl=closed_pnl,
                    take_profit=take_profit,
                    stop_loss=stop_loss,
                    tp_limit_price=tp_limit_price,
                    sl_limit_price=sl_limit_price,
                    create_time=int(update.get("createdTime", "0")),
                    update_time=int(update.get("updatedTime", "0")),
                )
            )
        return order_up

    def convert_exchange_order_type_to_order_type(self, data: str) -> EOrderType:
        if data == "Limit":
            return EOrderType.LIMIT
        if data == "Market":
            return EOrderType.MARKET
        return EOrderType.UNKNOWN

    def convert_exchange_order_status_to_order_status(self, data: str) -> EOrderStatus:
        if data == "New":
            return EOrderStatus.NEW
        if data == "PartiallyFilled":
            return EOrderStatus.PARTIALLY_FILLED
        if data == "Filled":
            return EOrderStatus.FILLED
        if data == "Rejected":
            return EOrderStatus.REJECTED
        if data == "Cancelled":
            return EOrderStatus.CANCELLED
        return EOrderStatus.UNKNOWN

    def convert_exchange_order_category_to_order_category(
        self, data: str
    ) -> EOrderCategory:
        if data == "spot":
            return EOrderCategory.SPOT
        if data == "linear":
            return EOrderCategory.LINEAR
        if data == "inverse":
            return EOrderCategory.INVERSE
        return EOrderCategory.UNKNOWN

    def convert_exchange_tif_to_tif(self, data: str) -> ETimeInForce:
        if data == "GTC":
            return ETimeInForce.GTC
        if data == "IOC":
            return ETimeInForce.IOC
        if data == "FOK":
            return ETimeInForce.FOK
        return ETimeInForce.UNKNOWN

    def convert_exchange_side_to_side(self, data: str) -> ESide:
        if data == "Sell":
            return ESide.SELL
        return ESide.BUY

    """
    Denormalizer API
    """

    def convert_create_order_to_ws_request(
        self, create_order: CreateOrder
    ) -> WSRequest:
        payload: Mapping[str, Any] = {}
        args: Mapping[str, Any] = {}
        args["category"] = self.convert_order_category_to_exchange_category(
            create_order.category
        )
        args["symbol"] = self._trading_pairs_to_symbols_table[create_order.trading_pair]
        args["side"] = self.convert_order_side_to_exchange_side(create_order.side)
        args["orderType"] = self.convert_order_type_to_exchange_order_type(
            create_order.order_type
        )
        # HACK: only round to 2 for now
        args["qty"] = str(round(create_order.qty, 2))
        args["orderLinkId"] = create_order.client_order_id
        if create_order.order_type == EOrderType.LIMIT:
            assert (
                create_order.price is not None
            ), "Order price cannot be None on Limit Orders"
            args["price"] = str(round(create_order.price, 4))
        args["timeInForce"] = self.convert_tif_to_exchange_tif(create_order.tif)
        if create_order.order_type == EOrderType.LIMIT:
            if create_order.take_profit is not None:
                args["takeProfit"] = str(round(create_order.take_profit, 4))

            if create_order.stop_loss is not None:
                args["stopLoss"] = str(round(create_order.stop_loss, 4))
        if create_order.extra_params is not None:
            for key in create_order.extra_params:
                args[key] = create_order.extra_params[key]

        # INFO: args must be an array by Bybit specification
        payload["args"] = [args]
        payload["header"] = self._gen_request_headers()
        payload["op"] = self.CREATE_OP
        return WSJSONRequest(payload=payload)

    def convert_cancel_order_to_ws_request(
        self, cancel_order: CancelOrder
    ) -> WSRequest:
        payload: Mapping[str, Any] = {}
        args: Mapping[str, Any] = {}
        args["category"] = self.convert_order_category_to_exchange_category(
            cancel_order.category
        )
        args["symbol"] = self._trading_pairs_to_symbols_table[cancel_order.trading_pair]
        args["orderLinkId"] = cancel_order.client_order_id

        # INFO: args must be an array by Bybit specification
        payload["args"] = [args]
        payload["header"] = self._gen_request_headers()
        payload["op"] = self.CANCEL_OP
        return WSJSONRequest(payload=payload)

    def convert_amend_order_to_ws_request(self, amend_order: AmendOrder) -> WSRequest:
        return super().convert_amend_order_to_ws_request(amend_order)

    def convert_order_type_to_exchange_order_type(self, order_type: EOrderType) -> str:
        if order_type == EOrderType.MARKET:
            return "Market"
        if order_type == EOrderType.LIMIT:
            return "Limit"

        raise RuntimeError(f"Unknown order type: {order_type}")

    def convert_tif_to_exchange_tif(self, tif: ETimeInForce) -> str:
        if tif == ETimeInForce.GTC:
            return "GTC"
        if tif == ETimeInForce.IOC:
            return "IOC"
        if tif == ETimeInForce.FOK:
            return "FOK"
        raise RuntimeError(f"Unknown time in force: {tif}")

    def convert_order_category_to_exchange_category(
        self, order_category: EOrderCategory
    ) -> str:
        if order_category == EOrderCategory.SPOT:
            return "spot"
        if order_category == EOrderCategory.LINEAR:
            return "linear"
        if order_category == EOrderCategory.INVERSE:
            return "inverse"
        raise RuntimeError(f"Unknown order category: {order_category}")

    def convert_order_side_to_exchange_side(self, side: ESide) -> str:
        if side == ESide.BUY:
            return "Buy"
        if side == ESide.SELL:
            return "Sell"
