import time
import os
import tempfile
from typing import Optional, Any, AsyncGenerator, List

# import requests
# import msal
from playwright.async_api import (
    Page,
    Locator,
    Download,
    TimeoutError as PlaywrightTimeoutError,
)
from datapools.worker.plugins.base_plugin import PlaywrightBrowser, StudyUrlTask, MAGIC_MIN_BYTES, BasePluginException


from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerContent, StudyUrlTask, CrawlerPostponeSession, CrawlerNop
from ..base_plugin import (
    BasePlugin,
    BaseTag,
    browser,
)
from ...worker import WorkerTask

# api_base_url = "https://api.onedrive.com/v1.0/"
# scopes = ["wl.signin", "wl.offline_access", "onedrive.readwrite"]


class OneDrive(BasePlugin):
    tag_id: Optional[BaseTag] = None

    def __init__(self, ctx):
        super().__init__(ctx)

    @staticmethod
    def is_supported(url):
        p = BasePlugin.parse_url(url)
        return p.netloc == "1drv.ms"

    async def study(self, task: StudyUrlTask, timeout: int = 10000) -> List[BaseTag]:
        async with browser.open(task.url, timeout=timeout) as cm:
            tag_id = await self.find_license(cm.page)
            return [tag_id] if tag_id else []

    async def process(self, task: WorkerTask):
        b = PlaywrightBrowser()

        await b.start()
        async with b.open(task.url, timeout=30000) as cm:
            self.tag_id = await self.find_license(cm.page)

            if self.tag_id:
                async for r in self.scan_folder(cm.page):
                    yield r
            else:
                logger.error("License not found")

    async def find_license(self, page: Page) -> Optional[BaseTag]:
        rows = await self._wait_directory_ready(page)
        if rows is None:
            logger.info("directory listing failed")
            return None

        res = None
        logger.info(f"found {len(rows)} rows")
        for row in rows:
            (filetype, filename, btn_filename) = await self._parse_directory_row(row)
            if filename == self.license_filename and filetype == "txt":
                # downloading license file
                await btn_filename[0].click()  # changes page url

                btn_download = await self._wait_file_ready(page)
                if btn_download:
                    async with page.expect_download() as download_info:
                        # Perform the action that initiates download
                        await btn_download.click()
                        download = await download_info.value
                        logger.info(f"License.txt download info {download=}")

                    # Wait for the download process to complete and save the downloaded file somewhere
                    tmp_file_path = await self._download(download)
                    if os.path.getsize(tmp_file_path) <= self.license_max_size:
                        with open(tmp_file_path, "r") as f:
                            res = self.parse_tag_in_str(f.read())
                        os.remove(tmp_file_path)
                else:
                    logger.info("license panel not ready")
                await page.go_back()  # go back
                break
        return res

    async def _download(self, download: Download) -> str:
        path = os.path.join(tempfile.gettempdir(), download.suggested_filename + str(time.time()))
        logger.info(f"downloading to {path=}")
        await download.save_as(path)
        return path

    async def _wait_directory_ready(self, page: Page) -> Optional[List[Locator]]:
        btn_download = page.locator('button[name="Download"]')
        try:
            await btn_download.wait_for(state="visible", timeout=10000)
        except PlaywrightTimeoutError:
            logger.error("download button visibility timeout")
            return None

        rows = page.locator(".ms-List-cell")
        try:
            await rows.first.wait_for(state="visible", timeout=10000)
        except PlaywrightTimeoutError:
            logger.error("rows visibility timeout")
            return None
        return await rows.all()

    async def _parse_directory_row(self, row: Locator):
        img_type = await row.locator('.ms-DetailsRow-cell[data-automation-key="fileTypeIconColumn_1"] img').all()
        filetype = await img_type[0].get_attribute("alt")
        logger.info(filetype)
        btn_filename = await row.locator("button.ms-Link").all()
        filename = await btn_filename[0].get_attribute("title")
        logger.info(filename)
        return (filetype, filename, btn_filename)

    async def scan_folder(self, page: Page):
        logger.info(f"scanning folder {page.url=}")
        rows = await self._wait_directory_ready(page)
        if not rows:
            yield CrawlerPostponeSession()
            return

        for row in rows:
            (filetype, __filename, btn_filename) = await self._parse_directory_row(row)

            await btn_filename[0].click()  # changes page url
            if filetype == "Folder":
                async for r in self.scan_folder(page):
                    yield r
            else:
                async for r in self.process_file(page):
                    yield r
            await page.go_back()  # go back

    async def _wait_file_ready(self, page: Page) -> Optional[Locator]:
        # file panel is open over its directory content
        try:
            btn_close = page.locator('i.ms-Button-icon[data-icon-name="Cancel"]')
            try:
                await btn_close.wait_for(state="visible", timeout=10000)
            except PlaywrightTimeoutError:
                await page.screenshot(type="png", path=f"/tmp/timeout1.png")
                logger.error("close button visibility timeout")
                return None

            btn_download = page.locator('button[name="Download"]').last
            try:
                # btn_menu = page.locator("i.ms-Button-menuIcon.ms-Icon.is-expanded")
                # await btn_menu.click()
                # btn_download = page.locator("button.ms-ContextualMenu-link")
                await btn_download.wait_for(state="visible", timeout=10000)
            except PlaywrightTimeoutError:
                await page.screenshot(type="png", path=f"/tmp/timeout2.png")
                logger.error("download button visibility timeout")
                return None
            return btn_download
        except Exception:
            await page.screenshot(type="png", path=f"/tmp/wait_file_ready_exception.png")
        return None

    async def process_file(self, page: Page) -> AsyncGenerator[Any, CrawlerContent | CrawlerNop]:
        logger.info(f"scanning file {page.url=}")
        btn_download = await self._wait_file_ready(page)
        if not btn_download:
            yield CrawlerPostponeSession()
            return

        async with page.expect_download() as download_info:
            # Perform the action that initiates download
            await btn_download.click()
            download = await download_info.value
            logger.info(f"{download=}")

        # Wait for the download process to complete and save the downloaded file somewhere
        tmp_file_path = await self._download(download)
        with open(tmp_file_path, "rb") as f:
            buffer = f.read(MAGIC_MIN_BYTES)
            f.seek(0, 0)
            try:
                content_type = self.get_content_type_by_content(buffer)
                yield CrawlerContent(
                    copyright_tag_id=str(self.tag_id),
                    copyright_tag_keepout=self.tag_id.is_keepout(),  # type: ignore
                    content=f,
                    type=content_type,
                    url=page.url,
                )
            except BasePluginException:
                logger.error("Failed get content type")

        os.remove(tmp_file_path)


