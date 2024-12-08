import asyncio
import json
import os
import urllib
from typing import Optional

import websockets

from datapools.common.logger import logger
from datapools.common.types import BaseProducerSettings, SchedulerSettings, WorkerSettings
from datapools.producer import BaseProducer
from datapools.scheduler import CrawlerScheduler
from datapools.worker.worker import CrawlerWorker

"""
In cli mode `plugins` keys are used to define WorkerSettings.USE_ONLY_PLUGINS and ADDITIONAL_PLUGINS fields:
So only listed plugins will be loaded.

`queue.connection_url` expects Rabbitmq running locally. 
Run it as `docker run --rm -p 15672:15672 -p 5672:5672 rabbitmq:3.10.7-management` for example
"""
default_config = {
    "backend": {"api_url": "https://openlicense.ai/internal/", "hints_period": 10},
    "queue": {"connection_url": "amqp://guest:guest@localhost:5672", "size_limit": 1},
    "redis": {"host": "localhost", "port": 6379},
    "storage": {"worker": {"path": "/tmp/datapools_storage"}, "producer": {"path": None}},
    "plugins": {
        # "s3": {"aws_access_key_id": None, "aws_secret_access_key": None},
        # "google_drive": {"api_key": ""},
        # "imageshack": {},
    },
}

# async def crawl( hint_urls: Union[AnyUrl, Set[AnyUrl]], config_file: Optional[str] = None):


def crawl(datapool_id: int = 1, config_file: Optional[str] = None):
    async def crawl_async():

        # loading config from json or using default one
        if config_file is not None:
            with open(config_file, "r") as f:
                config = json.load(f)
        else:
            config = default_config

        # initializing and starting Scheduler
        s_cfg = SchedulerSettings()
        s_cfg.load(config)
        s_cfg.CLI_MODE = True
        scheduler = CrawlerScheduler(s_cfg)
        scheduler.run()

        # initializing and starting Worker
        w_cfg = WorkerSettings()
        w_cfg.load(config)
        w_cfg.CLI_MODE = True
        if not os.path.exists(w_cfg.STORAGE_PATH):
            os.mkdir(w_cfg.STORAGE_PATH)

        plugins_list = [plugin_name for plugin_name in config["plugins"]]
        w_cfg.USE_ONLY_PLUGINS = plugins_list
        w_cfg.ADDITIONAL_PLUGINS = plugins_list

        worker = CrawlerWorker(w_cfg)
        worker.run()

        # initializing and starting Producer
        p_cfg = BaseProducerSettings()
        p_cfg.load(config)
        p_cfg.CLI_MODE = True
        if p_cfg.STORAGE_PATH is not None and not os.path.exists(p_cfg.STORAGE_PATH):
            os.mkdir(p_cfg.STORAGE_PATH)

        producer = BaseProducer(p_cfg)
        producer.run()

        # get datapool contents stream from the backend
        o = urllib.parse.urlparse(f"{config[ 'backend_api_url' ]}get-datapool-stream")
        if o.scheme == "http":
            url = o._replace(scheme="ws").geturl()
        elif o.scheme == "https":
            url = o._replace(scheme="wss").geturl()
        logger.info(f"connecting backend websocket {url=}")

        async with websockets.connect(url) as ws:
            logger.info("connected backend websocket")
            await ws.send(json.dumps({"id": datapool_id}))
            logger.info("sent stream request")
            try:
                while True:
                    msg = json.loads(await ws.recv())
                    logger.info(f"{msg=}")
                    await scheduler.add_download_task(msg["url"], msg["type"])
            except websockets.exceptions.ConnectionClosed:
                logger.info("connection closed")

        logger.info("pushing end marker")
        # telling scheduler that this is the end of stream
        await scheduler.add_download_task("")

        await asyncio.gather(scheduler.wait(), worker.wait(), producer.wait())
        logger.info("waited all")

        await asyncio.gather(scheduler.stop(), worker.stop(), producer.stop())
        logger.info("stopped all")

    asyncio.run(crawl_async())
