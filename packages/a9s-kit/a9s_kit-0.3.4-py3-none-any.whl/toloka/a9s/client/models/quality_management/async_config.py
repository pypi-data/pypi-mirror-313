# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Literal, Sequence

from pydantic import BaseModel, Field
from typing_extensions import Self, deprecated

from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.form import AsyncQualityConfigFormV0
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.view import AsyncQualityConfigViewV0
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.viewform import (
    QualityActionViewForm,
    QualityRuleViewForm,
    QualityTriggerViewForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.viewform.condition import (
    AggregatedByAccountThresholdConditionViewForm,
    AnnotationNumberViewForm,
    TagsViewForm,
)
from toloka.a9s.client.models.quality_management.conditions import (
    AggregationByAnnotationByAccountConditionViewFormStrict,
    AggregationFunctionWithValueViewFormStrict,
    AggregationViewFormStrict,
    BasicAggregationFunctionViewFormStrict,
    WindowViewFormStrict,
)
from toloka.a9s.client.models.quality_management.rules import (
    AVERAGE_RULE_NAME,
    COUNT_RULE_NAME,
    AverageRuleParams,
    CountRuleParams,
)
from toloka.a9s.client.models.quality_management.signals import SignalViewFormStrict
from toloka.a9s.client.models.types import AsyncQualityConfigId, ProjectId
from toloka.a9s.client.models.utils import none_default_validator


class _BaseCreateRestrictionQualityActionParams(BaseModel):
    prolong_if_exists: bool | None = None
    period_hours: int | None = None
    period_days: int | None = None


class CreateProjectRestrictionQualityActionParams(_BaseCreateRestrictionQualityActionParams):
    scope: Literal['PROJECT'] = 'PROJECT'
    project_ids: Sequence[str]


class CreateBatchRestrictionQualityActionParams(_BaseCreateRestrictionQualityActionParams):
    scope: Literal['BATCH'] = 'BATCH'
    batch_ids: Sequence[str]


class CreateAllProjectsRestrictionQualityActionParams(_BaseCreateRestrictionQualityActionParams):
    scope: Literal['ALL_PROJECTS'] = 'ALL_PROJECTS'


CreateRestrictionQualityActionParams = (
    CreateProjectRestrictionQualityActionParams
    | CreateBatchRestrictionQualityActionParams
    | CreateAllProjectsRestrictionQualityActionParams
)


class CreateRestrictionQualityActionViewForm(QualityActionViewForm):
    action: Literal['create_restriction'] = 'create_restriction'
    params: CreateRestrictionQualityActionParams


QualityActionViewFormStrict = CreateRestrictionQualityActionViewForm


@deprecated('Rules are deprecated, use triggers instead')
class AverageQualityRuleViewForm(QualityRuleViewForm):
    name: Literal['AVERAGE'] = AVERAGE_RULE_NAME
    params: AverageRuleParams
    actions: Sequence[QualityActionViewFormStrict]


@deprecated('Rules are deprecated, use triggers instead')
class CountQualityRuleViewForm(QualityRuleViewForm):
    name: Literal['COUNT'] = COUNT_RULE_NAME
    params: CountRuleParams
    actions: Sequence[QualityActionViewFormStrict]


QualityRuleViewFormStrict = AverageQualityRuleViewForm | CountQualityRuleViewForm


class QualityTriggerViewFormStrict(QualityTriggerViewForm):
    conditions: Annotated[
        Sequence[AggregationViewFormStrict],
        Field(max_length=1),  # Only one condition is allowed for now
    ]
    actions: Sequence[QualityActionViewFormStrict]


@deprecated('Rules are deprecated, use triggers instead')
class AsyncQualityConfigFormV0Legacy(AsyncQualityConfigFormV0):
    rules: Sequence[QualityRuleViewFormStrict]


class AsyncQualityConfigFormV0Strict(AsyncQualityConfigFormV0):
    triggers: Sequence[QualityTriggerViewFormStrict]

    @classmethod
    def project_fast_answers(
        cls,
        project_id: ProjectId,
        window: WindowViewFormStrict,
        fast_answers_count_threshold: int,
        seconds_lte_threshold: int,
        use_last_n_answers: int | None,
        required_min_answers: int | None,
        restriction_period_hours: int | None,
        restriction_period_days: int | None,
        prolong_restriction_if_exists: bool = False,
    ) -> Self:
        """
        Creates a configuration to detect and restrict access for annotators with fast answers in a project.

        This method creates an asynchronous quality configuration that monitors task completion speed and applies
        restrictions when tasks are completed too quickly.

        Args:
            project_id: ID of the project to monitor.
            window: Window configuration specifying the time period to analyze signals.
            fast_answers_count_threshold: Minimum number of fast answers required to trigger restriction.
            seconds_lte_threshold: Maximum time in seconds for an answer to be considered "fast".
            use_last_n_answers: Number of recent answers to analyze. If None, all answers in window are analyzed.
            required_min_answers: Minimum number of answers required for analysis.
            restriction_period_hours: Duration of restriction in hours.
            restriction_period_days: Duration of restriction in days.
            prolong_restriction_if_exists: If True, extends existing restriction. Otherwise skips the action until the
                user is unrestricted.

        Returns:
            AsyncQualityConfig: Configuration object for detecting and handling fast answers.

        Example:
            To restrict users who complete 7+ tasks in under 60 seconds out of their last 10 tasks during last week for
            two weeks:

            >>> config = AsyncQualityConfig.project_fast_answers(
            >>>     project_id=project.id,
            >>>     window=WindowViewFormStrict(type='SLIDING', length_hours=168),
            >>>     fast_answers_count_threshold=7,
            >>>     seconds_lte_threshold=60,
            >>>     use_last_n_answers=10,
            >>>     required_min_answers=10,
            >>>     restriction_period_days=14
            >>> )
        """

        return cls(
            triggers=[
                QualityTriggerViewFormStrict(
                    conditions=[
                        AggregationByAnnotationByAccountConditionViewFormStrict(
                            signals=[
                                SignalViewFormStrict(name='task_action_duration'),
                            ],
                            aggregate_by_annotation_function=BasicAggregationFunctionViewFormStrict(name='SUM'),
                            aggregate_by_account_function=AggregationFunctionWithValueViewFormStrict(
                                name='COUNT_IF_LTE',
                                value=seconds_lte_threshold,
                            ),
                            aggregate_by_account_thresholds=AggregatedByAccountThresholdConditionViewForm(
                                aggregated_value_gte=fast_answers_count_threshold,
                            ),
                            annotations_number=AnnotationNumberViewForm(
                                use_last_n=use_last_n_answers,
                                required_min=required_min_answers,
                            ),
                            window=window,
                            tags=TagsViewForm(any_of=[project_id]),
                        )
                    ],
                    actions=[
                        CreateRestrictionQualityActionViewForm(
                            params=CreateProjectRestrictionQualityActionParams(
                                project_ids=[project_id],
                                prolong_if_exists=prolong_restriction_if_exists,
                                period_hours=restriction_period_hours,
                                period_days=restriction_period_days,
                            )
                        )
                    ],
                ),
            ],
        )


class AsyncQualityConfigViewV0Strict(AsyncQualityConfigViewV0):
    id: AsyncQualityConfigId
    triggers: Annotated[
        Sequence[QualityTriggerViewFormStrict] | None,
        Field(default_factory=list),
        none_default_validator(default_factory=list),
    ]
    created_at: str

    rules: Annotated[
        Sequence[QualityRuleViewFormStrict] | None,
        deprecated('Rules are deprecated, use triggers instead'),
    ] = None
