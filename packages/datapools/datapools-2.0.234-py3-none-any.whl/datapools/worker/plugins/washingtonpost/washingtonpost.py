import re
from urllib.parse import urlparse, urlunparse
from typing import Dict, Any

from bs4 import BeautifulSoup, Comment
from html2text import HTML2Text

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerBackTask, CrawlerContent, CrawlerDemoUser, DatapoolContentType
from ....common.http import download
from ...utils import canonicalize_url
from ..base_plugin import BasePlugin, BaseTag, CachedPairs
from ...worker import WorkerTask

DOMAIN = "www.washingtonpost.com"


class WashingtonPostPlugin(BasePlugin):

    base_url = f"https://{DOMAIN}/"
    authors = CachedPairs()

    def __init__(self, ctx, demo_mode: bool = False):
        super().__init__(ctx)
        self.demo_mode = demo_mode

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        if u.netloc != DOMAIN:
            logger.debug(f"Validation failed - Out of domain: {url}")
            return False
        if re.match("^/subscribe/.*$", u.path):  # these pages timeout
            logger.debug(f"Validation failed - Subscription page: {url}")
            return False
        if re.match("^/people/.*$", u.path):  # there are just too many of them
            logger.debug(f"Validation failed - People page: {url}")
            return False
        return True

    def is_article(self, url):
        path = urlparse(url).path
        pattern = r"^[\w\-/]{3,}/\d+/\d+/\d+/[\w-]+/$"
        return bool(re.match(pattern, path))

    def normalize(self, url):
        parts = list(urlparse(url))
        parts[5] = ""  # remove fragment
        clean_url = urlunparse(parts)
        return clean_url

    def extract(self, soup):
        content = soup.find("article")
        if not content:
            logger.debug("No <article>, trying <main>...")
            content = soup.find("main", attrs={"data-qa": "article-body", "id": "article-body"})
        if not content:
            logger.debug("No <main> either. Skipped.")
            return None

        filter_list = [
            dict(string=lambda s: isinstance(s, Comment)),
            dict(name="img"),
            dict(name="svg"),
            dict(name="button"),
            dict(name="div", string="Advertisement"),
            dict(name="div", attrs={"aria-roledescription": "carousel"}),
            dict(name="div", string="End of carousel"),
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
        logger.debug(f"Extracted content: {snippet}...")
        return markdown

    async def process(self, task: WorkerTask):
        url = str(task.url)
        logger.info(f"{url} - Processing... ")

        meta: Dict[str, Any] = {}
        content = await download(url, output_meta=meta)
        if meta["url"] != url:
            logger.debug(f"{url} - Redirect to {meta['url']}")
            url = meta["url"]

        soup = BeautifulSoup(content, "html.parser")

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
            (author_tag, user_name) = self._get_author_tag(soup, url)

            if author_tag is not None or platform_tag is not None:
                if self.demo_mode and user_name and author_tag and author_tag.is_valid():
                    yield CrawlerDemoUser(
                        user_name=user_name, short_tag_id=str(author_tag), platform="washingtonpost.com"
                    )

                content = self.extract(soup)
                if content:
                    # storage_id = self.ctx.storage.gen_id(url)
                    # logger.info(f"putting article into {storage_id=}")

                    # await self.ctx.storage.put(
                    #     storage_id,
                    #     BasePlugin.get_text_storage_content(content),
                    # )
                    yield CrawlerContent(
                        tag_id=str(author_tag) if author_tag is not None else None,
                        tag_keepout=author_tag.is_keepout() if author_tag is not None else False,
                        platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                        platform_tag_keepout=platform_tag.is_keepout() if platform_tag is not None else False,
                        type=DatapoolContentType.Text,
                        # storage_id=storage_id,
                        url=url,
                        content=BasePlugin.get_text_storage_content(content),
                    )

    def _get_author_tag(self, soup, url):
        author_link = soup.find_all("a", attrs={"data-qa": "author-name"}, href=True)
        if len(author_link) > 0:
            logger.debug(f"Author link {author_link} {author_link[0].text}")
            user_name = author_link[0].text
            logger.debug(f"Author name {user_name}")
            if not self.authors.contains(user_name, 3600):
                # full_author_url = BasePlugin.get_local_url(author_link[0]["href"], url)
                # logger.debug(f"{full_author_url=}")
                # response = requests.get(full_author_url)
                # soup2 = BeautifulSoup(response.content, "html.parser")

                if self.demo_mode:
                    short_tag_id = BasePlugin.gen_demo_tag(user_name)
                    tag = BaseTag(short_tag_id)
                else:
                    tag = BasePlugin.parse_tag_in(soup)
                self.authors.set(user_name, tag)
            else:
                tag = self.authors.get(user_name)
            return (tag, user_name)
        return (None, None)
