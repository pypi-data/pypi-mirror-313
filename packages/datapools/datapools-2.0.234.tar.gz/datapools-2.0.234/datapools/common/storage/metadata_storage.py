import os
from .file_storage import FileStorage


class MetadataStorage(FileStorage):
    def __init__(self, storage_path, must_exist: bool = False, depth: int = 0):
        super().__init__(os.path.join(storage_path, "metadata"), must_exist, depth)
