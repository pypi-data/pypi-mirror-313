from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.quality_management.async_config import (
    AsyncQualityConfigFormV0Legacy,
    AsyncQualityConfigFormV0Strict,
    AsyncQualityConfigViewV0Strict,
)

AsyncQualityConfigForm = AsyncQualityConfigFormV0Strict | AsyncQualityConfigFormV0Legacy


class AsyncQmsAsyncQualityConfigClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX = f'{AsyncBaseAnnotationStudioClient.V0_PREFIX}/async-quality-config'

    async def get(self, id: str) -> AsyncQualityConfigViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.API_PREFIX}/{id}',
        )
        return AsyncQualityConfigViewV0Strict.model_validate(response.json())

    async def create(self, form: AsyncQualityConfigForm) -> AsyncQualityConfigViewV0Strict:
        response = await self.client.make_request(
            method='POST',
            url=self.API_PREFIX,
            body=form.model_dump(mode='json'),
        )
        return AsyncQualityConfigViewV0Strict.model_validate(response.json())

    async def update(self, id: str, form: AsyncQualityConfigForm) -> AsyncQualityConfigViewV0Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/{id}',
            body=form.model_dump(mode='json'),
        )
        return AsyncQualityConfigViewV0Strict.model_validate(response.json())
