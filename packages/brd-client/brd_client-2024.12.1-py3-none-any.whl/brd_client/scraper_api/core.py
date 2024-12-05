import asyncio
import logging
from typing import List, Union

import aiohttp
import orjson

logger = logging.getLogger(__name__)


class SnapshotFailed(Exception):
    pass


class ScraperAPI:
    base_url = "https://api.brightdata.com"

    def __init__(self, api_token: str, delay: float = 5.0):
        self.api_token = api_token
        self.delay = delay

    async def collect(self, dataset_id: str, payload: Union[dict, List[dict]], **kwargs):
        async with self.session_maker() as session:
            # 1. trigger
            results = await self._trigger(session=session, dataset_id=dataset_id, payload=payload, **kwargs)
            # 2. wait ready
            await self._wait_ready(session=session, snapshot_id=results["snapshot_id"])
            # 3. retrieve
            return await self._retrieve(session=session, snapshot_id=results["snapshot_id"])

    async def list_snapshots(self, dataset_id: str, status: str = "ready"):
        url = f"/datasets/v3/snapshots"
        params = {"dataset_id": dataset_id, "status": status}
        async with self.session_maker() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def download_snapshot(self, snapshot_id: str, parse: bool = True):
        async with self.session_maker() as session:
            return await self._retrieve(session=session, snapshot_id=snapshot_id, parse=parse)

    def session_maker(self):
        headers = {"Authorization": f"Bearer {self.api_token}", "Content-type": "application/json"}
        return aiohttp.ClientSession(base_url=self.base_url, headers=headers)

    async def _trigger(
        self, session: aiohttp.ClientSession, dataset_id: str, payload: Union[dict, List[dict]], **kwargs
    ):
        url = "/datasets/v3/trigger"
        params = {"dataset_id": dataset_id, **kwargs}
        async with session.post(url, params=params, json=payload) as response:
            response.raise_for_status()
            return await response.json()

    async def _monitor(self, session: aiohttp.ClientSession, snapshot_id: str):
        url = f"/datasets/v3/progress/{snapshot_id}"
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def _wait_ready(self, session: aiohttp.ClientSession, snapshot_id: str):
        # 1st hit
        results = await self._monitor(session=session, snapshot_id=snapshot_id)
        status = results["status"]

        # wait
        while status == "running":
            await asyncio.sleep(self.delay)
            results = await self._monitor(session=session, snapshot_id=snapshot_id)
            status = results["status"]

        if status == "ready":
            return True
        else:
            raise SnapshotFailed(results)

    async def _retrieve(self, session: aiohttp.ClientSession, snapshot_id: str, parse: bool = True):
        sep = "\n"
        url = f"/datasets/v3/snapshot/{snapshot_id}"

        async with session.get(url) as response:
            response.raise_for_status()
            if response.content_type == "application/octet-stream":
                results = await response.text()
                if parse:
                    results = [orjson.loads(record) for record in results.rstrip(sep).split(sep) if record]
                return results
