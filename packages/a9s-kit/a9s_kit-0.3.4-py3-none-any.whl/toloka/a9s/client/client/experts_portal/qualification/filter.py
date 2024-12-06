from typing import Sequence
from uuid import UUID

from toloka.a9s.client.base.client import AsyncBaseExpertsPortalClient
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import (
    QualificationFilterForm,
)
from toloka.a9s.client.models.qualifications.qualification import (
    MatchFilterResultStrict,
    QualificationFilterViewStrict,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncExpertsPortalQualificationFilterControllerClient(AsyncBaseExpertsPortalClient):
    async def get_all(self) -> Sequence[QualificationFilterViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V0_PREFIX}/qualification/filter',
        )
        return [QualificationFilterViewStrict.model_validate(item) for item in response.json()]

    async def create(self, form: QualificationFilterForm) -> QualificationFilterViewStrict:
        response = await self.client.make_request(
            method='POST', url=f'{self.V0_PREFIX}/qualification/filter', body=model_dump_a9s(form)
        )
        return QualificationFilterViewStrict.model_validate(response.json())

    async def get(self, filter_id: UUID) -> QualificationFilterViewStrict:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.V0_PREFIX}/qualification/filter/{filter_id}'
        )
        return QualificationFilterViewStrict.model_validate(response.json())

    async def update(self, filter_id: UUID, form: QualificationFilterForm) -> QualificationFilterViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V0_PREFIX}/qualification/filter/{filter_id}',
            body=model_dump_a9s(form),
        )
        return QualificationFilterViewStrict.model_validate(response.json())

    async def match(self, filter_id: UUID, user_id: str) -> MatchFilterResultStrict:
        response = await self.client.make_request(
            method='POST', url=f'{self.V0_PREFIX}/qualification/filter/{filter_id}/match/{user_id}', body=None
        )
        return MatchFilterResultStrict.model_validate(response.json())
