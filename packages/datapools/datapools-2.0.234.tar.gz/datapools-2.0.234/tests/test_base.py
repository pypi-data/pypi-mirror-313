from datapools.worker.plugins.base_plugin import BasePlugin, BaseTag
from datapools.worker.plugins.ftp import FTPPlugin
from datapools.worker.types import WorkerContext
from datapools.common.types import InvalidUsageException
from datapools.worker.worker import CrawlerWorker
from datapools.common.utils import parse_size
from datapools.common.http import download
from tempfile import gettempdir

from bs4 import BeautifulSoup

from .fixtures import *


def test_tag_compare():
    t1 = BaseTag("asd", keepout=False)
    t2 = BaseTag("asd", keepout=False)
    assert t1 == t2

    t1 = BaseTag("asd", keepout=True)
    t2 = BaseTag("asd", keepout=True)
    assert t1 == t2

    t1 = BaseTag("asd", keepout=False)
    t2 = BaseTag("asd", keepout=True)
    assert t1 != t2

    t1 = BaseTag("asd", keepout=True)
    t2 = BaseTag("asd", keepout=False)
    assert t1 != t2

    t1 = BaseTag("asd", keepout=True)
    t2 = None
    assert t1 != t2

    t1 = None
    t2 = BaseTag("asd", keepout=True)
    assert t1 != t2

    t1 = BaseTag("asd", keepout=False)
    t2 = None
    assert t1 != t2

    t1 = None
    t2 = BaseTag("asd", keepout=False)
    assert t1 != t2


import string
import re


def test_tag_parsing():
    print(
        r"(?:^|.*\s)(?:https://)*openlicense.ai/(n/|t/|\b)(\w+)(?:$|\s|"
        + "|".join([re.escape(x) for x in ".,!?\"'@#$%^&*()"])
        + ")"
    )

    t = BasePlugin.parse_tag_in_str(
        '"Use of content under this domain in AI technologies is subject to the licensing terms defined in https://openlicense.ai/t/imageshack"'
    )
    assert isinstance(t, BaseTag)
    assert str(t) == "imageshack"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("\n https://openlicense.ai/tnd")
    assert isinstance(t, BaseTag)
    assert str(t) == "tnd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/t/ntd\nblabla")
    assert isinstance(t, BaseTag)
    assert str(t) == "ntd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("blabla openlicense.ai/t/asd \n")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("xopenlicense.ai/t/asd")
    assert t is None

    t = BasePlugin.parse_tag_in_str("\nhttps://openlicense.ai/n/asd blabla")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is True

    t = BasePlugin.parse_tag_in_str("openlicense.ai/n/asd blabla")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is True

    t = BasePlugin.parse_tag_in_str("xopenlicense.ai/n/asd")
    assert t is None

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/x/asd")
    assert t is None

    t = BasePlugin.parse_tag_in_str("openlicense.ai/x/asd")
    assert t is None


def test_ftp_link_parsing():
    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user:password@host:21")
    assert user == "user"
    assert passwd == "password"
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://host:21")
    assert user == "anonymous"
    assert passwd == ""
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user@host:22")
    assert user == "user"
    assert passwd == ""
    assert host == "host"
    assert port == 22

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user@host")
    assert user == "user"
    assert passwd == ""
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://host")
    assert user == "anonymous"
    assert passwd == ""
    assert host == "host"
    assert port == 21


def test_busy_count(session):
    class A(BasePlugin):
        @staticmethod
        def is_supported(url):
            return True

        async def process(self, task):
            pass

    class B(BasePlugin):
        @staticmethod
        def is_supported(url):
            return True

        async def process(self, task):
            pass

    tmp = gettempdir()
    ctx = WorkerContext(session=session, storage_path=tmp)

    assert A.get_busy_count() == 0
    assert B.get_busy_count() == 0
    a = A(ctx)
    a.is_busy = True
    assert A.get_busy_count() == 1
    assert B.get_busy_count() == 0
    b = B(ctx)
    b.is_busy = True
    assert A.get_busy_count() == 1
    assert B.get_busy_count() == 1
    a.is_busy = False
    assert A.get_busy_count() == 0
    assert B.get_busy_count() == 1
    b.is_busy = False
    assert A.get_busy_count() == 0
    assert B.get_busy_count() == 0


