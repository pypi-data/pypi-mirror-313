from datapools.common.logger import logger

from datapools.common.types import CrawlerNop, WorkerTask
from datapools.worker.plugins.base_plugin import (
    BasePlugin,
)
from datapools.worker.types import WorkerContext


class SamplePlugin(BasePlugin):
    def __init__(self, ctx: WorkerContext):
        super().__init__(ctx)

    @staticmethod
    def is_supported(__url):
        return False

    async def process(self, task: WorkerTask):
        logger.info(f"SamplePlugin: {task.url=}")
        yield CrawlerNop()
