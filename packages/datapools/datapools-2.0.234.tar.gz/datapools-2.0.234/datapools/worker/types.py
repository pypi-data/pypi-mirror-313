from enum import Enum
from typing import Optional
from ..common.session_manager import Session


class YieldResult(Enum):
    NoResult = 0
    ContentDownloadSuccess = 1
    ContentDownloadFailure = 2
    ContentIgnored = 3
    ContentReused = 4


class BaseTag:
    _tag: Optional[str] = None
    _is_keepout: Optional[bool] = None

    def __init__(self, tag, keepout=False):
        self._tag = tag
        self._is_keepout = keepout

    def __str__(self):
        return self._tag

    def __repr__(self):
        return f"BaseTag(tag={self._tag}, keepout={self._is_keepout})"

    def __eq__(self, other):
        if not isinstance(other, BaseTag):
            return False
        if not other.is_valid():
            return False
        return str(self) == str(other) and self._is_keepout == other._is_keepout

    def is_keepout(self):
        return self._is_keepout

    def is_valid(self):
        return type(self._tag) is str


class WorkerContext:
    session: Optional[Session]
    yield_result: YieldResult
    real_task_url: Optional[str]
    storage_path: str

    def __init__(self, session: Optional[Session], storage_path: str):
        self.session = session
        self.yield_result = YieldResult.NoResult
        self.storage_path = storage_path
