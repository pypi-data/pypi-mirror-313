import asyncio
import subprocess
import uvicorn
import logging
import pytest
from pathlib import Path
from pytest import fixture
from httpx import AsyncClient

from datapools.common.session_manager import Session, SessionManager, SessionStatus, URLState
from datapools.common.types import WorkerSettings, CrawlerHintURLStatus
from datapools.common.logger import setup_logger
from datapools.worker.worker import CrawlerWorker
from datapools.worker.types import WorkerContext

from .app import app as test_app
from multiprocessing import Process

TEST_APP_HOST = "localhost"
TEST_APP_PORT = 8000


@pytest.fixture(scope="module")
def setup():
    logging.info("SETUP")
    setup_logger()


@fixture()
def worker_settings(setup):
    return WorkerSettings()


@fixture()
def worker_context(worker_settings, session):
    return WorkerContext(session=session, storage_path=worker_settings.STORAGE_PATH)


@pytest.fixture(scope="module")
async def worker():
    global worker

    worker_settings = WorkerSettings()

    # if worker-config.json exists, then load it overwriting env config
    # cfg_path = "./config.json"
    # if os.path.isfile(cfg_path):
    #     worker_settings.fload(cfg_path)
    worker = CrawlerWorker(worker_settings)

    await worker.run()

    yield worker

    await worker.stop()


@fixture()
async def session_manager(worker_settings) -> SessionManager:
    res = SessionManager(worker_settings.REDIS_HOST)
    yield res
    await res.stop()


@fixture()
async def session(session_manager) -> Session:
    res = await session_manager.create(1)
    yield res
    await session_manager.remove(res.id)


@pytest.fixture(scope="session")
async def asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield
    loop.close()


# @pytest.fixture(scope="module")
# async def client(asyncio_loop, setup):
#     async with AsyncClient(app=app, base_url="http://localhost") as res:
#         logging.info("client before on_init()")
#         await on_init(app)

#         # bck = get_bck()
#         # total_sleep = 0.0
#         # while not bck.is_ready():
#         #     await asyncio.sleep(0.5)
#         #     total_sleep += 0.5
#         #     if total_sleep > 10:
#         #         logging.error("too long to get bck ready")
#         #         assert False
#         logging.info("client on_init() done ")
#         yield res
#         logging.info("CLIENT ON_SHUTDOWN")
#         await on_shutdown(app)
#         logging.info("CLIENT ON_SHUTDOWN DONE")


@pytest.fixture(scope="module")
async def app():

    proc = Process(
        target=uvicorn.run,
        args=(test_app,),
        kwargs={"host": TEST_APP_HOST, "port": TEST_APP_PORT, "log_level": "info"},
        daemon=True,
    )
    proc.start()
    await asyncio.sleep(0.1)  # time for the server to start

    yield

    proc.terminate()


def get_data_abs_path(name):
    base_path = Path(__file__).parent
    return str((base_path / f"data/{name}").resolve())
