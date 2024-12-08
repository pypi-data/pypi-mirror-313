import io
import uuid
import tempfile
from contextlib import AbstractContextManager
from typing import Optional

import boto3
import botocore
from botocore.config import Config

from datapools.common.logger import logger

from datapools.common.types import InvalidUsageException

from .base_storage import BaseStorage


class S3Reader(AbstractContextManager):
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def read(self):
        with tempfile.TemporaryFile() as f:
            self.bucket.download_fileobj(self.key, f)
            f.seek(0)
            res = f.read()

        # print(f"{res=}")
        return res

    def read_to(self, outfile):
        self.bucket.download_fileobj(self.key, outfile)
        outfile.seek(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class S3Storage(BaseStorage):
    def __init__(self, bucket_name, use_accelerated: bool = True):
        self.path = ""
        self.bucket_name = bucket_name
        if use_accelerated:
            config = Config(s3={"use_accelerate_endpoint": True})
            self.s3 = boto3.resource("s3", config=config)
        else:
            self.s3 = boto3.resource("s3")

        self.bucket = self.s3.Bucket(self.bucket_name)

    def use_path(self, path):
        if len(path) and path[-1] != "/":
            path += "/"
        self.path = path
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.path = ""

    def getkey(self, storage_id):
        return self.path + storage_id

    async def put(self, storage_id, content: str | bytes, content_type: Optional[str] = None):
        # logger.info(f"S3Storage.put {self.getkey(storage_id)=} {content_type=}")
        params = {
            "Body": content if not isinstance(content, str) else content.encode(),
            "Key": self.getkey(storage_id),
        }
        if content_type:
            params["ContentType"] = content_type
        self.bucket.put_object(**params)

    async def upload(self, storage_id, input_path, content_type: Optional[str] = None):
        params = {"Filename": input_path, "Key": self.getkey(storage_id)}
        if content_type:
            params["ExtraArgs"] = {"ContentType": content_type}
        self.bucket.upload_file(**params)

    async def has(self, storage_id) -> bool:
        try:
            self.bucket.Object(self.getkey(storage_id)).load()
            return True
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def get_reader(self, storage_id):
        return S3Reader(self.bucket, self.getkey(storage_id))

    async def read(self, storage_id):
        try:
            with self.get_reader(storage_id) as reader:
                return reader.read()
        except botocore.exceptions.ClientError as e:
            logger.error(f"client err: {e}")
        return None

    async def remove(self, storage_id):
        # logger.info(f"remove {self.getkey(storage_id)=}")
        res = self.bucket.delete_objects(
            Delete={
                "Objects": [
                    {"Key": self.getkey(storage_id)},
                ],
                "Quiet": True,
            },
        )
        # logger.info(res)

    @staticmethod
    def gen_id():
        return str(uuid.uuid4())
