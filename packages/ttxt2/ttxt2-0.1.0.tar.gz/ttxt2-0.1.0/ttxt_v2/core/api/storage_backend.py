from abc import ABC, abstractmethod


class IStorageBackend(ABC):
    @abstractmethod
    async def write_batch(self, file_name: str, data: bytes):
        pass
