from typing import Sequence
from uuid import UUID

from toloka.a9s.client.base.client import AsyncBaseExpertsPortalClient
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import UserQualificationForm
from toloka.a9s.client.models.qualifications.user_qualification import UserQualificationViewStrict
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncExpertsPortalUserQualificationControllerClient(AsyncBaseExpertsPortalClient):
    async def create(self, form: UserQualificationForm) -> UserQualificationViewStrict:
        response = await self.client.make_request(
            method='POST', url=f'{self.V0_PREFIX}/user-qualification', body=model_dump_a9s(form)
        )
        return UserQualificationViewStrict.model_validate(response.json())

    async def delete(self, user_qualification_id: UUID) -> None:
        await self.client.make_retriable_request(
            method='DELETE', url=f'{self.V0_PREFIX}/user-qualification/{user_qualification_id}'
        )

    async def get_user_qualifications(self, account_id: str) -> Sequence[UserQualificationViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.V0_PREFIX}/user-qualification/user/{account_id}'
        )
        return [UserQualificationViewStrict.model_validate(item) for item in response.json()]
