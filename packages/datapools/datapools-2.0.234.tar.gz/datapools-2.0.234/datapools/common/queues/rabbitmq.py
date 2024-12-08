import asyncio
import json
import logging
import time
import traceback
from typing import List, Optional, Union, Set
from urllib.parse import urlparse

import aio_pika
import aiormq
from httpx import AsyncClient
from pydantic import BaseModel

from ..logger import logger
from ..stoppable import Stoppable
from .types import QueueRole, QueueRoutedMessage, BaseQueueMessage

MAX_PUBLISHING_TASKS = 100
# MAX_ACK_TASKS = 100

logging.getLogger("aio_pika").setLevel(logging.WARNING)


class RestAPI:
    def __init__(self, connection_url):
        p = urlparse(connection_url)
        # TODO: port should be configurable
        self.url = f"http://{p.username}:{p.password}@{p.hostname}:15672/api/"

        logging.getLogger("httpx").setLevel(logging.WARNING)  # disable verbose logging when global level is INFO

    async def get_queue(self, queue_name):
        async with AsyncClient() as client:
            r = await client.get(f"{self.url}queues/%2f/{queue_name}")
            q = r.json()
            # print(q)
            return q


class RabbitmqParams(BaseModel):
    exchange_type: Optional[aio_pika.ExchangeType] = aio_pika.ExchangeType.DIRECT
    exchange_name: Optional[str] = None
    routing_key: Optional[Union[str, List[str]]] = None
    prefetch_count: Optional[int] = 1
    exclusive: Optional[bool] = False
    x_max_priority: Optional[int] = None


class AsyncDeque(asyncio.Queue):
    async def put_front(self, item):
        """Put an item into the queue.

        Put an item into the queue. If the queue is full, wait until a free
        slot is available before adding item.
        """
        while self.full():
            putter = self._get_loop().create_future()
            self._putters.append(putter)
            try:
                await putter
            except:
                putter.cancel()  # Just in case putter is not done yet.
                try:
                    # Clean self._putters from canceled putters.
                    self._putters.remove(putter)
                except ValueError:
                    # The putter could be removed from self._putters by a
                    # previous get_nowait call.
                    pass
                if not self.full() and not putter.cancelled():
                    # We were woken up by get_nowait(), but can't take
                    # the call.  Wake up the next in line.
                    self._wakeup_next(self._putters)
                raise
        return self.put_nowait_front(item)

    def put_nowait_front(self, item):
        """Put an item into the queue without blocking.

        If no free slot is immediately available, raise QueueFull.
        """
        if self.full():
            raise asyncio.queues.QueueFull
        self._put_front(item)
        self._unfinished_tasks += 1
        self._finished.clear()
        self._wakeup_next(self._getters)

    def _put_front(self, item):
        self._queue.appendleft(item)


