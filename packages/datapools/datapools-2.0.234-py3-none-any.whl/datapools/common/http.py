import aiohttp
from typing import Optional
from .logger import logger


async def download(
    url, headers={}, follow_redirects=True, max_redirects=5, timeout=5, output_meta: Optional[dict] = None
):
    logger.debug(f"http.download {url=}")
    try:
        # async with httpx.AsyncClient(max_redirects=max_redirects, timeout=timeout) as client:
        #     r = await client.get(url, follow_redirects=follow_redirects, headers=headers, timeout=timeout)
        #     return r.content
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(connect=3, sock_connect=3, sock_read=timeout)
        ) as session:
            response = await session.get(
                url, headers=headers, allow_redirects=follow_redirects, max_redirects=max_redirects
            )
            response.raise_for_status()

            if output_meta is not None:
                output_meta["url"] = str(response.url)
            return await response.read()

    except Exception as e:
        logger.debug(f"failed get content of {url}: {e}")
