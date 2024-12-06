import os

import aiofiles

from ttxt_v2.utils.logger import logger

from .storage_backend import IStorageBackend


class LocalStorageBackend(IStorageBackend):
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(self.file_path, exist_ok=True)

    async def write_batch(self, file_name: str, data: bytes):
        try:
            full_path = os.path.join(self.file_path, file_name)
            async with aiofiles.open(full_path, mode="wb") as f:
                await f.write(data)
            logger.info(f"Wrote data to {full_path}")
        except Exception as e:
            logger.error(f"Failed to write batch to local file {file_name}: {e}")
