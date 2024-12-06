# pyright: reportGeneralTypeIssues=false

__all__ = [
    'MoneyConfigAnnotationSettingsStrict',
    'MoneyConfigForm',
    'MoneyConfigFormStrict',
    'MoneyConfigIdViewStrict',
    'MoneyConfigStatusWorkflowSettingsStrict',
    'MoneyConfigViewStrict',
    'PipelineMoneyConfigViewStrict',
    'PipelineMoneyConfigListViewStrict',
]

from typing import Literal, Sequence
from uuid import UUID

from toloka.a9s.client.models.generated.ai.toloka.experts.portal.money.repository.config import (
    MoneyConfigAnnotationSettings,
    MoneyConfigCommonSettings,
    MoneyConfigSnippetSettings,
    MoneyConfigStatusWorkflowSettings,
)
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.money.web import (
    MoneyConfigForm,
    MoneyConfigIdView,
    MoneyConfigView,
)
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import (
    PipelineMoneyConfigListView,
    PipelineMoneyConfigView,
)
from toloka.a9s.client.models.types import MoneyConfigId, MoneyConfigVersionId


class MoneyConfigIdViewStrict(MoneyConfigIdView):
    config_id: MoneyConfigId
    version_id: MoneyConfigVersionId


class MoneyConfigStatusWorkflowSettingsStrict(MoneyConfigStatusWorkflowSettings):
    type: Literal['status_workflow'] = 'status_workflow'


class MoneyConfigAnnotationSettingsStrict(MoneyConfigAnnotationSettings):
    type: Literal['annotation'] = 'annotation'


# TODO: check that price in specific_settings and snippet_settings is the same
class MoneyConfigFormStrict(MoneyConfigForm):
    name: str
    currency: Literal['BU', 'USD'] = 'BU'
    requester_id: str
    snippet_settings: MoneyConfigSnippetSettings
    common_settings: MoneyConfigCommonSettings
    specific_settings: MoneyConfigAnnotationSettingsStrict | MoneyConfigStatusWorkflowSettingsStrict


class MoneyConfigViewStrict(MoneyConfigView):
    config_id: MoneyConfigId
    version_id: MoneyConfigVersionId
    created_at: str
    created_by_account_id: str
    requester_id: str


class PipelineMoneyConfigViewStrict(PipelineMoneyConfigView):
    pipeline_config_id: UUID
    version_id: MoneyConfigVersionId
    created_at: str
    currency: Literal['USD', 'BU']
    requester_id: str


class PipelineMoneyConfigListViewStrict(PipelineMoneyConfigListView):
    pipeline_money_configs: Sequence[PipelineMoneyConfigViewStrict]
