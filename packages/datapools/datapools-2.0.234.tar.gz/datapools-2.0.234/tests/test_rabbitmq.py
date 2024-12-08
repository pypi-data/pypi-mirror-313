import os
import asyncio
import time
import pytest
from datapools.common.queues import GenericQueue, QueueRole, QueueMessage, QueueMessageType
from datapools.common.logger import logger


@pytest.mark.anyio
async def test_rabbitmq_basic():
    rq = None
    wq = None
    try:
        wq = GenericQueue(
            role=QueueRole.Publisher,
            name="test_q",
            url=os.environ.get("QUEUE_CONNECTION_URL"),
        )
        await wq.run()
        assert await wq.is_ready(timeout=5)

        await wq.push(QueueMessage(message_type=QueueMessageType.Task, data="test"))

        rq = GenericQueue(
            role=QueueRole.Receiver,
            name="test_q",
            url=os.environ.get("QUEUE_CONNECTION_URL"),
        )
        await rq.run()
        assert await rq.is_ready(timeout=5)

        message = await rq.pop(timeout=1)
        assert message is not None
        qm = QueueMessage.decode(message.body)
        assert qm.type == QueueMessageType.Task
        assert qm.data == "test"

    finally:
        if wq:
            await wq.delete()
            await wq.stop()
        if rq:
            await rq.delete()
            await rq.stop()


@pytest.mark.anyio
async def test_rabbitmq_size():
    rq = None
    wq = None
    try:
        SIZE = 10000

        wq = GenericQueue(
            role=QueueRole.Publisher,
            name="test_q",
            url=os.environ.get("QUEUE_CONNECTION_URL"),
        )
        assert wq.queue.is_producer()
        await wq.run()
        assert await wq.is_ready(timeout=5)

        start = time.time()
        for i in range(SIZE):
            await wq.push(QueueMessage(message_type=QueueMessageType.Task, data=f"test{i}"))
        await wq.until_empty()
        logger.info(f"pushed {SIZE} messages in {time.time()-start} {time.time()=}")

        rq = GenericQueue(role=QueueRole.Receiver, name="test_q", url=os.environ.get("QUEUE_CONNECTION_URL"), size=100)
        assert rq.queue.is_receiver()
        await rq.run()
        logger.info(f"rq started {time.time()=}")
        assert await rq.is_ready(timeout=5)
        logger.info(f"rq ready {time.time()=}")

        # while True:
        #     await asyncio.sleep(1)
        expected = set(f"test{i}" for i in range(SIZE))

        start = time.time()
        for i in range(SIZE):
            # logger.info(i)
            message = await rq.pop(timeout=1)
            assert message is not None
            qm = QueueMessage.decode(message.body)
            assert qm.type == QueueMessageType.Task
            assert qm.data in expected
            expected.discard(qm.data)

            if i % 2 == 0:
                await rq.mark_done(message)
            else:
                await rq.reject(message, requeue=False)

        assert len(expected) == 0

        await rq.until_empty()
        logger.info(f"poped {SIZE} messages in {time.time()-start}")

        # no messages left in queue
        message = await rq.pop(timeout=1)
        assert message is None
    finally:
        if wq:
            await wq.delete()
            await wq.stop()
        if rq:
            await rq.delete()
            await rq.stop()
