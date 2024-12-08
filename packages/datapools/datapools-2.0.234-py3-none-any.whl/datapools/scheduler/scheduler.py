import asyncio
import json
from copy import copy
import time
import traceback
from typing import Optional, Dict, Set, Tuple
from pydantic import AnyUrl, BaseModel

from ..common.backend_api import BackendAPI, BackendAPIException, BackendConnectionFailure
from ..common.logger import logger
from ..common.queues import (
    GenericQueue,
    QueueMessage,
    QueueMessageType,
    QueueRole,
    get_session_queue_name,
    # MESSAGE_HINT_URL_PRIORITY,
    # MESSAGE_BACK_TASK_PRIORITY,
)
from ..common.robots import is_allowed_by_robots_txt

# from .common.tasks_db import Hash
# from .common.tasks_db.redis import RedisTasksDB
from ..common.counter_cache import CounterCache
from ..common.session_manager import SessionManager, SessionStatus, Session
from ..common.stoppable import Stoppable
from ..common.types import (
    CrawlerBackTask,
    CrawlerHintURL,
    CrawlerHintURLStatus,
    DatapoolContentType,
    InvalidUsageException,
    SchedulerSettings,
    WorkerTask,
    SchedulerEvaluationReport,
    EvaluationStatus,
)


class WorkerReportQueueData(BaseModel):
    q: GenericQueue
    added_urls: CounterCache

    class Config:
        arbitrary_types_allowed = True


