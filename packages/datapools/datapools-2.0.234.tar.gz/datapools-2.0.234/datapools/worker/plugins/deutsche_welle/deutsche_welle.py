import re
from urllib.parse import urlparse, urlunparse
from typing import Optional


from bs4 import BeautifulSoup, Comment
from html2text import HTML2Text

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerBackTask, CrawlerContent, DatapoolContentType, CrawlerPostponeSession
from ...utils import canonicalize_url
from ..base_plugin import BasePlugin, BaseTag

DOMAIN = "www.dw.com"


class DeutscheWellePlugin(BasePlugin):

    base_url = f"https://{DOMAIN}/en/"

    def __init__(self, ctx):
        super().__init__(ctx)

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        # logger.info( f'dw.is_supported {url=} {u.netloc=} {DOMAIN=}')
        return u.netloc == DOMAIN

    def is_article(self, url):
        path = urlparse(url).path
        pattern = r"^/en/.+/a-\d+/$"
        return bool(re.match(pattern, path))

    def normalize(self, url):
        parts = list(urlparse(url))
        parts[5] = ""  # remove fragment
        clean_url = urlunparse(parts)
        return clean_url

    def extract(self, soup):
        content = soup.find("article")
        if not content:
            logger.debug("No <article>. Skipped.")
            return None

        # remove ads
        for element in content.find_all("div"):
            for v in element.attrs.values():
                if "advertisement" in v:
                    element.extract()
                    break
            if element.attrs.get("data-tracking-name", "") == "content-detail-kicker":
                element.extract()

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

        snippet = re.sub("\n+", " ", markdown)[:160].strip()
        logger.info(f"Extracted content: {snippet}...")
        return markdown

    async def process(self, task):
        url = task.url
        logger.info(f"{url} - Processing...")

        s = await self.get_url_soup(url)
        if not s:
            yield CrawlerPostponeSession()
            return
        (soup, url) = s

        platform_tag = await self.get_platform_tag(DOMAIN, soup, 3600)

        logger.debug("Adding new links...")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # next_url = urljoin(url, href)
            # next_url = self.normalize(next_url)

            full_local_url = BasePlugin.get_local_url(href, url)
            if full_local_url:
                full_local_url = canonicalize_url(full_local_url)
                logger.info(full_local_url)
                yield CrawlerBackTask(url=full_local_url)

        if self.is_article(url):
            content = self.extract(soup)
            if content:
                # storage_id = self.ctx.storage.gen_id(url)
                # logger.info(f"putting article into {storage_id=}")

                # await self.ctx.storage.put(
                #     storage_id,
                #     BasePlugin.get_text_storage_content(content),
                # )
                yield CrawlerContent(
                    platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                    platform_keepout=platform_tag.is_keepout() if platform_tag is not None else None,
                    type=DatapoolContentType.Text,
                    # storage_id=storage_id,
                    url=url,
                    content=BasePlugin.get_text_storage_content(content),
                )
            else:
                logger.info("NO CONTENT")
