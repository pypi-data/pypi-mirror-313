import asyncio
import inspect
import logging
import re
import urllib.parse
from typing import Callable, Union

import aiohttp

from .core import BRDProxy

logger = logging.getLogger(__name__)


# BRD가 파싱해준 데이터에서 link가 빠져있을 때 - link가 빠지면 쓸모 없는 데이터!
class BrdMissRequiredResultsType(Exception):
    def __init__(self, msg):
        super().__init__("Bright Data missed required results type AGAIN while parsing the HTML!", msg)


class BrdMissRequiredField(Exception):
    def __init__(self, msg):
        super().__init__("Bright Data missed required attribute AGAIN while parsing the HTML!", msg)


# 파싱된 검색 결과 중 "link"가 존재하는지 확인해야 하는 속성들
REQUIRED_RESULTS_TYPE = {
    "text": ["organic"],
    "images": ["images"],
    "videos": ["organic"],
    "news": ["news"],
    "shopping": ["shopping"],
}
REQUIRED_FIELD = {
    "shopping": ["link"],
    "text": ["link"],
    "images": ["link"],
    "videos": ["link"],
    "shopping": ["shopping"],
}


# Bright Data에서 제공하는 Parsed SERP의 스키마
async def get_google_schema(api_token: str):
    PARSING_SCHEMA_URL = "https://api.brightdata.com/serp/google/parsing_schema"

    headers = dict()
    if api_token:
        headers.update({"Authorization": f"Bearer {api_token}"})

    async with aiohttp.ClientSession() as session:
        async with session.get(PARSING_SCHEMA_URL) as response:
            response.raise_for_status()
            return await response.json()


