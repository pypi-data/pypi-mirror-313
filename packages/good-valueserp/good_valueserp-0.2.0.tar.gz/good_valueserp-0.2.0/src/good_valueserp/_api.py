import collections
import os
from typing import Any, Dict, Generator, List, Optional, Protocol, AsyncGenerator
from fast_depends import inject
import httpx
import requests
from loguru import logger
import jsonlines
import orjson

# from genson import SchemaBuilder
from pydantic import BaseModel
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from good_common.dependencies import BaseProvider

# from edgepath.sources.base import Cursor, datetime_to_milliseconds
from ._models import (
    Batch,
    BatchResults,
    Destination,
    ResultRecord,
    ResultSet,
    S3Object,
    SearchParameters,
    ResultItems,
)

from good_object_storage import Bucket, BucketProvider

# from ._s3 import S3Bucket, S3BucketProvider

# from requests.packages.urllib3.util.retry import Retry


# from edgepath.sources.google_serp.s3 import S3Bucket, S3Object


def _filter_nulls_empty_strings(d: dict) -> dict:
    return {k: v for k, v in d.items() if v not in (None, "")}


class AsyncValueSerp:
    base_path = "https://api.valueserp.com/"

    @inject
    def __init__(
        self,
        api_key: Optional[str] = None,
        bucket: Bucket = BucketProvider(bucket_name="edgepath-serp-results"),
    ):
        self._api_key = api_key or os.getenv("VALUESERP_API_KEY")
        self._bucket = bucket

        self._client = None

        self._batches = {}
        self._batch_searches = collections.defaultdict(dict)
        self._batch_results = collections.defaultdict(list)

    @property
    def bucket(self) -> Bucket:
        if not self._bucket:
            raise ValueError("Bucket is not defined")
        return self._bucket

    def _build_url(self, *paths) -> str:
        return self.base_path + "/".join(map(str, paths))

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(120, connect=60.0),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def _get(self, *paths, **parameters) -> Dict[str, Any]:
        url = self._build_url(*paths)
        parameters["api_key"] = self._api_key
        response = await self._client.get(
            url, params=_filter_nulls_empty_strings(parameters)
        )
        if response.status_code != 200:
            logger.error(response.text)
        response.raise_for_status()
        return response.json()

    async def _post(self, *paths, params: Dict = {}, body: Dict):
        url = self._build_url(*paths)
        params["api_key"] = self._api_key
        response = await self._client.post(
            url, params=_filter_nulls_empty_strings(params), json=body
        )
        if response.status_code != 200:
            logger.error(response.text)
        response.raise_for_status()
        return response.json()

    async def _put(self, *paths, params: Dict = {}, body: Dict):
        url = self._build_url(*paths)
        params["api_key"] = self._api_key
        try:
            response = await self._client.put(url, params=params, json=body)
            if response.status_code != 200:
                logger.error(response.text)
            response.raise_for_status()

        except Exception as e:
            logger.error(e)
            logger.error(response.text)
            raise e
        return response.json()

    async def _delete(self, *paths, **parameters) -> dict:
        url = self._build_url(*paths)
        parameters["api_key"] = self._api_key
        response = await self._client.delete(
            url, params=_filter_nulls_empty_strings(parameters)
        )
        response.raise_for_status()
        return response.json()

    async def search(self, query: SearchParameters):
        return ResultItems.model_validate(
            await self._get(
                "search", **query.model_dump(exclude_none=True, mode="json")
            )
        )

    async def get_batches(self, name: Optional[str] = None) -> List[Batch]:
        batches = []
        response = await self._get("batches")
        for batch in response.get("batches", []):
            obj = Batch(**batch)
            if name:
                if obj.name == name:
                    batches.append(obj)
            else:
                batches.append(obj)
        return batches

    async def list_destinations(self) -> List[Destination]:
        destinations = []
        response = await self._get("destinations")
        for destination in response.get("destinations", []):
            destinations.append(Destination(**destination))
        return destinations

    async def iter_batch_searches(
        self, batch_id: str
    ) -> AsyncGenerator[SearchParameters, None]:
        page = 1
        while True:
            try:
                response = await self._get("batches", batch_id, "searches", page)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 500:
                    break
                raise e
            for search in response.get("searches", []):
                yield SearchParameters(
                    **{
                        **search,
                        "batch_id": batch_id,
                    }
                )

            searches_page_count = response.get("searches_page_count", 0)
            searches_page_current = response.get("searches_page_current", 0)

            if searches_page_current >= searches_page_count:
                break

            page += 1

    async def get_batch_results(
        self,
        *,
        batch_id: Optional[str] = None,
        batch: Optional[Batch] = None,
        fetch_s3_links: bool = True,
        fetch_jsonlines_links: bool = True,
    ) -> BatchResults:
        if not batch_id and batch:
            batch_id = batch.id

        if not batch_id:
            raise ValueError("Must provide batch_id or batch")

        results = await self._get("batches", batch_id, "results")

        if fetch_s3_links and not fetch_jsonlines_links:
            for i, _result in enumerate(results.get("results", [])):
                s3_objects = await self.get_batch_s3_objects(
                    batch_id, _result.get("id")
                )
                results["results"][i]["s3_object_keys"] = [o.key for o in s3_objects]

        batch_results = BatchResults(**results)

        if not batch_results or batch_results.results is None:
            raise ValueError(f"Batch {batch_id} has no results")

        if fetch_jsonlines_links and batch_id:
            download_results = []
            for result in batch_results.results:
                _result: dict[str, dict[str, Any]] = await self._get(
                    "batches", batch_id, "results", result.id, "jsonlines"
                )
                s3_objects = await self.get_batch_s3_objects(batch_id, result.id)
                logger.info(s3_objects)
                download_results.append(
                    dict(
                        **_result.get("result"),
                        s3_object_keys=[o.key for _, o in s3_objects],
                    )
                )

            batch_results = BatchResults(
                request_info=batch_results.request_info,
                batch_id=batch_results.batch_id,
                results=download_results,
            )

        return batch_results

    async def download_result_records(self, *, result: ResultSet):
        for link in result.get_download_links(filetype="jsonl"):
            async with self._client as client:
                async with client.stream("GET", link) as response:
                    with jsonlines.Reader(response.text) as reader:
                        for line in reader:
                            yield ResultRecord(
                                **line, result_id=result.id, batch_id=result.batch_id
                            )

    async def stream_result_records(
        self,
        *,
        result: ResultSet,
    ) -> AsyncGenerator[ResultRecord, None]:
        if result.s3_object_keys:
            s3_object_keys = [
                f for f in result.s3_object_keys if f.endswith(".jsonl")
            ] or result.s3_object_keys

            async with self.bucket as bucket:
                for key in s3_object_keys:
                    obj = await bucket.get(key)
                    if not obj:
                        logger.error(f"Object not found: {key}")
                        continue
                    data = await obj.download()
                    if key.endswith(".jsonl"):
                        for line in jsonlines.Reader(data):
                            yield ResultRecord(
                                **line,
                                result_id=result.id,
                                batch_id=result.batch_id,
                            )
                    elif key.endswith(".json"):
                        data = await obj.download()
                        yield ResultRecord(
                            **orjson.loads(data),
                            result_id=result.id,
                            batch_id=result.batch_id,
                        )

    async def get_batch(self, batch_id: str) -> Batch:
        response = await self._get("batches", batch_id)
        return Batch(**response.get("batch", {}))

    async def get_batch_s3_objects(
        self,
        batch_id: str,
        result_id: int,
    ) -> List[S3Object]:
        # if not self.bucket:
        #     raise ValueError("Bucket is not defined")
        objects = []
        async with self.bucket as bucket:
            async for obj in bucket.items(
                prefix=f"Batch_Results_{batch_id}_{result_id}"
            ):
                objects.append(obj)
        return objects

    @classmethod
    def serialize(cls, obj: BaseModel, remove_attributes: List[str] = []):
        d = obj.model_dump(mode="json", exclude_none=True)
        return {
            k: v for k, v in d.items() if v is not None and k not in remove_attributes
        }

    async def create_batch(self, batch: Batch):
        response = await self._post("batches", body=self.serialize(batch))
        try:
            if response.get("request_info", {}).get("success") is True:
                return Batch(**response.get("batch"))
        except Exception as e:
            logger.error(e)

    async def update_batch(self, batch: Batch):
        if not batch.id:
            raise ValueError("Batch must have an id")
        response = await self._put("batches", batch.id, body=self.serialize(batch))
        try:
            if response.get("request_info", {}).get("success") is True:
                return Batch(**response.get("batch"))
        except Exception as e:
            logger.error(e)

    async def delete_batch(
        self, batch_id: Optional[str] = None, batch: Optional[Batch] = None
    ):
        if not batch_id and not batch:
            raise ValueError("Batch id or Batch object must be provided")
        if batch:
            if not batch.id:
                raise ValueError("Batch must have an id")
            batch_id = batch.id

        response = await self._delete("batches", batch_id)

        assert response.get("request_info", {}).get("success") is True

    async def start_batch(
        self, batch_id: Optional[str] = None, batch: Optional[Batch] = None
    ):
        if not batch_id and not batch:
            raise ValueError("Batch id or Batch object must be provided")
        if batch:
            if not batch.id:
                raise ValueError("Batch must have an id")
            batch_id = batch.id
        response = await self._get("batches", batch_id, "start")
        assert response.get("request_info", {}).get("success") is True

    async def stop_batch(
        self, batch_id: Optional[str] = None, batch: Optional[Batch] = None
    ):
        if not batch_id and not batch:
            raise ValueError("Batch id or Batch object must be provided")
        if batch:
            if not batch.id:
                raise ValueError("Batch must have an id")
            batch_id = batch.id
        response = await self._get("batches", batch_id, "stop")
        assert response.get("request_info", {}).get("success") is True

    async def stop_all(self):
        response = await self._get("batches", "stop_all")
        assert response.get("request_info", {}).get("success") is True

    async def add_searches(self, batch_id: str, searches: List[SearchParameters]):
        response = await self._put(
            "batches",
            batch_id,
            body={"searches": [self.serialize(search) for search in searches]},
        )
        if response.get("request_info", {}).get("success") is True:
            return Batch(**response.get("batch"))
        else:
            raise ValueError(f"Failed to add searches to batch [{response.text}]")

    async def update_search(self, batch_id: str, search: SearchParameters):
        response = await self._post(
            "batches", batch_id, "searches", search.id, body=self.serialize(search)
        )
        if response.get("request_info", {}).get("success") is True:
            return SearchParameters(**response.get("search"))
        else:
            raise ValueError("Failed to update search")

    async def iter_logs(self):
        page = 1
        while True:
            response = await self._get("errorlogs", page=page)
            for error in response.get("logs", []):
                yield error

            errors_page_count = response.get("page_count_total", 0)
            errors_page_current = response.get("page", page)

            if errors_page_current >= errors_page_count:
                break

            page += 1


class AsyncValueSerpProvider(BaseProvider[AsyncValueSerp], AsyncValueSerp):
    pass
