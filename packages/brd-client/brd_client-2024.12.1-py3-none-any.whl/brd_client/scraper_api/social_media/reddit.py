import logging
from typing import List

from ..core import ScraperAPI

logger = logging.getLogger(__name__)


class Reddit(ScraperAPI):
    async def posts(self, *urls: str):
        DATASET_ID = "gd_lvz8ah06191smkebj4"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    # [CHECK] 댓글의 일부만 수집됨, 인기 댓글순 또는 시간순 정렬 파라미터 없는지?
    async def comments(self, *urls: str, days_back: int = 7):
        DATASET_ID = "gd_lvzdpsdlw09j6t702"
        
        params = dict()
        params.update({"days_back": days_back})
            
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url, **params} for url in urls])

    async def profiles(self, *urls: str):
        raise NotImplementedError
