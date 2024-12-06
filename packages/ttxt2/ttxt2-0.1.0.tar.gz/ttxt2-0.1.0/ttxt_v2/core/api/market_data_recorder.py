import asyncio
import os
import time
import zlib
from collections import defaultdict
from dataclasses import asdict, dataclass
from enum import Enum, IntEnum
from typing import Dict, List, Optional

import msgpack

from ttxt_v2.utils.logger import logger

from .base_queue import IQueue
from .enums import EventType
from .event import BaseEvent
from .queue_consumer import IQueueConsumer
from .storage_backend import IStorageBackend
from .trading_pair import TradingPair

HOME = os.getenv("HOME")
assert HOME is not None, "Users need to have HOME env variable"


class CompressionLevel(IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 5
    HIGH = 9


@dataclass
class MarketDataRecorderConfig:
    exchange: str
    tickers: List[TradingPair]
    batch_size: int = 10 * 1024 * 1024  # 10Mb per batch per ticker
    file_path: str = f"{HOME}/Documents/"
    compression_level: CompressionLevel = CompressionLevel.NONE


class MarketDataRecorder(IQueueConsumer):
    """
    Class for recording market data and saving it via a storage strategy.
    The recorder reads events from a queue and batches them in chunks of
    10MB per ticker then serializes and write them with the possibility
    of compressions.

    Attributes:
        _config (MarketDataRecorderConfig): Configuration for the recorder
        queue (IQueue): The queue from which events will be read.
        storage_backend (IStorageBackend): The backend used for writing
        events to files / S3 / etc.
        _tickers: The lists of tickers
        _buffers (Dict[str,List[bytes]]): Dictionary of buffer per ticker where events
        are serialized.
        _start_times (Dict[str,Optional[int]]): Dictionary to map the files to the time
        of the first event (roughly)
        _locks (Dict[str,asyncio.Lock]): Locks to protect the files when we write to them.
        _stop_event (asyncio.Event): Event that is triggered when we want to stop recording.
        _background_task (Optional[asyncio.Task]): The task running in the background which
        will get events and serialize them.
    """

    def __init__(
        self,
        config: MarketDataRecorderConfig,
        msg_queue: IQueue,
        backend: IStorageBackend,
    ):
        self._config = config
        self.queue = msg_queue
        self.storage_backend = backend
        self._tickers = [self._ticker_key(ticker) for ticker in self._config.tickers]
        self._buffers: Dict[str, List[bytes]] = defaultdict(list)
        self._buffer_sizes: Dict[str, int] = defaultdict(int)
        self._start_times: Dict[str, Optional[int]] = {
            ticker: None for ticker in self._tickers
        }
        self._locks: Dict[str, asyncio.Lock] = {
            ticker: asyncio.Lock() for ticker in self._tickers
        }
        self._stop_event: asyncio.Event = asyncio.Event()
        self._background_task: Optional[asyncio.Task] = None

    async def start(self):
        logger.info(f"Starting MarketDataRecorder for {self._config.exchange}")
        self._background_task = asyncio.create_task(self.queue_reader(self.queue))

    async def stop(self):
        logger.info("Stopping MarketDataRecorder and waiting for it to finish")
        self._stop_event.set()
        if self._background_task:
            await self._background_task
        logger.info(f"MarketDataRecorder for {self._config.exchange} stopped")

    async def queue_reader(self, queue: IQueue):
        try:
            while not self._stop_event.is_set():
                event: BaseEvent = await queue.poll()
                await self.process_event(event)
        except asyncio.CancelledError:
            logger.info("MarketRecorder stopped reading from queue...")
        finally:
            await self._flush_all_buffers()

    async def process_event(self, event: BaseEvent):
        try:
            if event.event_type in [
                EventType.OB_EVENT,
                EventType.MT_EVENT,
                EventType.KL_EVENT,
            ]:
                trading_pair = event.payload.data.trading_pair
                ticker = self._ticker_key(trading_pair)
                if ticker not in self._tickers:
                    logger.warning(f"Unknown ticker: {ticker}")
                    return

                event_dict = asdict(event)
                event_bytes = msgpack.packb(
                    event_dict,
                    use_bin_type=True,
                    default=lambda o: o.value if isinstance(o, Enum) else o,
                )
                assert event_bytes is not None, "Failed to serialize data"
                async with self._locks[ticker]:
                    # Set the start time if not set
                    if self._start_times[ticker] is None:
                        self._start_times[ticker] = int(time.time_ns() / 1_000_000)

                    self._buffers[ticker].append(event_bytes)
                    self._buffer_sizes[ticker] += len(event_bytes)

                    if self._buffer_sizes[ticker] >= self._config.batch_size:
                        await self._flush_buffer(ticker)
        except Exception as e:
            logger.error(f"Error in processing event {event}, exception: {e}")

    async def _flush_buffer(self, ticker: str):
        async with self._locks[ticker]:
            buffer = self._buffers[ticker]
            if not buffer:
                return
            data = b"".join(buffer)
            start_time_ms = self._start_times[ticker]
            assert start_time_ms is not None, "Start time cannot be None"
            file_name = self._generate_file_name(ticker, start_time_ms)
            try:
                if self._config.compression_level != CompressionLevel.NONE:
                    compression_level_value = self._config.compression_level.value
                    try:
                        data = zlib.compress(data, level=compression_level_value)
                        logger.info(
                            f"Compressed data for {ticker} with level {self._config.compression_level.name}"
                        )
                    except Exception as e:
                        logger.error(f"Compression failed for {ticker}: {e}")
                await self.storage_backend.write_batch(file_name, data)
                logger.info(f"Wrote buffer for {ticker} to {file_name}")
            except Exception as e:
                logger.error(
                    f"Failed to write batch for {ticker} to file {file_name}: {e}"
                )
                """
                TODO: (ivan)
                Handle potential data loss
                Optionally, implement retry logic or save data elsewhere
                """
            finally:
                self._buffers[ticker].clear()
                self._buffer_sizes[ticker] = 0
                self._start_times[ticker] = None  # Will be set on next event

    async def _flush_all_buffers(self):
        tasks = []
        for ticker in self._tickers:
            tasks.append(self._flush_buffer(ticker))
        if tasks:
            await asyncio.gather(*tasks)

    def _generate_file_name(self, ticker: str, start_time_ms: int) -> str:
        exchange = self._config.exchange.upper()
        base, quote = ticker.split("_")
        ext = ".bin"
        if self._config.compression_level != CompressionLevel.NONE:
            ext += ".gz"
        file_name = f"{exchange}_{base}_{quote}_{start_time_ms}{ext}"
        return file_name

    def _ticker_key(self, ticker: TradingPair) -> str:
        return f"{ticker.base}_{ticker.quote}".upper()
