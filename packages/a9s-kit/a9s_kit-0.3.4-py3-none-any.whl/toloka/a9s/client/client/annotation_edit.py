from typing import AsyncGenerator

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.converter import model_to_query_params
from toloka.a9s.client.models.annotation_edit import AnnotationEditListV1Strict, AnnotationEditViewV1Strict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_edit.web.v1.annotation_edits.form import (
    AnnotationEditQueryParamsV1,
)
from toloka.a9s.client.pagination import async_paginate
from toloka.a9s.client.sort import SortValue, from_sort_string, to_sort_string


class AsyncAnnotationStudioAnnotationEditsClient(AsyncBaseAnnotationStudioClient):
    async def find(self, query_params: AnnotationEditQueryParamsV1) -> AnnotationEditListV1Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/annotation-edits',
            params=model_to_query_params(query_params),
        )
        return AnnotationEditListV1Strict.model_validate(response.json())

    async def get_all(
        self, query_params: AnnotationEditQueryParamsV1
    ) -> AsyncGenerator[AnnotationEditViewV1Strict, None]:
        sort_criteria: dict[str, SortValue]
        if query_params.sort is None:
            sort_criteria = {'id': 'asc'}
        else:
            sort_criteria = from_sort_string(query_params.sort)
            sort_criteria['id'] = 'asc'

        async def get_next_page(page: AnnotationEditListV1Strict | None) -> AnnotationEditListV1Strict:
            last_id = max(edit.id for edit in page.data) if page else None
            return await self.find(
                query_params.model_copy(update={'sort': to_sort_string(sort_criteria), 'id_gt': last_id})
            )

        edit: AnnotationEditViewV1Strict
        async for edit in async_paginate(get_next_page=get_next_page):
            yield edit
