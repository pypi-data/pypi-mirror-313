import logging
from typing import List

from ..core import ScraperAPI

logger = logging.getLogger(__name__)


class TikTok(ScraperAPI):
    async def posts(self, *urls: str):
        DATASET_ID = "gd_lu702nij2f790tmv9h"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def comments(self, *urls: str):
        DATASET_ID = "gd_lkf2st302ap89utw5k"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def profiles(self, *urls: str):
        DATASET_ID = "gd_l1villgoiiidt09ci"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])
