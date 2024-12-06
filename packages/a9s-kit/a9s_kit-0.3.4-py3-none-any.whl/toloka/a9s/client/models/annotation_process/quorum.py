# pyright: reportGeneralTypeIssues=false


from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_params import QuorumAnnotationProcessParameters
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model import QuorumAnnotationProcessView
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.form import (
    QuorumConfigForm,
)


class QuorumConfigBatchForm(QuorumConfigForm):
    batch_id: str
    project_id: None = None


class QuorumConfigProjectForm(QuorumConfigForm):
    batch_id: None = None
    project_id: str


class QuorumAnnotationProcessViewDataStrict(QuorumAnnotationProcessView):
    type: Literal['quorum'] = 'quorum'


class QuorumAnnotationProcessParametersStrict(QuorumAnnotationProcessParameters):
    type: Literal['quorum'] = 'quorum'