################################################################
# Google Search
################################################################
class GoogleSearchAPI(BRDProxy):
    url = "http://www.google.com/search"

    def __init__(
        self,
        username: str,
        password: str,
        *,
        gl: str = None,
        hl: str = None,
        uule: str = None,
        device: Union[int, str] = 0,
        num_per_page: int = 100,
        parse_results: bool = True,
    ):
        """
        Args:
            gl: geolocation, Two-letter country code used to define the country of search. [US, KR, ...]
            hl: host language, Two-letter language code used to define the page language. [en, ko, ...]
            uule: uule, Stands for the encoded location you want to use for your search and will be used to change geo-location. ["United States", ...]
            device: brd_mobile, [0: desktop, 1: random mobile, ios: iPhone, ipad: iPad, android: Android, android_tablet: Android tablet]
            parse_results: brd_json, Bright Data custom parameter allowing to return parsed JSON instead of raw HTML.
        """
        super().__init__(username=username, password=password)

        self.gl = gl
        self.hl = hl
        # self.jobs_search_type = jobs_search_type
        self.uule = uule
        self.device = device
        self.num_per_page = num_per_page
        self.parse_results = parse_results

        self.default_params = dict()
        if gl:
            # Validator Here
            self.default_params.update({"gl": self.gl})
        if hl:
            # Validator Here
            self.default_params.update({"hl": self.hl})
        if uule:
            # Validator Here
            self.default_params.update({"uule": self.uule})
        if device:
            # Validator Here
            self.default_params.update({"brd_mobile": self.device})
        if parse_results:
            # Validator Here
            self.default_params.update({"brd_json": int(self.parse_results)})

        self._results_page = None

    # Text Search
    async def search(
        self,
        q: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        tbm: str = None,
        ibp: str = None,
        max_results: int = 100,
        max_retries: int = 10,
        return_records: bool = True,
    ):
        search_query = self.args_to_search_operator(before=before, after=after, site=site)
        search_query.append(q)
        q = " ".join(search_query)
        params = {"tbm": tbm, "ibp": ibp, **self.default_params, "q": q}
        params = {k: v for k, v in params.items() if v is not None}

        for i in range(max_retries):
            try:
                # 1st hit
                results_page_1 = await self.get(**params, start=0, num=self.num_per_page)
                results_cnt = results_page_1["general"].get("results_cnt")

                # 2nd hit
                next_page_start = results_page_1["pagination"]["next_page_start"]
                coros = list()
                for start in range(next_page_start, min(results_cnt, max_results), self.num_per_page):
                    coros.append(self.get(**params, start=start, num=self.num_per_page))
                results_pages_remains = await asyncio.gather(*coros)
                results_pages = [
                    results_page_1,
                    *[r for r in results_pages_remains if not r["general"].get("empty", False)],
                ]

                if return_records:
                    records = list()
                    for results_page in results_pages:
                        new_records = self.generate_records(results_page)
                        records += new_records
                    return records

                return [results_page_1, *[r for r in results_pages if not r["general"].get("empty", False)]]

            except (BrdMissRequiredResultsType, BrdMissRequiredField, aiohttp.ClientResponseError) as ex:
                _msg = f"failed {i+1}/{max_retries}, {ex.__class__.__name__}"
                logger.warning(_msg)
                latest_exception = ex
        else:
            raise latest_exception

    # Image Search
    async def images(
        self,
        q: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(q=q, before=before, after=after, site=site, tbm="isch", max_results=max_results)

    # Video Search
    async def videos(
        self,
        q: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(q=q, before=before, after=after, site=site, tbm="vid", max_results=max_results)

    # News
    async def news(
        self,
        q: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(q=q, before=before, after=after, site=site, tbm="nws", max_results=max_results)

    # Shopping
    async def shopping(
        self,
        q: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(q=q, before=before, after=after, site=site, tbm="shop", max_results=max_results)

    # Jobs
    async def jobs(
        self,
        q: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(
            q=q,
            before=before,
            after=after,
            site=site,
            ibp="htl;jobs",
            max_results=max_results,
        )

    async def get(self, **params):
        results_page = await super().get(**params)
        self._results_page = results_page

        if not self.parse_results:
            return results_page

        # override logging
        _log = "[general] " + ", ".join([f"{k}: {v}" for k, v in results_page["general"].items()])
        logger.debug(_log)
        _log = "[input] " + ", ".join([f"{k}: {v}" for k, v in results_page["input"].items()])
        logger.debug(_log)

        # validation
        _ = self.validate(results_page)

        return results_page

    @staticmethod
    def validate(results_page):
        if results_page["pagination"]["current_page"] > 1:
            return

        search_type = results_page["general"]["search_type"]
        required_results_types = REQUIRED_RESULTS_TYPE[search_type]
        for required_results_type in required_results_types:
            if required_results_type not in results_page:
                _msg = f"no {required_results_type} for {search_type}!"
                raise BrdMissRequiredResultsType(_msg)

        for results_type, required_fields in REQUIRED_FIELD.items():
            if results_type not in results_page:
                continue

            results_for_result_type = results_page[results_type]
            if isinstance(results_for_result_type, dict):
                if "items" in results_for_result_type:
                    results_for_result_type = results_for_result_type["items"]
                else:
                    continue

            for r in results_for_result_type:
                for field in required_fields:
                    if field not in r:
                        _sample = ", ".join([f"{k}: {v}" for k, v in r.items()])
                        _msg = f"[{results_type}] {_sample}"
                        raise BrdMissRequiredField(_msg)

    @staticmethod
    def args_to_search_operator(**params):
        search_query = list()
        for k, v in params.items():
            if v is not None:
                search_query.append(":".join([k, v]))
        return search_query

    @staticmethod
    def generate_records(results_page):
        SYS_ATTRS = ["input", "general", "pagination", "pagination"]
        SYS_PARAMS = ["brd_json", "start", "num"]
        SITE_PATTERN = r"site:([^\s]+)"

        # parse query parameters
        original_url = results_page["input"]["original_url"]
        parsed_url = urllib.parse.urlparse(urllib.parse.unquote_plus(original_url))
        query = {k: v for k, v in urllib.parse.parse_qsl(parsed_url.query) if k not in SYS_PARAMS}
        site = site = re.search(SITE_PATTERN, query["q"])
        if site:
            site = site.group(1)
            q = query["q"].replace(f"site:{site}", "").strip()
            query.update({"q": q, "site": site})
        location = results_page["general"].get("location")
        if location:
            query.update({"location": location})

        # generate records
        records = list()
        for attr, results in results_page.items():
            # ignore system attributes
            if attr in SYS_ATTRS:
                continue

            # if results is not list
            if isinstance(results, dict):
                results = [results]

            # gerate records to publish
            for result in results:
                records.append(
                    {
                        "key": {
                            "query": query,
                            "request_id": results_page["input"]["request_id"],
                            "original_url": original_url,
                            "results_type": attr,
                            "timestamp": results_page["general"]["timestamp"],
                        },
                        "value": result,
                    }
                )

        return records
