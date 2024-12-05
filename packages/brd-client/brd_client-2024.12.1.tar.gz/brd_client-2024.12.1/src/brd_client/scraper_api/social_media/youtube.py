import logging
from typing import List

from ..core import ScraperAPI

logger = logging.getLogger(__name__)


class YouTube(ScraperAPI):
    async def posts(self, *urls: str):
        DATASET_ID = "gd_lk56epmy2i5g7lzu0k"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    # [CHECK] 댓글의 일부만 수집됨, 인기 댓글순 또는 시간순 정렬 파라미터 없는지?
    async def comments(self, *urls: str):
        DATASET_ID = "gd_lk9q0ew71spt1mxywf"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def profiles(self, *urls: str):
        DATASET_ID = "gd_lk538t2k2p1k3oos71"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])
