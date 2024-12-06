from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.quality_management.config import (
    QualityConfigFormV0Legacy,
    QualityConfigFormV0Strict,
    QualityConfigViewV0Strict,
)
from toloka.a9s.client.models.types import QualityConfigId

QualityConfigForm = QualityConfigFormV0Strict | QualityConfigFormV0Legacy


class AsyncQmsQualityConfigClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX = f'{AsyncBaseAnnotationStudioClient.V0_PREFIX}/quality-config'

    async def get(self, id: QualityConfigId) -> QualityConfigViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.API_PREFIX}/{id}',
        )
        return QualityConfigViewV0Strict.model_validate(response.json())

    async def create(self, form: QualityConfigForm) -> QualityConfigViewV0Strict:
        response = await self.client.make_request(
            method='POST',
            url=self.API_PREFIX,
            body=form.model_dump(mode='json'),
        )
        return QualityConfigViewV0Strict.model_validate(response.json())

    async def update(self, id: QualityConfigId, form: QualityConfigForm) -> QualityConfigViewV0Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/{id}',
            body=form.model_dump(mode='json'),
        )
        return QualityConfigViewV0Strict.model_validate(response.json())
