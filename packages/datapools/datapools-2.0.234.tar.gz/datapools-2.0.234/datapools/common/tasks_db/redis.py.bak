import json
import time
from typing import Literal, Union

import redis

from ..logger import logger
from .tasks_db import (
    Hash,
    Task,
    TaskInProgress,
    TaskOrNone,
    TasksDB,
    TasksInProgress,
)

URL_HASHES_KEY = "tasks_url_hashes"  # sorted set
URL_DONE_HASHES_KEY = "tasks_url_done_hashes"  # set
TASKS_QUEUE_KEY = "tasks_queue"  # hash
TASKS_IN_PROGRESS_KEY = "tasks_in_progress"  # hash


class RedisTasksDB(TasksDB):
    def __init__(self, host, port=6379, db=0, protocol=3):
        super().__init__()
        self.redis = redis.Redis(
            host=host, port=port, db=db, protocol=protocol
        )

    def is_ready(self) -> bool:
        try:
            self.redis.ping()
            return True
        except redis.exceptions.ConnectionError:
            return False

    def add(
        self, task, score=0, ignore_existing=False, ignore_done=False
    ) -> Union[Hash, Literal[False]]:
        hash = TasksDB._get_hash(task["url"])
        if (ignore_existing or not self.has(task)) and (
            ignore_done or not self.has_done(task)
        ):
            pipe = self.redis.pipeline()
            pipe.zadd(URL_HASHES_KEY, {hash: score})
            pipe.hset(TASKS_QUEUE_KEY, hash, json.dumps(task))
            res = pipe.execute()
            logger.info(f"redis::add() {hash=} {res=}")
            return hash
        return False

    def has(self, task) -> bool:
        hash = self._get_hash(task["url"])
        score = self.redis.zscore(URL_HASHES_KEY, hash)
        logger.info(f"redis::has() {hash=} {score=}")
        return score is not None

    def has_done(self, task) -> bool:
        hash = self._get_hash(task["url"])
        return self.redis.sismember(URL_DONE_HASHES_KEY, hash)

    def _remove_task(self, hash):
        pipe = self.redis.pipeline()
        pipe.hget(TASKS_QUEUE_KEY, hash)
        pipe.hdel(TASKS_QUEUE_KEY, hash)
        res = pipe.execute()
        return json.loads(res[0])  # result of hget()

    def _remove_done_task(self, hash):
        self.redis.srem(URL_DONE_HASHES_KEY, hash)

    def pop(self, progress_data: dict = {}) -> TaskOrNone:
        # get hash with max score ( =priority )
        i = 0
        while True:
            # looping until task in queue is found
            hashes = self.redis.zrevrange(URL_HASHES_KEY, i, i + 9)
            n = len(hashes)
            if n > 0:
                for hash in hashes:
                    logger.info(f"checking task {hash}")
                    if self.redis.hexists(TASKS_QUEUE_KEY, hash):
                        logger.info("available")

                        # 1. get url from tasks queue and remove it at once ( like "pop" )
                        task = self._remove_task(hash)

                        logger.info(f"redis::pop() {hash=} {task=}")

                        if (
                            task
                        ):  # possibly not if concurrent schedulers are running
                            # 2. insert url into progress list along with start timestamp and other user defined data
                            progress_data["task"] = task
                            progress_data["datetime"] = time.time()
                            self.redis.hset(
                                TASKS_IN_PROGRESS_KEY,
                                hash,
                                json.dumps(progress_data),
                            )

                            res = {"id": hash, "url": task["url"]}
                            return res
                    else:
                        logger.info("not available")
                i += n
            else:
                break

        return None

    def get_progress_list(self, offset, limit) -> TasksInProgress:
        keys = self.redis.hkeys(TASKS_IN_PROGRESS_KEY)
        keys = keys[offset : offset + limit]
        if len(keys) > 0:
            tasks = self.redis.hmget(TASKS_IN_PROGRESS_KEY, keys)
            for i in range(0, len(tasks)):
                tasks[i] = json.loads(tasks[i])
            res = dict(zip(keys, tasks))
        else:
            res = {}
        return res

    def _remove_progress(self, hash) -> TaskInProgress:
        # start transaction
        pipe = self.redis.pipeline()

        # 1. get from progress list and remove value
        pipe.hget(TASKS_IN_PROGRESS_KEY, hash)
        pipe.hdel(TASKS_IN_PROGRESS_KEY, hash)

        res = pipe.execute()
        return json.loads(res[0])  # result of hget()

    def undo_progress(self, hash) -> TaskInProgress:
        progress = self._remove_progress(hash)
        logger.info(f"redis::undo_progress() {hash=} {progress=}")

        # 2. insert task into the queue
        self.redis.hset(TASKS_QUEUE_KEY, hash, json.dumps(progress["task"]))
        return progress

    def get_progress(self, hash) -> TaskInProgress:
        progress = self.redis.hget(TASKS_IN_PROGRESS_KEY, hash)
        return json.loads(progress)

    def remove(self, hash) -> Task:
        try:
            progress = self._remove_progress(hash)
            logger.info(f"redis::_remove_progress() {hash=} {progress=}")
            task = progress["task"]
        except Exception:
            try:
                task = self._remove_task(hash)
            except Exception:
                task = self._remove_done_task(hash)

        self.redis.zrem(URL_HASHES_KEY, hash)

        return task

    def set_done(self, hash) -> Task:
        # progress = self._remove_progress( hash )
        pipe = self.redis.pipeline()
        pipe.zrem(URL_HASHES_KEY, hash)
        pipe.sadd(URL_DONE_HASHES_KEY, hash)
        pipe.execute()

        # return progress[ 'task' ]
        return {}
