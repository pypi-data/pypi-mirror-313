import re
import asyncio
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup, Comment
from html2text import HTML2Text
from typing import Optional, Tuple, Dict, Any

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import (
    CrawlerBackTask,
    CrawlerContent,
    DatapoolContentType,
    CrawledContentMetadata,
    CrawlerPostponeSession,
)
from ...utils import canonicalize_url
from ..base_plugin import BasePlugin, BaseTag
from ...worker import WorkerTask

DOMAIN = "www.theguardian.com"


class TheGuardianPlugin(BasePlugin):

    base_url = f"https://{DOMAIN}/"

    def __init__(self, ctx):
        super().__init__(ctx)

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        # logger.info( f'dataphoenix.info {u=}')
        return u.netloc[-16:] == ".theguardian.com"

    def is_article(self, url):
        path = urlparse(url).path
        pattern = r"^/[\w/-]+/\d+/\w+/\d+/[\w/-]+$"
        return bool(re.match(pattern, path))

    def normalize(self, url):
        parts = list(urlparse(url))
        parts[5] = ""  # remove fragment
        clean_url = urlunparse(parts)
        return clean_url

    def extract(self, soup: BeautifulSoup) -> Optional[Tuple[str, str]]:
        content = soup.find("article")
        if not content:
            logger.debug("No <article>. Skipped.")
            return None

        title = soup.find("h1")
        if not title:
            logger.debug("No <h1>. Skipped.")
            return None

        filter_list = [
            dict(string=lambda s: isinstance(s, Comment)),
            dict(name="img"),
            dict(name="svg"),
            dict(name="button"),
            dict(name="video"),
            dict(name="picture"),
            dict(name="source"),
            dict(name="small"),
            dict(name="footer"),
            dict(name="gu-island"),
        ]
        for tag_params in filter_list:
            for element in content.find_all(**tag_params):
                element.extract()

        unwrap_tags = ["figure", "figcaption", "form", "span", "a"]
        for tag in unwrap_tags:
            for element in content.find_all(tag):
                element.unwrap()

        for element in content.descendants:
            if element.name:
                element.attrs = {}

        text_maker = HTML2Text(bodywidth=80)
        text_maker.ignore_links = True
        markdown = text_maker.handle(str(content))
        markdown = re.sub("\n[ \t]+", "\n", markdown)
        markdown = re.sub("\n{2,}", "\n\n", markdown)

        i = markdown.find("Explore more on these topics")
        if i > 0:
            markdown = markdown[:i].strip()

        snippet = re.sub("\n+", " ", markdown)[:160].strip()
        logger.debug(f"Extracted content: {snippet}...")
        return markdown, title.text.strip()

    async def process(self, task: WorkerTask):
        url = str(task.url)
        logger.debug(f"{url} - Processing...")

        s = await self.get_url_soup(url)
        if s is None:
            yield CrawlerPostponeSession()
            return
        (soup, url) = s
        await asyncio.sleep(5)

        platform_tag = await self.get_platform_tag(DOMAIN, soup, 3600)

        logger.debug("Adding new links...")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_local_url = BasePlugin.get_local_url(href, url)
            if full_local_url:
                full_local_url = canonicalize_url(full_local_url)
                # logger.info(full_local_url)
                yield CrawlerBackTask(url=full_local_url)

        if self.is_article(url):
            e = self.extract(soup)
            if e:
                body, title = e
                logger.info(f"the guardian {title=}")
                # storage_id = self.ctx.storage.gen_id(url)
                # logger.info(f"putting article into {storage_id=}")

                # await self.ctx.storage.put(
                #     storage_id,
                #     BasePlugin.get_text_storage_content(content),
                # )
                yield CrawlerContent(
                    platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                    platform_tag_keepout=platform_tag.is_keepout() if platform_tag is not None else False,
                    type=DatapoolContentType.Text,
                    # storage_id=storage_id,
                    url=url,
                    content=BasePlugin.get_text_storage_content(body),
                    metadata=CrawledContentMetadata(title=title),
                )
