import pytest
from typing import AsyncGenerator, Union, Optional, Callable, List, Dict, Any
from .fixtures import *
from datapools.worker.plugins.base_plugin import BasePlugin, UnexpectedContentTypeException, DownloadFailureException
from datapools.worker.types import WorkerContext
from datapools.common.http import download
from datapools.common.types import (
    BaseCrawlerResult,
    CrawlerBackTask,
    DatapoolContentType,
    WorkerTask,
    StudyUrlTask,
    CrawlerNop,
)


class FakePlugin(BasePlugin):

    @staticmethod
    def is_supported(url):
        return True

    def process(self, task: WorkerTask):
        yield CrawlerNop()


@pytest.mark.anyio
async def test_download(
    app,
    #    session,
    #    worker,
    worker_context,
):
    path = get_data_abs_path("empty_meta.mp3")

    plugin = FakePlugin(worker_context)

    content = await download(f"http://{TEST_APP_HOST}:{TEST_APP_PORT}/download?path={path}")

    with open(path, "rb") as f:
        content2 = f.read()
        assert content == content2


@pytest.mark.anyio
async def test_astream(
    app,
    #    session,
    #    worker,
    worker_context,
):
    path = get_data_abs_path("empty_meta.mp3")

    plugin = FakePlugin(worker_context)

    content = bytes()
    async for chunk in plugin.astream(
        f"http://{TEST_APP_HOST}:{TEST_APP_PORT}/download?path={path}", expected_type=DatapoolContentType.Audio
    ):
        content += chunk

    with open(path, "rb") as f:
        content2 = f.read()
        assert content == content2

    # expecting Video instead of Audio
    try:
        async for chunk in plugin.astream(
            f"http://{TEST_APP_HOST}:{TEST_APP_PORT}/download?path={path}", expected_type=DatapoolContentType.Video
        ):
            pass
    except DownloadFailureException:
        pass
    else:
        assert False, "Should fail on Audio!=Video"
