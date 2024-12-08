import asyncio
import re

from playwright.async_api import TimeoutError as PlaywriteTimeoutError, expect, Page

from ....common.logger import logger
from ....common.types import StudyUrlTask
from typing import List

# from ....common.storage import BaseStorage
from ....common.types import CrawlerBackTask, CrawlerContent, CrawlerNop, DatapoolContentType
from ..base_plugin import BasePlugin, BaseTag, browser
from ...worker import WorkerTask

# import traceback


class DataPhoenixInfoPlugin(BasePlugin):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.header_tag_id = None

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        # logger.debug( f'dataphoenix.info {u=}')
        return u.netloc == "dataphoenix.info"

    async def study(self, task: StudyUrlTask, timeout: int = 10000) -> List[BaseTag]:
        return await super().study(task, timeout=timeout)

    async def process(self, task: WorkerTask):
        logger.debug(f"dataphoenix_info::process({task.url})")

        logger.debug(f"loading url {task.url}")
        async with browser.open(task.url) as cm:
            page = cm.page
            
            await page.goto(str(task.url))  # "https://dataphoenix.info/news/"

            # check if <meta/> tag exists with our tag
            self.header_tag_id = await BasePlugin.parse_meta_tag(page, "robots")
            logger.debug(f"{self.header_tag_id=}")

            if not self.header_tag_id:
                logger.debug("No <meta> tag found")
                return

            if re.match(
                r"^http(s?)://dataphoenix.info/(news|papers|articles|videos)(?:$|/)",
                str(task.url),  # linter..
            ):
                logger.debug("parsing feed")
                async for yielded in self._process_feed(page):
                    yield yielded
            else:
                logger.debug("parsing single page")
                async for yielded in self._process_single_page(page, task.url):
                    yield yielded

    async def _process_single_page(self, page: Page, url: str):
        await self._try_remove_banner(page)

        # article consists of header, excerpt and body
        # TODO: support video
        ps = await page.locator("h1.gh-post-page__title").all()
        if len(ps) == 0:
            logger.error("Not parsable page (header)")
            # await page.screenshot(
            #     path="/app/tmp/not_parsable_page_header.png"
            # )
            return
        header = await ps[0].inner_text()

        # optional Excerpt
        ps = await page.locator("p.gh-post-page__excerpt").all()
        excerpt = await ps[0].inner_text() + "\n"

        body = ""
        ps = await page.locator("div.gh-post-page__content > p").all()
        for p in ps:
            body += await p.inner_text() + "\n"

        # storage_id = self.ctx.storage.gen_id(url)
        # logger.debug(f"putting article into {storage_id=}")

        # await self.ctx.storage.put(storage_id, BasePlugin.get_text_storage_content(body, header=header, excerpt=excerpt))

        priority_timestamp = await BasePlugin.parse_html_time_tag(page, ".gh-post-info__date")
        logger.debug(f"{priority_timestamp=}")

        yield CrawlerContent(
            tag_id=str(self.header_tag_id),
            tag_keepout=self.header_tag_id.is_keepout(),
            type=DatapoolContentType.Text,
            priority_timestamp=priority_timestamp,
            # storage_id=storage_id,
            url=url,
            content=BasePlugin.get_text_storage_content(body, header=header, excerpt=excerpt),
        )

    async def _process_feed(self, page: Page):
        total_news = 0
        while True:

            urls = await page.locator("a.gh-archive-page-post-title-link").all()
            n = len(urls)
            logger.debug(f"items on page {n=}, yielding from {total_news}")
            for i in range(total_news, n):
                href = await urls[i].get_attribute("href")
                if href is not None:
                    logger.debug(f"yielding {href=}")
                    yield CrawlerBackTask(url="https://dataphoenix.info" + href)

            total_news = n

            # logger.debug( 'creating button locator')
            button = page.locator("a.gh-load-more-button")

            # logger.debug( 'getting disabled attr')
            visible = await button.is_visible()

            logger.debug(f"button {visible=}")
            if not visible:
                break

            # ready = False
            # for i in range(0, 2):
            #     try:
            #         logger.debug(f"waiting until button is ready for clicks ({i})")
            #         await button.click(trial=True, timeout=10000)
            #         logger.debug("button is ready for clicks")
            #         ready = True
            #         break
            #     except PlaywriteTimeoutError:
            #         # logger.debug( e )
            #         # logger.debug( traceback.format_exc() )
            await self._try_remove_banner(page)

            # if not ready:
            #     logger.error("ready wait failed error")
            #     # await page.screenshot(path="/app/tmp/screenshot.png")
            #     break

            try:
                await button.click(no_wait_after=True, timeout=10000)
                # logger.debug( "clicked More Posts")
            except PlaywriteTimeoutError:
                logger.error("click More Posts timeout")
                # await page.screenshot(path="/app/tmp/screenshot.png")
                break

            # for i in range(0, 10):
            #     html = await button.evaluate("el => el.outerHTML")
            #     logger.debug(html)
            #     await asyncio.sleep(0.2)

            # button = page.locator("button.js-load-posts.c-btn--loading")
            # await button.wait_for()
            # logger.debug("button changed to Loading")

            # button = page.locator("button.js-load-posts:not(.c-btn--loading)")
            # await button.wait_for()
            # logger.debug("button changed back to More Posts")

            await asyncio.sleep(2)

        yield CrawlerNop()

    async def _try_remove_banner(self, page: Page):
        close_button = await page.locator("span.sp-popup-close").all()
        if len(close_button) == 0:
            return False

        logger.debug("Modal found, clicking modal close button")

        await close_button[0].click(no_wait_after=True)
        logger.debug("waiting modal to dissapear")
        await expect(close_button[0]).to_have_count(0)
        logger.debug("modal dissapeared")
        return True
