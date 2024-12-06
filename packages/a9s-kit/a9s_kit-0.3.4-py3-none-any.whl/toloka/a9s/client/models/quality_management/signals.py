from dataclasses import dataclass
from string import Template
from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.viewform.condition import (
    SignalViewForm,
)
from toloka.a9s.client.models.utils import TemplateField


@dataclass
class StatusIsSignal(TemplateField):
    status: str

    @classmethod
    def get_template(cls) -> Template:
        return Template('status_is_${status}')

    @classmethod
    def get_pattern(cls) -> str:
        return r'^status_is_(?P<status>[\s]+)$'


@dataclass
class StatusWasSetToSignal(TemplateField):
    status: str

    @classmethod
    def get_template(cls) -> Template:
        return Template('status_was_set_to_${status}')

    @classmethod
    def get_pattern(cls) -> str:
        return r'^status_was_set_to_(?P<status>[\s]+)$'


@dataclass
class MetricIsSignal(TemplateField):
    metric: str

    @classmethod
    def get_template(cls) -> Template:
        return Template('metric_${metric}_is')

    @classmethod
    def get_pattern(cls) -> str:
        return r'^metric_(?P<metric>[\s]+)_is$'


@dataclass
class MetricWasSetToSignal(TemplateField):
    metric: str

    @classmethod
    def get_template(cls) -> Template:
        return Template('metric_${metric}_was_set_to')

    @classmethod
    def get_pattern(cls) -> str:
        return r'^metric_(?P<metric>[\s]+)_was_set_to$'


ContiniuousSignalName = (
    Literal[
        'annotation_edit_is_in_progress',
        'task_is_assigned',
        'task_is_actionable',
        'task_is_done',
    ]
    | StatusIsSignal
    | MetricIsSignal
)
InstantSignalName = (
    Literal[
        'annotation_edit_duration',
        'annotation_edit_was_created',
        'annotation_edit_was_done',
        'annotation_edit_was_skipped',
        'annotation_edit_was_expired',
        'task_was_assigned',
        'task_was_skipped',
        'task_was_expired',
        'task_was_revoked',
        'task_was_submitted',
        'task_action_duration',
        'task_was_done',
    ]
    | StatusWasSetToSignal
    | MetricWasSetToSignal
)
SignalName = ContiniuousSignalName | InstantSignalName | str


class SignalViewFormStrict(SignalViewForm):
    name: SignalName
