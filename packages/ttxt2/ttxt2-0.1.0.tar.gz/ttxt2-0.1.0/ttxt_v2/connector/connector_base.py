import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ttxt_v2.connector.connector_urls import ConnectorURL
from ttxt_v2.connector.denormalizer_base import DenormalizerBase
from ttxt_v2.connector.normalizer_base import NormalizerBase
from ttxt_v2.core.api import (
    AsyncioQueue,
    BaseEvent,
    ConnectorStatus,
    EAccountType,
    EConnectorStatus,
    EOrderCategory,
    EUpdateType,
    Event,
    EventType,
    EWebSocketType,
    InstrumentInfo,
    IQueue,
    IQueueActor,
    Kline,
    LocalStorageBackend,
    MarketDataRecorder,
    MarketDataRecorderConfig,
    MessageHeader,
    Orderbook,
    TradingPair,
    Wallet,
)
from ttxt_v2.core.web import (
    BaseAuth,
    RESTMethod,
    WebAssitantFactory,
    WSAssistant,
    WSRequest,
    WSResponse,
)
from ttxt_v2.utils.async_websocket_retrier import websocket_reconnect
from ttxt_v2.utils.logger import logger

from .connector_config import ConnectorConfig, OperationMode, StorageType, TradingMode
from .denormalizer_base import DenormalizerBase
from .normalizer_base import NormalizerBase


