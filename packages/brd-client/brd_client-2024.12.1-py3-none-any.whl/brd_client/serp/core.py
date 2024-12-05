import logging

import aiohttp

logger = logging.getLogger(__name__)


################################################################
# Base Class
################################################################
class BRDProxy:
    proxy = "https://brd.superproxy.io:22225"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        self.proxy_auth = aiohttp.BasicAuth(username, password)

    async def get(self, **params):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url, proxy=self.proxy, proxy_auth=self.proxy_auth, params=params
            ) as response:
                # logging
                _log = " ".join([response.request_info.method, response.request_info.url.human_repr()])
                logger.info(_log)

                # raise
                response.raise_for_status()

                # read
                if response.content_type == "application/json":
                    return await response.json()
                return await response.text()
