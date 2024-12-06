__all__ = [
    'AsyncAnnotationStudioAnnotationMetricsClient',
    'AnnotationMetricCreateFormV1Strict',
    'AnnotationMetricUpdateFormV1Strict',
    'AnnotationMetricViewV1Strict',
]

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.annotation_metric import (
    AnnotationMetricCreateFormV1Strict,
    AnnotationMetricUpdateFormV1Strict,
    AnnotationMetricViewV1Strict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.metric import (
    AnnotationMetricCreateFormV1,
    AnnotationMetricUpdateFormV1,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioAnnotationMetricsClient(AsyncBaseAnnotationStudioClient):
    async def create(self, form: AnnotationMetricCreateFormV1) -> AnnotationMetricViewV1Strict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-metrics',
            body=model_dump_a9s(form),
        )
        return AnnotationMetricViewV1Strict.model_validate(response.json())

    async def get(self, metric_id: str) -> AnnotationMetricViewV1Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/annotation-metrics/{metric_id}',
        )
        return AnnotationMetricViewV1Strict.model_validate(response.json())

    async def update(self, metric_id: str, form: AnnotationMetricUpdateFormV1) -> AnnotationMetricViewV1Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-metrics/{metric_id}',
            body=model_dump_a9s(form),
        )
        return AnnotationMetricViewV1Strict.model_validate(response.json())

    async def delete(self, metric_id: str) -> None:
        await self.client.make_request(
            method='DELETE',
            url=f'{self.V1_PREFIX}/annotation-metrics/{metric_id}',
        )
