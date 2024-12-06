from typing import AsyncGenerator

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.converter import model_to_query_params
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.restriction.web.v0.form import (
    GetRestrictionListQueryParamsV0,
    RestrictionFormV0,
)
from toloka.a9s.client.models.quality_management.restriction import RestrictionListViewV0Strict, RestrictionViewV0Strict
from toloka.a9s.client.pagination import async_paginate
from toloka.a9s.client.sort import SortValue, from_sort_string, to_sort_string


class AsyncQmsRestrictionClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX = f'{AsyncBaseAnnotationStudioClient.V0_PREFIX}/restrictions'

    async def get(self, id: str) -> RestrictionViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.API_PREFIX}/{id}',
        )
        return RestrictionViewV0Strict.model_validate(response.json())

    async def create(self, form: RestrictionFormV0) -> RestrictionViewV0Strict:
        response = await self.client.make_request(
            method='POST',
            url=self.API_PREFIX,
            body=form.model_dump(mode='json'),
        )
        return RestrictionViewV0Strict.model_validate(response.json())

    async def update(self, id: str, form: RestrictionFormV0) -> RestrictionViewV0Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/{id}',
            body=form.model_dump(mode='json'),
        )
        return RestrictionViewV0Strict.model_validate(response.json())

    async def delete(self, id: str) -> None:
        await self.client.make_retriable_request(
            method='DELETE',
            url=f'{self.API_PREFIX}/{id}',
        )

    async def find(self, query_params: GetRestrictionListQueryParamsV0) -> RestrictionListViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=self.API_PREFIX,
            params=model_to_query_params(query_params),
        )
        return RestrictionListViewV0Strict.model_validate(response.json())

    async def get_all(
        self, query_params: GetRestrictionListQueryParamsV0
    ) -> AsyncGenerator[RestrictionViewV0Strict, None]:
        sort_criteria: dict[str, SortValue]
        if query_params.sort is None:
            sort_criteria = {'id': 'asc'}
        else:
            sort_criteria = from_sort_string(query_params.sort)
            sort_criteria['id'] = 'asc'

        async def get_next_page(page: RestrictionListViewV0Strict | None) -> RestrictionListViewV0Strict:
            last_id = max(restriction.id for restriction in page.data) if page else None
            return await self.find(
                query_params.model_copy(update={'sort': to_sort_string(sort_criteria), 'id_gt': last_id})
            )

        restriction: RestrictionListViewV0Strict
        async for restriction in async_paginate(get_next_page=get_next_page):
            yield restriction
