import asyncio
import subprocess
import os
import io
import re
import asyncio
from cachetools import TTLCache
from asyncache import cached
from typing import Union
from contextlib import AbstractContextManager

from ..logger import logger
from .base_storage import BaseStorage


ONE_MB = 1024 * 1024


@cached(cache=TTLCache(maxsize=10000, ttl=60))
def get_lock(path: str):
    return asyncio.Lock()


@cached(cache=TTLCache(maxsize=10000, ttl=60))
async def get_dir_size(path: str):
    return await get_dir_size_nc(path)


async def get_dir_size_nc(path: str):
    logger.info("getting storage total size")
    cmd = f"du -sb {path}"
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, __stderr = await proc.communicate()
    res = stdout.decode()
    m = re.match(r"^(\d+)", res)
    if m:
        g = m.groups()
        if g:
            # empty directory takes 4K.
            # TODO: should not be hardcoded..
            size = int(g[0]) - 4096
            logger.info(f"got storage total size: {size}")
            return size
    return None


class FileStorageContextManager(AbstractContextManager):
    f: io.IOBase

    def __init__(self, path, mode):
        logger.debug(f"Opening storage file: {path}, size={os.path.getsize(path)}")
        self.f = open(path, mode)

    def __enter__(self):
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()


class FileStorage(BaseStorage):
    dst_path: str
    depth: int

    def __init__(self, dst_path: str, must_exist: bool = False, depth: int = 0):
        if must_exist is False:
            os.makedirs(dst_path, exist_ok=True)
        # else:
        #     if not os.path.exists(dst_path):
        #         raise FileNotFoundError()
        self.dst_path = dst_path
        self.depth = depth

    async def put(self, storage_id, content: Union[str, bytes, io.IOBase]):
        path = self.get_path(storage_id)
        if self.depth > 0:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        logger.debug(f"FileStorage::put {path=}")
        with open(path, "wb") as f:
            if isinstance(content, str):
                content = content.encode()
            if isinstance(content, bytes):
                f.write(content)
                f.flush()
            elif isinstance(content, io.IOBase):
                content.seek(0, 0)
                total = 0
                while True:
                    buffer = content.read(ONE_MB)
                    if not buffer:
                        break
                    f.write(buffer)
                    total += len(buffer)
                    await asyncio.sleep(0)
                logger.debug(f"put {total=}")
            else:
                raise Exception(f"Unknown source {type(content)=}")

    async def read(self, storage_id):
        # TODO: make async generator and read by chunks
        with open(self.get_path(storage_id), "rb") as f:
            res = f.read()
            return res

    def get_reader(self, storage_id) -> FileStorageContextManager:
        return FileStorageContextManager(self.get_path(storage_id), "rb")

    async def remove(self, storage_id):
        path = self.get_path(storage_id)
        logger.debug(f"unlink {path=}")
        os.unlink(path)

    async def has(self, storage_id):
        path = self.get_path(storage_id)
        return os.path.exists(path)

    def get_path(self, storage_id):
        args = [] if self.depth == 0 else list(storage_id)[0 : self.depth]
        return os.path.join(self.dst_path, *args, storage_id)

    async def clear(self):
        subprocess.run(
            f'rm -rf {os.path.join(self.dst_path, "*")}',
            check=True,
            shell=True,
        )

    async def get_total_size(self, cache_allowed=True):
        async with get_lock(self.dst_path):
            if cache_allowed:
                return await get_dir_size(self.dst_path)
            return await get_dir_size_nc(self.dst_path)
