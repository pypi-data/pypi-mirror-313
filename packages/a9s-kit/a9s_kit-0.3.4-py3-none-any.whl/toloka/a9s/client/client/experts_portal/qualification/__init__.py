from typing import Sequence
from uuid import UUID

from toloka.a9s.client.base.client import AsyncBaseExpertsPortalClient
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import (
    QualificationForm,
    QualificationLegacyForm,
)
from toloka.a9s.client.models.qualifications.qualification import (
    QualificationLegacyListViewStrict,
    QualificationLegacyViewStrict,
    QualificationListViewStrict,
    QualificationViewStrict,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncExpertsPortalQualificationControllerClient(AsyncBaseExpertsPortalClient):
    async def get_list(self) -> Sequence[QualificationViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V0_PREFIX}/qualification',
        )
        return QualificationListViewStrict.model_validate(response.json()).qualifications

    async def create(self, form: QualificationForm) -> QualificationViewStrict:
        response = await self.client.make_request(
            method='POST', url=f'{self.V0_PREFIX}/qualification', body=model_dump_a9s(form)
        )
        return QualificationViewStrict.model_validate(response.json())

    async def get(self, qualification_id: UUID) -> QualificationViewStrict:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.V0_PREFIX}/qualification/{qualification_id}'
        )
        return QualificationViewStrict.model_validate(response.json())

    async def update(self, qualification_id: UUID, form: QualificationForm) -> QualificationViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V0_PREFIX}/qualification/{qualification_id}',
            body=model_dump_a9s(form),
        )
        return QualificationViewStrict.model_validate(response.json())

    async def get_legacy_list(self, qualification_id: UUID | None = None) -> Sequence[QualificationLegacyViewStrict]:
        params = {'qualification_id': str(qualification_id)} if qualification_id else None
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V0_PREFIX}/qualification/legacy',
            params=params,
        )
        return QualificationLegacyListViewStrict.model_validate(response.json()).legacy_qualifications

    async def create_legacy(self, form: QualificationLegacyForm) -> QualificationLegacyViewStrict:
        response = await self.client.make_request(
            method='POST', url=f'{self.V0_PREFIX}/qualification/legacy', body=model_dump_a9s(form)
        )
        return QualificationLegacyViewStrict.model_validate(response.json())

    async def get_legacy(self, qualification_id: UUID) -> QualificationLegacyViewStrict:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.V0_PREFIX}/qualification/legacy/{qualification_id}'
        )
        return QualificationLegacyViewStrict.model_validate(response.json())

    async def update_legacy(
        self, qualification_id: UUID, form: QualificationLegacyForm
    ) -> QualificationLegacyViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V0_PREFIX}/qualification/legacy/{qualification_id}',
            body=model_dump_a9s(form),
        )
        return QualificationLegacyViewStrict.model_validate(response.json())

    async def delete_legacy(self, qualification_id: UUID) -> None:
        await self.client.make_retriable_request(
            method='DELETE', url=f'{self.V0_PREFIX}/qualification/legacy/{qualification_id}'
        )
