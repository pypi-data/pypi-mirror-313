import time
from bs4 import BeautifulSoup
from typing import Optional, Tuple, List
from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import (
    CrawlerContent,
    CrawlerDemoUser,
    DatapoolContentType,
    StudyUrlTask,
    CrawlerBackTask,
    CrawledContentMetadata,
    CrawlerPostponeSession,
)
from ..base_plugin import BasePlugin, BaseTag, CachedPairs, browser
from ...utils import canonicalize_url
from ...worker import WorkerTask


class WikipediaSoupPlugin(BasePlugin):
    users = CachedPairs()
    demo_tag: Optional[BaseTag]

    def __init__(self, ctx, demo_tag=None):
        super().__init__(ctx)
        self.demo_tag = BaseTag(demo_tag) if demo_tag is not None else None

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        return BasePlugin.is_same_or_subdomain(u.netloc, "en.wikipedia.org")

    async def study(self, task: StudyUrlTask, __timeout: int = 3000) -> List[BaseTag]:
        if self.demo_tag is not None:
            return [self.demo_tag]
        return await super().study(task)

    async def process(self, task: WorkerTask):
        logger.info(f"WikipediaSoup::process({task.url})")

        s = await self.get_url_soup(task.url)
        if not s:
            # yield CrawlerPostponeSession()
            return
        (soup, url) = s

        # logger.debug("Adding new links...")
        # for link in soup.find_all("a", href=True):
        #     href = link["href"]
        #     # next_url = urljoin(url, href)
        #     # next_url = self.normalize(next_url)

        #     full_local_url = BasePlugin.get_local_url(href, url)
        #     if full_local_url:
        #         full_local_url = canonicalize_url(full_local_url)
        #         # logger.info(full_local_url)
        #         yield CrawlerBackTask(url=full_local_url)

        p = BasePlugin.parse_url(task.url)

        if self.demo_tag is None:
            platform_tag = await self.get_platform_tag(p.netloc, soup, 3600)
        else:
            platform_tag = self.demo_tag

        # article header and body
        header_text = soup.find(id="firstHeading").text
        body_text = soup.find(id="mw-content-text").text

        # logger.info(f"{header_text=}")
        # logger.info(f"{body_text=}")

        # locate "History" link
        ca_history = soup.find(id="ca-history")
        if ca_history:
            history_url_loc = ca_history.find("a")
            if history_url_loc:
                history_url = history_url_loc.get_attribute_list("href")[0]
                history_url = BasePlugin.get_local_url(history_url, url)
                # TODO: shared ownership to be implemented later
                #       for now use the creator of the article as the copyright owner.
                #       Commented code below is more or less valid
                # users = await self._collect_users(history_url)
                # if len(users) > 0:
                #     storage_id = self.ctx.storage.gen_id(task.url)
                #     logger.info(f"putting article into {storage_id=}")

                #     await self.ctx.storage.put(
                #         storage_id,
                #         json.dumps(
                #             {"body": body_text, "users": users}
                #         ),  # TODO: structure
                #     )

                # TODO: until shared ownership is not supported, we use creator of the article as the copyright owner
                (creator_tag, user_name) = await self._get_article_creator(history_url)
                if creator_tag or platform_tag:
                    # storage_id = self.ctx.storage.gen_id(task.url)
                    # logger.info(f"putting article into {storage_id=}")

                    # await self.ctx.storage.put(storage_id, BasePlugin.get_text_storage_content(body_text))

                    if self.demo_tag and user_name and creator_tag and creator_tag.is_valid():
                        logger.info(f"yielding demo user {str(creator_tag)}")
                        yield CrawlerDemoUser(
                            user_name=user_name, short_tag_id=str(creator_tag), platform="wikipedia.org"
                        )

                    logger.debug(f"getting metadata")
                    metadata = self._get_content_metadata(soup)

                    logger.debug(f"yielding content {task.url}")
                    yield CrawlerContent(
                        platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                        platform_tag_keepout=platform_tag.is_keepout() if platform_tag is not None else False,
                        tag_id=str(creator_tag) if creator_tag is not None else None,
                        tag_keepout=creator_tag.is_keepout() if creator_tag is not None else False,
                        type=DatapoolContentType.Text,
                        # storage_id=storage_id,
                        url=task.url,
                        content=BasePlugin.get_text_storage_content(body_text, header_text),
                        metadata=metadata,
                    )

        # parsing links as back tasks
        logger.debug(f"parsing links")
        async for yielded in self.parse_links(soup, url):
            if isinstance(yielded, CrawlerBackTask) and self.is_page_with_content(yielded.url):
                logger.debug(f"yielding {yielded.url}")
                yield yielded
            else:
                logger.debug(f"no content: {yielded.url}")
        logger.debug(f"processed {task.url}")

    def _get_content_metadata(self, soup: BeautifulSoup) -> Optional[CrawledContentMetadata]:
        h1_span = soup.select(".mw-page-title-main")
        if h1_span:
            title = h1_span[0].text
            if title:
                return CrawledContentMetadata(title=title)
        return None

    @staticmethod
    def is_page_with_content(url: str):
        def has_sub(sub):
            try:
                url.index(sub)
                return True
            except ValueError:
                return False

        return has_sub("/wiki") and not any(
            has_sub(sub) for sub in ["/wiki/Special:", "/wiki/Wikipedia:", "/wiki/File:", "/w/"]
        )

    async def _get_article_creator(self, history_url) -> Tuple[Optional[BaseTag], Optional[str]]:
        """
        get the earliest user from the history list.
        """
        history_url += "&dir=prev"

        logger.debug(f"loading url {history_url}")
        s = await self.get_url_soup(history_url)
        if not s:
            return None, None
        (soup, __u) = s

        author_link = soup.select(".mw-userlink")
        if len(author_link) > 0:
            author_link = author_link[-1]

            logger.debug(f"got creator link {author_link=}")
            title = author_link.get_attribute_list("title")
            if title and title[0]:
                title = title[0]
                if title[0:5] == "User:":
                    username = title[5:]  # title structure is "User:$username"
                    logger.debug(f"got {username=}")

                    if not self.users.contains(username, 36000):
                        logger.debug("username not cached")
                        tag = None
                        if self.demo_tag is None:
                            href = author_link.get_attribute_list("href")
                            if href and href[0]:
                                href = href[0]
                                user_url = BasePlugin.get_local_url(href, history_url)
                                tag = await self._parse_user_page(user_url)
                        else:
                            short_tag_id = BasePlugin.gen_demo_tag(username)
                            tag = BaseTag(short_tag_id)
                        if tag:
                            self.users.set(username, tag)
                    if self.users.contains(username, 36000):
                        return (self.users.get(username), username)
        return (None, None)

    async def _parse_user_page(self, user_link) -> Optional[BaseTag]:
        """user_link is something like https://en.wikipedia.org/wiki/User:FrB.TG.
        Expecting tag in the text representation of the page."""
        logger.debug(f"parsing user page {user_link}")
        s = await self.get_url_soup(user_link)
        if s:
            (soup, __u) = s
            content = soup.find(id="mw-content-text")
            if content:
                return await BasePlugin.parse_tag_in(content.text)
        return None
