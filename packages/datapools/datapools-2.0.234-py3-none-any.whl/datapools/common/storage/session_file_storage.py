import os
from .file_storage import FileStorage

# from ..logger import logger


class SessionFileStorage(FileStorage):
    def __init__(self, dstpath: str, session_id: str, must_exist: bool = False):
        super().__init__(os.path.join(dstpath, session_id), must_exist=must_exist)
