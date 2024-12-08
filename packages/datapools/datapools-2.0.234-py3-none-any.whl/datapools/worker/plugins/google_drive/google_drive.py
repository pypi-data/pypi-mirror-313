import os
import asyncio

# import asyncio
# import io
import traceback
from typing import Optional, List

from google.auth.api_key import Credentials

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerContent, CrawlerDemoUser, StudyUrlTask, CrawlerPostponeSession
from ....common.http import download
from ..base_plugin import BasePlugin, BasePluginException, BaseTag
from ...worker import WorkerTask, YieldResult

# from googleapiclient.http import MediaIoBaseDownload


# from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

PARSING_RULES_FILENAME = "FILES_STRUCTURE.txt"
RULE_ANY_PART = "*"
RULE_USER_PART = "{user}"


class GoogleDrivePlugin(BasePlugin):
    tag_id: Optional[BaseTag] = None
    rules: List[str]
    demo_mode: bool

    def __init__(self, ctx, demo_mode=False, api_key=None):
        super().__init__(ctx)
        if not api_key:
            api_key = os.environ.get("GOOGLE_DRIVE_API_KEY")
        self.creds = Credentials(api_key)
        self.demo_mode = demo_mode

    # https://drive.google.com/drive/folders/1CPDmula2V83KWOocJR9jVvsTk6tVSpKd?usp=sharing

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        if u.netloc == "drive.google.com":
            if u.path[0:15] == "/drive/folders/":
                return True

        return False

    async def study(self, task: StudyUrlTask, __timeout: int = 3000) -> List[BaseTag]:
        u = self.parse_url(task.url)
        folder_id = u.path.split("/")[3]

        with build("drive", "v3", credentials=self.creds) as drive:
            tag_id = await self.find_license(folder_id, drive)
            return [tag_id] if tag_id else []

    async def process(self, task: WorkerTask):
        u = self.parse_url(task.url)
        folder_id = u.path.split("/")[3]

        with build("drive", "v3", credentials=self.creds) as drive:
            self.tag_id = await self.find_license(folder_id, drive)
            if self.tag_id:
                self.rules = await self.find_parsing_rules(folder_id, drive)
                logger.info(f"{self.rules=}")

                async for msg in self.scan_folder(folder_id, drive):
                    yield msg
            else:
                logger.error(f"failed find license tag in {task.url}")

    def _get_download_url(self, file_id):
        return f"https://drive.usercontent.google.com/download?export=download&id={file_id}&authuser=0"
        # return f"https://drive.google.com/uc?export=download&id={file_id}"

        # return f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={self.creds.token}"

    async def find_license(self, folder_id, drive):
        try:
            files_res = (
                drive.files()
                .list(
                    q=f"name='{BasePlugin.license_filename}' and '{folder_id}' in parents",
                    pageSize=1,
                    fields="files(id)",
                )
                .execute()
            )
            file_id = files_res.get("files")[0]["id"]

            # TODO: control max file size, because license is downloaded into memory

            url = self._get_download_url(file_id)
            headers = {}
            tag_id = await download(url, headers)
            logger.info(f"download {tag_id=}")
            tag_id = await BasePlugin.parse_tag_in(tag_id.decode())
            logger.info(f"{tag_id=}")
            return tag_id

        except Exception as e:
            logger.error(f"find_license exception {e}")

    async def find_parsing_rules(self, folder_id, drive):
        try:
            files_res = (
                drive.files()
                .list(
                    q=f"name='{PARSING_RULES_FILENAME}' and '{folder_id}' in parents",
                    pageSize=1,
                    fields="files(id)",
                )
                .execute()
            )
            file_id = files_res.get("files")[0]["id"]

            url = self._get_download_url(file_id)
            headers = {}
            rules = await download(url, headers)
            rules = rules.decode()
            logger.info(f"downloaded {rules=}")

            res = []
            for rule in rules.split("\n"):
                rule = rule.strip()
                if rule:
                    rule_parts = rule.split("/")
                    for i in range(0, len(rule_parts)):
                        part = rule_parts[i]
                        if part == RULE_ANY_PART or part == RULE_USER_PART or (part == "" and i == 0):
                            pass
                        else:
                            raise Exception(f"Invalid rule {rule_parts=}")
                    res.append(rule_parts)
            return res

        except Exception:
            pass

    @staticmethod
    def list_folder(folder_id, drive):
        res = []

        page_token = None
        while True:
            results = (
                drive.files()
                .list(
                    q="'" + folder_id + "' in parents",
                    pageSize=100,
                    pageToken=page_token,
                    fields="nextPageToken, files(id, name, mimeType)",
                )
                .execute()
            )
            items = results.get("files", [])
            res += items

            page_token = results.get("nextPageToken", None)
            if page_token is None:
                break
        return res

    async def scan_folder(self, folder_id, drive, parent_path="/"):
        logger.info(f"scanning folder {folder_id}")
        # print(folder_id)
        # this gives us a list of all folders with that name
        # folder = drive.files().get( fileId=folder_id ).execute()
        # print(type(folder))

        items = self.list_folder(folder_id, drive)
        for item in items:
            # logger.info(f"{item=}")

            if parent_path == "/" and (
                item["name"] == BasePlugin.license_filename or item["name"] == PARSING_RULES_FILENAME
            ):
                continue

            file_id = item["id"]
            logger.info(f"{file_id=}")

            if item["mimeType"] == "application/vnd.google-apps.folder":
                async for yielded in self.scan_folder(file_id, drive, f'{parent_path}{item["name"]}/'):
                    yield yielded
                    if isinstance(yielded, CrawlerPostponeSession):
                        break
            else:
                try:
                    datapool_content_type = BasePlugin.get_content_type_by_mime_type(item["mimeType"])
                except BasePluginException:
                    logger.error(f'Not supported mime type {item["mimeType"]}')
                    continue

                # logger.info(f'downloading file {file_id} {item["name"]}')
                # TODO: this works too, but is getting blocked  when running from lsrv2
                # fileRequest = drive.files().get_media(fileId=file_id)
                # fh = io.BytesIO()
                # downloader = MediaIoBaseDownload(fh, fileRequest)
                # done = False
                # while done is False:
                #     status, done = downloader.next_chunk()
                # fh.seek(0)
                # content = fh.read()
                # direct url seems to work better than API access
                url = self._get_download_url(file_id)
                # content = await self.download(url)
                # if content is not None:
                #     logger.info(f"file size={len(content)}")

                author_tag = None
                if self.demo_mode:
                    path = f"{parent_path}{item['name']}"
                    logger.info(f"{path=}")

                    # if file full path matches any structural rule,
                    # then trying to create demo user from the match info
                    match = self._match_structure_rules(path)
                    if match and "user" in match:
                        short_tag_id = BasePlugin.gen_demo_tag(match["user"])
                        author_tag = BaseTag(short_tag_id)
                        yield CrawlerDemoUser(
                            user_name=match["user"], short_tag_id=short_tag_id, platform="drive.google.com"
                        )

                # if not author_tag:
                #     if datapool_content_type == DatapoolContentType.Image:
                #         author_tag = BasePlugin.parse_image_tag(content)

                # obj_url = f'https://drive.google.com/file/d/{file_id}/view'
                obj_url = url
                # storage_id = self.ctx.storage.gen_id(obj_url)
                # await self.ctx.storage.put(storage_id, content)

                yield CrawlerContent(
                    tag_id=str(author_tag) if author_tag is not None else None,
                    tag_keepout=author_tag.is_keepout() if author_tag is not None else None,
                    copyright_tag_id=str(self.tag_id),
                    copyright_tag_keepout=self.tag_id.is_keepout(),
                    type=datapool_content_type,
                    # storage_id=storage_id,
                    url=obj_url,
                    # content=content,
                )
                if self.ctx.yield_result == YieldResult.ContentDownloadSuccess:
                    await asyncio.sleep(20)
                elif self.ctx.yield_result == YieldResult.ContentDownloadFailure:
                    yield CrawlerPostponeSession()
                    break

    def _match_structure_rules(self, path):
        # self.rules is [
        #     ["*" | "{user}"...],
        #     ["*" | "{user}"...],
        # ]
        if self.rules is not None:
            path_parts = path.split("/")
            n = len(path_parts)
            for rule_parts in self.rules:
                if len(rule_parts) != n:
                    continue

                res = {}
                for i in range(0, n):
                    if rule_parts[i] == RULE_USER_PART:
                        res["user"] = path_parts[i]
                return res