class ConnectorBase(IQueueActor, NormalizerBase, DenormalizerBase, ABC):
    """
    Abstract base class for a connector to a cryptocurrency exchange.

    Attributes:
        _config (ConnectorConfig): Configuration for the connector.
        _auth (BaseAuth): Authenticator for the connector.
        _web_assistant_factory (WebAssitantFactory): Factory to create web assistants.
        _public_ws (Optional[WSAssistant]): WebSocket assistant for public streams.
        _public_queue_stream (IQueue): Queue for public data streams.
    """

    def __init__(
        self,
        config: Optional[ConnectorConfig] = None,
        public_queue: Optional[IQueue] = None,
        signal_queue: Optional[IQueue] = None,
        api_key: str = "",
        api_secret: str = "",
    ):
        """
        Initializes the connector with the given configuration and public queue.

        Args:
            config (ConnectorConfig): Configuration for the connector.
            public_queue (IQueue): Queue for public data streams.
        """
        super().__init__()
        self._config = config
        logger.debug(f"Connector config: {self._config}")
        logger.debug(f"API_KEY:{api_key},API_SECRET:{api_secret}")

        self._api_key = api_key
        self._api_secret = api_secret
        self._auth = self.authenticator
        self._web_assistant_factory = self._create_web_assistant_factory()
        self._urls = self._get_connector_urls()
        self._public_ws: Optional[WSAssistant] = None
        self._trade_ws: Optional[WSAssistant] = None
        self._private_ws: Optional[WSAssistant] = None
        self._public_queue_stream = public_queue
        self._signal_queue_stream = signal_queue
        self._clock_drift: int = 0
        self._ob_map: Dict[TradingPair, Orderbook] = {}
        if self._config is not None and self._config.ob_config is not None:
            self._trading_pairs_to_symbols_table: Dict[TradingPair, str] = (
                self._gen_trading_pairs_table()
            )
            self._symbols_to_trading_pairs_table: Dict[str, TradingPair] = (
                self._gen_symbols_table()
            )

        # INFO: Setup recorder if it is set
        self._recorder: Optional[MarketDataRecorder] = None
        if self._config is not None and self._config.recording_config is not None:
            if self._config.recording_config.enable:
                self.create_recorder()
                assert (
                    self._recorder is not None
                ), "Recorder cannot be None when enable recording is True"

    def create_recorder(self):
        """
        Initializes the recorder if the appropriate flags are set in the
        exchange configuration.
        """
        assert (
            self._config is not None
        ), "You need to specify config to use this feature"

        try:
            tickers: List[TradingPair] = []
            for ticker in self._trading_pairs_to_symbols_table:
                tickers.append(ticker)
            market_recorder_config = MarketDataRecorderConfig(
                exchange=self._config.exchange, tickers=tickers
            )
            # HACK: (ivan) for now this is the size
            queue = AsyncioQueue(capacity=1048576)
            if self._config.recording_config.storage_type == StorageType.LOCAL:
                backend = LocalStorageBackend(
                    file_path=market_recorder_config.file_path,
                )
                self._recorder = MarketDataRecorder(
                    config=market_recorder_config, msg_queue=queue, backend=backend
                )
            else:
                raise RuntimeError(
                    f"Unknown backend: {self._config.recording_config.storage_type.value}"
                )

        except Exception as e:
            logger.error(f"Could not create recorder: %s", str(e))

    def get_orderbook(self, pair: TradingPair) -> Optional[Orderbook]:
        """
        Allow the user to query the orderbook status to obtain the most up to date orderbook
        if they need to.
        """
        return self._ob_map[pair]

    @property
    def orderbooks(self) -> Dict[TradingPair, Orderbook]:
        """
        Return the orderbook map which stores all orderbooks for all subscribed tickers
        """
        return self._ob_map

    @property
    def get_config(self) -> ConnectorConfig:
        """
        Returns the configuration of the connector.

        Returns:
            ConnectorConfig: The configuration of the connector.
        """
        assert self._config is not None, "Config cannot be None"
        return self._config

    @property
    @abstractmethod
    def authenticator(self) -> BaseAuth:
        """
        Abstract property to get the authenticator for the connector.

        Returns:
            BaseAuth: The authenticator for the connector.
        """
        pass

    @abstractmethod
    def _create_web_assistant_factory(self) -> WebAssitantFactory:
        """
        Abstract method to create a web assistant factory.

        Returns:
            WebAssitantFactory: The web assistant factory.
        """
        pass

    @abstractmethod
    def is_ws_trading_enabled(self) -> bool:
        pass

    """
    WebSockets API
    """

    @websocket_reconnect(EWebSocketType.PUBLIC)
    async def listen_public_stream(self):
        """
        Listens to the public data stream and processes market data.

        Raises:
            asyncio.CancelledError: If the listening task is cancelled.
        """
        assert self._config is not None, "Cannot listen to public stream without config"
        if not self._config.recording_config.enable:
            assert (
                self._public_queue_stream is not None
            ), "Cannot listen for public data if queue is None"
        self._public_ws = await self._web_assistant_factory.get_ws_assistant()
        url = (
            self._urls.PUBLIC_SPOT
            if self._config.operation_mode == OperationMode.SPOT
            else self._urls.PUBLIC_LINEAR
        )
        assert url != "", "Url cannot be empty"
        logger.info(f"Connecting on public URL: {url}")
        await self._public_ws.connect(url)
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

    def _update_orderbooks(self, orderbook: Orderbook):
        # INFO: update the orderbook map
        if (
            self._ob_map.get(orderbook.trading_pair) == None
            and orderbook.update_type == EUpdateType.SNAPSHOT
        ):
            self._ob_map[orderbook.trading_pair] = orderbook
        else:
            self._ob_map[orderbook.trading_pair].update(orderbook)

    async def _write_orderbooks(self):
        """
        Should write the orderbooks to the recorder if one is present
        and also send them to the user every 1 minute. This ensures the client
        is always up to date and also improves the usability of the recorder
        and replayer drastically.
        """
        assert self._config is not None, "Config cannot be None"
        assert self._public_queue_stream is not None, "We need public queue to push to"
        try:
            while True:
                await asyncio.sleep(60)
                for _, value in self._ob_map.items():
                    ob_ev = BaseEvent(
                        event_type=EventType.OB_EVENT,
                        payload=Event[Orderbook](
                            header=MessageHeader(
                                exchange=self._config.exchange,
                                timestamp=int(time.time_ns() / 1_000_000),
                            ),
                            data=value,
                        ),
                    )
                    await self.publish_to_queue(self._public_queue_stream, ob_ev)
        except asyncio.CancelledError:
            logger.info("Orderbook writer stopped...")

    async def _find_clock_drift(self) -> int:
        server_time = await self.get_server_time_ms()
        ms_time = time.time_ns() // 1_000_000
        return ms_time - server_time

    async def start_trading_session(self):
        try:
            if self.is_ws_trading_enabled():
                trading_ws = asyncio.create_task(self._trade_stream())
            else:
                trading_ws = asyncio.create_task(self._basic_trade_loop())

            private_ws = asyncio.create_task(self._private_stream())
            await asyncio.gather(trading_ws, private_ws)
        except asyncio.CancelledError:
            logger.warning("Stopping trading session coroutine")

    async def _basic_trade_loop(self):
        """
        Trading loop used for when we are not trading over websockets. This function
        will poll the signal queue and process the signal ni a virtual method which
        will then dispatch the HTTP call and return the result as an Optional[BaseEvent].
        This base event will then be sent to the user.
        """
        assert self._config is not None, "Cannot trade without config"
        try:
            while True:
                ev = await self._signal_queue_stream.poll()
                if self._config.trading_mode == TradingMode.TRADE:
                    user_ev = await self._process_http_signals(ev)
                    if user_ev is not None:
                        assert (
                            self._public_queue_stream is not None
                        ), "We need queue to stream results to"
                        await self.publish_to_queue(self._public_queue_stream, user_ev)
        except asyncio.CancelledError:
            logger.warning("Basic trading loop cancelled.")
        except Exception as e:
            logger.error(f"Basic trading loop error: {e}")

    @websocket_reconnect(EWebSocketType.TRADE)
    async def _trade_stream(self):
        """
        This is the high-performance trading stream responsible for getting signals from
        the signal queue and transforming them to WSRequests. These requests are then sent
        to the user after processing is performed to ensure the responses are in standardized
        format of type: Optional[BaseEvent]
        """
        assert (
            self._signal_queue_stream is not None
        ), "Cannot have a trading session with None signal queue"
        assert (
            self._public_queue_stream is not None
        ), "Cannot have a trading session with a None public queue"
        assert self._config is not None, "Cannot have trading session without config"
        self._trade_ws = await self._web_assistant_factory.get_ws_assistant()

        await self._trade_ws.connect(self._urls.TRADE)
        await self._on_websocket_connected(EWebSocketType.TRADE)
        await self._subscribe_to_trade_stream()
        pinger = asyncio.create_task(self.pinger_trade())
        try:
            while True:
                event = await self._signal_queue_stream.poll()
                exch_reqs = self._process_signal_event(event)
                # INFO: only send to exchange if trading is enabled
                if self._config.trading_mode == TradingMode.TRADE:
                    for req in exch_reqs:
                        await self._trade_ws.send(req)
                        resp = await self._trade_ws.receive()
                        if resp is not None and resp.data is not None:
                            event = self._process_trade_data(resp)
                            if event is not None:
                                await self._public_queue_stream.publish(event)
        except asyncio.CancelledError:
            logger.warning("Cancelling trade stream")
            raise
        finally:
            pinger.cancel()
            await pinger

    @websocket_reconnect(EWebSocketType.PRIVATE)
    async def _private_stream(self):
        """
        Listens to the private data stream and processes events.

        Raises:
            asyncio.CancelledError: If the listening task is cancelled.
        """
        assert (
            self._public_queue_stream is not None
        ), "Cannot listen to private stream with None public queue"
        self._private_ws = await self._web_assistant_factory.get_ws_assistant()
        await self._private_ws.connect(self._urls.PRIVATE)
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

    async def queue_reader(self, queue: IQueue) -> BaseEvent:
        """no need to read FOR NOW design may change"""
        return NotImplemented

    async def cleanup(self):
        """
        Cleans up the connector by disconnecting the WebSocket and closing the web assistant factory.
        """
        logger.info("Cleaning up the connector...")
        if self._public_ws:
            await self._public_ws.disconnect()
        if self._trade_ws:
            await self._trade_ws.disconnect()
        if self._private_ws:
            await self._private_ws.disconnect()
        await self._web_assistant_factory.close()

    async def _on_websocket_disconnected(
        self, exc: Exception, websocket_type: EWebSocketType
    ):
        assert self._config is not None, "Config cannot be None"
        if self._public_queue_stream is not None:
            disconnected_event = ConnectorStatus(
                msg=str(exc),
                status=EConnectorStatus.DISCONNECTED,
                websocket_type=websocket_type,
            )
            await self._public_queue_stream.publish(
                BaseEvent(
                    event_type=EventType.CONNECTOR_STATUS_EVENT,
                    payload=Event[ConnectorStatus](
                        header=MessageHeader(
                            exchange=self._config.exchange, timestamp=int(time.time())
                        ),
                        data=disconnected_event,
                    ),
                )
            )

    async def _on_websocket_reconnecting(
        self, exc: Exception, websocket_type: EWebSocketType
    ):
        assert self._config is not None, "Config cannot be None"
        if self._public_queue_stream is not None:
            disconnected_event = ConnectorStatus(
                msg=str(exc),
                status=EConnectorStatus.RECONNECTING,
                websocket_type=websocket_type,
            )
            await self._public_queue_stream.publish(
                BaseEvent(
                    event_type=EventType.CONNECTOR_STATUS_EVENT,
                    payload=Event[ConnectorStatus](
                        header=MessageHeader(
                            exchange=self._config.exchange, timestamp=int(time.time())
                        ),
                        data=disconnected_event,
                    ),
                )
            )

    async def _on_websocket_connected(self, websocket_type: EWebSocketType):
        assert self._config is not None, "Config cannot be None"
        if self._public_queue_stream is not None:
            disconnected_event = ConnectorStatus(
                msg="Websocket connected",
                status=EConnectorStatus.CONNECTED,
                websocket_type=websocket_type,
            )
            await self._public_queue_stream.publish(
                BaseEvent(
                    event_type=EventType.CONNECTOR_STATUS_EVENT,
                    payload=Event[ConnectorStatus](
                        header=MessageHeader(
                            exchange=self._config.exchange, timestamp=int(time.time())
                        ),
                        data=disconnected_event,
                    ),
                )
            )

    """
    REST API Helpers
    """

    async def api_request(
        self,
        path_url: str,
        method: RESTMethod = RESTMethod.GET,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        is_auth_required: bool = False,
        return_err: bool = False,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        last_exception = None
        rest_assistant = await self._web_assistant_factory.get_rest_assistant()
        url = self._urls.BASE + path_url
        logger.debug("API request URL: %s", url)
        params = dict(sorted(params.items())) if isinstance(params, dict) else params
        data = dict(sorted(data.items())) if isinstance(data, dict) else data

        try:
            request_result = await rest_assistant.execute_request(
                url=url,
                params=params,
                data=data,
                method=method,
                is_auth_required=is_auth_required,
                ret_err=return_err,
                headers=headers,
            )
            if isinstance(request_result, dict):
                return request_result
            else:
                logger.warning("API request received request not in dictionary format")
                return {"res": request_result}
        except IOError as req_exc:
            last_exception = req_exc
            logger.error(
                "API request error: %s",
                str(last_exception),
            )
            raise

    @abstractmethod
    async def _subscribe_to_public_stream(self):
        """
        Abstract method to subscribe to the public data stream.
        """
        pass

    @abstractmethod
    async def _subscribe_to_trade_stream(self):
        """
        Abstract method to subscribe to the trade data stream.
        """
        pass

    @abstractmethod
    async def _subscribe_to_private_stream(self):
        """
        Abstract method to subscribe to the private data stream.
        """
        pass

    @abstractmethod
    async def _process_market_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Abstract method to process market data from the WebSocket response.

        Args:
            response (WSResponse): The WebSocket response containing market data.

        Returns:
            Optiona[BaseEvent]: The processed event if the method was successfull otherwise None
        """
        pass

    @abstractmethod
    def _process_trade_data(self, response: WSResponse) -> Optional[BaseEvent]:
        """
        Abstract method to process trade acknowledgment data from the WebSocket response.

        Args:
            response (WSResponse): The WebSocket response containing market data.

        Returns:
            Optiona[BaseEvent]: The processed event if the method was successfull otherwise None
        """
        pass

    @abstractmethod
    def _process_private_data(self, response: WSResponse) -> Optional[List[BaseEvent]]:
        """
        Abstract method to process private data from the WebSocket response.

        Args:
            response (WSResponse): The WebSocket response containing market data.

        Returns:
            Optiona[BaseEvent]: The processed event if the method was successfull otherwise None
        """
        pass

    @abstractmethod
    def _process_signal_event(self, event: BaseEvent) -> List[WSRequest]:
        """
        Abstract method to process event from the signal event queue and return the WSRequest to send to the exchange.

        Args:
            event (BaseEvent): The signal sent by the user to be decoded into requests.

        Returns:
            WSRequest: Request to be sent to the trade websocket connection.
        """
        pass

    @abstractmethod
    async def _process_http_signals(self, event: BaseEvent) -> Optional[BaseEvent]:
        """
        Abstract method to process event from the signal queue, perform the appropriate HTTP call.
        Parse the result and potentially return the event type to the user which can be used
        to inform the user of the results.

        Args:
            event (BaseEvent): The event sent by the user to be decoded.

        Returns:
            Optional[BaseEvent]: The event to be sent back to the user.
        """
        pass

    @abstractmethod
    def _get_connector_urls(self) -> ConnectorURL:
        pass

    async def _wait_ws_connected(self, ws: Optional[WSAssistant]):
        while ws is None:
            await asyncio.sleep(1)
        while not ws.connected:
            await asyncio.sleep(1)

    async def pinger(self):
        """
        Abstract method to send periodic ping messages to keep the WebSocket connection alive.
        """
        await self._wait_ws_connected(self._public_ws)

    async def pinger_trade(self):
        """
        Abstract method to send periodic ping messages to keep the WebSocket connection alive.
        """
        await self._wait_ws_connected(self._trade_ws)

    async def pinger_private(self):
        """
        Abstract method to send periodic ping messages to keep the WebSocket connection alive.
        """
        await self._wait_ws_connected(self._private_ws)

    """
    REST API Abstract methods
    """

    @abstractmethod
    async def get_server_time_ms(self) -> int:
        pass

    @abstractmethod
    async def fetch_wallet_balance(
        self, account_type: EAccountType = EAccountType.UNIFIED
    ) -> Wallet:
        pass

    @abstractmethod
    async def cancel_all_orders(
        self,
        order_category: EOrderCategory = EOrderCategory.SPOT,
        symbol: Optional[TradingPair] = None,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def fetch_klines(
        self,
        symbol: TradingPair,
        interval: str,
        start_time: str,
        end_time: str,
        category: EOrderCategory = EOrderCategory.SPOT,
        limit: int = 1000,
    ) -> List[Kline]:
        pass

    async def fetch_instrument_info(
        self, pair: TradingPair, category: EOrderCategory = EOrderCategory.SPOT
    ) -> List[InstrumentInfo]:
        """
        Fetch instrument info for a given trading pair and category from Bybit.

        :param pair: The trading pair (base and quote coin).
        :param category: The product type (spot, linear, inverse, option). Default is "spot".
        :return: A list of InstrumentInfo objects.
        """
        return NotImplemented

    @abstractmethod
    def _gen_symbols_table(self) -> Dict[str, TradingPair]:
        pass

    @abstractmethod
    def _gen_trading_pairs_table(self) -> Dict[TradingPair, str]:
        pass
