import asyncio
from typing import Optional, List

# import traceback

# import time
from playwright.async_api import TimeoutError as PlaywriteTimeoutError, Page, Locator

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerBackTask, DatapoolContentType, WorkerTask, StudyUrlTask, CrawlerContent
from ...utils import canonicalize_url
from ..base_plugin import BasePlugin, BaseTag, browser
from ...worker import WorkerTask


class DefaultPlugin(BasePlugin):
    # def __init__(self, ctx):
    #     super().__init__(ctx)

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        return u.scheme in ("https", "http")

    async def study(self, task: StudyUrlTask, timeout: int = 10000) -> List[BaseTag]:
        async with browser.open(task.url, timeout=timeout) as cm:
            logger.info(f"DefaultPlugin::study {cm.page.url=}")

            real_url = cm.page.url
            if not self.get_local_url(real_url, task.url):
                logger.debug("redirected to different domain")
                return []

            url = real_url

            tags = []

            p = BasePlugin.parse_url(url)
            platform_tag = await self.get_platform_tag(p.netloc, cm.page, 3600)
            if platform_tag:
                tags.append(platform_tag)

            # search for <article>'s with tags
            articles = await cm.page.locator("article").all()
            for article in articles:
                article_body = await article.inner_text()

                author_tag = BasePlugin.parse_tag_in_str(article_body)
                logger.debug(f"{author_tag=}")
                if author_tag is not None:
                    tags.append(author_tag)

            return tags

    async def process(self, task: WorkerTask):
        if self.ctx.session is None:
            raise Exception("invalid usage")

        logger.debug(f"DefaultPlugin::process({task.url})")

        # if task.content_type in (DatapoolContentType.Image, DatapoolContentType.Video, DatapoolContentType.Audio):
        #     # simply let worker to download and process content
        #     yield CrawlerContent(
        #         type=task.content_type,
        #         # storage_id=storage_id,
        #         url=task.url,
        #     )
        #     return
        try:
            async with browser.open(task.url) as cm:
                page = cm.page

                self.ctx.real_task_url = page.url
                if not self.get_local_url(page.url, task.url):
                    logger.info(f"redirected to different domain {task.url} => {page.url}")
                    return

                url = page.url

                p = BasePlugin.parse_url(url)
                platform_tag = await self.get_platform_tag(p.netloc, page, 3600)

                bodys = page.locator("body")
                body = bodys.nth(0)
                body_text = ""
                n_images = 0
                n_videos = 0
                n_audios = 0
                n_articles = 0
                n_hrefs = 0
                expect_changes = True
                while expect_changes:
                    expect_changes = False

                    # 1. detecting changes on the page
                    new_text = await body.inner_text()

                    # a. new body contains old body plus more text => replace old with new
                    old_text = body_text

                    if body_text in new_text:
                        body_text = new_text
                        # b. new body head intersects old body tail => merge them
                        # body  =12345678
                        # new   =     67890
                        # result=1234567890
                    else:
                        body_text = BasePlugin.merge_head_tail(body_text, new_text)
                    if old_text != body_text:
                        logger.debug("expect changes by BODY")
                        expect_changes = True

                    # 1. searching for <article>
                    articles = await page.locator("article").all()
                    new_n_articles = len(articles)
                    if new_n_articles != n_articles:
                        logger.debug("expect changes by ARTICLES COUNT")
                        expect_changes = True
                    while n_articles < new_n_articles:
                        article = articles[n_articles]

                        article_body = await article.inner_text()
                        # article_body += " https://openlicense.ai/t/22a"

                        author_tag = BasePlugin.parse_tag_in_str(article_body)
                        if author_tag is not None:
                            # do not trust timestamps by default
                            # priority_timestamp = await BasePlugin.parse_html_time_tag(article)
                            # logger.debug(f"{priority_timestamp=}")

                            # search for article header
                            headers = await article.locator("h1").all()
                            if len(headers) > 0:
                                header = await headers[0].inner_text()
                            else:
                                header = None

                            # yielding article as Text content
                            logger.info(f'yielding TEXT content "{header if header else len(article_body)}"')
                            yield CrawlerContent(
                                platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                                platform_tag_keepout=platform_tag.is_keepout() if platform_tag is not None else None,
                                tag_id=str(author_tag),
                                tag_keepout=author_tag.is_keepout(),
                                type=DatapoolContentType.Text,
                                content=BasePlugin.get_text_storage_content(article_body, header),
                                content_key=header,
                                url=url,
                            )

                            # search images in the article
                            images = await article.locator("img").all()
                            logger.debug(f"found {len(images)=} in article")
                            for img in images:
                                try:
                                    # TODO: is it possible that we miss image that is not ready yet?
                                    src = await img.get_attribute("src", timeout=1000)
                                    if src is None:
                                        logger.warning(f"no src in article img {img=}, skipped for now")
                                        continue
                                    full_local_url = BasePlugin.get_local_url(src, page.url)

                                    logger.info(f"yielding ARTICLE IMAGE content {full_local_url}")
                                    yield CrawlerContent(
                                        platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                                        platform_tag_keepout=(
                                            platform_tag.is_keepout() if platform_tag is not None else None
                                        ),
                                        tag_id=str(author_tag),
                                        tag_keepout=author_tag.is_keepout(),
                                        type=DatapoolContentType.Image,
                                        url=full_local_url,
                                    )
                                except PlaywriteTimeoutError:
                                    # element may be not ready yet, no problems, will get it on the next iteration
                                    # logger.info( 'get_attribute timeout' )
                                    logger.debug("expect changes by ARTICLES IMAGES EXCEPTION")
                                    expect_changes = True
                                    break

                            # TODO: <video's
                            # TODO: <audio's
                        n_articles += 1

                    # 2. all images on the page. Images which were already yielded as article content from above will be filtered by scheduler as duplicate tasks, don't bother
                    images = await page.locator("img").all()
                    new_n_images = len(images)
                    if new_n_images != n_images:
                        logger.debug("expect changes by IMAGES COUNT")
                        expect_changes = True
                    while n_images < new_n_images:
                        try:
                            # logger.info(f"{n_images=}")
                            if await self.has_href_parent(page, images[n_images]):
                                n_images += 1
                                continue

                            src = await images[n_images].get_attribute("src", timeout=100)
                            n_images += 1

                            logger.debug(f"{src=}")
                            if src is None:
                                logger.debug("--------------------------------------")
                                outerHTML = await images[n_images - 1].evaluate("el => el.outerHTML")
                                logger.debug(f"{outerHTML=}")
                                continue

                            full_local_url = BasePlugin.get_local_url(src, page.url)
                            if full_local_url:
                                # TODO: getting image from browser works somehow but
                                #   requires image type detection, quality check, crossOrigin understading etc
                                #   So for now let's do not in optimal way
                                # content = await self.download(full_local_url)
                                # getting content from browser page instead of downloading it again
                                # content = await BasePlugin.get_webpage_image_bytes(images[n_images-1])
                                # if content:
                                copyright_tag = BasePlugin.parse_tag_in_str(body_text)

                                logger.info(f"yielding IMAGE content {full_local_url}")
                                yield CrawlerContent(
                                    platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                                    platform_tag_keepout=(
                                        platform_tag.is_keepout() if platform_tag is not None else None
                                    ),
                                    copyright_tag_id=str(copyright_tag) if copyright_tag is not None else None,
                                    copyright_tag_keepout=(
                                        copyright_tag.is_keepout() if copyright_tag is not None else None
                                    ),
                                    type=DatapoolContentType.Image,
                                    # storage_id=storage_id,
                                    url=full_local_url,
                                )
                            else:
                                logger.debug(f"non local: {src=} {page.url=}")

                        except PlaywriteTimeoutError:
                            # element may be not ready yet, no problems, will get it on the next iteration
                            # logger.info( 'get_attribute timeout' )
                            logger.debug("expect changes by IMAGES EXCEPTION")
                            expect_changes = True
                            break

                    # 3. all videos on the page. Videos which were already yielded as article content from above will be filtered by scheduler as duplicate tasks, don't bother
                    videos = await page.locator("video").all()
                    new_n_videos = len(videos)
                    if new_n_videos != n_videos:
                        logger.debug("expect changes by VIDEO COUNT")
                        expect_changes = True
                    while n_videos < new_n_videos:
                        try:
                            # TODO: do we need this?
                            # if not await videos[n_videos].is_visible():
                            #     logger.info( f'video is not visible, skipped')
                            #     n_videos += 1
                            #     continue

                            if await self.has_href_parent(page, videos[n_videos]):
                                logger.debug("video has <A> parent, skipped")
                                n_videos += 1
                                continue

                            src = await videos[n_videos].get_attribute("src", timeout=100)

                            if not src:
                                source = await videos[n_videos].locator("source").all()
                                if len(source) > 0:
                                    outerHTML = await source[0].evaluate("el => el.outerHTML")
                                    logger.debug(f"source {outerHTML=}")

                                    src = await source[0].get_attribute("src", timeout=100)
                                    if not src:
                                        src = await source[0].get_attribute("data-src", timeout=100)

                                else:
                                    logger.debug("no source")

                            n_videos += 1

                            logger.debug(f"video {src=}")
                            if src is None:
                                logger.debug("--------------------------------------")
                                outerHTML = await videos[n_videos - 1].evaluate("el => el.outerHTML")
                                logger.debug(f"{outerHTML=}")
                                continue

                            # logger.info( f'video without <A>: {src}')
                            # logger.info( body_text)

                            full_local_url = BasePlugin.get_local_url(src, page.url, allow_external=True)
                            if full_local_url:
                                # TODO: getting image from browser works somehow but
                                #   requires image type detection, quality check, crossOrigin understading etc
                                #   So for now let's do not in optimal way
                                # content = await self.download(full_local_url)
                                # getting content from browser page instead of downloading it again
                                # content = await BasePlugin.get_webpage_image_bytes(images[n_images-1])
                                # if content:
                                copyright_tag = BasePlugin.parse_tag_in_str(body_text)

                                logger.info(f"yielding VIDEO content {full_local_url}")
                                yield CrawlerContent(
                                    platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                                    platform_tag_keepout=(
                                        platform_tag.is_keepout() if platform_tag is not None else None
                                    ),
                                    copyright_tag_id=str(copyright_tag) if copyright_tag is not None else None,
                                    copyright_tag_keepout=(
                                        copyright_tag.is_keepout() if copyright_tag is not None else None
                                    ),
                                    type=DatapoolContentType.Video,
                                    # storage_id=storage_id,
                                    url=full_local_url,
                                )
                            else:
                                logger.debug(f"non local: {src=} {page.url=}")

                        except PlaywriteTimeoutError:
                            # element may be not ready yet, no problems, will get it on the next iteration
                            # logger.info( 'get_attribute timeout' )
                            logger.debug("expect changes by VIDEO EXCEPTION")
                            expect_changes = True
                            break

                    # 4. all audios on the page. Audios which were already yielded as article content from above will be filtered by scheduler as duplicate tasks, don't bother
                    audios = await page.locator("audio").all()
                    new_n_audios = len(audios)
                    if new_n_audios != n_audios:
                        logger.debug("expect changes by AUDIO COUNT")
                        expect_changes = True
                    while n_audios < new_n_audios:
                        try:
                            if await self.has_href_parent(page, audios[n_audios]):
                                n_audios += 1
                                continue

                            src = await audios[n_audios].get_attribute("src", timeout=100)
                            if not src:
                                source = await audios[n_audios].locator("source").all()
                                if len(source) > 0:
                                    src = await source[0].get_attribute("src", timeout=100)
                                    if not src:
                                        src = await source[0].get_attribute("data-src", timeout=100)

                            n_audios += 1

                            logger.debug(f"audio {src=}")
                            if src is None:
                                logger.debug("--------------------------------------")
                                outerHTML = await audios[n_audios - 1].evaluate("el => el.outerHTML")
                                logger.debug(f"{outerHTML=}")
                                continue

                            full_local_url = BasePlugin.get_local_url(src, page.url, allow_external=True)
                            if full_local_url:
                                # TODO: getting image from browser works somehow but
                                #   requires image type detection, quality check, crossOrigin understading etc
                                #   So for now let's do not in optimal way
                                # content = await self.download(full_local_url)
                                # getting content from browser page instead of downloading it again
                                # content = await BasePlugin.get_webpage_image_bytes(images[n_images-1])
                                # if content:
                                copyright_tag = BasePlugin.parse_tag_in_str(body_text)

                                logger.info(f"yielding AUDIO content {full_local_url}")
                                yield CrawlerContent(
                                    platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                                    platform_tag_keepout=(
                                        platform_tag.is_keepout() if platform_tag is not None else None
                                    ),
                                    copyright_tag_id=str(copyright_tag) if copyright_tag is not None else None,
                                    copyright_tag_keepout=(
                                        copyright_tag.is_keepout() if copyright_tag is not None else None
                                    ),
                                    type=DatapoolContentType.Audio,
                                    # storage_id=storage_id,
                                    url=full_local_url,
                                )
                            else:
                                logger.debug(f"non local: {src=} {page.url=}")

                        except PlaywriteTimeoutError:
                            # element may be not ready yet, no problems, will get it on the next iteration
                            # logger.info( 'get_attribute timeout' )
                            logger.debug("expect changes by AUDIO EXCEPTION")
                            expect_changes = True
                            break

                    # 5. hrefs
                    hrefs = await page.locator("a").all()
                    new_n_hrefs = len(hrefs)
                    if new_n_hrefs != n_hrefs:
                        logger.debug("expect changes by HREFS COUNT")
                        expect_changes = True
                    while n_hrefs < new_n_hrefs:
                        try:
                            href = await hrefs[n_hrefs].get_attribute("href", timeout=100)
                            n_hrefs += 1
                            if href is None:
                                outerHTML = await hrefs[n_hrefs - 1].evaluate("el => el.outerHTML")
                                logger.debug(f"no href in {outerHTML}")
                                continue

                            full_local_url = BasePlugin.get_local_url(href, page.url)
                            if full_local_url:
                                # strict constraint on urls, else may get endless recursions etc
                                full_local_url = canonicalize_url(full_local_url)
                                logger.debug(f"backtask: {full_local_url}")

                                yield CrawlerBackTask(url=full_local_url)
                            else:
                                logger.debug(f"non local: {href=} {page.url=}")

                        except PlaywriteTimeoutError:
                            # element may be not ready yet, no problems, will get it on the next iteration
                            # logger.info( 'get_attribute timeout' )
                            logger.debug("expect changes by HREFS EXCEPTION")
                            expect_changes = True
                            break

                    scroll_height1 = await page.evaluate("document.body.scrollHeight")
                    await page.mouse.wheel(0, browser.viewport_height * 0.8)
                    scroll_height2 = await page.evaluate("document.body.scrollHeight")
                    logger.debug(f"*********** {scroll_height1=} {scroll_height2=} ****************")
                    if scroll_height1 != scroll_height2:
                        logger.debug("expect changes by SCROLL HEIGHT")
                        expect_changes = True

                    await asyncio.sleep(1)
                    # await page.screenshot(path=f'/home/psu/page.png')

                # logger.info("default::process() done")

                # await page.screenshot(path='/home/psu/bottom.png')
                # print('done')
                # print( f'{n_images=}')
                # print( f'{n_hrefs=}')
        except PlaywriteTimeoutError:
            logger.error(f"Opening {task.url} timeout")

    async def has_href_parent(self, page: Page, element: Locator) -> bool:
        parent = element.locator("xpath=..")
        while await parent.count():
            tag_name = await parent.evaluate("el => el.tagName")
            # logger.info( tag_name )
            if str(tag_name).lower() == "a":
                return True
            parent = parent.locator("xpath=..")
        return False
