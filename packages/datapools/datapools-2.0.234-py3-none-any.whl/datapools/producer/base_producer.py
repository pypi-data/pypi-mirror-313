import asyncio
import json
import time
import functools

# import importlib
# import inspect
import os

# import sys
import traceback

# from enum import Enum
from typing import Optional, Set, Dict, Any, List

from ..common.utils import parse_size
from ..common.backend_api import BackendAPI, BackendAPIException
from ..common.logger import logger
from ..common.queues import (
    GenericQueue,
    QueueMessage,
    QueueMessageType,
    QueueRole,
    QueueRoutedMessage,
    get_session_queue_name,
)
from ..common.session_manager import SessionManager, Session, ContentStatus
from ..common.stoppable import Stoppable

# from ..common.storage.file_storage import FileStorage
# from ..common.storage.metadata_storage import MetadataStorage
from ..common.storage.session_file_storage import SessionFileStorage
from ..common.types import (
    DatapoolContentType,
    BaseProducerSettings,
    InvalidUsageException,
    SchedulerEvaluationReport,
    EvaluationStatus,
    WorkerEvaluationReport,
    ProducerTask,
)
from ..worker.utils import get_worker_storage_invalidation_routing_key


def timer(name):
    def timer_inner(func):
        def wrap(*args, **kwargs):
            started_at = time.time()
            result = func(*args, **kwargs)
            logger.info(f"timer: {name}: {time.time() - started_at}")
            return result

        return wrap

    return timer_inner


def atimer(name):
    def timer_inner(func):
        @functools.wraps(func)
        async def wrap(*args, **kwargs):
            started_at = time.time()
            result = await func(*args, **kwargs)
            logger.info(f"atimer: {name}: {time.time() - started_at}")
            return result

        return wrap

    return timer_inner


# from .rules import DatapoolRulesChecker


