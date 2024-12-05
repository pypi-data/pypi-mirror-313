import logging
from typing import List

from ..core import ScraperAPI

logger = logging.getLogger(__name__)


class Twitter(ScraperAPI):
    async def posts(self, *urls: str):
        DATASET_ID = "gd_lwxkxvnf1cynvib9co"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def comments(self, *urls: str):
        raise NotImplementedError

    async def profiles(self, *urls: str):
        DATASET_ID = "gd_lwxmeb2u1cniijd7t4"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])
