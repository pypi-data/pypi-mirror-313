import json
from abc import abstractmethod
from enum import Enum
from typing import Optional, Any, Dict, Union, List, TypeAlias
from ..types import BaseMessage
from ..logger import logger

# from ..logger import logger
# MESSAGE_STUDY_URL_PRIORITY: int = 3
# MESSAGE_HINT_URL_PRIORITY: int = 2
# MESSAGE_BACK_TASK_PRIORITY: int = 1


class QueueRole(Enum):
    Publisher = 1
    Receiver = 2
    Both = 3


class QueueMessageType(Enum):
    Task = 1
    ReportTaskStatus = 2  # to scheduler
    StorageInvalidation = 3
    Stop = 4
    ProcessIteration = 5
    DelayedTask = 6
    ReportEvaluation = 7  # to scheduler
    MilvusUpdate = 8  # producer internal


class BaseQueueMessage:
    priority: Optional[int] = None

    @abstractmethod
    def encode(self): ...

    @staticmethod
    @abstractmethod
    def decode(binary: bytes): ...


class QueueMessage(BaseQueueMessage):
    type: QueueMessageType
    session_id: Optional[str] = None
    data: Optional[Union[BaseMessage, Dict[Any, Any]]] = None

    def __init__(
        self,
        message_type: QueueMessageType,
        data=None,
        session_id: Optional[str] = None,
        priority: Optional[int] = None,
    ):
        self.session_id = session_id
        self.type = message_type
        self.data = data
        self.priority = priority

    def encode(self):
        # logger.info(f"encoding {self.type=} {self.data=} {isinstance(self.data, BaseMessage)=}")
        # logger.info(self.data.model_dump())
        return json.dumps(
            {
                "session_id": self.session_id,
                "type": self.type.value,
                "data": json.dumps(self.data.model_dump() if isinstance(self.data, BaseMessage) else self.data),
            }
        ).encode()

    @staticmethod
    def decode(binary):
        j = json.loads(binary.decode())
        res = QueueMessage(
            session_id=j.get("session_id"), message_type=QueueMessageType(j["type"]), data=json.loads(j["data"])
        )
        return res


class QueueRoutedMessage(BaseQueueMessage):
    routing_key: str
    data: BaseMessage

    def __init__(self, routing_key: str, data: BaseMessage, priority: int = 0):
        self.data = data
        self.priority = priority
        self.routing_key = routing_key

    def encode(self):
        # logger.info( f'encoding {self.type=} {self.data=}')
        return json.dumps({"data": json.dumps(self.data.to_dict())}).encode()

    @staticmethod
    def decode(routing_key, binary):
        j = json.loads(binary.decode())
        res = QueueRoutedMessage(routing_key=routing_key, data=json.loads(j["data"]))
        return res


def get_session_queue_name(prefix, session_id):
    return f"{prefix}_{session_id}"
