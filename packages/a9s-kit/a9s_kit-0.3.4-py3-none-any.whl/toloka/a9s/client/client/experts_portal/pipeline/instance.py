from typing import Sequence
from uuid import UUID

from toloka.a9s.client.base.client import AsyncBaseExpertsPortalClient
from toloka.a9s.client.models.qualifications.pipeline import (
    GetPipelineInstanceListQueryParamsStrict,
    PipelineInstanceFormStrict,
    PipelineInstancePatchFormStrict,
    PipelineInstanceViewStrict,
    ProgressLogListViewStrict,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncExpertsPortalPipelineInstanceControllerClient(AsyncBaseExpertsPortalClient):
    async def get_list(
        self, query_params: GetPipelineInstanceListQueryParamsStrict
    ) -> Sequence[PipelineInstanceViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V0_PREFIX}/pipeline/instance',
            params=model_dump_a9s(query_params),
        )
        return [PipelineInstanceViewStrict.model_validate(item) for item in response.json()['instances']]

    async def create(self, form: PipelineInstanceFormStrict) -> PipelineInstanceViewStrict:
        response = await self.client.make_request(
            method='POST', url=f'{self.V0_PREFIX}/pipeline/instance', body=model_dump_a9s(form)
        )
        return PipelineInstanceViewStrict.model_validate(response.json())

    async def drop_progress(self, pipeline_id: str, account_id: str) -> None:
        await self.client.make_retriable_request(
            method='DELETE',
            url=f'{self.V0_PREFIX}/pipeline/instance',
            params={'pipeline_id': pipeline_id, 'account_id': account_id},
        )

    async def get(self, instance_id: UUID) -> PipelineInstanceViewStrict:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.V0_PREFIX}/pipeline/instance/{instance_id}'
        )
        return PipelineInstanceViewStrict.model_validate(response.json())

    async def patch(self, instance_id: UUID, form: PipelineInstancePatchFormStrict) -> PipelineInstanceViewStrict:
        response = await self.client.make_retriable_request(
            method='PATCH',
            url=f'{self.V0_PREFIX}/pipeline/instance/{instance_id}',
            body=model_dump_a9s(form),
        )
        return PipelineInstanceViewStrict.model_validate(response.json())

    async def get_logs(self, instance_id: UUID) -> ProgressLogListViewStrict:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.V0_PREFIX}/pipeline/instance/{instance_id}/logs'
        )
        return ProgressLogListViewStrict.model_validate(response.json())
