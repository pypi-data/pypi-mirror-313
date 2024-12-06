import asyncio
import time
from typing import Any, Dict, List, Optional, cast

import numpy as np

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
    Position,
    PositionUpdate,
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
from ttxt_v2.utils.date_time import convert_date_to_utc_timestamp
from ttxt_v2.utils.logger import logger

from .binance_auth import BinanceAuth


class BinanceFutures(ConnectorBase):
    def __init__(
        self,
        config: Optional[ConnectorConfig] = None,
        public_queue: Optional[IQueue] = None,
        signal_queue: Optional[IQueue] = None,
        api_key: str = "",
        api_secret: str = "",
    ):
        super().__init__(config, public_queue, signal_queue, api_key, api_secret)
        self._request_id = 0  # For generating unique IDs for WS requests

    def is_ws_trading_enabled(self) -> bool:
        return True

    @property
    def authenticator(self) -> BaseAuth:
        return BinanceAuth(api_key=self._api_key, api_secret=self._api_secret)

    def _create_web_assistant_factory(self) -> WebAssitantFactory:
        return WebAssitantFactory(auth=self._auth)

    def _get_connector_urls(self) -> ConnectorURL:
        return ConnectorURL(
            PUBLIC_SPOT="",  # Not used for futures
            PUBLIC_LINEAR="wss://ws-fapi.binance.com/ws-fapi/v1",
            PUBLIC_INVERSE="",
            TRADE="wss://ws-fapi.binance.com/ws-fapi/v1",
            BASE="https://fapi.binance.com",  # REST API base URL for futures
            PRIVATE="wss://ws-fapi.binance.com/ws-fapi/v1",
        )

    async def _subscribe_to_public_stream(self):
        """
        Subscribes to the public WebSocket stream by sending subscription requests over JSON.
        """
        assert (
            self._public_ws is not None and self._public_ws.connected
        ), "Public WS should be connected"
        subscription_reqs = self._create_public_ws_subscription_requests()
        for req in subscription_reqs:
            logger.debug(f"BinanceFutures public subscription req: {req}")
            await self._public_ws.send(req)

    def _create_public_ws_subscription_requests(self) -> List[WSJSONRequest]:
        """
        Creates subscription requests for the public WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        streams = []

        if self._config.ob_config is not None:
            # Depth updates with partial book of 20 levels at 100ms
            for ticker in self._config.ob_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker].lower()
                stream_name = f"{symb}@depth20@100ms"
                streams.append(stream_name)

        if self._config.mt_config is not None:
            for ticker in self._config.mt_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker].lower()
                stream_name = f"{symb}@aggTrade"
                streams.append(stream_name)

        if self._config.kl_config is not None:
            interval = self._config.kl_config.timeframe
            for ticker in self._config.kl_config.tickers:
                symb = self._trading_pairs_to_symbols_table[ticker].lower()
                stream_name = f"{symb}@kline_{interval}"
                logger.debug(f"Binance kline stream: {stream_name}")
                streams.append(stream_name)

        subscription_requests = []
        if streams:
            payload = {
                "method": "SUBSCRIBE",
                "params": streams,
                "id": self._next_request_id(),
            }
            subscription_requests.append(WSJSONRequest(payload=payload))
        return subscription_requests

    def _next_request_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def _subscribe_to_trade_stream(self):
        """
        Subscribes to the trade WebSocket stream and authenticates the connection.
        """
        assert (
            self._trade_ws is not None and self._trade_ws.connected
        ), "Trade WS needs to be connected"
        """
        request_id = self._next_request_id()
        auth_payload = {
            "id": request_id,
            "method": "session.logon",
            "params": {},
        }
        auth_request = WSJSONRequest(payload=auth_payload, is_auth_required=True)
        await self._trade_ws.send(auth_request)
        """

    async def _subscribe_to_private_stream(self):
        """
        Subscribes to the private user data stream using the new WebSocket API.
        """
        assert (
            self._private_ws is not None and self._private_ws.connected
        ), "Private WS needs to be connected"

        request_id = self._next_request_id()
        auth_payload = {
            "id": request_id,
            "method": "session.logon",
            "params": {},
        }
        auth_request = WSJSONRequest(payload=auth_payload, is_auth_required=True)
        await self._private_ws.send(auth_request)

    async def _process_market_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Processes market data received from the WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        try:
            message = response.data
            m_data = message.get("data", {})
            event_type = m_data.get("e", "")
            if event_type == "depthUpdate":
                normalized_orderbook = self.convert_exchange_orderbook_to_orderbook(
                    m_data
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
            elif event_type == "aggTrade":
                normalized_trades = self.convert_exchange_trades_to_trades(m_data)
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
            elif event_type == "kline":
                normalized_kline = self.convert_exchange_klines_to_klines(m_data)
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
                logger.warning(f"Unknown public event type: {event_type}")
                return None
        except Exception as e:
            logger.error(
                f"Error processing market data: {str(e)}. Response: {str(response.data)}"
            )
            return None

    def _process_trade_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Processes trade responses received from the WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        try:
            message = response.data
            if "error" in message:
                logger.error(f"Trade error: {message['error']}")
                return None

            # Handle responses to trade requests
            if "id" in message and "result" in message:
                result = message["result"]
                order_ack = self.convert_exchange_order_ack_to_order_ack(result)
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
                logger.warning(f"Unknown trade response: {message}")
            return None
        except Exception as e:
            logger.error(f"Error processing trade data: {str(e)}")
            return None

    def _process_private_data(self, response: WSResponse) -> Optional[List[BaseEvent]]:
        """
        Processes private data received from the WebSocket stream.
        """
        assert self._config is not None, "Config cannot be None"
        try:
            message = response.data
            event_type = message.get("e", "")

            if event_type == "ACCOUNT_UPDATE":
                events = []

                wallet_update = self.convert_exchange_wallet_update_to_wallet(message)
                if wallet_update:
                    events.append(
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
                    )

                position_update = self.convert_exchange_account_update_to_positions(
                    message
                )
                if position_update:
                    events.append(
                        BaseEvent(
                            event_type=EventType.POSITION_UPDATE_EVENT,
                            payload=Event[PositionUpdate](
                                header=MessageHeader(
                                    exchange=self._config.exchange,
                                    timestamp=position_update.timestamp,
                                ),
                                data=position_update,
                            ),
                        )
                    )
                return events
            elif event_type == "ORDER_TRADE_UPDATE":
                order_update = self.convert_exchange_order_update_to_order_update(
                    message
                )
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
            else:
                logger.warning(f"Unknown private event type: {message}")
                return None
        except Exception as e:
            logger.error(f"Error processing private data: {str(e)}")
            return None

    def _process_signal_event(self, event: BaseEvent) -> List[WSRequest]:
        """
        Processes events from the signal queue and converts them to WSRequests.
        """
        if event.event_type == EventType.CREATE_ORDER_EVENT:
            ws_request = self.convert_create_order_to_ws_request(
                cast(CreateOrder, event.payload.data)
            )
            return [ws_request]
        elif event.event_type == EventType.CANCEL_ORDER_EVENT:
            ws_request = self.convert_cancel_order_to_ws_request(
                cast(CancelOrder, event.payload.data)
            )
            return [ws_request]
        else:
            logger.warning(f"Unsupported event type in signal: {event.event_type}")
            return []

    async def _process_http_signals(self, event: BaseEvent) -> Optional[BaseEvent]:
        """
        Not used since trading is over WebSockets.
        """
        return None

    async def get_server_time_ms(self) -> int:
        try:
            res = await self.api_request("/eapi/v1/time")
            return int(res.get("serverTime", 0))
        except Exception:
            logger.error(f"Server time error")
        finally:
            logger.info("Returning server time as 0")
            return 0

    async def fetch_wallet_balance(
        self, account_type: EAccountType = EAccountType.CONTRACT
    ) -> Wallet:
        path_url = "/fapi/v2/account"
        response = await self.api_request(
            path_url=path_url, method=RESTMethod.GET, is_auth_required=True
        )
        timestamp = int(time.time_ns() / 1_000_000)
        wallet = {}
        assets = response.get("assets", [])
        for asset in assets:
            asset_name = asset["asset"]
            wallet[asset_name] = CoinBalance(
                total=float(asset["walletBalance"]),
                available=float(asset["availableBalance"]),
                realised_pnl=float(asset.get("realizedProfit", 0)),
                unrealised_pnl=float(asset["unrealizedProfit"]),
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
        Fetches Kline (candlestick) data for a given trading pair and interval over a time range.
        This method handles fetching data in batches if the total number of klines exceeds the API limit.

        :param symbol: The trading pair for which to fetch klines.
        :param interval: The interval at which to fetch klines (e.g., '1m', '5m').
        :param start_time: The start time in '%d/%m/%Y %H:%M' format.
        :param end_time: The end time in '%d/%m/%Y %H:%M' format.
        :param category: The order category (default is SPOT).
        :param limit: The maximum number of klines to fetch per request (default is 1000, max is 1500).
        :return: A list of Kline objects.
        """
        # Constants
        MAX_LIMIT = 1500  # Binance API max limit
        limit = min(limit, MAX_LIMIT)

        # Convert date strings to UTC timestamps in milliseconds
        start_timestamp = int(convert_date_to_utc_timestamp(start_time) * 1000)
        end_timestamp = int(convert_date_to_utc_timestamp(end_time) * 1000)

        # Prepare request parameters
        pair = symbol.base + symbol.quote
        params = {
            "pair": pair,
            "contractType": "PERPETUAL",
            "interval": interval,
            "limit": limit,
        }

        # API endpoint for continuous klines
        path_url = "/fapi/v1/continuousKlines"

        # Initialize variables for looping
        klines = []
        current_start_time = start_timestamp

        # Map interval string to milliseconds
        interval_mapping = {
            "1m": 60 * 1000,
            "3m": 3 * 60 * 1000,
            "5m": 5 * 60 * 1000,
            "15m": 15 * 60 * 1000,
            "30m": 30 * 60 * 1000,
            "1h": 60 * 60 * 1000,
            "2h": 2 * 60 * 60 * 1000,
            "4h": 4 * 60 * 60 * 1000,
            "6h": 6 * 60 * 60 * 1000,
            "8h": 8 * 60 * 60 * 1000,
            "12h": 12 * 60 * 60 * 1000,
            "1d": 24 * 60 * 60 * 1000,
            "3d": 3 * 24 * 60 * 60 * 1000,
            "1w": 7 * 24 * 60 * 60 * 1000,
            "1M": 30 * 24 * 60 * 60 * 1000,
        }

        interval_ms = interval_mapping.get(interval)
        if not interval_ms:
            raise ValueError(f"Invalid interval: {interval}")

        while current_start_time < end_timestamp:
            params["startTime"] = current_start_time
            params["endTime"] = end_timestamp

            try:
                response = await self.api_request(
                    path_url=path_url,
                    params=params,
                    is_auth_required=False,
                )
            except Exception as e:
                logger.error(f"Failed to fetch klines: {str(e)}")
                break

            if not response:
                break

            res = response["res"]
            # Parse the response into Kline objects
            for item in res:
                open_time = item[0]
                open_price = float(item[1])
                high_price = float(item[2])
                low_price = float(item[3])
                close_price = float(item[4])
                volume = float(item[5])
                close_time = item[6]

                kline = Kline(
                    trading_pair=symbol,
                    open=open_price,
                    close=close_price,
                    high=high_price,
                    low=low_price,
                    volume=volume,
                    start=int(open_time),
                    timestamp=int(close_time),
                    confirm=True,
                )
                klines.append(kline)

            last_kline_time = res[-1][0]
            current_start_time = last_kline_time + interval_ms

            await asyncio.sleep(0.1)

        return klines

    async def fetch_instrument_info(
        self,
        pair: TradingPair,
        category: EOrderCategory = EOrderCategory.SPOT,
    ) -> List[InstrumentInfo]:
        """
        Fetches instrument information for a given trading pair.

        :param pair: The trading pair to fetch information for.
        :param category: The order category (default is SPOT).
        :return: An InstrumentInfo object containing the symbol information.
        """
        path_url = "/fapi/v1/exchangeInfo"

        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.GET,
            is_auth_required=False,
        )

        symbol_str = f"{pair.base.upper()}{pair.quote.upper()}"
        symbol_info = None
        for symbol in response.get("symbols", []):
            if symbol["symbol"] == symbol_str:
                symbol_info = symbol
                break

        if symbol_info is None:
            raise ValueError(f"Symbol {symbol_str} not found in exchange info.")

        # Parse the symbol_info to create an InstrumentInfo object
        tradable: bool = symbol_info.get("status", "") == "TRADING"
        base_precision = int(symbol_info.get("baseAssetPrecision", 0))
        quote_precision = int(symbol_info.get("quotePrecision", 0))
        qty_precision = int(symbol_info.get("quantityPrecision", 0))
        filters = symbol_info.get("filters", [])

        # Initialize variables
        min_order_qty = 0.0
        max_order_qty = 0.0
        min_order_amt = 0.0
        tick_size = 0.0
        step_size = 0.0

        for f in filters:
            filter_type = f["filterType"]
            if filter_type == "PRICE_FILTER":
                tick_size = float(f["tickSize"])
            elif filter_type == "LOT_SIZE":
                min_order_qty = float(f["minQty"])
                max_order_qty = float(f["maxQty"])
                step_size = float(f["stepSize"])
                # Calculate qty_precision from step_size if not already provided
                if step_size != 0:
                    qty_precision = max(qty_precision, int(abs(np.log10(step_size))))
            elif filter_type == "MIN_NOTIONAL":
                min_order_amt = float(f["notional"])

        instrument_info = InstrumentInfo(
            pair=pair,
            tradebale=tradable,
            base_precision=base_precision,
            quote_precision=quote_precision,
            qty_precision=qty_precision,
            min_order_qty=min_order_qty,
            max_order_qty=max_order_qty,
            min_order_amt=min_order_amt,
            tick_size=tick_size,
        )

        return [instrument_info]

    async def cancel_all_orders(
        self,
        order_category: EOrderCategory = EOrderCategory.SPOT,
        symbol: Optional[TradingPair] = None,
    ) -> Dict[str, Any]:
        if symbol is None:
            raise ValueError("Symbol must be provided to cancel all orders")

        path_url = "/fapi/v1/allOpenOrders"
        data = {
            "symbol": symbol,
        }

        response = await self.api_request(
            path_url=path_url,
            method=RESTMethod.DELETE,
            data=data,
            is_auth_required=True,
        )
        return response

    def _gen_symbols_table(self) -> Dict[str, TradingPair]:
        """
        Generates a mapping from exchange symbols to TradingPair objects.
        """
        res = {}
        if self._config is None:
            return res

        for config_section in [
            self._config.ob_config,
            self._config.mt_config,
            self._config.kl_config,
        ]:
            if config_section is not None:
                for ticker in config_section.tickers:
                    symb = (ticker.base + ticker.quote).upper()
                    res[symb] = ticker

        return res

    def _gen_trading_pairs_table(self) -> Dict[TradingPair, str]:
        """
        Generates a mapping from TradingPair objects to exchange symbols.
        """
        res = {}
        if self._config is None:
            return res

        for config_section in [
            self._config.ob_config,
            self._config.mt_config,
            self._config.kl_config,
        ]:
            if config_section is not None:
                for ticker in config_section.tickers:
                    symb = (ticker.base + ticker.quote).upper()
                    res[ticker] = symb

        return res

    """
    Denormalizer API
    """

    def convert_create_order_to_ws_request(
        self, create_order: CreateOrder
    ) -> WSRequest:
        """
        Converts a CreateOrder event to a WSRequest for placing an order via WebSocket.
        """
        params = self.convert_create_order_to_exchange_format(create_order)
        payload = {
            "id": self._next_request_id(),
            "method": "order.place",
            "params": params,
        }
        ws_request = WSJSONRequest(payload=payload)
        return ws_request

    def convert_cancel_order_to_ws_request(
        self, cancel_order: CancelOrder
    ) -> WSRequest:
        """
        Converts a CancelOrder event to a WSRequest for canceling an order via WebSocket.
        """
        params = self.convert_cancel_order_to_exchange_format(cancel_order)
        payload = {
            "id": self._next_request_id(),
            "method": "order.cancel",
            "params": params,
        }
        ws_request = WSJSONRequest(payload=payload)
        return ws_request

    def convert_amend_order_to_ws_request(self, amend_order: AmendOrder) -> WSRequest:
        # Implement if necessary
        return super().convert_amend_order_to_ws_request(amend_order)

    """
    Helper Methods
    """

    def convert_create_order_to_exchange_format(
        self, create_order: CreateOrder
    ) -> Dict[str, Any]:
        data = {
            "symbol": self._trading_pairs_to_symbols_table[create_order.trading_pair],
            "side": self.convert_order_side_to_exchange_side(create_order.side),
            "type": self.convert_order_type_to_exchange_order_type(
                create_order.order_type
            ),
            "quantity": str(create_order.qty),
        }
        if create_order.order_type == EOrderType.LIMIT:
            data["price"] = str(create_order.price)
            data["timeInForce"] = self.convert_tif_to_exchange_tif(create_order.tif)
        if create_order.client_order_id:
            data["newClientOrderId"] = create_order.client_order_id
        if create_order.take_profit is not None:
            data["stopPrice"] = str(create_order.take_profit)
        if create_order.stop_loss is not None:
            data["stopPrice"] = str(create_order.stop_loss)
        if create_order.extra_params:
            data.update(create_order.extra_params)
        return data

    def convert_cancel_order_to_exchange_format(
        self, cancel_order: CancelOrder
    ) -> Dict[str, Any]:
        data = {
            "symbol": self._trading_pairs_to_symbols_table[cancel_order.trading_pair],
        }
        if cancel_order.client_order_id:
            data["origClientOrderId"] = cancel_order.client_order_id
        return data

    """
    Normalizer API
    """

    def convert_exchange_orderbook_to_orderbook(self, data: Dict) -> Orderbook:
        bids = [
            OrderbookEntry(price=float(bid[0]), qty=float(bid[1]))
            for bid in data.get("b", [])
        ]
        asks = [
            OrderbookEntry(price=float(ask[0]), qty=float(ask[1]))
            for ask in data.get("a", [])
        ]
        timestamp = data.get("E", int(time.time() * 1000))
        update_type = EUpdateType.SNAPSHOT
        symbol = data.get("s", "")
        seq = data.get("u", 0)
        return Orderbook(
            update_type=update_type,
            trading_pair=self._symbols_to_trading_pairs_table[symbol],
            bids=bids,
            asks=asks,
            timestamp=timestamp,
            seq=seq,
        )

    def convert_exchange_klines_to_klines(self, data: Dict) -> Kline:
        confirm = data["x"]
        kline_data = data["k"]
        symbol = kline_data["s"]
        return Kline(
            trading_pair=self._symbols_to_trading_pairs_table[symbol],
            open=float(kline_data["o"]),
            close=float(kline_data["c"]),
            high=float(kline_data["h"]),
            low=float(kline_data["l"]),
            volume=float(kline_data["v"]),
            start=int(kline_data["t"]),
            timestamp=int(kline_data["T"]),
            confirm=confirm,
        )

    def convert_exchange_trades_to_trades(self, data: Dict) -> MarketTrades:
        trade = MarketTradesData(
            price=float(data["p"]),
            qty=float(data["q"]),
            side=ESide.BUY if not data["m"] else ESide.SELL,
        )
        symbol = data["s"]
        return MarketTrades(
            trading_pair=self._symbols_to_trading_pairs_table[symbol],
            trades=[trade],
        )

    def convert_exchange_order_ack_to_order_ack(self, data: dict) -> OrderAck:
        order_ack = OrderAck(
            order_id=str(data["clientOrderId"]),
            ack_type=EAckType.CREATE,
            timestamp=int(data.get("transactTime", time.time() * 1000)),
        )
        return order_ack

    def convert_exchange_wallet_update_to_wallet(self, data: dict) -> Wallet:
        timestamp = data.get("E", int(time.time() * 1000))
        wallet = {}
        update_data = data.get("a", {})
        balances = update_data.get("B", [])
        if not balances:
            return Wallet()
        for balance in balances:
            asset = balance["a"]
            wallet[asset] = CoinBalance(
                total=float(balance["wb"]),
                available=float(balance["cw"]),
                realised_pnl=0.0,  # Not provided in this event
                unrealised_pnl=0.0,  # Not provided in this event
            )
        return Wallet(wallet=wallet, timestamp=timestamp)

    def convert_exchange_account_update_to_positions(
        self, data: dict
    ) -> Optional[PositionUpdate]:
        timestamp = data.get("E", int(time.time() * 1000))
        update_data = data.get("a", {})
        positions = update_data.get("P", [])
        if not positions:
            return None
        position_updates = []
        for position in positions:
            symbol: TradingPair = self._symbols_to_trading_pairs_table[position["s"]]
            amt: float = float(position["pa"])
            entry_price: float = float(position["ep"])
            unrealized_pnl: float = float(position["up"])
            margin_type = position["mt"]
            isolated_wallet = float(position.get("iw", "0"))
            side = position["ps"]
            position_updates.append(
                Position(
                    symbol=symbol,
                    amount=amt,
                    entry_price=entry_price,
                    unrealized_pnl=unrealized_pnl,
                    margin_type=margin_type,
                    isolated_wallet=isolated_wallet,
                    position_side=side,
                )
            )
        return PositionUpdate(positions=position_updates, timestamp=timestamp)

    def convert_exchange_order_update_to_order_update(self, data: dict) -> OrderUpdate:
        timestamp = data.get("E", int(time.time() * 1000))
        order_data = data.get("o", {})
        update_item = OrderUpdateItem(
            symbol=order_data["s"],
            order_id=order_data["i"],
            side=self.convert_exchange_side_to_side(order_data["S"]),
            order_type=self.convert_exchange_order_type_to_order_type(order_data["o"]),
            price=float(order_data["p"]),
            qty=float(order_data["q"]),
            tif=self.convert_exchange_tif_to_tif(order_data["f"]),
            order_status=self.convert_exchange_order_status_to_order_status(
                order_data["X"]
            ),
            custom_order_id=order_data.get("c", ""),
            cum_exec_qty=float(order_data["z"]),
            cum_exec_value=float(order_data["Z"]),
            cum_exec_fee=float(order_data.get("n", "0")),
            closed_pnl=float(order_data.get("rp", "0")),
            take_profit=0.0,  # Not provided
            stop_loss=0.0,  # Not provided
            tp_limit_price=0.0,  # Not provided
            sl_limit_price=0.0,  # Not provided
            create_time=int(order_data["O"]),
            update_time=int(order_data["T"]),
        )
        order_update = OrderUpdate(
            timestamp=timestamp,
            updates=[update_item],
        )
        return order_update

    def convert_exchange_order_category_to_order_category(
        self, data: str
    ) -> EOrderCategory:
        # NOTE: not needed for exchanges
        return super().convert_exchange_order_category_to_order_category(data)

    def convert_exchange_order_type_to_order_type(self, data: str) -> EOrderType:
        mapping = {
            "LIMIT": EOrderType.LIMIT,
            "MARKET": EOrderType.MARKET,
        }
        return mapping.get(data, EOrderType.UNKNOWN)

    def convert_exchange_order_status_to_order_status(self, data: str) -> EOrderStatus:
        mapping = {
            "NEW": EOrderStatus.NEW,
            "PARTIALLY_FILLED": EOrderStatus.PARTIALLY_FILLED,
            "FILLED": EOrderStatus.FILLED,
            "CANCELED": EOrderStatus.CANCELLED,
            "REJECTED": EOrderStatus.REJECTED,
        }
        return mapping.get(data, EOrderStatus.UNKNOWN)

    def convert_exchange_tif_to_tif(self, data: str) -> ETimeInForce:
        mapping = {
            "GTC": ETimeInForce.GTC,
            "IOC": ETimeInForce.IOC,
            "FOK": ETimeInForce.FOK,
        }
        return mapping.get(data, ETimeInForce.UNKNOWN)

    def convert_exchange_side_to_side(self, data: str) -> ESide:
        return ESide.BUY if data == "BUY" else ESide.SELL

    def convert_order_type_to_exchange_order_type(self, order_type: EOrderType) -> str:
        mapping = {
            EOrderType.LIMIT: "LIMIT",
            EOrderType.MARKET: "MARKET",
        }
        return mapping.get(order_type, "LIMIT")

    def convert_tif_to_exchange_tif(self, tif: ETimeInForce) -> str:
        mapping = {
            ETimeInForce.GTC: "GTC",
            ETimeInForce.IOC: "IOC",
            ETimeInForce.FOK: "FOK",
        }
        return mapping.get(tif, "GTC")

    def convert_order_side_to_exchange_side(self, side: ESide) -> str:
        return "BUY" if side == ESide.BUY else "SELL"

    def convert_order_category_to_exchange_category(
        self, order_category: EOrderCategory
    ) -> str:
        # INFO: not needed for now
        return super().convert_order_category_to_exchange_category(order_category)
