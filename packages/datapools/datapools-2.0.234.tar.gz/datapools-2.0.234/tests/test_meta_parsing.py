
from .fixtures import *
from datapools.worker.plugins.base_plugin import BasePlugin, BaseTag
from datapools.worker.worker import CrawlerWorker, WorkerSettings, CrawlerContent


def get_content(name):
    with open(get_data_abs_path(name), "rb") as f:
        return f.read()


def test_image_datetime_parsing():
    assert BasePlugin.parse_image_datetime(get_content("empty_meta.jpg")) is None
    assert BasePlugin.parse_image_datetime(get_content("with_createdate.jpg")) == 1721901600  # 2024-07-25 10:00:00


def test_image_copyright_parsing():
    assert BasePlugin.parse_image_tag(get_content("empty_meta.jpg")) is None

    tag = BasePlugin.parse_image_tag(get_content("with_copyright.jpg"))
    assert isinstance(tag, BaseTag)
    assert str(tag) == "asd"
    assert tag.is_keepout() is False


def test_audio_datetime_parsing():
    assert BasePlugin.parse_audio_datetime(get_content("empty_meta.mp3")) is None
    assert BasePlugin.parse_audio_datetime(get_content("with_datetime.mp3")) == 1721901600  # 2024-07-25 10:00:00


def test_audio_tag_parsing():
    # bytes input
    assert BasePlugin.parse_audio_tag(get_content("empty_meta.mp3")) is None

    # io.IOBase input
    with open(get_data_abs_path("empty_meta.mp3"), "rb") as f:
        assert BasePlugin.parse_audio_tag(f) is None

    # bytes input
    tag = BasePlugin.parse_audio_tag(get_content("with_copyright.mp3"))
    assert isinstance(tag, BaseTag)
    assert str(tag) == "asd"
    assert tag.is_keepout() is False

    # io.IOBase input
    with open(get_data_abs_path("with_copyright.mp3"), "rb") as f:
        tag = BasePlugin.parse_audio_tag(f)
        assert isinstance(tag, BaseTag)
        assert str(tag) == "asd"
        assert tag.is_keepout() is False


def test_video_tag_parsing():
    # bytes input
    assert BasePlugin.parse_video_datetime(get_content("empty_meta.mp4")) is None
    assert BasePlugin.parse_video_tag(get_content("empty_meta.mp4")) is None
    assert BasePlugin.parse_video_datetime(get_content("with_datetime.mp4")) == BasePlugin.parse_datetime(
        "2015-07-09T08:08:26.000000Z"
    )
    tag = BasePlugin.parse_video_tag(get_content("with_copyright.mp4"))
    assert isinstance(tag, BaseTag)
    assert str(tag) == "asd"

    # file input
    with open(get_data_abs_path("empty_meta.mp4"), "rb") as f:
        f.read()  # moving file pointer to the end
        assert BasePlugin.parse_video_datetime(f) is None
        assert BasePlugin.parse_video_tag(f) is None

    with open(get_data_abs_path("with_datetime.mp4"), "rb") as f:
        f.read()  # moving file pointer to the end
        dt = BasePlugin.parse_video_datetime(f)
        assert dt is not None
        assert dt == BasePlugin.parse_datetime("2015-07-09T08:08:26.000000Z")

    with open(get_data_abs_path("with_copyright.mp4"), "rb") as f:
        f.read()  # moving file pointer to the end
        tag = BasePlugin.parse_video_tag(f)
        assert isinstance(tag, BaseTag)
        assert str(tag) == "asd"

    # assert BasePlugin.parse_video_tag(get_content("generated.mp4")) is None


def test_trusted_tags():
    def get_cc(tag_id: str | None, copyright_tag_id: str | None, platform_tag_id: str | None) -> CrawlerContent:
        return CrawlerContent(
            tag_id=tag_id,
            tag_keepout=False,
            copyright_tag_id=copyright_tag_id,
            copyright_tag_keepout=False,
            platform_tag_id=platform_tag_id,
            platform_tag_keepout=False,
            url="url",
        )

    cfg = WorkerSettings()
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, None, None)) is False
    assert CrawlerWorker.is_trusted_content(cfg, get_cc("tag1", None, None)) is False
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, "tag1", None)) is False
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, None, "tag1")) is False

    cfg = WorkerSettings(TRUSTED_TAGS=["tag2"])
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, None, None)) is False
    assert CrawlerWorker.is_trusted_content(cfg, get_cc("tag1", None, None)) is False
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, "tag1", None)) is False
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, None, "tag1")) is False

    cfg = WorkerSettings(TRUSTED_TAGS=["tag1", "tag2"])
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, None, None)) is False
    assert CrawlerWorker.is_trusted_content(cfg, get_cc("tag1", None, None)) is True
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, "tag2", None)) is True
    assert CrawlerWorker.is_trusted_content(cfg, get_cc(None, None, "tag1")) is True
