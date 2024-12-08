from typing import Union, List, Optional
from bs4 import BeautifulSoup

from playwright.async_api import Locator

from ....common.logger import logger
from ....common.types import (
    CrawlerBackTask,
    CrawlerContent,
    DatapoolContentType,
    CrawlerDemoUser,
    StudyUrlTask,
    CrawledContentMetadata,
)
from ....common.http import download
from ..base_plugin import BasePlugin, BaseTag, browser
from ...worker import WorkerTask
from ...utils import canonicalize_url

DOMAIN = "freesound.org"


class FreesoundOrgPlugin(BasePlugin):
    demo_tag: Optional[BaseTag]

    def __init__(self, ctx, demo_tag=None):
        super().__init__(ctx)
        self.demo_tag = BaseTag(demo_tag) if demo_tag else None

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        return u.netloc == DOMAIN

    async def study(self, task: StudyUrlTask, timeout: int = 10000) -> List[BaseTag]:
        if self.demo_tag is not None:
            return [self.demo_tag]
        return await super().study(task, timeout=timeout)

    async def process(self, task: WorkerTask):
        if self.ctx.session is None:
            raise Exception("invalid usage")

        logger.info(f"FreeSound::process({task.url})")

        async with browser.open(task.url) as cm:
            page = cm.page

            if self.demo_tag is None:
                platform_tag = await self.get_platform_tag(DOMAIN, page, 3600)
            else:
                platform_tag = self.demo_tag

            session_meta = await self.ctx.session.get_meta()

            logger.debug("Adding new links...")
            links = await page.locator("a").all()
            # logger.info(f"found {len(links)=}")
            added = 0
            for link in links:
                href = await link.get_attribute("href")
                if href is None:
                    # logger.info(f"no href {link}")
                    continue
                full_local_url = BasePlugin.get_local_url(href, session_meta["url"])
                # logger.info(f"{full_local_url=}")
                if full_local_url:
                    full_local_url = canonicalize_url(full_local_url)
                    # logger.info(f"canonicalized {full_local_url=}")
                    if self.is_supported(full_local_url) and not await self.ctx.session.has_url(full_local_url):
                        u = BasePlugin.parse_url(full_local_url)
                        if u.path[0:8] == "/search/":
                            # logger.info(full_local_url)
                            yield CrawlerBackTask(url=full_local_url)
                            added += 1
            logger.debug(f"yielded {added} back tasks")

            sounds = await page.locator(".bw-search__result").all()
            for sound in sounds:

                copyright_owner_tag = None
                date = None

                # looking for the owner page link
                links = await sound.locator("a").all()
                for link in links:
                    href = await link.get_attribute("href")
                    if href is None:
                        continue
                    href_parts = href.split("/")  # expecting "/people/username/" structure
                    if (
                        len(href_parts) == 4
                        and href_parts[0] == ""
                        and href_parts[1] == "people"
                        and href_parts[3] == ""
                    ):
                        if self.demo_tag is None:
                            copyright_owner_tag = await self.parse_user_profile(href, session_meta)
                        else:
                            # demo functionality for royalties spreadout demo
                            user_name = href_parts[2]
                            short_tag_id = BasePlugin.gen_demo_tag(user_name)
                            copyright_owner_tag = BaseTag(short_tag_id)
                            yield CrawlerDemoUser(
                                user_name=user_name, short_tag_id=short_tag_id, platform="freesound.org"
                            )
                        break

                if copyright_owner_tag is not None:
                    logger.info(f"found {copyright_owner_tag=}")

                if platform_tag is None and copyright_owner_tag is None:
                    logger.debug("no tag available")
                    continue

                # searching for date div
                date_div = sound.locator(".text-light-grey.h-spacing-left-1.d-none.d-lg-block.no-text-wrap").first
                raw_date = await date_div.text_content()
                logger.debug(f"{raw_date=}")
                if raw_date is None:
                    logger.error("date not found")
                    continue

                date = BasePlugin.parse_datetime(raw_date)

                # downloading audio content
                player = sound.locator(".bw-player").first
                mp3_url = await player.get_attribute("data-mp3")  # TODO: also ogg available as "data-ogg"

                full_mp3_url = BasePlugin.get_local_url(mp3_url, session_meta["url"])
                logger.debug(full_mp3_url)

                yield CrawlerContent(
                    copyright_tag_id=(str(copyright_owner_tag) if copyright_owner_tag is not None else None),
                    copyright_tag_keepout=(
                        copyright_owner_tag.is_keepout() if copyright_owner_tag is not None else False
                    ),
                    platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                    platform_tag_keepout=(platform_tag.is_keepout() if platform_tag is not None else False),
                    type=DatapoolContentType.Audio,
                    url=full_mp3_url,
                    priority_timestamp=date,
                    metadata=await self._get_content_metadata(sound),
                )

    async def _get_content_metadata(self, sound: Locator) -> Optional[CrawledContentMetadata]:
        a = await sound.locator(".bw-link--black").all()
        if a:
            title = await a[0].inner_text()
            if title:
                return CrawledContentMetadata(title=title)
        return None

    async def parse_user_profile(self, href, session_meta) -> Union[BaseTag, None]:
        username = href.split("/")[-2]
        if not self.copyright_tags_cache.contains(username, 3600):
            # getting full profile url
            url = canonicalize_url(BasePlugin.get_local_url(href, session_meta["url"]))

            logger.debug(f"parsing user profile {url=}")

            r = await download(url)
            # logger.debug( f'text: {r}')
            logger.debug(f"got url content length={len(r)}")

            soup = BeautifulSoup(r, "html.parser")
            description = soup.body.find("div", attrs={"class": "bw-profile__description"})
            logger.debug(f"{description=}")
            if description:
                logger.debug(f"{description.contents=}")
                self.copyright_tags_cache.set(username, BasePlugin.parse_tag_in_str(description.contents[0]))
            else:
                self.copyright_tags_cache.set(username, None)
        return self.copyright_tags_cache.get(username)
