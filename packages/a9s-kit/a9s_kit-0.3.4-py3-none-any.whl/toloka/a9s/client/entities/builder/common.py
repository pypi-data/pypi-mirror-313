from typing import Annotated, Mapping

from pydantic import BaseModel, ConfigDict, Field

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.status_workflow.web.ui.form import (
    StatusWorkflowTimeoutForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.status_workflow.web.ui.status_form import (  # noqa: E501
    StatusForm,
)


class StatusWorkflowForm(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    statuses: Mapping[str, StatusForm]
    timeouts: Mapping[str, StatusWorkflowTimeoutForm] | None = None


class QuorumForm(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    max_annotations: Annotated[int, Field(ge=1)]
    max_annotation_per_annotator: Annotated[int | None, Field(ge=1)] = None
    skip_allowed: bool | None = None
