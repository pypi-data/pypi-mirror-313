from typing import AsyncGenerator

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.converter import model_to_query_params
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.batch import BatchListViewV1Strict, BatchViewV1Strict
from toloka.a9s.client.models.generated.ai.toloka.a9s.services.batch.web.v1.model.form import (
    BatchCreateFormV1,
    BatchUpdateFormV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.services.batch.web.v1.model.view import (
    BatchStatsViewV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.services.batch.web.v1.param import BatchFilterParamV1
from toloka.a9s.client.models.utils import model_dump_a9s
from toloka.a9s.client.pagination import async_paginate
from toloka.a9s.client.sort import SortValue, from_sort_string, to_sort_string


class AsyncAnnotationStudioBatchesClient(AsyncBaseAnnotationStudioClient):
    async def create(self, form: BatchCreateFormV1) -> BatchViewV1Strict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/batches',
            body=model_dump_a9s(form),
        )
        return BatchViewV1Strict.model_validate(response.json())

    async def get(self, batch_id: str) -> BatchViewV1Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/batches/{batch_id}',
        )
        return BatchViewV1Strict.model_validate(response.json())

    async def update(self, batch_id: str, form: BatchUpdateFormV1) -> BatchViewV1Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/batches/{batch_id}',
            body=model_dump_a9s(form),
        )
        return BatchViewV1Strict.model_validate(response.json())

    async def find(self, query_params: BatchFilterParamV1) -> BatchListViewV1Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/batches',
            params=model_to_query_params(query_params),
        )
        return BatchListViewV1Strict.model_validate(response.json())

    async def get_all(self, query_params: BatchFilterParamV1) -> AsyncGenerator[BatchViewV1Strict, None]:
        sort_criteria: dict[str, SortValue]
        if query_params.sort is None:
            sort_criteria = {'id': 'asc'}
        else:
            sort_criteria = from_sort_string(query_params.sort)
            sort_criteria['id'] = 'asc'

        async def get_next_page(page: BatchListViewV1Strict | None) -> BatchListViewV1Strict:
            last_id = max(project.id for project in page.data) if page else None
            return await self.find(
                query_params.model_copy(update={'sort': to_sort_string(sort_criteria), 'id_gt': last_id})
            )

        batch: BatchViewV1Strict
        async for batch in async_paginate(get_next_page=get_next_page):
            yield batch

    async def stop(self, batch_id: str) -> BatchViewV1Strict:
        try:
            response = await self.client.make_request(
                method='POST',
                url=f'{self.V1_PREFIX}/batches/{batch_id}/stop',
                body=None,
            )
        except AnnotationStudioError as e:
            if e.status == 409 and e.detail == 'Batch is already stopped':
                return await self.get(batch_id=batch_id)
            raise e
        return BatchViewV1Strict.model_validate(response.json())

    async def start(self, batch_id: str) -> BatchViewV1Strict:
        try:
            response = await self.client.make_request(
                method='POST',
                url=f'{self.V1_PREFIX}/batches/{batch_id}/start',
                body=None,
            )
        except AnnotationStudioError as e:
            if e.status == 409 and e.detail == 'Batch is already started':
                return await self.get(batch_id=batch_id)
            raise e
        return BatchViewV1Strict.model_validate(response.json())

    async def complete(self, batch_id: str) -> BatchViewV1Strict:
        try:
            response = await self.client.make_request(
                method='POST',
                url=f'{self.V1_PREFIX}/batches/{batch_id}/complete',
                body=None,
            )
        except AnnotationStudioError as e:
            if e.status == 409 and e.detail == 'Batch is already completed':
                return await self.get(batch_id=batch_id)
            raise e
        return BatchViewV1Strict.model_validate(response.json())

    async def get_stats(self, batch_id: str) -> BatchStatsViewV1:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/batches/{batch_id}/stats',
        )
        return BatchStatsViewV1.model_validate(response.json())
