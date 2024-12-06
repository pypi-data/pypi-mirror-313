__all__ = [
    'AnnotationFilterParamV1Strict',
    'UploadAnnotationFormV1Strict',
    'UploadAnnotationViewV1Strict',
    'AnnotationViewV1Strict',
    'EditAnnotationFormV1Strict',
    'AnnotationListViewV1Strict',
    'AsyncAnnotationStudioAnnotationsClient',
]


from typing import Any, AsyncGenerator, Mapping, overload

from pydantic import BaseModel

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.converter import model_to_query_params
from toloka.a9s.client.models.annotation import (
    AnnotationFilterParamV1Strict,
    AnnotationListViewV1Strict,
    AnnotationViewV1Strict,
    EditAnnotationFormV1Strict,
    UploadAnnotationFormV1Strict,
    UploadAnnotationViewV1Strict,
    ValuesType,
    get_annotation_values_type,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.form import (
    EditAnnotationFormV1,
    UploadAnnotationFormV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.param import AnnotationFilterParamV1
from toloka.a9s.client.models.utils import model_dump_a9s
from toloka.a9s.client.pagination import async_paginate
from toloka.a9s.client.sort import SortValue, from_sort_string, to_sort_string


class AsyncAnnotationStudioAnnotationsClient(AsyncBaseAnnotationStudioClient):
    @overload
    async def upload(
        self, form: UploadAnnotationFormV1Strict[ValuesType]
    ) -> UploadAnnotationViewV1Strict[ValuesType]: ...

    @overload
    async def upload(self, form: UploadAnnotationFormV1) -> UploadAnnotationViewV1Strict[Any]: ...

    async def upload(
        self, form: UploadAnnotationFormV1 | UploadAnnotationFormV1Strict[ValuesType]
    ) -> UploadAnnotationViewV1Strict[Any]:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotations',
            body=model_dump_a9s(form),
        )

        annotation_values_type: type[ValuesType] | None
        if isinstance(form, UploadAnnotationFormV1Strict):
            annotation_values_type = get_annotation_values_type(type(form))
        else:
            annotation_values_type = None

        result_type: type[UploadAnnotationViewV1Strict[Any]]
        if annotation_values_type is None:
            result_type = UploadAnnotationViewV1Strict[Mapping[str, Any]]
        else:
            result_type = UploadAnnotationViewV1Strict[annotation_values_type]  # type: ignore[valid-type]

        return result_type.model_validate(response.json())

    @overload
    async def get(
        self,
        annotation_id: str,
        values_type: type[ValuesType],
    ) -> AnnotationViewV1Strict[ValuesType]: ...

    @overload
    async def get(
        self,
        annotation_id: str,
        values_type: None = None,
    ) -> AnnotationViewV1Strict[Mapping[str, Any]]: ...

    async def get(
        self,
        annotation_id: str,
        values_type: type[ValuesType] | None = None,
    ) -> AnnotationViewV1Strict[ValuesType] | AnnotationViewV1Strict[Mapping[str, Any]]:
        view_values_type: type[ValuesType] | type[Mapping[str, Any]]
        if values_type is None:
            view_values_type = Mapping[str, Any]  # type: ignore[type-abstract]
        else:
            view_values_type = values_type

        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/annotations/{annotation_id}',
        )
        return AnnotationViewV1Strict[view_values_type].model_validate(response.json())  # type: ignore[valid-type]

    @overload
    async def edit(
        self, annotation_id: str, form: EditAnnotationFormV1Strict[ValuesType]
    ) -> AnnotationViewV1Strict[ValuesType]: ...

    @overload
    async def edit(
        self, annotation_id: str, form: EditAnnotationFormV1
    ) -> AnnotationViewV1Strict[Mapping[str, Any]] | AnnotationViewV1Strict[BaseModel]: ...

    async def edit(
        self, annotation_id: str, form: EditAnnotationFormV1 | EditAnnotationFormV1Strict[ValuesType]
    ) -> AnnotationViewV1Strict[Any]:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotations/{annotation_id}/edit',
            body=model_dump_a9s(form),
        )

        annotation_values_type: type[ValuesType] | None
        if isinstance(form, EditAnnotationFormV1Strict):
            annotation_values_type = get_annotation_values_type(type(form))
        else:
            annotation_values_type = None

        result_type: type[AnnotationViewV1Strict[Any]]
        if annotation_values_type is None:
            result_type = AnnotationViewV1Strict[type(form.values)]  # type: ignore[misc,assignment]
        else:
            result_type = AnnotationViewV1Strict[annotation_values_type]  # type: ignore[valid-type]
        return result_type.model_validate(response.json())

    @overload
    async def find(
        self,
        query_params: AnnotationFilterParamV1,
        values_type: type[ValuesType],
    ) -> AnnotationListViewV1Strict[ValuesType]: ...

    @overload
    async def find(
        self,
        query_params: AnnotationFilterParamV1,
        values_type: None = None,
    ) -> AnnotationListViewV1Strict[Mapping[str, Any]]: ...

    async def find(
        self,
        query_params: AnnotationFilterParamV1,
        values_type: type[ValuesType] | None = None,
    ) -> AnnotationListViewV1Strict[ValuesType] | AnnotationListViewV1Strict[Mapping[str, Any]]:
        view_values_type: type[ValuesType | Mapping[str, Any]]
        if values_type is None:
            view_values_type = Mapping[str, Any]  # type: ignore[type-abstract]
        else:
            view_values_type = values_type

        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/annotations',
            params=model_to_query_params(query_params),
        )
        return AnnotationListViewV1Strict[view_values_type].model_validate(response.json())  # type: ignore[valid-type]

    @overload
    async def get_all(
        self,
        query_params: AnnotationFilterParamV1,
        values_type: type[ValuesType],
    ) -> AsyncGenerator[AnnotationViewV1Strict[ValuesType], None]:
        yield None  # type: ignore

    @overload
    async def get_all(
        self,
        query_params: AnnotationFilterParamV1,
        values_type: None = None,
    ) -> AsyncGenerator[AnnotationViewV1Strict[Mapping[str, Any]], None]:
        yield None  # type: ignore

    async def get_all(
        self,
        query_params: AnnotationFilterParamV1,
        values_type: type[ValuesType] | None = None,
    ) -> (
        AsyncGenerator[AnnotationViewV1Strict[ValuesType], None]
        | AsyncGenerator[AnnotationViewV1Strict[Mapping[str, Any]], None]
    ):
        sort_criteria: dict[str, SortValue]
        if query_params.sort is None:
            sort_criteria = {'id': 'asc'}
        else:
            sort_criteria = from_sort_string(query_params.sort)
            sort_criteria['id'] = 'asc'

        async def get_next_page(
            page: AnnotationListViewV1Strict[Any] | None,
        ) -> AnnotationListViewV1Strict[Any]:
            last_id = max(annotation.id for annotation in page.data) if page else None
            return await self.find(
                query_params.model_copy(update={'sort': to_sort_string(sort_criteria), 'id_gt': last_id}),
                values_type=values_type,
            )

        annotation: AnnotationViewV1Strict[Any]
        async for annotation in async_paginate(get_next_page=get_next_page):
            yield annotation
