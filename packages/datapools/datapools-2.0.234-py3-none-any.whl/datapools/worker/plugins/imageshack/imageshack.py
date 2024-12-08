import asyncio

# import traceback
from typing import Tuple, Optional

from bs4 import BeautifulSoup
from playwright.async_api import TimeoutError as PlaywriteTimeoutError
from playwright.async_api import Page

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.http import download
from ....common.types import (
    CrawlerBackTask,
    CrawlerContent,
    CrawlerDemoUser,
    DatapoolContentType,
    CrawledContentMetadata,
)
from ...utils import canonicalize_url
from ..base_plugin import BasePlugin, BaseTag, browser
from ...worker import WorkerTask

# from typing import List

DOMAIN = "imageshack.com"


class ImageshackPlugin(BasePlugin):
    demo_tag: BaseTag
    want_demo_users: bool

    def __init__(self, ctx, demo_tag=None, want_demo_users: bool = False):
        super().__init__(ctx)
        self.demo_tag = BaseTag(demo_tag)
        self.want_demo_users = want_demo_users

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        # logger.info( f'imageshack {u=}')
        return u.netloc == DOMAIN

    async def process(self, task: WorkerTask):
        if self.ctx.session is None:
            raise Exception("invalid usage")

        logger.info(f"imageshack::process({task.url})")

        async with browser.open(task.url) as cm:
            page = cm.page

            if not self.demo_tag.is_valid():
                platform_tag = await self.get_platform_tag(DOMAIN, page, 3600)
            else:
                platform_tag = self.demo_tag

            session_meta = await self.ctx.session.get_meta()

            n_images = 0
            n_hrefs = 0
            expect_changes = True
            while expect_changes:
                expect_changes = False

                # 1.search for photo LINKS and return them as new tasks
                hrefs = await page.locator("a.photo, a.hero-wrapper").all()
                new_n_hrefs = len(hrefs)
                if new_n_hrefs != n_hrefs:
                    expect_changes = True

                while n_hrefs < new_n_hrefs:
                    try:
                        href = await hrefs[n_hrefs].get_attribute("href", timeout=100)
                        n_hrefs += 1

                        full_local_url = BasePlugin.get_local_url(href, session_meta["url"])
                        if full_local_url:
                            # strict constraint on urls, else may get endless recursions etc
                            full_local_url = canonicalize_url(full_local_url)
                            logger.debug(f"adding task: {full_local_url}")

                            yield CrawlerBackTask(url=full_local_url)
                        else:
                            logger.debug(f'non local: {href=} {session_meta["url"]=}')

                    except PlaywriteTimeoutError:
                        # element may be not ready yet, no problems, will get it on the next iteration
                        # logger.debug( 'get_attribute timeout' )
                        expect_changes = True
                        break

                # 2. search for single photo IMAGE
                images = await page.locator("img#lp-image").all()
                new_n_images = len(images)
                if new_n_images > n_images:
                    expect_changes = True

                while n_images < new_n_images:
                    try:
                        src = await images[n_images].get_attribute("src", timeout=100)
                        n_images += 1

                        logger.debug(f"{src=}")
                        if src is None:
                            logger.debug("--------------------------------------")
                            outerHTML = await images[n_images - 1].evaluate("el => el.outerHTML")
                            logger.debug(f"{outerHTML=}")
                            continue

                        full_local_url = BasePlugin.get_local_url(src, session_meta["url"])
                        logger.debug(full_local_url)

                        copyright_owner_tag = None

                        # check for user license on his public profile page
                        profile_link = await page.locator("a.profile-link").all()
                        if len(profile_link):
                            href = await profile_link[0].get_attribute("href")
                            if href is not None:
                                # strict constraint on urls, else may get endless recursions etc
                                full_profile_url = canonicalize_url(BasePlugin.get_local_url(href, session_meta["url"]))
                                logger.debug(f"adding task: {full_profile_url}")

                                yield CrawlerBackTask(url=full_profile_url)

                                (copyright_owner_tag, logo_url) = await self.parse_user_profile(href)
                                if not copyright_owner_tag and self.want_demo_users is True:
                                    # demo functionality for royalties spreadout demo
                                    user_name = href.split("/")[-1]
                                    short_tag_id = BasePlugin.gen_demo_tag(user_name)
                                    logger.debug(f'demo for "{user_name}" is {short_tag_id=}')
                                    copyright_owner_tag = BaseTag(short_tag_id)
                                    yield CrawlerDemoUser(
                                        user_name=user_name,
                                        short_tag_id=short_tag_id,
                                        platform="imageshack.com",
                                        logo_url=logo_url,
                                    )

                        if copyright_owner_tag is not None:
                            logger.debug(f"found {copyright_owner_tag=}")

                        metadata = await self._get_content_metadata(page)

                        if platform_tag or copyright_owner_tag:
                            yield CrawlerContent(
                                copyright_tag_id=(
                                    str(copyright_owner_tag) if copyright_owner_tag is not None else None
                                ),
                                copyright_tag_keepout=(
                                    copyright_owner_tag.is_keepout() if copyright_owner_tag is not None else False
                                ),
                                platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                                platform_tag_keepout=(platform_tag.is_keepout() if platform_tag is not None else False),
                                type=DatapoolContentType.Image,
                                priority_timestamp=await BasePlugin.parse_html_time_tag(page, ".user-area time"),
                                url=full_local_url,
                                metadata=metadata,
                            )

                    except PlaywriteTimeoutError:
                        # element may be not ready yet, no problems, will get it on the next iteration
                        # logger.debug( 'get_attribute timeout' )
                        expect_changes = True
                        break

                scroll_height1 = await page.evaluate("document.body.scrollHeight")
                await page.mouse.wheel(0, browser.viewport_height * 0.8)
                scroll_height2 = await page.evaluate("document.body.scrollHeight")
                logger.debug(f"*********** {scroll_height1=} {scroll_height2=} ****************")
                if scroll_height1 != scroll_height2:
                    expect_changes = True

                await asyncio.sleep(1)

    async def _get_content_metadata(self, page: Page) -> Optional[CrawledContentMetadata]:
        h1 = await page.locator(".image-info h1").all()
        if h1:
            logger.debug("got h1")
            title = await h1[0].inner_text()
            if title:
                logger.debug(f"got h1 {title=}")
                return CrawledContentMetadata(title=title)
        return None

    async def parse_user_profile(self, href) -> Tuple[Optional[BaseTag], Optional[str]]:
        username = href.split("/")[-1]
        if not self.copyright_tags_cache.contains(username, 3600):
            url = f"https://{DOMAIN}/{href}"

            logger.debug(f"parsing user profile {url=}")

            r = await download(url)
            # logger.debug( f'text: {r}')
            logger.debug(f"got url content length={len(r) if r else 0}")

            soup = BeautifulSoup(r, "html.parser")
            tag: Optional[BaseTag] = None
            logo_url: Optional[str] = None

            about = soup.body.find("div", attrs={"class": "bio tall"})
            if about:
                tag = BasePlugin.parse_tag_in_str(about.contents[0])

            logger.debug(f"user profile {tag=}")

            logo_div = soup.body.find("div", attrs={"class": "avatar"})
            if logo_div:
                logo_img = logo_div.find("img")
                if logo_img:
                    logo_url = BasePlugin.get_local_url(logo_img.get("src"), f"https://{DOMAIN}")
            self.copyright_tags_cache.set(username, (tag, logo_url))
        return self.copyright_tags_cache.get(username)