class RabbitmqQueue(Stoppable):
    connection: Optional[aio_pika.robust_connection.RobustConnection] = None
    channel: Optional[aio_pika.channel.Channel] = None
    queue_w: AsyncDeque
    queue_r: asyncio.Queue
    # queue_ack: AsyncDeque
    queue_name: Optional[str]
    queue: Optional[aio_pika.queue.Queue] = None
    exchange_name: Optional[str]
    exchange: Optional[aio_pika.exchange.Exchange] = None
    _is_ready: asyncio.Event
    _publishing_tasks: Set[asyncio.Task]
    # _last_channel_activity: Optional[float]
    # _is_publishing: asyncio.Event
    # _acknack_tasks: Set[asyncio.Task]

    def __init__(
        self,
        role: QueueRole,
        connection_url: str,
        queue_name: Optional[str] = None,
        params: Optional[RabbitmqParams] = RabbitmqParams(),
    ):
        super().__init__()
        self.role = role
        self.url = connection_url
        self.params = params
        self.queue_name = queue_name
        self.queue_w = AsyncDeque()
        self.queue_r = asyncio.Queue()
        # self.queue_ack = AsyncDeque()
        self.rest_api = RestAPI(self.url)
        self._is_ready = asyncio.Event()
        # self._last_channel_activity = None

        self._publishing_tasks = set()
        # self._is_publishing = asyncio.Event()

        # self._acknack_tasks = set()
        # self._publishing_lock = asyncio.Lock()

        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None

        # self.channel_invalid_state_flag = asyncio.Event()

    async def run(self):
        # logger.info( f'{id(self.role)=} {id(QueueRole.Receiver)=} {id(QueueRole.Publisher)=}' )
        self.tasks.append(asyncio.create_task(self.connection_keeper()))
        # self.tasks.append(asyncio.create_task(self.ack_loop()))
        if self.is_producer():
            self.tasks.append(asyncio.create_task(self.publisher_loop()))
        if self.is_receiver():
            self.tasks.append(asyncio.create_task(self.receiver_loop()))
        await super().run()

    def is_producer(self):
        return self.role in (QueueRole.Publisher, QueueRole.Both)

    def is_receiver(self):
        return self.role in (QueueRole.Receiver, QueueRole.Both)

    async def stop(self):
        await super().stop()

    async def push(self, data):
        await self.push_w(data)

    async def pop(self, timeout=None):
        return await self.pop_r(timeout)

    async def push_w(self, data):
        await self.queue_w.put(data)

    async def push_r(self, data):
        await self.queue_r.put(data)

    async def pop_r(self, timeout=None) -> BaseQueueMessage | None:
        return await self._pop(self.queue_r, timeout)

    async def pop_w(self, timeout=None) -> BaseQueueMessage | None:
        return await self._pop(self.queue_w, timeout)

    # async def pop_ack(self, timeout=None):
    #     return await self._pop(self.queue_ack, timeout)

    async def _pop(self, queue: asyncio.Queue, timeout):
        if timeout is None:
            # logger.info(f'rabbitmq pop {self.queue_name} no timeout')
            res = await queue.get()
            # logger.info(f'rabbitmq {self.queue_name} poped {res}')
            return res
        elif timeout == 0:
            try:
                res = queue.get_nowait()
                return res
            except asyncio.QueueEmpty:
                return None
        try:
            res = await asyncio.wait_for(queue.get(), timeout)
            return res
        except asyncio.TimeoutError:
            return None

    async def until_empty(self):
        last_log = 0
        while True:
            logger.debug("---------------------------->")
            logger.debug(self.queue_r.empty())
            logger.debug(self.queue_w.empty())
            # logger.debug(self.queue_ack.empty())
            # and not self._is_publishing.is_set()
            logger.debug(len(self._publishing_tasks))
            # logger.debug(len(self._acknack_tasks))
            logger.debug("----------------------------<")

            if (
                self.queue_r.empty()
                and self.queue_w.empty()
                # and self.queue_ack.empty()
                # and not self._is_publishing.is_set()
                and len(self._publishing_tasks) == 0
                # and len(self._acknack_tasks) == 0
            ):
                # if receiver then is receiver queue empty?
                if self.is_receiver():
                    queue = await self.rest_api.get_queue(self.queue_name)
                    logger.debug(f"until_empty {queue=}")
                    if "message_stats" in queue:
                        if time.time() - last_log > 5:
                            last_log = time.time()
                            logger.debug(
                                f"=================== receiver queue size {self.queue_name} {self.params} {queue=}"
                            )
                        if (
                            queue.get("messages", -1) == 0
                            and queue.get("messages_unacknowledged", -1) == 0
                            # ensures that at least anything was put into and got out of the queue.
                            and queue["message_stats"].get("publish", 0) > 0
                            and queue["message_stats"].get("deliver_get", 0) >= queue["message_stats"].get("publish", 0)
                        ):
                            break
                    elif queue.get("messages", -1) == 0 and "message_stats" not in queue:
                        # non touched queue => nothing to wait
                        break
                elif self.role == QueueRole.Publisher:
                    break
                else:
                    raise Exception("not implemented")
            await asyncio.sleep(1)

    async def mark_done(self, message: aio_pika.IncomingMessage):
        await self._do_acknack(message, True)

    async def reject(self, message: aio_pika.IncomingMessage, requeue: bool):
        await self._do_acknack(message, False, requeue)

    async def is_ready(self, timeout: Optional[int] = None) -> bool:
        if not timeout:
            return self._is_ready.is_set()
        try:
            await asyncio.wait_for(self._is_ready.wait(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False

    def _gen_queue_exchange_name(self):
        return f"{self.queue_name}_exchange"

    # async def ack_loop(self):

    #     # def on_done(task):
    #     #     self._acknack_tasks.discard(task)

    #     while not await self.is_stopped():
    #         if not await self.is_ready(timeout=1):
    #             continue

    #         while True:
    #             r = await self.pop_ack(timeout=3)
    #             if not r:
    #                 break

    #             # if len(self._acknack_tasks) < MAX_ACK_TASKS:
    #             #     task = asyncio.create_task(self._do_acknack(r))
    #             #     task.add_done_callback(on_done)
    #             #     self._acknack_tasks.add(task)
    #             # else:
    #             await self._do_acknack(r)
    #             # logger.error(f"{self.channel.is_closed=}")
    #             # self.channel_invalid_state_flag.set()

    async def _do_acknack(self, message, ack: bool, requeue=False):
        try:
            if ack:
                await message.ack()
            else:
                await message.reject(requeue)
            # self._last_channel_activity = time.time()
        except:  #  aio_pika.exceptions.ChannelInvalidStateError:
            # await self.queue_ack.put_front(r)
            logger.error(f"ack/nack for {message.message_id=} failed with ChannelInvalidStateError")

    async def connection_keeper(self):
        try:
            while not await self.is_stopped(1):
                # logger.info("connection keeper loop")

                if not self.channel:
                    self._is_ready.clear()
                elif self.channel and self.channel.is_closed:
                    try:
                        await self.channel.reopen()
                        self._is_ready.set()
                        continue
                    except:
                        logger.warning("channel reopen failed")
                        pass  # go to recreation

                # elif self._last_channel_activity is not None and time.time() - self._last_channel_activity > 60:
                #     self._is_ready.clear()
                elif await self.is_ready():
                    # logger.info("connection keeper: channel ok")
                    continue

                logger.debug("creating connection")

                if self.channel is not None:
                    await self.channel.close()
                    self.channel = None

                if self.connection is not None:
                    await self.connection.close()
                    self.connection = None

                try:
                    self.connection = await aio_pika.connect_robust(self.url)
                except (aiormq.exceptions.AMQPConnectionError, StopAsyncIteration):
                    logger.info("Failed connect to rabbitmq, waiting..")
                    await asyncio.sleep(5)
                    continue

                logger.debug("connected")

                self.channel = await self.connection.channel()
                logger.info(f"rabbitmq {self.queue_name} {self.channel=}")

                # Maximum message count which will be processing at the same time.
                if self.is_receiver():
                    await self.channel.set_qos(prefetch_count=self.params.prefetch_count)

                # Declaring queue
                arguments = {}
                if self.params.x_max_priority is not None:
                    arguments["x-max-priority"] = self.params.x_max_priority
                logger.info(f"creating queue {self.queue_name} {arguments=}")
                self.queue = await self.channel.declare_queue(
                    name=self.queue_name,
                    durable=True,
                    arguments=arguments,
                    exclusive=self.params.exclusive,
                )

                self.exchange_name = (
                    self.params.exchange_name
                    if self.params.exchange_name is not None
                    else self._gen_queue_exchange_name()
                )
                logger.info(f"creating exchange {self.exchange_name}")
                if self.params.exchange_type == aio_pika.ExchangeType.TOPIC:
                    self.exchange = await self.channel.declare_exchange(
                        name=self.exchange_name, type=aio_pika.ExchangeType.TOPIC, durable=True
                    )
                elif self.params.exchange_type == aio_pika.ExchangeType.DIRECT:
                    self.exchange = await self.channel.declare_exchange(
                        name=self.exchange_name, type=aio_pika.ExchangeType.DIRECT, durable=False
                    )
                else:
                    raise Exception(f"not supported {self.params.exchange_type=}")

                # bind queue even if it's only publisher: else if receiver is not started yet then immediately pushed message will be lost
                if self.queue_name or self.params.routing_key:
                    rks = (
                        self.params.routing_key
                        if isinstance(self.params.routing_key, list)
                        else [self.params.routing_key]
                    )
                    for rk in rks:
                        if rk == "":
                            rk = self.queue_name
                        logger.debug(f"binding queue to {self.exchange_name=} {rk=}")
                        await self.queue.bind(self.exchange, routing_key=rk)

                # self._last_channel_activity = time.time()
                self._is_ready.set()
            if self.connection:
                await self.connection.close()
        except Exception as e:
            logger.error(f"Exception in connection_keeper() {e}, connection keeper stopped")
            logger.error(traceback.format_exc())

    async def publisher_loop(self):
        try:
            logger.info(f"rabbitmq {self.queue_name} publisher start")
            while not await self.is_stopped(timeout=0.1):
                if not await self.is_ready(1):
                    # logger.info("publisher not ready")
                    continue

                # logger.info("publisher ready")

                # logger.info(f"rabbitmq {self.connection=} --------------------")
                message: Optional[BaseQueueMessage] = None
                try:
                    # logger.info( f'puslisher {self.queue_name} loop iteration')
                    while len(self._publishing_tasks) < MAX_PUBLISHING_TASKS and await self.is_ready(timeout=0):
                        # TODO: possible milestone: when message is poped but not yet send to _do_publish() task
                        # it is possible that until_empty() decides that we are done here.
                        # This can be fixed with self._is_publishing.set() but things become very slow ( 10000 msg = 5sec without, 20 sec with it)
                        # self._is_publishing.set()
                        message = await self.pop_w(3)
                        if message is None:
                            # self._is_publishing.clear()
                            break

                        # logger.info(f"publisher loop {self.queue_name} poped {message.encode()=}")
                        # logger.info(f"publishing msg {message.encode()}")

                        def on_done(task: asyncio.Task):
                            # async with self._publishing_lock:
                            # logger.info(f"on_done {task.get_name()}")
                            self._publishing_tasks.discard(task)
                            self.queue_w.task_done()

                        # async with self._publishing_lock:
                        pub_task = asyncio.create_task(self._do_publish(message))
                        # pub_task.set_name(message.encode())
                        pub_task.add_done_callback(on_done)
                        self._publishing_tasks.add(pub_task)
                        # self._is_publishing.clear()
                        # await asyncio.sleep(0)

                    # logger.info(f'avg iteration: {times/n if n > 0 else "none"}, {n=}')
                except Exception as e:
                    # if self._is_publishing.is_set():
                    #     await self.queue_w.put_front(message)
                    #     self._is_publishing.clear()
                    self._is_ready.clear()

                    logger.error("exception in RabbitmqQueue::publisher_loop (internal)")
                    logger.error(traceback.format_exc())
            logger.info(f"rabbitmq {self.queue_name} publisher done")

        except Exception as e:
            logger.error("exception in RabbitmqQueue::publisher_loop, publisher stopped")
            logger.error(traceback.format_exc())

    async def _do_publish(self, message):
        try:
            if isinstance(message, QueueRoutedMessage):
                routing_key = message.routing_key
            else:
                routing_key = self.queue_name

            # logger.info(f"publishing into {routing_key=} ")

            await self.exchange.publish(
                aio_pika.Message(
                    body=(message.encode() if isinstance(message, BaseQueueMessage) else json.dumps(message).encode()),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    priority=message.priority if isinstance(message, BaseQueueMessage) else None,
                ),
                routing_key=routing_key,
            )
            self._last_channel_activity = time.time()
        except Exception as e:
            logger.warning(f"_do_publish putting back: {e}")
            # logger.info(f"{message.encode()}")
            await self.queue_w.put_front(message)
            self._is_ready.clear()
        finally:
            # logger.info(f"_do_publish done on {message.encode()}")
            pass

    async def receiver_loop(self):
        try:
            logger.info(f"rabbitmq {self.queue_name} receiver start")
            while not await self.is_stopped(timeout=0.1):
                # logger.info("receiver loop")
                if not await self.is_ready(timeout=1):
                    # logger.info("receiver not ready")
                    continue

                try:

                    # async def clb(message):
                    #     # logger.info(f"readmessage: {message.body}")
                    #     await self.push_r(message)

                    # await self.queue.consume(clb, timeout=3)
                    # logger.info("consume done")
                    async with self.queue.iterator(timeout=3) as q:
                        async for message in q:
                            # logger.debug(f"readmessage: {message.body}")
                            await self.push_r(message)
                            # self._last_channel_activity = time.time()

                except asyncio.TimeoutError:
                    # logger.info("timeout exc")
                    pass
                except aiormq.exceptions.ChannelInvalidStateError:
                    self._is_ready.clear()
                    # logger.info("invalid state exc")
                    pass
                except aiormq.exceptions.ChannelNotFoundEntity:
                    self._is_ready.clear()
                    # logger.info("no cahnnel exc")
                    pass
                except aiormq.exceptions.ChannelClosed:
                    self._is_ready.clear()
                    # logger.info("no cahnnel exc")
                    pass
                except Exception as e:
                    self._is_ready.clear()
                    logger.error(f"!!!!!!!!!!!!!!!!!! exception in rabbitmq receiver_loop: {e}")
                    logger.error(traceback.format_exc())

        except Exception as e:
            logger.error(f"!!!!!!!!!!!!!!!!!! exception in rabbitmq receiver loop {e}, receiver stopped")
            logger.error(traceback.format_exc())

    async def delete(self):
        channel = await self.connection.channel()
        await channel.queue_delete(self.queue_name)
        await channel.exchange_delete(self.exchange_name)
