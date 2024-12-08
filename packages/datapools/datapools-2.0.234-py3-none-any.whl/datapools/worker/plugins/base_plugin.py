from __future__ import annotations
import asyncio
import base64
import aiohttp
import traceback
import io
import sys
import subprocess
import json
from abc import ABCMeta, abstractmethod
from hashlib import md5
from cachetools import TTLCache
from asyncache import cached
from time import time
from typing import AsyncGenerator, Union, Optional, Callable, List, Dict, Any, Tuple
from urllib.parse import urljoin, urlparse
import magic
from dateutil import parser as date_parser


# from dateutil.tz import tzutc
from datetime import datetime

# import dns.resolver
import dns.asyncresolver

# import httpx
from PIL import Image
from PIL.ExifTags import Base as ExifTagsList
import mutagen
import calendar

from playwright.async_api import async_playwright, Browser, Playwright as AsyncPlaywright, BrowserContext, Page, Locator

from ...common.logger import logger
from ...common.http import download
from ...common.types import (
    BaseCrawlerResult,
    CrawlerBackTask,
    DatapoolContentType,
    WorkerTask,
    StudyUrlTask,
    InvalidUsageException,
)
from ..types import BaseTag
from ..utils import canonicalize_url
from ..types import WorkerContext
from ...producer.base_producer import atimer, timer

MAGIC_MIN_BYTES = 512000  # audio/mpeg seems to require that much..


try:
    from bs4 import BeautifulSoup
except ImportError:
    pass

import re


class BasePluginException(Exception):
    pass


class UnexpectedContentTypeException(BasePluginException):
    pass


class DownloadFailureException(BasePluginException):
    pass


class CachedPairs:
    def __init__(self):
        self.data = {}

    def contains(self, key, ttl):
        return key in self.data and time() - self.data[key][1] < ttl

    def set(self, key, value):
        self.data[key] = (value, time())

    def get(self, key):
        return self.data[key][0]


class Cache:
    def __init__(self):
        self.value = None
        self.time = None

    def is_valid(self, ttl):
        return self.time is not None and time() - self.time < ttl

    def set(self, value):
        self.value = value
        self.time = time()

    def get(self):
        return self.value

    def __repr__(self):
        return f"Cache({self.value=}, {self.time=})"


