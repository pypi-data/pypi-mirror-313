__all__ = [
    'AsyncExpertsPortalMoneyConfigClient',
    'MoneyConfigFormStrict',
    'MoneyConfigIdViewStrict',
    'MoneyConfigViewStrict',
]

from uuid import UUID

from toloka.a9s.client.base.client import AsyncBaseExpertsPortalClient
from toloka.a9s.client.models.money_config import (
    MoneyConfigFormStrict,
    MoneyConfigIdViewStrict,
    MoneyConfigViewStrict,
)
from toloka.a9s.client.models.types import MoneyConfigId, MoneyConfigVersionId
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncExpertsPortalMoneyConfigClient(AsyncBaseExpertsPortalClient):
    async def create(
        self,
        form: MoneyConfigFormStrict,
    ) -> MoneyConfigIdViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/money/config',
            body=model_dump_a9s(form),
        )
        return MoneyConfigIdViewStrict.model_validate(response.json())

    async def create_new_version(
        self,
        config_id: UUID,
        form: MoneyConfigFormStrict,
    ) -> MoneyConfigIdViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/money/config/{config_id}',
            body=model_dump_a9s(form),
        )
        return MoneyConfigIdViewStrict.model_validate(response.json())

    async def get_version(self, config_id: MoneyConfigId, version_id: MoneyConfigVersionId) -> MoneyConfigViewStrict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/money/config/{config_id}/{version_id}',
        )
        return MoneyConfigViewStrict.model_validate(response.json())

    async def get_last_version(self, config_id: MoneyConfigId) -> MoneyConfigViewStrict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/money/config/{config_id}/last',
        )
        return MoneyConfigViewStrict.model_validate(response.json())

    async def get_all_versions(self, config_id: MoneyConfigId) -> list[MoneyConfigViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/money/config/{config_id}/all',
        )
        return [MoneyConfigViewStrict.model_validate(item) for item in response.json()]

    async def get_all_configs(self) -> list[MoneyConfigViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/money/config/all',
        )
        return [MoneyConfigViewStrict.model_validate(item) for item in response.json()]
