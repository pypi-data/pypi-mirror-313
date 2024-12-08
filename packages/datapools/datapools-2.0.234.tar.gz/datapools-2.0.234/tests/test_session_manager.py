import asyncio
import logging
import pytest
from pytest import fixture
from .fixtures import *

from datapools.common.session_manager import Session, SessionManager, SessionStatus, URLState, SESSION_ID_LEN
from datapools.common.types import WorkerSettings, CrawlerHintURLStatus
from datapools.common.logger import setup_logger


# @pytest.fixture(scope="session")
# async def asyncio_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield
#     loop.close()


# TODO: move to some common lib to share among all tests
@pytest.mark.anyio
async def test_session_id(session):
    assert len(session.id) == SESSION_ID_LEN

@pytest.mark.anyio
async def test_session_status(session):
    assert await session.get_last_reported_status() == CrawlerHintURLStatus.Unprocessed

    await session.set_last_reported_status(CrawlerHintURLStatus.Success)
    assert await session.get_last_reported_status() == CrawlerHintURLStatus.Success


# @pytest.mark.anyio
# async def test_postponed(session_manager):
#     # no limits
#     assert await session_manager.list_postponed() == []
#     await session_manager.push_postponed("ses1")
#     assert await session_manager.list_postponed() == ["ses1"]
#     await session_manager.pop_postponed("ses1")
#     assert await session_manager.list_postponed() == []

#     # with limits
#     assert await session_manager.list_postponed(10) == []
#     await session_manager.push_postponed("ses1")
#     assert await session_manager.list_postponed(10) == ["ses1"]
#     await session_manager.pop_postponed("ses1")
#     assert await session_manager.list_postponed(10) == []


@pytest.mark.anyio
async def test_url_state(session):
    assert await session.has_url("WorkerTask.url") is False
    assert await session.get_url_state("WorkerTask.url") is None

    # add url
    await session.add_url("WorkerTask.url")
    assert await session.has_url("WorkerTask.url") is True
    state = await session.get_url_state("WorkerTask.url")
    assert isinstance(state, URLState)
    assert state.worker_id == ""
    assert state.status == CrawlerHintURLStatus.Unprocessed
    assert await session.all_urls_processed() is False

    # set worker
    await session.set_url_worker("WorkerTask.url", "worker1")
    state = await session.get_url_state("WorkerTask.url")
    assert isinstance(state, URLState)
    assert state.worker_id == "worker1"
    assert state.status == CrawlerHintURLStatus.Unprocessed
    assert await session.all_urls_processed() is False

    # set status
    await session.set_url_status("WorkerTask.url", CrawlerHintURLStatus.Success)
    state = await session.get_url_state("WorkerTask.url")
    assert isinstance(state, URLState)
    assert state.worker_id == "worker1"
    assert state.status == CrawlerHintURLStatus.Success
    assert await session.all_urls_processed() is True
