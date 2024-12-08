from cachetools import TTLCache
from asyncache import cached

from typing import Optional
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

from .http import download


@cached(cache=TTLCache(maxsize=10240, ttl=3600))
async def _get_robot_file_parser(robots_url: str) -> Optional[RobotFileParser]:
    # logger.info(f'creating robots.txt parser for {robots_url=}')
    rp = RobotFileParser()
    try:
        raw = await download(robots_url, timeout=2)
        rp.parse(raw.decode("utf-8").splitlines())
        return rp
    except:
        return None


async def is_allowed_by_robots_txt(url: str) -> bool:
    # logger.info(f'is_allowed_by_robots_txt({url=})')
    p = urlparse(url)
    if p.scheme in ("http", "https"):
        robots_url = f"{p.scheme}//{p.netloc}/robots.txt"
        rp = await _get_robot_file_parser(robots_url)
        if rp is not None:
            return rp.can_fetch("*", url)
    return True
