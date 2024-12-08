import io
import traceback
import time

import asyncio
import os
from ftplib import FTP_PORT
import aioftp
from urllib.parse import unquote
from pydantic import AnyUrl

try:
    from pydantic.tools import parse_obj_as
except ImportError:
    from pydantic import TypeAdapter

    parse_obj_as = TypeAdapter.validate_python

from typing import List, Optional, Callable

# import httpx

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerContent, StudyUrlTask, CrawlerPostponeSession
from ....common.http import download
from ..base_plugin import BasePlugin, BaseTag, BaseReader, BaseReaderException, ConnectionFailed, AuthFailed
from ...worker import WorkerTask, YieldResult


class FTPReader(BaseReader):
    filepath: str
    filesize: int
    host: str
    port: int
    user: str
    passwd: str

    def __init__(self, host, port, user, passwd, filepath, filesize):
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

        # filepath = "/Paintings of the World 3(13 min).mp4"
        # filesize = 461417090

        self.filepath = filepath
        self.filesize = int(filesize)

    async def read_to(self, f: io.IOBase, stopper: Callable):
        total = 0
        i = 0
        is_stopped = False
        done = True
        try:
            client = aioftp.Client(socket_timeout=10, connection_timeout=10, path_timeout=10)
            try:
                await client.connect(self.host, self.port)
            except asyncio.TimeoutError as e:
                raise ConnectionFailed() from e

            try:
                await client.login(self.user, self.passwd)
            except aioftp.errors.StatusCodeError as e:
                logger.error("Failed login")
                raise AuthFailed() from e

            stream = await client.download_stream(self.filepath)
            async for block in stream.iter_by_block():
                if not block:
                    break
                # async for block in stream.iter_by_block():

                # logger.info(f"{type(block)=} {len(block)=}")

                f.write(block)
                # logger.info("wrote")
                total += len(block)

                if int(total / self.filesize * 100) >= i * 10:
                    # if True:
                    logger.info(f"FTP read total {total} vs {self.filesize} ({int(total/self.filesize*100)}%)")
                    i += 1

                if total >= self.filesize:
                    done = True
                    break
                if await stopper():
                    logger.info("aborting")
                    # await self.client.abort()
                    # stream.close()
                    # is_stopped = True
                    break
                # else:
                # await stream.finish()

            logger.info(f"FTP read done, {total=} ({int(total/self.filesize*100)}%)")
        except aioftp.errors.StatusCodeError as e:
            logger.info("FTPReader aioftp.errors.StatusCodeError")
            if not is_stopped:
                raise BaseReaderException() from e
        except ConnectionResetError as e:
            logger.info("FTPReader ConnectionResetError")
            if not done:
                raise BaseReaderException() from e
        except asyncio.TimeoutError as e:
            logger.info("FTPReader asyncio.TimeoutError")
            raise BaseReaderException() from e


