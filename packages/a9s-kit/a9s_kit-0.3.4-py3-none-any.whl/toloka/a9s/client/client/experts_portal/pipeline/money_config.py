from typing import Sequence
from uuid import UUID

from toloka.a9s.client.base.client import AsyncBaseExpertsPortalClient
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import (
    PipelineMoneyConfigForm,
)
from toloka.a9s.client.models.money_config import PipelineMoneyConfigViewStrict
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncExpertsPortalPipelineMoneyConfigControllerClient(AsyncBaseExpertsPortalClient):
    async def get_versions(self, pipeline_config_id: UUID) -> Sequence[PipelineMoneyConfigViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V0_PREFIX}/pipeline/money-config',
            params={'pipeline_config_id': str(pipeline_config_id)},
        )
        return [
            PipelineMoneyConfigViewStrict.model_validate(item) for item in response.json()['pipeline_money_configs']
        ]

    async def create_version(self, form: PipelineMoneyConfigForm) -> PipelineMoneyConfigViewStrict:
        response = await self.client.make_request(
            method='POST', url=f'{self.V0_PREFIX}/pipeline/money-config', body=model_dump_a9s(form)
        )
        return PipelineMoneyConfigViewStrict.model_validate(response.json())

    async def get_version(self, version_id: UUID) -> PipelineMoneyConfigViewStrict:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.V0_PREFIX}/pipeline/money-config/{version_id}'
        )
        return PipelineMoneyConfigViewStrict.model_validate(response.json())
