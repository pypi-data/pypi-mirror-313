__all__ = [
    'AsyncAnnotationStudioQuorumClient',
    'QuorumAnnotationProcessViewStrict',
    'AssignQuorumForm',
    'UpdateQuorumForm',
    'QuorumConfigBatchForm',
    'QuorumConfigProjectForm',
    'AssignResultView',
    'QuorumConfigView',
]


from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.annotation_process.quorum import (
    QuorumConfigBatchForm,
    QuorumConfigProjectForm,
)
from toloka.a9s.client.models.annotation_process.view import QuorumAnnotationProcessViewStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.form import (
    AssignQuorumForm,
    UpdateQuorumForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.view import (
    AssignResultView,
    QuorumConfigView,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioQuorumClient(AsyncBaseAnnotationStudioClient):
    async def update_quorum(self, form: UpdateQuorumForm) -> QuorumAnnotationProcessViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.UI_API_PREFIX}/annotation-processes/quorum/update-quorum',
            body=model_dump_a9s(form),
        )
        return QuorumAnnotationProcessViewStrict.model_validate(response.json())

    async def assign(self, form: AssignQuorumForm) -> AssignResultView:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/annotation-processes/quorum/assign',
            body=model_dump_a9s(form),
        )
        return AssignResultView.model_validate(response.json())

    async def set_batch_defaults(self, form: QuorumConfigBatchForm) -> QuorumConfigView:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/annotation-processes/quorum/set-batch-defaults',
            body=model_dump_a9s(form),
        )
        return QuorumConfigView.model_validate(response.json())

    async def set_project_defaults(self, form: QuorumConfigProjectForm) -> QuorumConfigView:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/annotation-processes/quorum/set-project-defaults',
            body=model_dump_a9s(form),
        )
        return QuorumConfigView.model_validate(response.json())

    async def get_batch_defaults(self, batch_id: str) -> QuorumConfigView | None:
        try:
            response = await self.client.make_retriable_request(
                method='GET',
                params={'batch_id': batch_id},
                url=f'{self.UI_API_PREFIX}/annotation-processes/quorum/get-batch-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return QuorumConfigView.model_validate(response.json())

    async def get_project_defaults(self, project_id: str) -> QuorumConfigView | None:
        try:
            response = await self.client.make_request(
                method='GET',
                params={'project_id': project_id},
                url=f'{self.UI_API_PREFIX}/annotation-processes/quorum/get-project-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return QuorumConfigView.model_validate(response.json())
