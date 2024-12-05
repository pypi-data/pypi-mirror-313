import logging
from typing import List

from ..core import ScraperAPI

logger = logging.getLogger(__name__)


class Instagram(ScraperAPI):
    async def posts(self, *urls: str):
        DATASET_ID = "gd_lk5ns7kz21pck8jpis"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def comments(self, *urls: str):
        DATASET_ID = "gd_ltppn085pokosxh13"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def profiles(self, *urls: str):
        DATASET_ID = "gd_l1vikfch901nx3by4"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def reels(self, *urls: str):
        DATASET_ID = "gd_lyclm20il4r5helnj"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])