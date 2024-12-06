from typing import Sequence
from uuid import UUID

from toloka.a9s.client.base.client import AsyncBaseExpertsPortalClient
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import (
    PipelineConfigForm,
    PipelineConfigPatchForm,
)
from toloka.a9s.client.models.qualifications.pipeline import (
    PipelineConfigListViewStrict,
    PipelineConfigViewStrict,
)
from toloka.a9s.client.models.types import PipelineId
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncExpertsPortalPipelineConfigControllerClient(AsyncBaseExpertsPortalClient):
    async def create(self, form: PipelineConfigForm) -> PipelineConfigViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V0_PREFIX}/pipeline/config',
            body=model_dump_a9s(form),
        )
        return PipelineConfigViewStrict.model_validate(response.json())

    async def get_all_latest(self) -> Sequence[PipelineConfigViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.V0_PREFIX}/pipeline/config/latest'
        )
        return PipelineConfigListViewStrict.model_validate(response.json()).configs

    async def get_all(self, pipeline_id: PipelineId) -> Sequence[PipelineConfigViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET', params={'pipeline_id': pipeline_id}, url=f'{self.V0_PREFIX}/pipeline/config'
        )
        return PipelineConfigListViewStrict.model_validate(response.json()).configs

    async def patch(self, config_id: UUID, form: PipelineConfigPatchForm) -> PipelineConfigViewStrict:
        response = await self.client.make_retriable_request(
            method='PATCH',
            url=f'{self.V0_PREFIX}/pipeline/config/{config_id}',
            body=model_dump_a9s(form),
        )
        return PipelineConfigViewStrict.model_validate(response.json())
