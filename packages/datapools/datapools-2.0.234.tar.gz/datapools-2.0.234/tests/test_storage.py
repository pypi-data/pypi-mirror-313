import pytest
import os

# from random import randint
import time
from datapools.worker.plugins.base_plugin import BasePlugin, BaseTag
from datapools.worker.plugins.ftp import FTPPlugin
from datapools.worker.types import WorkerContext
from datapools.common.storage import FileStorage, SessionFileStorage
from .fixtures import *

from tempfile import gettempdir


@pytest.mark.anyio
async def test_file_storage():
    tmp = gettempdir()

    path = os.path.join(tmp, str(time.time()))
    assert not os.path.exists(path)
    FileStorage(path, must_exist=False)
    assert os.path.exists(path)

    s = FileStorage(tmp, must_exist=True)

    data = str(time.time())
    storage_id = s.gen_id(data)
    path = s.get_path(storage_id)

    assert not await s.has(storage_id)
    await s.put(storage_id, data)
    assert os.path.isfile(path)
    assert await s.has(storage_id)

    data2 = await s.read(storage_id)
    assert isinstance(data2, bytes)
    assert data2.decode() == data

    reader = s.get_reader(storage_id)
    with reader as f:
        data2 = f.read()
        assert isinstance(data2, bytes)
        assert data2.decode() == data

    await s.remove(storage_id)
    assert not os.path.exists(path)
    assert not await s.has(storage_id)

    # print("xxxxxxxxxxxxxxxxxxx")
    # s = FileStorage(tmp, depth=2)
    # start = time.time()
    # for _ in range(0, 10000):
    #     a = "a" * randint(100, 100000)
    #     storage_id = s.gen_id(a)
    #     await s.put(storage_id, a)
    #     await s.remove(storage_id)
    # print(f"benchmark {time.time()-start}")


@pytest.mark.anyio
async def test_storage_depth():
    tmp = gettempdir()
    storage_path = os.path.join(tmp, str(time.time()))

    def get_storage(depth):
        return FileStorage(storage_path, depth=depth)

    assert get_storage(0).get_path("asd") == os.path.join(storage_path, "asd")
    assert get_storage(1).get_path("asd") == os.path.join(storage_path, "a", "asd")
    assert get_storage(2).get_path("asd") == os.path.join(storage_path, "a", "s", "asd")

    s2 = get_storage(2)
    storage_id = "abcdef"
    await s2.put(storage_id, "somecontent")
    assert os.path.exists(os.path.join(storage_path, "a", "b", storage_id))
    await s2.clear()


@pytest.mark.anyio
async def test_session_storage_total_size():
    session_id = str(time.time())
    s = SessionFileStorage(gettempdir(), session_id)

    assert await s.get_total_size(cache_allowed=False) == 0

    content = "a" * 1000
    storage_id = s.gen_id(content)
    await s.put(storage_id, content)

    assert await s.get_total_size(cache_allowed=False) == len(content)

    await s.clear()

    assert await s.has(storage_id) is False

    assert await s.get_total_size(cache_allowed=False) == 0
