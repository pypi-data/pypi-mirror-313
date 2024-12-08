# from pydantic import Dict
from hashlib import md5
from typing import Dict, Literal, TypeAlias, Union


class TasksDBException(Exception):
    pass


# class Task:
#     pass

# class TaskInProgress:
#     pass

Hash: TypeAlias = str
TaskInProgress: TypeAlias = dict
Task: TypeAlias = dict
TasksInProgress: TypeAlias = Dict[Hash, TaskInProgress]
TaskOrNone: TypeAlias = Union[dict, None]


class TasksDB:
    def __init__(self):
        pass

    def add(self, task, score=0, ignore_existing=False, ignore_done=False) -> Union[Hash, Literal[False]]:
        # puts new url to the queue
        # score may define priority of the task
        # should return False if url is already in the queue
        raise TasksDBException("implement add()")

    def has(self, task) -> bool:
        # checks if URL is not in the queue already
        raise TasksDBException("implement has()")

    def has_done(self, task) -> bool:
        # checks if URL is not in the done list already
        raise TasksDBException("implement has_done()")

    def pop(self, progress_data=None) -> TaskOrNone:
        # returns first url from the queue
        # task should be moved to the progress list
        # progress_data may contain data associated with worker, who is going to process this url
        raise TasksDBException("implement get()")

    def remove(self, hash) -> Task:
        # completely removes the task ( queue, progress and done list )
        raise TasksDBException("implement remove()")

    def get_progress_list(self, offset, limit) -> TasksInProgress:
        # returns list of tasks in the range [offset:offset+limit-1]
        raise TasksDBException("implement get_progress_list()")

    def get_progress(self, hash) -> TaskInProgress:
        # returns task progress data
        raise TasksDBException("implement get_progress()")

    def undo_progress(self, hash) -> TaskInProgress:
        # moves task back to the queue
        raise TasksDBException("implement undo_progress()")

    def set_done(self, hash) -> Task:
        # moves task to the done list
        raise TasksDBException("implement set_done()")

    def is_ready(self) -> bool:
        raise TasksDBException("implement is_ready()")

    @staticmethod
    def _get_hash(url):
        return md5(url.encode()).hexdigest()