# config = {
#     "client_id": "db2b17ab-0fb4-46ba-81a9-4b781d72ef42",
#     "authority": "https://login.microsoftonline.com/e6f25b1a-9192-4786-a9f8-3a75493cb599",
#     "oidc_authority": "https://login.contoso.com/e6f25b1a-9192-4786-a9f8-3a75493cb599/v2.0",
#     "scope": ["https://graph.microsoft.com/.default"],
#     "secret": "V4l8Q~X2jYZNATxf32u~gcWNOuABUAjr_EpNRdjP",
#     "endpoint": "https://graph.microsoft.com/v1.0/drive",
#     # "endpoint": "https://graph.microsoft.com/v1.0/users",
# }
# import json
# import base64


# async def main():
#     app = msal.ConfidentialClientApplication(
#         config["client_id"],
#         authority=config["authority"],
#         client_credential=config["secret"],
#         # oidc_authority=config.get("oidc_authority"),  # For External ID with custom domain
#         # token_cache=...  # Default cache is in memory only.
#         # You can learn how to use SerializableTokenCache from
#         # https://msal-python.readthedocs.io/en/latest/#msal.SerializableTokenCache
#     )

#     # The pattern to acquire a token looks like this.
#     result = None

#     # Firstly, looks up a token from cache
#     # Since we are looking for token for the current app, NOT for an end user,
#     # notice we give account parameter as None.
#     result = app.acquire_token_silent(config["scope"], account=None)
#     if not result:
#         result = app.acquire_token_for_client(scopes=config["scope"])
#     print(result)

#     if "access_token" in result:
#         sharingUrl = "https://1drv.ms/f/s!Avx63pYATxvPaeTHYSGDztFTjOI"
#         base64Value = base64.b64encode(sharingUrl.encode()).decode()
#         encodedUrl = "u!" + base64Value.replace("=", "").replace("/", "_").replace("+", "-")

#         print(encodedUrl)

#         graph_data = requests.get(  # Use token to call downstream service
#             f"https://graph.microsoft.com/v1.0/shares/{encodedUrl}",
#             headers={"Authorization": "Bearer " + result["access_token"]},
#         ).json()
#         print("Graph API call result: %s" % json.dumps(graph_data, indent=2))
#         # # Calling graph using the access token
#         # graph_data = requests.get(  # Use token to call downstream service
#         #     config["endpoint"],
#         #     headers={"Authorization": "Bearer " + result["access_token"]},
#         # ).json()
#         # print("Graph API call result: ")
#         # print(json.dumps(graph_data, indent=2))
#     else:
#         print(result.get("error"))
#         print(result.get("error_description"))
#         print(result.get("correlation_id"))  # You may need this when reporting a bug
