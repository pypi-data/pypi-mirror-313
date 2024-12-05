import logging
from typing import List

from ..core import ScraperAPI

logger = logging.getLogger(__name__)


class Amazon(ScraperAPI):
    async def reviews(self, urls: List[str], days_range: int = 0, keyword=None):
        DATASET_ID = "gd_le8e811kzy4ggddlq"
        payload = list()
        for url in urls:
            opt = {"url": url, "days_range": days_range}
            if keyword:
                opt.update({"keyword": keyword})
        return await self.collect(dataset_id=DATASET_ID, payload=payload)

    async def products(self, urls: List[str]):
        DATASET_ID = "gd_lwhideng15g8jg63s7"
        return await self.collect(dataset_id=DATASET_ID, payload=[{"url": url} for url in urls])

    async def descover_by_category(self, urls: List[str]):
        DATASET_ID = "gd_l1villgoiiidt09ci"
        TYPE = "discover_new"
        DISCOVER_BY = "category_url"
        return await self.collect(
            dataset_id=DATASET_ID, payload=[{"url": url} for url in urls], type=TYPE, discover_by=DISCOVER_BY
        )

    async def descover_by_category_url(self, urls: List[str]):
        DATASET_ID = "gd_l1villgoiiidt09ci"
        TYPE = "discover_new"
        DISCOVER_BY = "category_url"
        return await self.collect(
            dataset_id=DATASET_ID, payload=[{"url": url} for url in urls], type=TYPE, discover_by=DISCOVER_BY
        )

    async def descover_by_keywords(self, keywords: List[str], domain: str = "https://www.amazon.com"):
        DATASET_ID = "gd_l1villgoiiidt09ci"
        TYPE = "discover_new"
        DISCOVER_BY = "keywords"
        payload = [{"keywords": k, "domain": domain} for k in keywords]
        return await self.collect(dataset_id=DATASET_ID, payload=payload, type=TYPE, discover_by=DISCOVER_BY)
