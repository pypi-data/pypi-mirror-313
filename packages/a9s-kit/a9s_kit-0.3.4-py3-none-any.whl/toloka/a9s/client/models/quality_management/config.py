# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Literal, Sequence

from pydantic import BaseModel, Field
from typing_extensions import deprecated

from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.form import QualityConfigFormV0
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.view import QualityConfigViewV0
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.viewform import (
    QualityFilterViewForm,
    QualityMetricViewForm,
    RevokeAccessRuleViewForm,
)
from toloka.a9s.client.models.quality_management.conditions import AggregationViewFormStrict
from toloka.a9s.client.models.quality_management.rules import (
    AVERAGE_RULE_NAME,
    COUNT_RULE_NAME,
    AverageRuleParams,
    CountRuleParams,
)
from toloka.a9s.client.models.types import QualityConfigId
from toloka.a9s.client.models.utils import none_default_validator


@deprecated('Revoke access rules are deprecated, use filters instead')
class AverageRevokeAccessRuleViewForm(RevokeAccessRuleViewForm):
    name: Literal['AVERAGE'] = AVERAGE_RULE_NAME
    params: AverageRuleParams


@deprecated('Revoke access rules are deprecated, use filters instead')
class CountRevokeAccessRuleViewForm(RevokeAccessRuleViewForm):
    name: Literal['COUNT'] = COUNT_RULE_NAME
    params: CountRuleParams


RevokeAccessRuleViewFormStrict = AverageRevokeAccessRuleViewForm | CountRevokeAccessRuleViewForm


class AnnotationEditTimeParams(BaseModel):
    metric_name: str
    cumulative_metric_name: str


class AnnotationEditTimeViewFormStrict(QualityMetricViewForm):
    type: Literal['ANNOTATION_EDIT_TIME'] = 'ANNOTATION_EDIT_TIME'
    params: AnnotationEditTimeParams


QualityMetricViewFormStrict = AnnotationEditTimeViewFormStrict


class QualityFilterViewFormStrict(QualityFilterViewForm):
    conditions: Annotated[
        Sequence[AggregationViewFormStrict],
        Field(max_length=1),
    ]


@deprecated('Revoke access rules are deprecated, use filters instead')
class QualityConfigFormV0Legacy(QualityConfigFormV0):
    revoke_access_rules: Sequence[RevokeAccessRuleViewFormStrict]
    metrics: Sequence[QualityMetricViewFormStrict]


class QualityConfigFormV0Strict(QualityConfigFormV0):
    metrics: Sequence[QualityMetricViewFormStrict]
    filters: Sequence[QualityFilterViewFormStrict]


class QualityConfigViewV0Strict(QualityConfigViewV0):
    id: QualityConfigId
    metrics: Annotated[
        Sequence[AnnotationEditTimeViewFormStrict],
        Field(default_factory=list),
        none_default_validator(default_factory=list),
    ]
    filters: Annotated[
        Sequence[QualityFilterViewFormStrict],
        Field(default_factory=list),
        none_default_validator(default_factory=list),
    ]
    created_at: str

    revoke_access_rules: Annotated[
        Sequence[RevokeAccessRuleViewFormStrict] | None,
        Field(deprecated='Revoke access rules are deprecated, use filters instead'),
    ] = None
