from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.annotation_process.view import PostAcceptanceAnnotationProcessViewStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.post_acceptance.web.ui.form import (
    UpdateVerdictForm,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioPostAcceptanceClient(AsyncBaseAnnotationStudioClient):
    async def update_verdict(self, form: UpdateVerdictForm) -> PostAcceptanceAnnotationProcessViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.UI_API_PREFIX}/annotation-processes/post-acceptance/update-verdict',
            body=model_dump_a9s(form),
        )
        return PostAcceptanceAnnotationProcessViewStrict.model_validate(response.json())
