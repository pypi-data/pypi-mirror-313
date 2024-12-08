from typing import Optional, Tuple, List

from playwright.async_api import Page

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import (
    CrawlerContent,
    CrawlerDemoUser,
    DatapoolContentType,
    StudyUrlTask,
    CrawlerBackTask,
    CrawledContentMetadata,
)
from ..base_plugin import BasePlugin, BaseTag, CachedPairs, browser
from ...worker import WorkerTask


class WikipediaPlugin(BasePlugin):
    users = CachedPairs()
    history_page: Page
    user_page: Page
    demo_tag: Optional[BaseTag]

    def __init__(self, ctx, demo_tag=None):
        super().__init__(ctx)
        self.demo_tag = BaseTag(demo_tag) if demo_tag is not None else None

    @staticmethod
    def is_supported(url):
        return False  # disabled in favour of WikipediaSoupPlugin
        u = BasePlugin.parse_url(url)
        return BasePlugin.is_same_or_subdomain(u.netloc, "en.wikipedia.org")

    async def study(self, task: StudyUrlTask, __timeout: int = 3000) -> List[BaseTag]:
        if self.demo_tag is not None:
            return [self.demo_tag]
        return await super().study(task)

    async def process(self, task: WorkerTask):
        logger.info(f"wikipedia::process({task.url})")

        async with browser.blank() as history_cm:
            self.history_page = history_cm.page
            async with browser.blank() as user_cm:
                self.user_page = user_cm.page

                logger.info(f"loading url {task.url}")
                async with browser.open(task.url) as cm:
                    page = cm.page

                    p = BasePlugin.parse_url(task.url)

                    if self.demo_tag is None:
                        platform_tag = await self.get_platform_tag(p.netloc, page, 3600)
                    else:
                        platform_tag = self.demo_tag

                    # article header and body
                    headers = page.locator("h1#firstHeading")
                    header = headers.nth(0)
                    header_text = await header.inner_text()

                    bodys = page.locator("#mw-content-text")
                    body = bodys.nth(0)
                    body_text = await body.inner_text()

                    # locate "History" link
                    history_url_loc = await page.locator("#ca-history a").all()
                    if len(history_url_loc) > 0:
                        history_url = await history_url_loc[0].get_attribute("href")
                        history_url = BasePlugin.get_local_url(history_url, task.url)
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

                            logger.info(f"getting metadata")
                            metadata = await self._get_content_metadata(page)

                            logger.info(f"yielding content {task.url}")
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
                    logger.info(f"parsing links")
                    async for yielded in self.parse_links(page):
                        if isinstance(yielded, CrawlerBackTask) and self.is_page_with_content(yielded.url):
                            logger.debug(f"yielding {yielded.url}")
                            yield yielded
                        else:
                            logger.debug(f"no content: {yielded.url}")
                    logger.info(f"processed {task.url}")

    async def _get_content_metadata(self, page: Page) -> Optional[CrawledContentMetadata]:
        h1_span = await page.locator(".mw-page-title-main").all()
        if h1_span:
            title = await h1_span[0].inner_text()
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

        logger.info(f"loading url {history_url}")
        await self.history_page.goto(history_url)

        author_link = self.history_page.locator(".mw-userlink").last
        if await author_link.count() > 0:
            logger.info(f"got creator link {author_link=}")
            title = await author_link.get_attribute("title")
            if title and title[0:5] == "User:":
                username = title[5:]  # title structure is "User:$username"
                logger.info(f"got {username=}")

                if not self.users.contains(username, 36000):
                    logger.info("username not cached")
                    if self.demo_tag is None:
                        href = await author_link.get_attribute("href")
                        user_url = BasePlugin.get_local_url(href, history_url)
                        tag = await self._parse_user_page(user_url)
                    else:
                        short_tag_id = BasePlugin.gen_demo_tag(username)
                        tag = BaseTag(short_tag_id)
                    self.users.set(username, tag)
                return (self.users.get(username), username)
        return (None, None)

    # TODO: will be needed when shared ownership is implemented
    # async def _collect_users(self, history_url):
    #     """Collects users from article history page.
    #     Behavior depends on is_demo_mode flag.
    #     In demo mode all users are returned, in non demo mode only users with tag are returned
    #     TODO: not tested
    #     """
    #     res: Dict[str, Optional[str]] = {}  # username => tag
    #     history_url += "&limit=1000"
    #     while True:
    #         logger.info(f"loading url {history_url}")
    #         await self.history_page.goto(history_url)

    #         author_links = await self.history_page.locator(".mw-userlink").all()
    #         if len(author_links) == 0:
    #             break

    #         for link in author_links:
    #             title = await link.get_attribute("title")
    #             username = title[5:]  # title structure is "User:$username"
    #             if not username in self.users:
    #                 href = await link.get_attribute("href")
    #                 user_url = BasePlugin.get_local_url(href, history_url)
    #                 self.users[username] = await self._parse_user_page(user_url)

    #             if self.is_demo_mode or self.users[username] is not None:
    #                 res[username] = self.users[username]

    #         # link to the next batch of users
    #         next_link = await self.history_page.locator(".mw-nextlink").all()
    #         if len(next_link) == 0:
    #             break
    #         href = await next_link.get_attribute("href")
    #         history_url = BasePlugin.get_local_url(href, history_url)
    #     return res

    async def _parse_user_page(self, user_link) -> Optional[BaseTag]:
        """user_link is something like https://en.wikipedia.org/wiki/User:FrB.TG.
        Expecting tag in the text representation of the page."""
        logger.info(f"parsing user page {user_link}")
        await self.user_page.goto(user_link)
        return await BasePlugin.parse_tag_in(self.user_page, "#mw-content-text")