class FTPPlugin(BasePlugin):
    client: Optional[aioftp.Client] = None
    client_lock: Optional[asyncio.Lock] = None
    copyright_tags: List[BaseTag]
    host: Optional[str] = ""
    port: Optional[int] = 0
    user: Optional[str] = ""
    passwd: Optional[str] = ""

    def __init__(self, ctx, demo_tag=None):
        super().__init__(ctx)
        self.copyright_tags = []
        if demo_tag:
            self.copyright_tags.append(BaseTag(demo_tag))

    @staticmethod
    def is_supported(url):
        p = BasePlugin.parse_url(url)
        return p.scheme == "ftp"

    @staticmethod
    def parse_ftp_url(url):
        user = "anonymous"
        passwd = ""
        port = int(FTP_PORT)

        u = parse_obj_as(AnyUrl, url)
        if u.username is not None:
            user = unquote(u.username)
        if u.password is not None:
            passwd = u.password
        host = u.host
        if u.port is not None:
            port = u.port

        return (user, passwd, host, port)

    async def keepalive(self):
        last_noop = 0
        while self.client:
            try:
                now = time.time()
                if now - last_noop > 10:
                    async with self.client_lock:
                        await self.client.command("NOOP", "2xx")
                    last_noop = now
            except asyncio.TimeoutError:
                logger.error("FTP keepalive timeout")
            await asyncio.sleep(1)

    async def _init(self, url, socket_timeout, connection_timeout, path_timeout):
        (user, passwd, host, port) = self.parse_ftp_url(url)
        self.client = aioftp.Client(
            socket_timeout=socket_timeout, connection_timeout=connection_timeout, path_timeout=path_timeout
        )
        self.client_lock = asyncio.Lock()

        await self.client.connect(host, port)
        await self.client.login(user, passwd)

        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def _deinit(self):
        logger.info("FTP finally")
        self.client = None
        self.client_lock = None

    async def study(self, task: StudyUrlTask, __timeout: int = 3000) -> List[BaseTag]:
        try:
            await self._init(task.url, 3, 3, 3)

            # self.client cannot be None here, suppressing mypy
            pwd = await self.client.get_current_directory()  # type: ignore
            logger.info(pwd)

            dir_list = await self.client.list(pwd)  # type: ignore
            logger.info(dir_list)

            await self._try_find_license(dir_list)
            return self.copyright_tags

        except Exception as e:
            logger.error(f"FTP study error {e}")
            logger.error(traceback.format_exc())
            raise

        finally:
            self._deinit()

    async def process(self, task: WorkerTask):
        await self._init(task.url, 10, 10, 10)

        asyncio.create_task(self.keepalive())

        try:
            async with self.client_lock:  # type: ignore
                pwd = await self.client.get_current_directory()  # type: ignore
            logger.info(pwd)
            async for x in self._scan_dir(pwd, 0):
                yield x
        except Exception as e:
            logger.error(f"FTP error {e}")
            logger.error(traceback.format_exc())
            raise
        finally:
            self._deinit()

    async def _scan_dir(self, path, rec):
        async with self.client_lock:
            dir_list = await self.client.list(path)
        logger.info(dir_list)

        local_copyright_tag = await self._try_find_license(dir_list)
        if len(self.copyright_tags) == 0:
            logger.info(f"no copyright tag in {path}")
            return
        copyright_tag = self.copyright_tags[-1]

        # copyright_tag is pushed to self.copyright_tags

        for item in dir_list:
            filepath = str(item[0])
            logger.info(
                "\t" * rec
                + item[1]["type"]
                + "\t"
                + filepath
                + "\t"
                + (item[1]["size"] if item[1]["type"] == "file" else "")
            )
            if item[1]["type"] == "dir":
                async for x in self._scan_dir(filepath, rec + 1):
                    yield x
            elif item[1]["type"] == "file":
                filename = os.path.split(filepath)[-1]
                if filename == BasePlugin.license_filename:
                    continue

                yield CrawlerContent(
                    copyright_tag_id=str(copyright_tag),
                    copyright_tag_keepout=copyright_tag.is_keepout(),
                    url=filepath,
                    content=FTPReader(self.host, self.port, self.user, self.passwd, filepath, item[1]["size"]),
                )
                if self.ctx.yield_result == YieldResult.ContentDownloadFailure:
                    yield CrawlerPostponeSession()
                    break
            else:
                raise Exception(f"unknown type of {str(item[0])} - {item[1]['type']}")
        if local_copyright_tag:
            self.copyright_tags.pop()

    async def _try_find_license(self, dir_contents) -> Optional[BaseTag]:
        for item in dir_contents:
            file_path = item[0]
            filename = os.path.split(file_path)[-1]
            # logger.info(path_parts)

            if filename == BasePlugin.license_filename and item[1]["type"] == "file":
                logger.info(f"found {BasePlugin.license_filename}")
                content = await download(file_path)
                if content:
                    logger.info(f"got license content: {content=}")
                    tag = await BasePlugin.parse_tag_in(content.decode())
                    # logger.info(f"{tag_id=}")
                    logger.info(f"{tag=}")
                    if tag:
                        self.copyright_tags.append(tag)
                        return tag
        return None

    async def download(self, path):
        res = b""
        async with self.client_lock:
            async with self.client.download_stream(path) as stream:
                async for block in stream.iter_by_block():
                    res += block
        return res
