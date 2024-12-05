import logging
from typing import List

from ..core import ScraperAPI

logger = logging.getLogger(__name__)


class Facebook(ScraperAPI):
    async def posts(self, *urls: str):
        DATASET_ID = "gd_lyclm1571iy3mv57zw"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def comments(self, *urls: str):
        DATASET_ID = "gd_lkay758p1eanlolqw8"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def profiles(self, *urls: str):
        raise NotImplementedError("Bright Data는 아직 Facebook Profile에 대한 Scraper API 기능을 제공하지 않음!")

    async def reels(self, *urls: str, start_date: str, end_date: str):
        DATASET_ID = "gd_lkay758p1eanlolqw8"
        params = dict()
        if start_date:
            params.update({"start_date": start_date})
        if end_date:
            params.update({"end_date": end_date})
        return await self.collect(
            dataset_id=DATASET_ID,
            payload=[{"url": url, **params} for url in urls],
        )
