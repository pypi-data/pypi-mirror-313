from urllib.parse import urlparse

# from pydantic import AnyUrl, BaseModel
from ..logger import logger
from .types import *

import aio_pika  # TODO:make conditional import


class GenericQueue:
    def __init__(
        self,
        role: QueueRole,
        url=None,
        name: Optional[str] = None,
        exchange_name: Optional[str] = None,
        exchange_type: Optional[aio_pika.ExchangeType] = aio_pika.ExchangeType.DIRECT,
        size: Optional[int] = 1,
        routing_key: Optional[str] = None,
        max_priority: Optional[int] = None,
        exclusive: Optional[bool] = False,
    ):
        parsed = urlparse(url)
        if parsed.scheme == "amqp":

            from .rabbitmq import RabbitmqParams, RabbitmqQueue

            params = RabbitmqParams(
                prefetch_count=size,
                exclusive=exclusive,
                exchange_name=exchange_name,
                exchange_type=exchange_type,
                routing_key=routing_key,
                x_max_priority=max_priority,
            )

            logger.info(f"RabbitmqQueue {url=}")
            self.queue = RabbitmqQueue(role, url, name, params)
        else:
            raise Exception(f"not supported {url=}")

    async def run(self):
        await self.queue.run()

    async def is_ready(self, timeout: Optional[int] = None):
        return await self.queue.is_ready(timeout)

    async def stop(self):
        await self.queue.stop()

    async def until_empty(self):
        await self.queue.until_empty()

    async def push(self, data):
        await self.queue.push(data)

    async def pop(self, timeout=None):
        return await self.queue.pop(timeout)

    async def reject(self, message, requeue=True):
        await self.queue.reject(message, requeue)

    async def mark_done(self, message):
        await self.queue.mark_done(message)

    async def delete(self):
        await self.queue.delete()
