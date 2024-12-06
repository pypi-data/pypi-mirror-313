from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.generated.ai.toloka.gts.config.web.v0.form import (
    GroundTruthConfigForm,
)
from toloka.a9s.client.models.generated.ai.toloka.gts.web.v0.form import (
    GroundTruthBucketForm,
    GroundTruthForm,
)
from toloka.a9s.client.models.ground_truth import (
    GroundTruthBucketViewV0Strict,
    GroundTruthConfigViewV0Strict,
    GroundTruthListViewV0Strict,
    GroundTruthViewV0Strict,
)
from toloka.a9s.client.models.types import GroundTruthBucketId, GroundTruthConfigId, GroundTruthId
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncGroundTruthConfigClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX: str = f'{AsyncBaseAnnotationStudioClient.V0_PREFIX}/ground-truth-config'

    async def get(self, id: GroundTruthConfigId) -> GroundTruthConfigViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.API_PREFIX}/{id}',
        )
        return GroundTruthConfigViewV0Strict.model_validate(response.json())

    async def update(self, id: GroundTruthConfigId, form: GroundTruthConfigForm) -> GroundTruthConfigViewV0Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/{id}',
            body=model_dump_a9s(form),
        )
        return GroundTruthConfigViewV0Strict.model_validate(response.json())

    async def delete(self, id: GroundTruthConfigId) -> None:
        await self.client.make_request(
            method='DELETE',
            url=f'{self.API_PREFIX}/{id}',
        )

    async def create(self, form: GroundTruthConfigForm) -> GroundTruthConfigViewV0Strict:
        response = await self.client.make_request(
            method='POST',
            url=self.API_PREFIX,
            body=model_dump_a9s(form),
        )
        return GroundTruthConfigViewV0Strict.model_validate(response.json())


class AsyncGroundTruthBucketClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX: str = f'{AsyncBaseAnnotationStudioClient.V0_PREFIX}/ground-truth-bucket'

    async def get(self, id: GroundTruthBucketId) -> GroundTruthBucketViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.API_PREFIX}/{id}',
        )
        return GroundTruthBucketViewV0Strict.model_validate(response.json())

    async def update(self, id: GroundTruthBucketId, form: GroundTruthBucketForm) -> GroundTruthBucketViewV0Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/{id}',
            body=model_dump_a9s(form),
        )
        return GroundTruthBucketViewV0Strict.model_validate(response.json())

    async def create(self, form: GroundTruthBucketForm) -> GroundTruthBucketViewV0Strict:
        response = await self.client.make_request(
            method='POST',
            url=self.API_PREFIX,
            body=model_dump_a9s(form),
        )
        return GroundTruthBucketViewV0Strict.model_validate(response.json())


class AsyncGroundTruthClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX: str = f'{AsyncBaseAnnotationStudioClient.V0_PREFIX}/ground-truth'

    async def get(self, id: GroundTruthId) -> GroundTruthViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.API_PREFIX}/{id}',
        )
        return GroundTruthViewV0Strict.model_validate(response.json())

    async def update(self, id: GroundTruthId, form: GroundTruthForm) -> GroundTruthViewV0Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/{id}',
            body=model_dump_a9s(form),
        )
        return GroundTruthViewV0Strict.model_validate(response.json())

    async def get_by_bucket(self, bucket_id: GroundTruthBucketId) -> GroundTruthListViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=self.API_PREFIX,
            params={'bucket_id': bucket_id},
        )
        return GroundTruthListViewV0Strict.model_validate(response.json())

    async def create(self, form: GroundTruthForm) -> GroundTruthViewV0Strict:
        response = await self.client.make_request(
            method='POST',
            url=self.API_PREFIX,
            body=model_dump_a9s(form),
        )
        return GroundTruthViewV0Strict.model_validate(response.json())
