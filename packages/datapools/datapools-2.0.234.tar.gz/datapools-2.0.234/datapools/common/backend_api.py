import httpx

from typing import List
from ..common.logger import logger
from ..common.types import CrawlerHintURLStatus, CrawlerHintURL  # , DatapoolRules

# class TagDatapool(BaseModel):
#     id: int
#     rules: DatapoolRules

#     class Config:
#         validate_assignment = True


class BackendAPIException(Exception):
    def __str__(self):
        return f"BackendAPIException: {self.args[0] if self.args else ''}"


class BackendConnectionFailure(BackendAPIException):
    pass


class BackendAPI:
    def __init__(self, url):
        self.url = url

    async def get_hint_urls(self, limit) -> List[CrawlerHintURL]:
        res = await self.get_uri("get-hint-urls", {"limit": limit})
        if res is not None:
            hints = []
            for r in res:
                try:
                    hint = CrawlerHintURL(**r)
                    hints.append(hint)
                except:
                    pass
            return hints
        return []

    async def set_hint_url_status(self, hint_id, status: CrawlerHintURLStatus, session_id=None):
        return await self.get_uri(
            "set-hint-url-status", {"id": hint_id, "status": status.value, "session_id": session_id}
        )

    # async def notify_session_stopped(self, session_id):
    #     return await self.get_uri(f"notify-crawler-session-stopped/{session_id}")

    async def add_crawled_content(self, data):
        return await self.get_uri("add-crawled-content", data)

    async def add_demo_user(self, data):
        return await self.get_uri("add-demo-user", data)

    async def get_uri(self, uri, data={}):
        async with httpx.AsyncClient() as client:
            url = self.url + uri
            logger.debug(f"posting to {url=} {data=}")

            try:
                r = await client.post(url, json=data)
                if r.status_code == 200:
                    return r.json()
                else:
                    logger.error(f"Non 200 http response {r=}")
                    raise BackendAPIException("non 200 response")
            except httpx.ConnectError as e:
                logger.error(f"Failed connect Backend API server: {e}")
                raise BackendConnectionFailure() from e