class BaseProducer(Stoppable):
    cfg: BaseProducerSettings
    report_queues: Dict[str, GenericQueue]
    eval_queue: GenericQueue
    worker_reports_queue: GenericQueue
    todo_tasks: Set[asyncio.Task]
    # storage: FileStorage
    # metadata_storage: MetadataStorage
    qps_stats: List[float]

    def __init__(self, cfg: Optional[BaseProducerSettings] = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else BaseProducerSettings()
        self.session_manager = SessionManager(self.cfg.REDIS_HOST, self.cfg.REDIS_PORT)
        # storage_path = self.cfg.STORAGE_PATH if self.cfg.STORAGE_PATH is not None else self.cfg.WORKER_STORAGE_PATH
        # self.storage = FileStorage(storage_path, depth=2)
        # self.metadata_storage = MetadataStorage(storage_path, depth=2)
        self.qps_stats = []

        if not self.cfg.CLI_MODE:
            self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)

        self.todo_tasks = set()

        # receives tasks from workers
        self.eval_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.EVAL_TASKS_QUEUE_NAME,
            size=self.cfg.MAX_PROCESSING_TASKS,
        )
        logger.debug("created receiver eval_tasks")

        # will invalidate worker cache entries
        self.worker_reports_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.STORAGE_INVALIDATION_QUEUE_NAME,
        )
        logger.debug("created publisher worker_tasks")

        # sends reports to the scheduler
        self.report_queues = {}

        if self.cfg.CLI_MODE is True:
            self.stop_task_received = asyncio.Event()

        # self.datapool_rules_checker = DatapoolRulesChecker()

    async def run(self):
        self.tasks.append(asyncio.create_task(self.router_loop()))
        await self.eval_queue.run()
        await self.worker_reports_queue.run()
        await super().run()

    async def wait(self):
        if self.cfg.CLI_MODE is False:
            logger.error("base_producer invalid usage")
            raise InvalidUsageException("not a cli mode")

        logger.debug("BaseProducer wait()")
        await self.stop_task_received.wait()
        logger.debug("BaseProducer stop_task_received")
        waiters = [
            self.eval_queue.until_empty(),
            self.worker_reports_queue.until_empty(),
        ] + [self.report_queues[session_id].until_empty() for session_id in self.report_queues]
        await asyncio.gather(*waiters)
        logger.debug("BaseProducer wait done")

    async def stop(self):
        logger.debug("waiting todo tasks..")
        while len(self.todo_tasks) > 0:
            await asyncio.sleep(0.2)
        logger.debug("todo tasks done")

        waiters = [self.eval_queue.stop(), self.worker_reports_queue.stop()] + [
            self.report_queues[session_id].stop() for session_id in self.report_queues
        ]
        await asyncio.gather(*waiters)
        await super().stop()
        logger.info("BaseProducer stopped")

    async def router_loop(self):
        try:

            def on_done(task: asyncio.Task):
                logger.debug(f"_process_task done {task=}")
                self.todo_tasks.discard(task)
                logger.debug(f"{len(self.todo_tasks)} still working")

            last_queues_cleanup = 0
            last_qps = 0
            # last_storage_size_check = 0
            # storage_size_limit = parse_size(self.cfg.STORAGE_SIZE_LIMIT)
            while not await self.is_stopped():
                now = time.time()
                if now - last_qps > 10:
                    last_qps = now
                    # moving average qps
                    # 1. keep stats for the last 60s
                    self.qps_stats = [timestamp for timestamp in self.qps_stats if now - timestamp < 60]
                    # 2.average qps
                    logger.info(f"qps: {round(len(self.qps_stats)/60, 1)}")

                if now - last_queues_cleanup > 60:
                    last_queues_cleanup = now

                    session_ids = await self.session_manager.get_active_sessions()
                    new_queues = {}
                    for session_id, queue in self.report_queues.items():
                        if session_id not in session_ids:
                            logger.info(f"stopping queue {queue.queue.queue_name}")
                            await queue.stop()
                        else:
                            new_queues[session_id] = queue
                    self.report_queues = new_queues

                # if now - last_storage_size_check > 60:
                #     cur_size = await self.storage.get_total_size()
                #     if cur_size >= storage_size_limit:
                #         logger.info(f"Out of storage size limit: {cur_size} >= {storage_size_limit}")
                #         await asyncio.sleep(10)
                #     else:
                #         last_storage_size_check = now

                if len(self.todo_tasks) < self.cfg.MAX_PROCESSING_TASKS:
                    message = await self.eval_queue.pop(timeout=3)
                    if message:
                        logger.debug(f"{message.message_id=} {message.redelivered}")

                        task = asyncio.create_task(self._process_task(message))
                        task.add_done_callback(on_done)
                        self.todo_tasks.add(task)
                else:
                    await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Catched: {traceback.format_exc()}")
            logger.error(f"!!!!!!! Exception in Datapools::router_loop() {e}")

    # @atimer("process_task")
    async def _process_task(self, message):

        qm = QueueMessage.decode(message.body)
        logger.debug(f"processing {message.message_id=} {qm.session_id=}")

        # storage_file_path: Optional[str] = None
        # metadata_file_path: Optional[str] = None
        started_evaluation = False
        try:
            session = await self.session_manager.get(qm.session_id)
            if (
                session is None or not await session.is_alive()
            ):  # TODO: PROCESS EVEN IF SESSION IS STOPPED - crawled content still have to be processed to the end
                # logger`.info(f"session is deleted or stopped {qm.session_id=} {message.message_id}")
                logger.debug(f"session is deleted {qm.session_id=} {message.message_id}")
                await self.eval_queue.mark_done(message)
                if qm.type == QueueMessageType.Task:
                    task = ProducerTask(**qm.data)
                    await self.cleanup_worker_storage(qm.session_id, task.storage_id)
                return

            await self._try_init_report_queue(session.id)

            if qm.type == QueueMessageType.Task:
                task = ProducerTask(**qm.data)
                logger.debug(f"Producer got: {task}")

                if task.type == DatapoolContentType.Image:
                    prev_ttl = 10
                elif task.type == DatapoolContentType.Video:
                    prev_ttl = 60
                elif task.type == DatapoolContentType.Audio:
                    prev_ttl = 30
                elif task.type == DatapoolContentType.Text:
                    prev_ttl = 10
                else:
                    raise Exception(f"BUG: Unknown {task.type=}")

                if not await session.start_evaluation(message.message_id, prev_ttl=prev_ttl):
                    logger.info(f"message is being processed already {qm.session_id} {message.message_id}")
                    await self.eval_queue.reject(message, requeue=True)
                    await asyncio.sleep(5)
                    return

                started_evaluation = True

                # copying file
                # put data into persistent storage
                # @atimer("storage_put")
                # async def storage_put():
                #     # nonlocal storage_file_path, metadata_file_path
                #     nonlocal metadata_file_path

                #     # session_storage = SessionFileStorage(self.cfg.WORKER_STORAGE_PATH, session.id)
                #     # if not await session_storage.has(task.storage_id):
                #     #     raise FileNotFoundError(session_storage.get_path(task.storage_id))

                #     # with session_storage.get_reader(task.storage_id) as raw_data_reader:
                #     #     await self.storage.put(task.storage_id, raw_data_reader)
                #     # storage_file_path = self.storage.get_path(task.storage_id)

                #     # if task.metadata is not None:
                #     #     await self.metadata_storage.put(task.storage_id, json.dumps(task.metadata.model_dump()))
                #     #     metadata_file_path = self.metadata_storage.get_path(task.storage_id)

                # # copy data to producer storage
                # # (storage_file_path, metadata_file_path) = await storage_put()
                # await storage_put()

                await self.process_content(session, task)

            elif qm.type == QueueMessageType.Stop:
                logger.info("base_producer: stop task received")
                self.stop_task_received.set()
            else:
                raise Exception(f"!!!!!!!!!!!!!!! BUG: unexpected {message=} {qm=}")

            # @atimer("task mark_done")
            # async def mark_done():
            self.qps_stats.append(time.time())
            await self.eval_queue.mark_done(message)

            # await mark_done()
        except BackendAPIException as e:
            logger.error("Caught BackendAPIException")
            logger.error(traceback.format_exc())
            # if storage_file_path is not None:
            #     os.unlink(storage_file_path)
            # if metadata_file_path is not None:
            #     os.unlink(metadata_file_path)
            await self.eval_queue.reject(message, requeue=True)
            await asyncio.sleep(5)
        except Exception as e:
            logger.error("Caught Exception")
            logger.error(traceback.format_exc())
            # if storage_file_path is not None:
            #     os.unlink(storage_file_path)
            # if metadata_file_path is not None:
            #     os.unlink(metadata_file_path)

            await self.cleanup_worker_storage(session.id, task.storage_id)

            await self.eval_queue.reject(message, requeue=False)

            await self._report_evaluation(session, task, EvaluationStatus.Failure)

        finally:
            if started_evaluation:
                await session.finish_evaluation(message.message_id)

    async def cleanup_worker_storage(self, session_id, storage_id):
        session_storage = SessionFileStorage(self.cfg.WORKER_STORAGE_PATH, session_id, must_exist=True)
        if await session_storage.has(storage_id):
            await session_storage.remove(storage_id)

    async def process_content(self, session: Session, task: ProducerTask):
        if await session.exists():  # session may have been deleted while processing content
            await self.cleanup_worker_storage(session.id, task.storage_id)

            await self._report_evaluation(session, task, EvaluationStatus.Success)

    # @atimer("report_evaluation")
    async def _report_evaluation(
        self, session: Session, task: ProducerTask, status: EvaluationStatus, report_data: Optional[Any] = None
    ):
        # @atimer(f"session.set_content_status {session.id}")
        async def set_content_status():
            await session.set_content_status(
                task.content_key,
                (
                    ContentStatus.EVALUATION_SUCCESS
                    if status == EvaluationStatus.Success
                    else ContentStatus.EVALUATION_FAILURE
                ),
            )

        await set_content_status()

        if session.id in self.report_queues:

            # @atimer("scheduler report")
            async def report_scheduler():
                report = SchedulerEvaluationReport(status=status, data=report_data)
                await self.report_queues[session.id].push(
                    QueueMessage(session_id=session.id, message_type=QueueMessageType.ReportEvaluation, data=report)
                )

            await report_scheduler()

        # @atimer("report_worker")
        # async def report_worker():
        #     await self.worker_reports_queue.push(
        #         QueueMessage(
        #             session_id=session.id,
        #             message_type=QueueMessageType.ReportEvaluation,
        #             data=WorkerEvaluationReport(
        #                 url=task.url,
        #                 storage_id=task.storage_id,
        #                 status=status,
        #             ),
        #         )
        #     )

        # await report_worker()

    async def _try_init_report_queue(self, session_id):
        if session_id not in self.report_queues:
            q_name = get_session_queue_name(self.cfg.REPORTS_QUEUE_NAME, session_id)
            q = GenericQueue(role=QueueRole.Publisher, url=self.cfg.QUEUE_CONNECTION_URL, name=q_name)
            await q.run()
            self.report_queues[session_id] = q