class PlaywrightBrowserContextManager:
    owner: PlaywrightBrowser
    url: Optional[str]
    page: Page

    def __init__(self, owner: PlaywrightBrowser, url: Optional[str], timeout: int | float):
        self.owner = owner
        self.url = url
        self.timeout = timeout

    async def __aenter__(self):
        await self.owner.try_start()
        self.page = await self.owner.context.new_page()
        if self.url is not None:
            await self.page.goto(self.url, timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.page.close()


class PlaywrightBrowser:
    playwright: AsyncPlaywright
    browser: Browser
    context: BrowserContext
    viewport_width: int = 1920
    viewport_height: int = 1024
    started: bool = False
    start_lock: asyncio.Lock

    def __init__(self):
        self.start_lock = asyncio.Lock()

    async def start(self):
        logger.debug("starting browser")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.context = await self.browser.new_context(
            viewport={"width": self.viewport_width, "height": self.viewport_height},
            user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        )
        logger.debug("started browser")

    def open(self, url: str, timeout: int | float = 30000):
        return PlaywrightBrowserContextManager(self, str(url), timeout)

    def blank(self):
        return PlaywrightBrowserContextManager(self, url=None, timeout=30000)

    async def try_start(self):
        if not self.started:
            async with self.start_lock:
                if not self.started:
                    await self.start()
                    self.started = True


browser = PlaywrightBrowser()


class BasePlugin(metaclass=ABCMeta):

    license_filename = "LICENSE.txt"
    license_max_size = 1024
    _busy_count = 0
    _is_busy = False
    _regexp = re.compile(
        r"(?:^|.*\s)(?:https://)*openlicense.ai/(n/|t/|\b)(\w+)(?:$|\s|"
        + "|".join([re.escape(x) for x in ".,!?\"'@#$%^&*()[]~`:;-+="])
        + ")",
        re.MULTILINE | re.DOTALL,
    )
    copyright_tags_cache: CachedPairs
    platform_tag_cache: Cache

    def __init__(self, ctx: WorkerContext):
        self.ctx = ctx
        self._is_busy = False
        self.copyright_tags_cache = CachedPairs()
        self.platform_tag_cache = Cache()

    def __del__(self):
        if self._is_busy:
            self.is_busy = False  # calling @is_busy.setter
            logger.warning("was busy on destruction!!")

    @property
    def is_busy(self):
        return self._is_busy

    @is_busy.setter
    def is_busy(self, b: bool):
        if self._is_busy != b:
            self._is_busy = b
            if b:
                type(self)._busy_count += 1
                logger.debug(f"busy count of plugin {type(self).__name__} is {type(self)._busy_count} (incremented)")
            else:
                type(self)._busy_count -= 1
                logger.debug(f"busy count of plugin {type(self).__name__} is {type(self)._busy_count} (decremented)")

    @classmethod
    def get_busy_count(cls):
        return cls._busy_count

    @staticmethod
    async def get_url_soup(url: str) -> Tuple[BeautifulSoup, str] | None:
        meta: Dict[str, Any] = {}
        content = await download(url, output_meta=meta)
        if content is not None:
            if meta["url"] != url:
                logger.debug(f"{url} - Redirect to {meta['url']}")
                url = meta["url"]

            soup = BeautifulSoup(content, "html.parser")
            return (soup, url)
        return None

    async def astream(
        self,
        url,
        expected_type: Optional[DatapoolContentType] = None,
        headers={},
        follow_redirects=True,
        max_redirects=5,
        timeout=30,
    ):
        logger.debug(f"BasePlugin.astream {url=}")

        # will try to check content type by http content-type header or ( if header check fails ) by content itself
        is_header_checked = False
        is_content_checked = False
        type_by_header: Optional[DatapoolContentType] = None
        type_by_content: Optional[DatapoolContentType] = None
        type_bytes = bytes()

        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(connect=3, sock_connect=3, sock_read=timeout)
            ) as session:
                async with session.get(
                    url, allow_redirects=follow_redirects, headers=headers, max_redirects=max_redirects
                ) as response:
                    if response.status != 200:
                        raise DownloadFailureException(response.status)

                    async for chunk in response.content.iter_chunked(64 * 1024):

                        if expected_type and not is_header_checked and not is_content_checked:
                            type_bytes += chunk

                            # check by content-type header
                            if not is_header_checked:
                                ct = response.headers.get("content-type")
                                if ct:
                                    is_header_checked = True
                                    try:
                                        type_by_header = self.get_content_type_by_mime_type(ct)
                                        # logger.info(f"astream:{type_by_header=}")
                                    except UnexpectedContentTypeException:
                                        pass

                            # then try to check by content itself
                            if not is_content_checked:
                                if len(type_bytes) >= MAGIC_MIN_BYTES:
                                    is_content_checked = True
                                    try:
                                        type_by_content = self.get_content_type_by_content(type_bytes)
                                        # logger.info(f"astream:{type_by_content=}")
                                    except UnexpectedContentTypeException:
                                        pass

                            if (is_header_checked and type_by_header and type_by_header != expected_type) or (
                                is_content_checked and type_by_content and type_by_content != expected_type
                            ):
                                raise UnexpectedContentTypeException(
                                    f"Unexpected content type: {expected_type} vs {type_by_header} or {type_by_content}"
                                )

                        yield chunk
        except (
            aiohttp.ClientConnectorError,
            aiohttp.ServerConnectionError,
            aiohttp.NonHttpUrlClientError,
        ) as e:
            logger.error(f"astream exception {e}")
            raise DownloadFailureException from e
        except DownloadFailureException as e:
            logger.error(f"failed download with http status {e}")
            raise
        except Exception as e:
            logger.error(f"astream Exception: {e}")
            logger.error(traceback.format_exc())
            raise DownloadFailureException from e

    @staticmethod
    def parse_url(url):
        return urlparse(url)

    @staticmethod
    @abstractmethod
    def is_supported(url) -> bool: ...

    @staticmethod
    def is_same_or_subdomain(dom1, dom2) -> bool:
        # blabla.domain.com could be considered a subdomain of www.domain.com
        if dom2[0:4] == "www.":
            dom2 = dom2[4:]
        if dom1 == dom2:
            return True
        s1 = dom1.split(".")
        s2 = dom2.split(".")
        return s1[-len(s2) : :] == s2

    @staticmethod
    def is_sub_url(url: str, sub_url: str) -> bool:
        p_url = BasePlugin.parse_url(url)
        p_sub = BasePlugin.parse_url(sub_url)
        if p_url.netloc != p_sub.netloc and p_sub.netloc != "":
            return False
        return p_sub.path.find(p_url.path) == 0

    @staticmethod
    def get_local_url(href, page_url, allow_external=False):
        # logger.info(f"get_local_url {href=} {page_url=}")
        pc = urlparse(page_url)
        # logger.info(pc)
        p = urlparse(href)
        # logger.info(f"{p=}")
        if (p.netloc == "" and p.path != "") or BasePlugin.is_same_or_subdomain(p.netloc, pc.netloc):
            return urljoin(page_url, href)
        elif allow_external and p.netloc != "":  # not local, but full url
            return href
        return False

    @staticmethod
    def merge_head_tail(head, tail):
        # returns intersection length
        m = len(head)
        n = len(tail)

        for i in range(max(0, m - n), m):
            head_slice = head[i:]
            tail_slice = tail[0 : m - i]
            # print(i, head_slice, tail_slice)

            if head_slice == tail_slice:
                return head + tail[i:]
        return head + tail

    @abstractmethod
    def process(self, task: WorkerTask) -> AsyncGenerator[BaseCrawlerResult, None]: ...

    async def study(self, task: StudyUrlTask, timeout: int = 3000) -> List[BaseTag]:
        async with browser.open(task.url, timeout=timeout) as cm:
            logger.info(f"studying {cm.page.url=}")

            real_url = cm.page.url
            if not self.get_local_url(real_url, task.url):
                logger.debug("redirected to different domain")
                return []

            url = real_url

            tags = []

            p = BasePlugin.parse_url(url)
            platform_tag = await self.get_platform_tag(p.netloc, cm.page, 3600)
            if platform_tag:
                tags.append(platform_tag)
                logger.info(f"found {platform_tag=}")

            return tags

    @staticmethod
    def is_imported(module):
        return module in sys.modules

    @classmethod
    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    async def parse_dns_tag(cls, domain) -> Union[BaseTag, None]:
        logger.debug(f"parse_dns_tag {domain=}")
        try:
            records = await dns.asyncresolver.resolve(domain, "TXT")
            for record in records:
                logger.debug(f"{str(record)=}")
                tag = BasePlugin.parse_tag_in_str(str(record))
                if tag is not None:
                    logger.debug(f"found dns {tag=}")
                    return tag
        except dns.resolver.NoAnswer:
            logger.error("dns no answer exception")
        except dns.resolver.LifetimeTimeout:
            logger.error("dns timeout exception")
        except dns.resolver.NoNameservers:
            logger.error("dns no nameservers exception")
        return None

    @classmethod
    async def parse_meta_tag(cls, content, meta_name) -> Optional[BaseTag]:
        if BasePlugin.is_imported("bs4") and isinstance(content, BeautifulSoup):
            return BasePlugin.parse_tag_in_bs_content(content, "meta")
        if BasePlugin.is_imported("playwright.async_api") and isinstance(content, Page):
            metas = content.locator(f'meta[name="{meta_name}"]')
            for meta in await metas.all():
                c = await meta.get_attribute("content")

                tag = BasePlugin.parse_tag_in_str(c)
                if tag is not None:
                    return tag
        return None

    @classmethod
    def parse_tag_in_str(cls, string) -> Union[BaseTag, None]:
        # logger.info(f"parse_tag_in_str {string=}")
        tag = BasePlugin._regexp.match(string)
        if tag is not None:
            return BaseTag(tag.group(2), tag.group(1) == "n/")
        return None

    @classmethod
    def parse_tag_in_bs_content(cls, content: BeautifulSoup, locator: str) -> Optional[BaseTag]:
        tag = content.find(locator, attrs={"content": BasePlugin._regexp})
        if tag is not None:
            return BaseTag(tag.group(2), tag.group(1) == "n/")
        return None

    @classmethod
    async def parse_tag_in(cls, content, loc: str = "") -> Optional[BaseTag]:
        if type(content) is str:
            return BasePlugin.parse_tag_in_str(content)
        elif BasePlugin.is_imported("bs4") and isinstance(content, BeautifulSoup):
            return BasePlugin.parse_tag_in_bs_content(content, loc)

        elif BasePlugin.is_imported("playwright.async_api") and isinstance(content, (Page, Locator)):
            elems = content.locator(loc)
            for elem in await elems.all():
                c = await elem.text_content()
                if c is not None:
                    return BasePlugin.parse_tag_in_str(c)
        return None

    @staticmethod
    def get_content_type_by_mime_type(mime) -> DatapoolContentType:
        # logger.info(f"{mime=}")
        parts = mime.split("/")
        if parts[0] == "image":
            return DatapoolContentType.Image
        if parts[0] == "video" or mime == "application/mxf":
            return DatapoolContentType.Video
        if parts[0] == "audio":
            return DatapoolContentType.Audio
        if parts[0] == "text" or mime == "application/json":
            return DatapoolContentType.Text

        raise UnexpectedContentTypeException(f"not supported {mime=}")

    @staticmethod
    def get_content_type_by_content(content: Union[bytes, str, io.IOBase]) -> DatapoolContentType:
        if isinstance(content, (bytes, str)):
            mime = magic.from_buffer(content, mime=True)
        elif isinstance(content, io.IOBase):
            content.seek(0, 0)
            buffer = content.read(MAGIC_MIN_BYTES)  # TODO: enough?
            mime = magic.from_buffer(buffer, mime=True)
        else:
            raise BasePluginException(f"not supported input: {type(content)}")

        if mime:
            return BasePlugin.get_content_type_by_mime_type(mime)
        raise BasePluginException("not supported content")

    @classmethod
    def _getexif(cls, content: Union[bytes, io.IOBase]) -> Image.Exif:
        if isinstance(content, bytes):
            image = Image.open(io.BytesIO(content))
        elif isinstance(content, io.IOBase):
            image = Image.open(content)  # type: ignore
        else:
            raise Exception(f"Unsupport image content {type(content)=}")
        return image.getexif()

    @classmethod
    def parse_image_tag(cls, content: Union[bytes, io.IOBase]) -> Optional[BaseTag]:
        # load image from bytes content, parse Copyright exif field for a license tag
        try:
            exifdata = cls._getexif(content)
            cp = exifdata.get(ExifTagsList.Copyright)
            # logger.info( f'{cp=} {type(cp)=}')

            if isinstance(cp, str):
                return cls.parse_tag_in_str(cp)
        except Exception as e:
            logger.error(f"Failed process image (tag): {e}")
        return None

    @classmethod
    def parse_image_datetime(cls, content: Union[bytes, io.IOBase]) -> Optional[int]:
        try:
            exifdata = cls._getexif(content)
            dt = exifdata.get(ExifTagsList.DateTimeOriginal) or exifdata.get(ExifTagsList.DateTime)
            if isinstance(dt, str):
                return cls.parse_datetime(dt, "%Y:%m:%d %H:%M:%S")
        except Exception as e:
            logger.error(f"Failed process image (datetime): {e}")
        return None

    @classmethod
    def get_audio_meta(cls, content: Union[bytes, io.IOBase]) -> Optional[dict]:
        if isinstance(content, bytes):
            return mutagen.File(io.BytesIO(content))
        if isinstance(content, io.IOBase):
            return mutagen.File(content)
        raise Exception(f"Unsupport audio content {type(content)=}")

    @classmethod
    def _get_video_meta(cls, content: Union[bytes, io.IOBase]) -> Optional[dict]:
        """returns video stream info of a video file using ffprobe command line interface"""
        args = ["ffprobe", "-v", "quiet", "-i", "pipe:0", "-show_streams", "-show_format", "-print_format", "json"]

        if isinstance(content, bytes):
            logger.debug("video meta by bytes")
            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # type: ignore
            out, err = p.communicate(input=content)
        elif isinstance(content, io.IOBase):
            logger.debug("video meta by IOBase")
            content.seek(0, 0)
            p = subprocess.Popen(args, stdin=content.fileno(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # type: ignore
            out, err = p.communicate()
        if p.returncode != 0:
            logger.error(f"Failed call ffprobe: {out=} {err=} {p.returncode=}")
            return None
        resp = out.decode("utf-8")
        # logger.info(resp)
        return json.loads(resp)

    @classmethod
    def parse_audio_tag(cls, content: Union[bytes, io.IOBase]) -> Optional[BaseTag]:
        # https://mutagen-specs.readthedocs.io/en/latest/id3/id3v2.2.html
        # http://www.unixgods.org/Ruby/ID3/docs/ID3_comparison.html
        try:
            m = cls.get_audio_meta(content)
            if m:
                for key in ("TCOP", "WCOP", "TCR", "WCP"):
                    copyright = m.get(key)
                    if copyright:
                        for t in copyright.text:
                            tag = BasePlugin.parse_tag_in_str(t)
                            if tag:
                                return tag
        except Exception as e:
            logger.error(f"Failed process audio (datetime): {e}")
        return None

    @classmethod
    def parse_audio_datetime(cls, content: Union[bytes, io.IOBase]) -> Optional[int]:
        # https://mutagen-specs.readthedocs.io/en/latest/id3/id3v2.2.html
        # http://www.unixgods.org/Ruby/ID3/docs/ID3_comparison.html
        try:
            m = cls.get_audio_meta(content)
            if m:
                dt = m.get("TDRC")
                if dt:
                    return cls.parse_datetime(str(dt))

                y = m.get("TYE") or m.get("TYER")  # YYYY
                if y:
                    dt = str(y)
                    fmt = "%Y"

                    dm = m.get("TDA") or m.get("TDAT")  # DDMM
                    if dm:
                        dt += str(dm)
                        fmt += "%d%m"

                    t = m.get("TIM") or m.get("TIME")  # HHMM
                    if t:
                        dt += str(t)
                        fmt += "%H%M"

                    if dt:
                        return cls.parse_datetime(dt, fmt)

        except Exception as e:
            logger.error(f"Failed process audio (datetime): {e}")
            # logger.error(traceback.format_exc())
        return None

    @classmethod
    def parse_video_tag(cls, content: Union[bytes, io.IOBase]) -> Optional[BaseTag]:
        info = BasePlugin._get_video_meta(content)
        logger.debug(info)
        if info and "format" in info and "copyright" in info["format"]["tags"]:
            return BasePlugin.parse_tag_in_str(info["format"]["tags"]["copyright"])
        return None

    @classmethod
    def parse_video_datetime(cls, content: Union[bytes, io.IOBase]) -> Optional[int]:
        info = BasePlugin._get_video_meta(content)
        logger.debug(info)
        if info and "streams" in info:
            for stream in info["streams"]:
                if stream.get("codec_type") == "video":
                    if "tags" in stream and "creation_time" in stream["tags"]:
                        return BasePlugin.parse_datetime(stream["tags"]["creation_time"])
                    break
        return None

    @classmethod
    def parse_content_tag(
        cls, content: Union[bytes, str, io.IOBase], content_type: DatapoolContentType
    ) -> Optional[BaseTag]:
        if content_type == DatapoolContentType.Image:
            if isinstance(content, (bytes, io.IOBase)):
                return BasePlugin.parse_image_tag(content)
            logger.warning(f"unsupported content type for Image: {type(content)=}")
            return None
        elif content_type == DatapoolContentType.Audio:
            if isinstance(content, (bytes, io.IOBase)):
                return BasePlugin.parse_audio_tag(content)
            logger.warning(f"unsupported content type for Audio: {type(content)=}")
            return None
        if content_type == DatapoolContentType.Video:
            if isinstance(content, (bytes, io.IOBase)):
                return BasePlugin.parse_video_tag(content)
            logger.warning(f"unsupported content type for Video: {type(content)=}")
            return None
        if content_type == DatapoolContentType.Text:
            if isinstance(content, str):
                return BasePlugin.parse_tag_in_str(content)
            logger.warning(f"unsupported content type for Text: {type(content)=}")
            return None  # TODO: should support?
        raise BasePluginException(f"parse_content_tag: not supported content type {content_type}")

    async def get_platform_tag(self, domain, content, ttl=3600, meta_name=None) -> Union[BaseTag, None]:
        # logger.info( f'get_platform_tag {self.platform_tag_cache=}')
        # logger.info(f'now={time()}' )
        # logger.info(f'diff={time() - self.platform_tag_cache.time if self.platform_tag_cache.time is not None else "nan"}')

        if not self.platform_tag_cache.is_valid(ttl):
            dns_tag = await BasePlugin.parse_dns_tag(domain)
            if dns_tag:
                self.platform_tag_cache.set(dns_tag)
            else:
                # check if <meta/> tag exists with our tag
                header_tag = await BasePlugin.parse_meta_tag(content, meta_name)
                self.platform_tag_cache.set(header_tag)
        return self.platform_tag_cache.get()

    @staticmethod
    async def get_webpage_image_bytes(img_locator):
        """for playwright only"""
        b64 = await img_locator.evaluate(
            '(img) => {\
            img.crossOrigin="anonymous";\
            var canvas = document.createElement("canvas");\
            canvas.width = img.width;\
            canvas.height = img.height;\
            var ctx = canvas.getContext("2d");\
            ctx.drawImage(img, 0, 0);\
            var dataURL = canvas.toDataURL("image/png");\
            return dataURL;\
        }'
        )
        n = len("data:image/png;base64,")
        return base64.b64decode(b64[n:])

    async def parse_links(self, content, url: Optional[str] = None):
        """gather all links on the page and yield them as subtasks. Only current domain urls are counted"""
        if isinstance(content, Page):
            async for link in self.parse_links_playwright(content):
                yield link
        elif isinstance(content, BeautifulSoup):
            assert url is not None
            async for link in self.parse_links_bs4(content, url):
                yield link
        else:
            raise InvalidUsageException(type(content))

    async def parse_links_playwright(self, page: Page):
        # logger.info( f'base_plugin::parse_links()')
        hrefs = await page.locator("a").all()
        # logger.info( f'base_plugin::parse_links() got {len(hrefs)=}')
        for href_loc in hrefs:
            href = await href_loc.get_attribute("href")
            # logger.info(href)
            if href is not None:
                # logger.info( f'parse_link {href=} {type(href)=} {page.url} {type(page.url)=}')

                full_local_url = BasePlugin.get_local_url(href, page.url)
                # logger.info(full_local_url)
                if full_local_url:
                    # strict constraint on urls, else may get endless recursions etc
                    full_local_url = canonicalize_url(full_local_url)
                    # logger.info(full_local_url)

                    # logger.info( f'---------yielding {full_local_url=}')
                    yield CrawlerBackTask(url=full_local_url)
                    # logger.info( f'---------yielded {video_url=}')
                else:
                    # logger.info(f"non local: {href=} {page.url=}")
                    pass

    async def parse_links_bs4(self, soup: BeautifulSoup, url: str):
        hrefs = soup.find_all("a")
        # logger.info( f'base_plugin::parse_links() got {len(hrefs)=}')
        for href_loc in hrefs:
            href = href_loc.get_attribute_list("href")
            if href and href[0]:

                href = href[0]
                logger.debug(f"parse_link {href=} {type(href)=} {url} {type(url)=}")

                full_local_url = BasePlugin.get_local_url(href, url)
                # logger.info(full_local_url)
                if full_local_url:
                    # strict constraint on urls, else may get endless recursions etc
                    full_local_url = canonicalize_url(full_local_url)
                    # logger.info(full_local_url)

                    # logger.info( f'---------yielding {full_local_url=}')
                    yield CrawlerBackTask(url=full_local_url)
                    # logger.info( f'---------yielded {video_url=}')
                else:
                    # logger.info(f"non local: {href=} {page.url=}")
                    pass

    @staticmethod
    def get_text_storage_content(body: str, header: Optional[str] = None, excerpt: Optional[str] = None) -> str:
        data = (header + "\n" if header else "") + (excerpt + "\n" if excerpt else "") + body
        return data

    @staticmethod
    def gen_demo_tag(user_name):
        return "demo_" + md5(user_name.encode()).hexdigest()[-8:]

    @staticmethod
    async def parse_html_time_tag(page: Union[Page, Locator], loc: Optional[str] = "") -> int | None:
        """
        Works only with <time> html tag.
        Returns unix timestamp
        """
        res = None
        time_link = await page.locator(f"time{loc}").all()
        if len(time_link):
            dt = await time_link[0].get_attribute("datetime")
            if dt is not None:
                return BasePlugin.parse_datetime(dt)
        return res

    @staticmethod
    def parse_datetime(raw: str, fmt: Optional[str] = None) -> int:
        if fmt is None:
            parsed = date_parser.parse(raw).replace(tzinfo=None)
            epoch = datetime(1970, 1, 1, 0, 0, 0)
            return int((parsed - epoch).total_seconds())
        dt = datetime.strptime(raw, fmt)
        return calendar.timegm(dt.utctimetuple())


class DirectContentUrl:
    pass


class BaseReader:
    @abstractmethod
    async def read_to(self, f: io.IOBase, stopper: Callable): ...


class BaseReaderException(Exception):
    pass


class ConnectionFailed(BaseReaderException):
    pass


class AuthFailed(BaseReaderException):
    pass


class ReadFailed(BaseReaderException):
    pass
