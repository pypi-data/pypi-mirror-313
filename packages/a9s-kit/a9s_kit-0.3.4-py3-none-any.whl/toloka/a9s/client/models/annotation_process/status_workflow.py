# pyright: reportGeneralTypeIssues=false


from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_params import StatusWorkflowAnnotationProcessParameters
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model import (
    StatusWorkflowAnnotationProcessView,
    StatusWorkflowAnnotationProcessViewUserView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.status_workflow.web.ui.form import (
    StatusWorkflowConfigForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.status_workflow.web.ui.view import (
    StatusWorkflowConfigView,
)
from toloka.a9s.client.models.types import StatusWorkflowConfigId


class StatusWorkflowConfigBatchForm(StatusWorkflowConfigForm):
    batch_id: str
    project_id: None = None


class StatusWorkflowConfigProjectForm(StatusWorkflowConfigForm):
    batch_id: None = None
    project_id: str


class StatusWorkflowAnnotationProcessViewUserViewStrict(StatusWorkflowAnnotationProcessViewUserView):
    account_id: str
    login: str


class StatusWorkflowAnnotationProcessViewDataStrict(StatusWorkflowAnnotationProcessView):
    responsible: StatusWorkflowAnnotationProcessViewUserViewStrict | None = None
    type: Literal['status-workflow'] = 'status-workflow'


class StatusWorkflowConfigViewStrict(StatusWorkflowConfigView):
    id: StatusWorkflowConfigId


class StatusWorkflowAnnotationProcessParametersStrict(StatusWorkflowAnnotationProcessParameters):
    type: Literal['status-workflow'] = 'status-workflow'