class CrawlerScheduler(Stoppable):
    # 1. task:
    #   - get hint urls from the backend, put into tasks_db, status is changed at the backend at once
    #   - check "processing" tasks: ping worker. If it's dead then task is moved back to the queue
    # 2. api: get urls from workers, put into tasks_db
    #   tips:
    #   - reject existing urls: request redis by url hash
    # 3. api: worker gets a new task(s?) from queue:
    #   tips:
    #   - tasks_db: (redis) task should be moved into a separate key as "in progress", worker ID/IP/etc should be remembered to be able to ping
    # 4. api: worker notifies about finished task
    #    - remove task from "processing"
    #    - if it's a backend hint url, then update its status by calling backend api

    todo_queues: Dict[str, GenericQueue]
    worker_report_queues: Dict[str, WorkerReportQueueData]
    producer_report_queues: Dict[str, GenericQueue]
    cli_tasks: Optional[asyncio.Queue] = None
    checks: Set[str]  # session_id
    checks_lock: asyncio.Lock

    def __init__(self, cfg: Optional[SchedulerSettings] = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else SchedulerSettings()

        if self.cfg.CLI_MODE is True:
            self.cli_tasks = asyncio.Queue()
        else:
            self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)

        self.session_manager = SessionManager(self.cfg.REDIS_HOST, self.cfg.REDIS_PORT)

        self.checks = set()
        self.checks_lock = asyncio.Lock()

        # self.tasks_db = RedisTasksDB(
        #     host=self.cfg.REDIS_HOST, port=self.cfg.REDIS_PORT
        # )
        self.todo_queues = {}
        self.worker_report_queues = {}
        self.producer_report_queues = {}

        if self.cfg.CLI_MODE:
            # TODO: this mechanism will not work for multiple workers/producers
            self.stop_task_processed = asyncio.Event()

    async def wait(self):
        """for CLI mode usage only"""
        if not self.cfg.CLI_MODE:
            logger.error("scheduler invalid usage")
            raise InvalidUsageException("not a cli mode")

        await self.stop_task_processed.wait()

        waiters = (
            [self.todo_queues[session_id].until_empty() for session_id in self.todo_queues]
            + [self.worker_report_queues[session_id].q.until_empty() for session_id in self.worker_report_queues]
            + [self.producer_report_queues[session_id].until_empty() for session_id in self.producer_report_queues]
        )

        await asyncio.gather(*waiters)
        logger.info("scheduler wait done")

    async def run(self):
        self.tasks.append(asyncio.create_task(self.hints_loop()))
        self.tasks.append(asyncio.create_task(self.worker_reports_loop()))
        self.tasks.append(asyncio.create_task(self.producer_reports_loop()))
        await super().run()

    async def stop(self):
        logger.info("scheduler stopping")
        waiters = (
            [self.todo_queues[session_id].stop() for session_id in self.todo_queues]
            + [self.worker_report_queues[session_id].q.stop() for session_id in self.worker_report_queues]
            + [self.producer_report_queues[session_id].stop() for session_id in self.producer_report_queues]
        )
        await asyncio.gather(*waiters)
        logger.info("queues stopped")
        await super().stop()
        logger.info("super stopped")

    async def _maybe_hard_stop(self, session: Session, meta: dict):

        need_hard_stop = False
        if await session.is_alive():
            num_since_last_tagged = meta["since_last_tagged"]
            # logger.info(f"{num_since_last_tagged=} vs {self.cfg.MAX_EMPTY_COMPLETE_TASKS=}")

            # logger.info(f'COMPLETE: {meta["complete_urls"]} vs MAX: {self.cfg.MAX_COMPLETE_TASKS}')
            need_hard_stop = (
                self.cfg.MAX_EMPTY_COMPLETE_TASKS is not None
                and num_since_last_tagged >= self.cfg.MAX_EMPTY_COMPLETE_TASKS
                and meta["ignore_missing_license"] is False
            ) or (self.cfg.MAX_COMPLETE_TASKS is not None and meta["evaluated_content"] >= self.cfg.MAX_COMPLETE_TASKS)

            if need_hard_stop:
                logger.info(f"HARD STOP {session.id}")
                await self.set_hint_url_status(meta.get("hint_id"), CrawlerHintURLStatus.Canceled, session, meta)
            else:
                async with self.checks_lock:
                    self.checks.add(session.id)
        return need_hard_stop

    async def _process_iteration(self, session_id):
        session = await self.session_manager.get(session_id)
        if session is None:
            return False
        meta = await session.get_meta()
        # logger.info(f"{meta=}")
        await self._maybe_hard_stop(session, meta)

    async def _process_evaluation_report(self, session_id, report: SchedulerEvaluationReport):
        logger.debug(f"_process_evaluation_report: {session_id=} {report=}")

        if report.data:
            data = json.loads(report.data)
            await self.api.add_crawled_content(data)

        session = await self.session_manager.get(session_id)
        if session is None:
            return False

        if not self.cfg.CLI_MODE:
            async with self.checks_lock:
                self.checks.add(session_id)

        if report.status == EvaluationStatus.Success:
            await session.inc_evaluated_content()
        elif report.status == EvaluationStatus.Failure:
            await session.inc_failed_content()

    async def _check_hint_url_finished(self, session_id):
        session = await self.session_manager.get(session_id)
        if not session:
            return

        meta = await session.get_meta()
        logger.info(f"{meta=}")

        # if failed_urls++ then failed_content is not incremented, so evaluated_content+failed_content cannot reach crawled_content
        # so failed_urls are counted as failed_content
        urls_done = await session.all_urls_processed()
        logger.info(f"{session.id=} {urls_done=}")
        if urls_done:
            content_done = await session.all_content_processed()
            logger.info(f"{session.id=} {content_done=}")
            if content_done:
                logger.info(f'Hint Url fully processed {meta["hint_id"]}')
                # whole task status = task url status
                # this way status of single page tasks ( like google drive bucket ) is easy to decide
                # TODO:(MAYBE) for multipage tasks some criteria like percentage of success/failure should be considered?
                url_state = await session.get_url_state(meta["url"])
                if url_state is not None:
                    logger.info(f"{session.id=} root {url_state}=")
                    await self.set_hint_url_status(meta["hint_id"], url_state.status, session, meta)
                else:
                    logger.error(f"BUG: {session.id} No url state for {meta['url']}")
                await session.cleanup()

    async def _process_task_status_report(self, session_id, task: WorkerTask):
        # hash, status: CrawlerHintURLStatus, contents
        logger.info(f"_process_task_status_report: {session_id=} {task=}")

        session = await self.session_manager.get(session_id)
        if session is None:
            return False

        if task.status in (
            CrawlerHintURLStatus.Success,
            CrawlerHintURLStatus.Failure,
            CrawlerHintURLStatus.Rejected,
            CrawlerHintURLStatus.Canceled,
        ):

            if not self.cfg.CLI_MODE:
                meta = await session.get_meta()
                # logger.info(f"{meta=}")

                await self._maybe_hard_stop(session, meta)

            # TODO: not cool to work with possibly closed session ( hard_stop may be set )
            # But if do these inc's before talking to backend and BackendException occurs then inc's will be done again and again
            if task.status == CrawlerHintURLStatus.Success:
                await session.inc_complete_urls()
            elif task.status == CrawlerHintURLStatus.Failure:
                await session.inc_failed_urls()
            elif task.status == CrawlerHintURLStatus.Rejected:
                await session.inc_rejected_urls()

    async def set_hint_url_status(self, hint_id, status: CrawlerHintURLStatus, session: Session, meta=None):
        if meta is None:
            meta = await session.get_meta()

        if status in (
            CrawlerHintURLStatus.Success,
            CrawlerHintURLStatus.Failure,
            CrawlerHintURLStatus.Rejected,
            CrawlerHintURLStatus.Canceled,
        ):
            await session.set_status(SessionStatus.STOPPED)
            if session.id in self.todo_queues:
                await self.todo_queues[session.id].delete()
                await self.todo_queues[session.id].stop()
                del self.todo_queues[session.id]
            if session.id in self.worker_report_queues:
                await self.worker_report_queues[session.id].q.delete()
                await self.worker_report_queues[session.id].q.stop()
                del self.worker_report_queues[session.id]
            if session.id in self.producer_report_queues:
                await self.producer_report_queues[session.id].delete()
                await self.producer_report_queues[session.id].stop()
                del self.producer_report_queues[session.id]

        if hint_id:
            if meta["last_reported_status"] != status:  # make sure that report is sent once only
                await session.set_last_reported_status(status)
                await self.api.set_hint_url_status(hint_id, status, session.id)
            else:
                logger.info(f"hint status report was already sent: {meta['last_reported_status']=}")

    async def _add_task(self, session_id, task: CrawlerHintURL | CrawlerBackTask):
        session = await self.session_manager.get(session_id)
        if session is None or not await session.is_alive():
            logger.debug(f"Session not found or is stopped {session_id=}")
            return False

        if isinstance(task, CrawlerHintURL):
            if not await session.has_url(task.url):  # for restarted hint url that will be False
                logger.debug(f'adding url "{task.url}" to session "{session_id}" ')
                await session.add_url(task.url)
                await session.update_meta({"postpone_duration": 0, "total_postponed": 0})

            await self._enqueue_worker_task(
                task,
                session_id,
                # priority=MESSAGE_HINT_URL_PRIORITY,
                status=task.status,
            )

        elif isinstance(task, CrawlerBackTask):
            # logger.info( f'{task["url"]=}')
            if not self.worker_report_queues[session_id].added_urls.has(task.url):
                self.worker_report_queues[session_id].added_urls.add(task.url)

                if not await session.has_url(task.url):
                    logger.debug(f'adding url "{task.url}" to session "{session_id}" ')
                    await session.add_url(task.url)

                    await self._enqueue_worker_task(
                        task,
                        session_id,  # priority=MESSAGE_BACK_TASK_PRIORITY
                    )
                else:
                    logger.debug("task exists, ignored")
                    return False
            else:
                self.worker_report_queues[session_id].added_urls.inc(task.url)
                logger.debug("task exists, ignored(cache)")
                return False
        # FIXME: outdated, review CLI logic
        elif "stop_running" in task:
            # await self.todo_queue.push(QueueMessage(session_id=session_id, message_type=QueueMessageType.Stop))
            pass
        else:
            raise Exception(f"unsupported {task=}")

        # logger.info( 'pushed')
        return True
        # return hash

    # return False

    async def try_running_session_queues(self, session_id) -> Tuple[GenericQueue, GenericQueue, GenericQueue]:
        if session_id not in self.todo_queues:
            queue_name = get_session_queue_name(self.cfg.WORKER_TASKS_QUEUE_NAME, session_id)
            logger.info(f"starting queue {queue_name=}")
            self.todo_queues[session_id] = GenericQueue(
                role=QueueRole.Publisher,
                url=self.cfg.QUEUE_CONNECTION_URL,
                name=queue_name,
                # max_priority=MESSAGE_HINT_URL_PRIORITY,
            )
            await self.todo_queues[session_id].run()

        if session_id not in self.worker_report_queues:
            queue_name = get_session_queue_name(self.cfg.REPORTS_QUEUE_NAME, session_id)
            logger.info(f"starting queue {queue_name=}")
            self.worker_report_queues[session_id] = WorkerReportQueueData(
                q=GenericQueue(
                    role=QueueRole.Receiver,
                    url=self.cfg.QUEUE_CONNECTION_URL,
                    name=queue_name,
                    size=100,
                    # max_priority=MESSAGE_HINT_URL_PRIORITY,
                ),
                added_urls=CounterCache(),
            )
            await self.worker_report_queues[session_id].q.run()

        if session_id not in self.producer_report_queues:
            queue_name = get_session_queue_name(self.cfg.PRODUCER_REPORTS_QUEUE_NAME, session_id)
            logger.info(f"starting queue {queue_name=}")
            self.producer_report_queues[session_id] = GenericQueue(
                role=QueueRole.Receiver,
                url=self.cfg.QUEUE_CONNECTION_URL,
                name=queue_name,
            )
            await self.producer_report_queues[session_id].run()
        return (
            self.todo_queues[session_id],
            self.worker_report_queues[session_id].q,
            self.producer_report_queues[session_id],
        )

    async def _enqueue_worker_task(
        self,
        task: CrawlerHintURL | CrawlerBackTask,
        session_id,
        status: Optional[CrawlerHintURLStatus] = None,  # priority: int,
    ):
        if await is_allowed_by_robots_txt(str(task.url)):
            logger.debug(f"_enqueue_worker_task {task=} {status=}")
            if isinstance(task, CrawlerHintURL):
                qtask = WorkerTask(url=str(task.url), status=status)
            elif isinstance(task, CrawlerBackTask):
                qtask = WorkerTask(
                    url=str(task.url),
                    status=status,
                    metadata=task.metadata,
                    content_type=task.type,
                    force_plugin=task.force_plugin,
                )
            else:
                raise Exception("Invalid usage")

            (todo_queue, __worker_reports_queue, __producer_reports_queue) = await self.try_running_session_queues(
                session_id
            )
            await todo_queue.push(
                QueueMessage(
                    session_id=session_id,
                    message_type=QueueMessageType.Task,
                    data=qtask.to_dict(),  # , priority=priority
                )
            )
        else:
            logger.warning(f"not allowed by robots.txt: {task.url}")

    async def add_download_task(self, url, content_type: Optional[DatapoolContentType] = None):
        """for cli mode: pushing url to the queue. Scheduler will run until empty string is added"""
        if self.cli_tasks is None:
            logger.error("scheduler invalid usage")
            raise InvalidUsageException("not a cli mode")
        await self.cli_tasks.put((url, content_type))

    async def _get_hints(self):
        hints = None
        if not self.cfg.CLI_MODE:
            # deployment mode
            try:
                hints = await self.api.get_hint_urls(limit=10)
                for hint in hints:
                    logger.info(f"got {hint=}")

                    need_new_session = hint.status in (CrawlerHintURLStatus.Success, CrawlerHintURLStatus.Unprocessed)
                    if not need_new_session:
                        session = await self.session_manager.get(hint.session_id)
                        if not session:
                            need_new_session = True
                    if need_new_session:
                        session = await self.session_manager.create(
                            hint_id=hint.id, url=hint.url, ignore_missing_license=hint.ignore_missing_license
                        )
                        logger.info(f"created session: {session.id}")
                    else:
                        await session.restart()
                        logger.info(f"reusing session: {session.id} with status {hint.status}")

                    hint.session_id = session.id

            except BackendConnectionFailure as e:
                pass
            except Exception as e:
                logger.error(f"Failed get hints: {e}")
                logger.error(traceback.format_exc())
        else:
            # cli mode
            try:
                (url, content_type) = await asyncio.wait_for(self.cli_tasks.get(), timeout=1)
                if len(url) > 0:
                    hints = [{"url": url, "content_type": content_type, "session_id": self.cli_session.id}]
                else:
                    hints = [{"stop_running": True, "session_id": self.cli_session.id}]
            except asyncio.TimeoutError:
                pass
        return hints

    async def hints_loop(self):
        # infinitely fetching URL hints by calling backend api

        if self.cfg.CLI_MODE:
            self.cli_session = await self.session_manager.create()
            logger.info(f"created session {self.cli_session.id}")

        try:
            prev_failed = False
            last_postponed_check = 0
            last_hints_check = 0
            last_sessions_cleanup = 0
            last_sessions_check = 0
            while not await self.is_stopped():
                if await self.session_manager.is_ready():
                    now = time.time()
                    # 1. sessions cleanup
                    if now - last_sessions_cleanup > 60:
                        last_sessions_cleanup = now
                        await self.session_manager.cleanup_active_sessions()

                    # 2. postponed sessions
                    if now - last_postponed_check > 10:
                        last_postponed_check = now

                        postponed_ids = await self.session_manager.list_postponed(10)
                        # logger.info(f"{postponed_ids=}")
                        for session_id in postponed_ids:
                            logger.debug(f"postponed: {session_id=}")
                            session = await self.session_manager.get(session_id)
                            if session:
                                # logger.info(f"postponed {session=}")
                                meta = await session.get_meta()
                                if now >= meta["last_postponed"] + meta["postpone_duration"]:
                                    logger.info(f"Postponed session retry: {session_id}")
                                    await session.set_status(SessionStatus.NORMAL)
                                    # await session.update_meta({"postpone_duration": 0})
                                    task = CrawlerHintURL(
                                        url=meta["url"],
                                        id=meta.get("hint_id", 0),
                                        status=CrawlerHintURLStatus.UnPostponed,
                                        session_id=session_id,
                                    )
                                    await self._add_task(session_id, task)
                                    await self.session_manager.remove_postponed(session_id)

                                else:
                                    logger.debug(
                                        f'too early: {meta["last_postponed"] + meta["postpone_duration"] - now}'
                                    )

                            else:
                                await self.session_manager.remove_postponed(session_id)

                    # 3. check sessions for stop
                    if now - last_sessions_check > 5:
                        last_sessions_check = now

                        # copy ids for further processing and release the lock asap
                        async with self.checks_lock:
                            checks = copy(self.checks)
                            self.checks.clear()
                        for session_id in checks:
                            await self._check_hint_url_finished(session_id)

                    # 4. hint urls
                    if now - last_hints_check > self.cfg.BACKEND_HINTS_PERIOD or self.cfg.CLI_MODE:
                        last_hints_check = now

                        hints = await self._get_hints()
                        if hints is not None:
                            if prev_failed:
                                logger.info("Backend is back")
                                prev_failed = False

                            for hint in hints:
                                logger.info(f"got hint: {hint}")

                                added = await self._add_task(hint.session_id, hint)
                                # catching set_hint_url_status BackendAPIException: if backend fails then trying again and again
                                while not await self.is_stopped():
                                    try:
                                        session = await self.session_manager.get(hint.session_id)
                                        if added:
                                            if hint.id:
                                                await self.set_hint_url_status(
                                                    hint.id, CrawlerHintURLStatus.Processing, session
                                                )
                                        else:
                                            logger.error("failed add task, REJECTING")
                                            if hint.id:
                                                await self.set_hint_url_status(
                                                    hint.id, CrawlerHintURLStatus.Rejected, session
                                                )
                                                await self.session_manager.remove(hint.session_id)
                                        break
                                    except BackendConnectionFailure:
                                        await asyncio.sleep(5)
                                    except BackendAPIException as e:
                                        logger.error("Catched BackendAPIException")
                                        logger.error(traceback.format_exc())
                                        await asyncio.sleep(5)
                                        # ..and loop again
                        else:
                            prev_failed = True

                else:
                    await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"!!!!!!! Exception in CrawlerScheduler::hints_loop() {e}")
            logger.error(traceback.format_exc())

    async def worker_reports_loop(self):
        # receive reports from workers
        try:
            qi = 0
            last_sessions_update = 0
            last_added_urls_cache_update = 0
            while not await self.is_stopped():
                now = time.time()
                # 1. check for new sessions
                if now - last_sessions_update > 10:
                    last_sessions_update = now
                    session_ids = await self.session_manager.get_active_sessions()
                    for session_id in session_ids:
                        await self.try_running_session_queues(session_id)

                # 2. last_added_urls_cache_update
                if now - last_added_urls_cache_update > 60:
                    last_added_urls_cache_update = now
                    for session_id in session_ids:
                        self.worker_report_queues[session_id].added_urls.clean(keep=10000)

                # 3. fetch message from the next queue
                if len(self.worker_report_queues) > 0:
                    if qi >= len(self.worker_report_queues):
                        qi = 0
                        await asyncio.sleep(0.1)
                    session_ids = list(self.worker_report_queues.keys())
                    session_id = session_ids[qi]
                    queue = self.worker_report_queues[session_id].q
                    qi += 1

                    start = time.time()
                    while time.time() - start < 1:
                        message = await queue.pop(timeout=0)
                        if not message:
                            break
                        try:
                            qm = QueueMessage.decode(message.body)
                            if qm.type == QueueMessageType.Task:
                                # logger.info("new task from worker")
                                # logger.info(f"{qm=}")
                                await self._add_task(qm.session_id, CrawlerBackTask(**qm.data))
                            elif qm.type == QueueMessageType.ReportTaskStatus:
                                await self._process_task_status_report(qm.session_id, WorkerTask(**qm.data))
                            elif qm.type == QueueMessageType.Stop:
                                logger.info("scheduler: got stop from worker")
                                self.stop_task_processed.set()
                            elif qm.type == QueueMessageType.ProcessIteration:
                                await self._process_iteration(qm.session_id)
                            elif qm.type == QueueMessageType.ReportEvaluation:
                                # remove this block later: reporting moved to the producer_reports_loop()
                                await self._process_evaluation_report(
                                    qm.session_id, SchedulerEvaluationReport(**qm.data)
                                )
                            else:
                                logger.error(f"Unsupported QueueMessage {qm=}")
                            await queue.mark_done(message)

                        except BackendConnectionFailure as e:
                            await queue.reject(message)
                            await asyncio.sleep(5)
                        except BackendAPIException as e:
                            logger.error("Caught BackendAPIException")
                            logger.error(traceback.format_exc())
                            await queue.reject(message)
                            await asyncio.sleep(5)

                        except Exception as __e:
                            logger.error(traceback.format_exc())
                            await queue.reject(message, requeue=False)
                            await asyncio.sleep(5)
                else:
                    await asyncio.sleep(0.2)

        except Exception as e:
            logger.error(f"!!!!!!! Exception in CrawlerScheduler::reports_loop() {e}")
            logger.error(traceback.format_exc())

    async def producer_reports_loop(self):
        qi = 0
        while not await self.is_stopped():
            try:
                if len(self.producer_report_queues):
                    if qi >= len(self.producer_report_queues):
                        qi = 0
                        await asyncio.sleep(0.1)

                    session_ids = list(self.producer_report_queues.keys())
                    session_id = session_ids[qi]
                    q = self.producer_report_queues[session_id]
                    qi += 1

                    start = time.time()
                    while time.time() - start < 1:
                        message = await q.pop(timeout=0)
                        if not message:
                            break
                        try:
                            qm = QueueMessage.decode(message.body)
                            if qm.type == QueueMessageType.ReportEvaluation:
                                await self._process_evaluation_report(
                                    qm.session_id, SchedulerEvaluationReport(**qm.data)
                                )
                            else:
                                logger.error(f"Unsupported QueueMessage {qm=}")
                            await q.mark_done(message)
                        except BackendConnectionFailure as e:
                            await q.reject(message)
                            await asyncio.sleep(5)
                        except BackendAPIException as e:
                            logger.error("Catched BackendAPIException")
                            logger.error(traceback.format_exc())
                            await q.reject(message)
                            await asyncio.sleep(5)

                        except Exception as __e:
                            logger.error(traceback.format_exc())
                            await q.reject(message, requeue=False)
                            await asyncio.sleep(5)
                else:
                    await asyncio.sleep(0.2)
            except Exception as e:
                logger.error(f"exception in producer_reports_loop {e}")
                logger.error(traceback.format_exc())
