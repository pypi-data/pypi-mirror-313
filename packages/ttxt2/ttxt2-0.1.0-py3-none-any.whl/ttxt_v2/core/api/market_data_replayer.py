import asyncio
import os
from dataclasses import dataclass
from typing import Optional

import aiofiles
import dacite
import msgpack

from ttxt_v2.core.api.queue_publisher import IQueuePublisher
from ttxt_v2.utils.logger import logger

from .base_queue import IQueue
from .enums import *
from .event import BaseEvent, Event
from .header import MessageHeader
from .kline import Kline
from .market_trades import MarketTrades
from .orderbook import Orderbook
from .trading_pair import TradingPair

HOME = os.getenv("HOME", "")
assert HOME is not None, "Users need to have a HOME env variable"


@dataclass
class MarketDataReplayerConfig:
    exchange: str
    ticker: TradingPair
    file_path: str = f"{HOME}/Documents"
    buffer_size: int = 8192


class MarketDataReplayer(IQueuePublisher):
    def __init__(self, config: MarketDataReplayerConfig, msg_queue: IQueue):
        self._config = config
        self._queue = msg_queue
        self._stop_event = asyncio.Event()
        self._background_task: Optional[asyncio.Task] = None
        file_name = f"{self._config.exchange}_{self._config.ticker.base}_{self._config.ticker.quote}".upper()
        self._file_path = f"{self._config.file_path}/{file_name}.bin"

    @property
    def config(self) -> MarketDataReplayerConfig:
        return self._config

    @property
    def queue(self) -> IQueue:
        return self._queue

    async def start(self):
        logger.info(f"Starting MarketDataReplayer with config: %s", str(self._config))
        self._background_task = asyncio.create_task(self._replay_data())

    async def stop(self):
        self._stop_event.set()
        if self._background_task:
            await self._background_task
        logger.info("MarketDataReplayer stopped")

    async def _replay_data(self):
        try:
            async with aiofiles.open(self._file_path, mode="rb") as f:
                unpacker = msgpack.Unpacker(raw=False)
                async for chunk in self._read_chunks(f, chunk_size=8192):
                    unpacker.feed(chunk)
                    for event_obj in unpacker:
                        if isinstance(event_obj, list):
                            for event_dict in event_obj:
                                event = self._deserialize_event(event_dict)
                                if event:
                                    await self.publish_to_queue(self._queue, event)
                                if self._stop_event.is_set():
                                    logger.info("Stop event is set. Stopping...")
                                    break
                        elif isinstance(event_obj, dict):
                            event = self._deserialize_event(event_obj)
                            if event:
                                await self.publish_to_queue(self._queue, event)
                            if self._stop_event.is_set():
                                break
                        else:
                            logger.error(f"Unexpected event type: {type(event_obj)}")

            logger.info(f"Finished replaying file: {self._file_path}")
        except asyncio.CancelledError:
            logger.warning("Replay data has been cancelled")
        except Exception as e:
            logger.error(f"Failed to replay from file {self._file_path}: {e}")

    async def _read_chunks(self, file, chunk_size: int = 8192):
        """
        Asynchronously reads the file in chunks.

        Args:
            file: The file object to read from.
            chunk_size (int): Size of each chunk to read.

        Yields:
            bytes: The chunk of data read.
        """
        while True:
            logger.debug("reading a chunk...")
            chunk = await file.read(chunk_size)
            if not chunk:
                logger.info("No more chunks to read")
                break
            yield chunk

    def _deserialize_event(self, event_dict: dict) -> Optional[BaseEvent]:
        try:
            # Decode based on event type
            event_type = EventType(event_dict["event_type"])
            payload_data = event_dict["payload"]["data"]
            header_data = event_dict["payload"]["header"]

            # Use the appropriate data type for each event type
            payload_class = self._get_payload_class(event_type)
            if not payload_class:
                logger.error(f"No payload class found for event type: {event_type}")
                return None

            # Configure dacite to handle enums and nested dataclasses
            config = dacite.Config(
                type_hooks={
                    EventType: EventType,
                    ESide: ESide,
                    EUpdateType: EUpdateType,
                    EOrderType: EOrderType,
                },
                cast=[Enum],
            )

            payload_header = dacite.from_dict(
                data_class=MessageHeader, data=header_data
            )
            # Deserialize payload using dacite
            payload_ev = dacite.from_dict(
                data_class=payload_class, data=payload_data, config=config
            )
            if event_type == EventType.OB_EVENT:
                payload = Event[Orderbook](header=payload_header, data=payload_ev)
            elif event_type == EventType.MT_EVENT:
                payload = Event[MarketTrades](header=payload_header, data=payload_ev)
            elif event_type == EventType.KL_EVENT:
                payload = Event[Kline](header=payload_header, data=payload_ev)
            else:
                raise RuntimeError("Unidentified event type")

            return BaseEvent(event_type=event_type, payload=payload)
        except Exception as e:
            logger.error(f"Failed to deserialize event {event_dict}: {e}")
            return None

    def _get_payload_class(self, event_type: EventType):
        """
        Maps EventType to its corresponding class.

        Args:
            event_type (EventType): The type of the event.

        Returns:
            Type: Corresponding class for the payload, or None if not found.
        """
        payload_mapping = {
            EventType.OB_EVENT: Orderbook,
            EventType.MT_EVENT: MarketTrades,
            EventType.KL_EVENT: Kline,
        }
        return payload_mapping.get(event_type)
