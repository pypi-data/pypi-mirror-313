from abc import abstractmethod

from contextlib import AbstractContextManager
from hashlib import md5


class BaseStorage:
    @abstractmethod
    async def put(self, storage_id, content): ...

    @abstractmethod
    def get_reader(self, storage_id) -> AbstractContextManager: ...

    @abstractmethod
    async def read(self, storage_id) -> bytes: ...

    @abstractmethod
    async def remove(self, storage_id): ...

    @abstractmethod
    async def has(self, storage_id): ...

    def gen_id(self, data: str | bytes):
        return md5(data.encode() if isinstance(data, str) else data).hexdigest()
