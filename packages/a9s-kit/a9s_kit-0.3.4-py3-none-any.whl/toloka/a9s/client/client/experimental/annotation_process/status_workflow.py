__all__ = [
    'AsyncAnnotationStudioStatusWorkflowClient',
    'StatusWorkflowAnnotationProcessViewStrict',
    'StatusWorkflowConfigViewStrict',
    'StatusWorkflowConfigForm',
    'UpdateStatusWorkflowForm',
]

from typing import Iterable

from pydantic import TypeAdapter

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowConfigBatchForm,
    StatusWorkflowConfigProjectForm,
    StatusWorkflowConfigViewStrict,
)
from toloka.a9s.client.models.annotation_process.view import StatusWorkflowAnnotationProcessViewStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.status_workflow.web.ui.form import (
    StatusWorkflowConfigForm,
    UpdateStatusWorkflowForm,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioStatusWorkflowClient(AsyncBaseAnnotationStudioClient):
    async def update_statuses(
        self, forms: Iterable[UpdateStatusWorkflowForm]
    ) -> list[StatusWorkflowAnnotationProcessViewStrict]:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/update-statuses',
            body=[model_dump_a9s(form) for form in forms],
        )
        return [StatusWorkflowAnnotationProcessViewStrict.model_validate(item) for item in response.json()]

    async def set_batch_defaults(self, form: StatusWorkflowConfigBatchForm) -> StatusWorkflowConfigViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/set-batch-defaults',
            body=model_dump_a9s(form),
        )
        return StatusWorkflowConfigViewStrict.model_validate(response.json())

    async def set_project_defaults(self, form: StatusWorkflowConfigProjectForm) -> StatusWorkflowConfigViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/set-project-defaults',
            body=model_dump_a9s(form),
        )
        return StatusWorkflowConfigViewStrict.model_validate(response.json())

    async def get_project_defaults(self, project_id: str) -> StatusWorkflowConfigViewStrict | None:
        try:
            response = await self.client.make_request(
                method='GET',
                params={'project_id': project_id},
                url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/get-project-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return StatusWorkflowConfigViewStrict.model_validate(response.json())

    async def get_batch_defaults(self, batch_id: str) -> StatusWorkflowConfigViewStrict | None:
        try:
            response = await self.client.make_request(
                method='GET',
                params={'batch_id': batch_id},
                url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/get-batch-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return StatusWorkflowConfigViewStrict.model_validate(response.json())

    async def get_possible_statuses(self, batch_id: str) -> list[str]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/get-possible-statuses',
            params={'batch_id': batch_id},
        )
        return TypeAdapter(list[str]).validate_python(response.json())
