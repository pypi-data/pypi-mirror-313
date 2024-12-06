from typing import Any

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.annotation_process import (
    AnnotationProcessListViewStrict,
    UploadFormV1Strict,
    UploadViewV1Strict,
    is_annotation_process_instance,
)
from toloka.a9s.client.models.annotation_process.quorum import (
    QuorumAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    AnnotationProcessViewStrict,
    QuorumAnnotationProcessViewStrict,
    StatusWorkflowAnnotationProcessViewStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.web.ui.view import (
    AnnotationProcessesProgressView,
)
from toloka.a9s.client.models.types import AnnotationId
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationProcessesClient(AsyncBaseAnnotationStudioClient):
    async def get_all(
        self,
        annotation_id: str | None = None,
        annotation_group_id: str | None = None,
        batch_id: str | None = None,
    ) -> AnnotationProcessListViewStrict:
        params = {'annotation_id': annotation_id, 'annotation_group_id': annotation_group_id, 'batch_id': batch_id}
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.UI_API_PREFIX}/annotation-processes', params=params
        )
        return AnnotationProcessListViewStrict.model_validate(response.json())

    async def get(self, id: str) -> AnnotationProcessViewStrict[Any]:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.UI_API_PREFIX}/annotation-processes/{id}'
        )
        return AnnotationProcessViewStrict.model_validate(response.json())

    async def get_all_progress(self, batch_id: str) -> AnnotationProcessesProgressView:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.UI_API_PREFIX}/annotation-processes/progress', params={'batch_id': batch_id}
        )
        return AnnotationProcessesProgressView.model_validate(response.json())

    async def upload_data(self, form: UploadFormV1Strict) -> UploadViewV1Strict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/upload-data',
            body=model_dump_a9s(form),
        )
        return UploadViewV1Strict.model_validate(response.json())

    async def get_status_workflow(
        self, annotation_id: AnnotationId
    ) -> StatusWorkflowAnnotationProcessViewStrict | None:
        processes = [
            process
            for process in (await self.get_all(annotation_id=annotation_id)).processes
            if is_annotation_process_instance(process, StatusWorkflowAnnotationProcessViewDataStrict)
        ]
        if len(processes) == 0:
            return None
        assert len(processes) == 1, 'At most one status workflow per annotation is allowed'
        return processes[0]

    async def get_quorum(self, annotation_group_id: str) -> QuorumAnnotationProcessViewStrict | None:
        processes = [
            process
            for process in (await self.get_all(annotation_group_id=annotation_group_id)).processes
            if is_annotation_process_instance(process, QuorumAnnotationProcessViewDataStrict)
        ]
        if len(processes) == 0:
            return None
        assert len(processes) == 1, 'At most one quorum per annotation group is allowed'
        return processes[0]