def test_domains():
    assert BasePlugin.is_same_or_subdomain("bbc.m.wikipedia.org", "www.wikipedia.org") is True
    assert BasePlugin.is_same_or_subdomain("pl.m.wikipedia.org", "pl.wikipedia.org") is False


def test_date_parsing():
    assert BasePlugin.parse_datetime("1970-01-01") == 0
    assert BasePlugin.parse_datetime("1970:01:01", "%Y:%m:%d") == 0
    assert BasePlugin.parse_datetime("1970:01:01 00:00:05", "%Y:%m:%d %H:%M:%S") == 5
    assert BasePlugin.parse_datetime("1970", "%Y") == 0
    assert BasePlugin.parse_datetime("1970-02", "%Y-%M") == 120


def test_is_sub_url():
    assert BasePlugin.is_sub_url(
        "https://www.freepik.com/", "https://www.freepik.com/free-photo/beautiful-landscape-mother-nature_14958789.htm"
    )
    assert not BasePlugin.is_sub_url(
        "https://www.freepik.com/free-video",
        "https://www.freepik.com/free-photo/beautiful-landscape-mother-nature_14958789.htm",
    )

    assert BasePlugin.is_sub_url("ftp://user:pass@my.server:223", "/my/image.png")


def test_get_local_url():
    uri = "//imagizer.imageshack.com/v2/240x240q70/c/692/imgresoa.jpg"
    base = "https://imageshack.com"
    assert BasePlugin.get_local_url(uri, base) == f"https:{uri}"


def is_subdir_file(path: str, subpath: str) -> bool:
    return subpath.startswith(path) and subpath.find("/", len(path)) != -1


def is_subdir(path: str, subpath: str) -> bool:
    return subpath.startswith(path) and subpath.endswith("/")


def test_paths():
    assert is_subdir_file("images/", "images/img1/")
    assert is_subdir("images/", "images/img1/")
    assert not is_subdir_file("images/img1/", "images/img101/")
    assert not is_subdir("images/img1/", "images/img101/")
    assert not is_subdir_file("images/img1/", "images/img1/1.png")
    assert is_subdir_file("images/", "images/img1/1.png")


def test_worker_plugin_config_entry():
    assert CrawlerWorker.get_config_key("S3ForFreemusicarchive") == "s3_for_freemusicarchive"
    assert CrawlerWorker.get_config_key("S3ForFreeMusicArchive") == "s3_for_free_music_archive"
    assert CrawlerWorker.get_config_key("S3ForFreemusicarchivePlugin") == "s3_for_freemusicarchive"
    assert CrawlerWorker.get_config_key("S3ForFreeMusicArchivePlugin") == "s3_for_free_music_archive"
    assert CrawlerWorker.get_config_key("LaionArtPlugin") == "laion_art"


def test_parse_size():
    assert parse_size("1M") == 10**6
    assert parse_size("1G") == 10**9
    assert parse_size("1K") == 10**3
    assert parse_size("1T") == 10**12
    assert parse_size("1Mi") == 2**20
    assert parse_size("1Gi") == 2**30
    assert parse_size("1Ki") == 2**10
    assert parse_size("1Ti") == 2**40

    assert parse_size("2M") == 2 * 10**6
    assert parse_size("3G") == 3 * 10**9
    assert parse_size("4K") == 4 * 10**3
    assert parse_size("5Mi") == 5 * 2**20
    assert parse_size("6Gi") == 6 * 2**30
    assert parse_size("7Ki") == 7 * 2**10
    assert parse_size("8T") == 8 * 10**12
    assert parse_size("9Ti") == 9 * 2**40

    assert parse_size("1234") == 1234

    try:
        parse_size("blabla")
        parse_size("1X")
        parse_size("1Bi")
    except InvalidUsageException:
        pass
    else:
        assert False


@pytest.mark.anyio
async def test_is_soup():
    (soup, _) = await BasePlugin.get_url_soup("https://en.wikipedia.org/wiki/Wikipedia:About")
    assert isinstance(soup, BeautifulSoup)
