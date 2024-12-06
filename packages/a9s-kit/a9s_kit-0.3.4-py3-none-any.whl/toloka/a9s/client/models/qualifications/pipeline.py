# pyright: reportGeneralTypeIssues=false

from typing import Literal, Sequence

from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.pipeline.config.domain import (
    PipelineStepsConfigV1,
)
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import (
    GetPipelineInstanceListQueryParams,
    PipelineConfigListView,
    PipelineConfigView,
    PipelineInstanceForm,
    PipelineInstanceListView,
    PipelineInstancePatchForm,
    PipelineInstanceView,
    ProgressLogListView,
    ProgressLogView,
)
from toloka.a9s.client.models.types import (
    PipelineConfigId,
    PipelineId,
    PipelineInstanceId,
    ProgressLogId,
)


class PipelineConfigViewStrict(PipelineConfigView):
    id: PipelineConfigId
    pipeline_id: PipelineId
    name: str
    description: str | None
    version: int
    status: Literal['ACTIVE', 'DISABLED']
    steps: PipelineStepsConfigV1
    created_at: str
    updated_at: str | None


class PipelineConfigListViewStrict(PipelineConfigListView):
    configs: Sequence[PipelineConfigViewStrict]


class PipelineInstanceViewStrict(PipelineInstanceView):
    id: PipelineInstanceId
    account_id: str
    pipeline_id: PipelineId
    pipeline_config_id: PipelineConfigId
    status: Literal['ACTIVE', 'FINISHED', 'FAILED']
    active_step_id: str | None
    completed_step_ids: Sequence[str]
    completed_idle_actions: Sequence[str]
    created_at: str
    updated_at: str | None


class PipelineInstanceListViewStrict(PipelineInstanceListView):
    instances: Sequence[PipelineInstanceViewStrict]


class PipelineInstanceFormStrict(PipelineInstanceForm):
    account_id: str
    pipeline_config_id: PipelineConfigId
    status: Literal['ACTIVE', 'FINISHED', 'FAILED'] | None
    active_step_id: str | None
    completed_step_ids: Sequence[str] | None
    completed_idle_actions: Sequence[str] | None


class PipelineInstancePatchFormStrict(PipelineInstancePatchForm):
    pipeline_config_id: PipelineConfigId | None
    status: Literal['ACTIVE', 'FINISHED', 'FAILED'] | None
    active_step_id: str | None
    completed_step_ids: Sequence[str] | None


class GetPipelineInstanceListQueryParamsStrict(GetPipelineInstanceListQueryParams):
    pipeline_config_id: PipelineConfigId | None
    status: Literal['ACTIVE', 'FINISHED', 'FAILED'] | None
    account_id: str | None


class ProgressLogViewStrict(ProgressLogView):
    id: ProgressLogId
    step_id: str
    step_result: Literal['PASSED', 'FAILED', 'SKIPPED', 'ON_REVIEW']
    created_at: str


class ProgressLogListViewStrict(ProgressLogListView):
    logs: Sequence[ProgressLogViewStrict]
