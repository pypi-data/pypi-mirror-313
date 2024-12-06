# pyright: reportGeneralTypeIssues=false

from typing import Literal, Sequence

from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.viewform.aggregation_function import (
    AggregationFunctionViewForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.viewform.condition import (
    AggregationByAccountConditionViewForm,
    AggregationByAnnotationByAccountConditionViewForm,
    AggregationByAnnotationBySignalNameByAccountConditionViewForm,
    WindowViewForm,
)
from toloka.a9s.client.models.quality_management.signals import SignalViewFormStrict

BasicAggregationFunctionName = Literal['SUM', 'COUNT', 'LAST', 'AVERAGE'] | str


class BasicAggregationFunctionViewFormStrict(AggregationFunctionViewForm):
    name: BasicAggregationFunctionName


AggregationFunctionWithValueName = Literal['COUNT_IF_LTE'] | str


class AggregationFunctionWithValueViewFormStrict(AggregationFunctionViewForm):
    name: AggregationFunctionWithValueName
    value: float


AggregationFunctionViewFormStrict = BasicAggregationFunctionViewFormStrict | AggregationFunctionWithValueViewFormStrict


class WindowViewFormSlidingStrict(WindowViewForm):
    type: Literal['SLIDING'] = 'SLIDING'
    length_hours: int


class WindowViewFormCurrentDayUtcStrict(WindowViewForm):
    type: Literal['CURRENT_DAY_UTC'] = 'CURRENT_DAY_UTC'
    length_hours: None = None


WindowViewFormStrict = WindowViewFormSlidingStrict | WindowViewFormCurrentDayUtcStrict


class AggregationByAnnotationByAccountConditionViewFormStrict(AggregationByAnnotationByAccountConditionViewForm):
    query_template: Literal['AGGREGATION_BY_ANNOTATION_BY_ACCOUNT'] = 'AGGREGATION_BY_ANNOTATION_BY_ACCOUNT'
    signals: Sequence[SignalViewFormStrict]
    aggregate_by_annotation_function: AggregationFunctionViewFormStrict
    aggregate_by_account_function: AggregationFunctionViewFormStrict
    window: WindowViewFormStrict | None = None


class AggregationByAccountConditionViewFormStrict(AggregationByAccountConditionViewForm):
    query_template: Literal['AGGREGATION_BY_ACCOUNT'] = 'AGGREGATION_BY_ACCOUNT'
    signals: Sequence[SignalViewFormStrict]
    aggregate_by_account_function: AggregationFunctionViewFormStrict
    window: WindowViewFormStrict | None = None


class AggregationByAnnotationBySignalNameByAccountConditionViewFormStrict(
    AggregationByAnnotationBySignalNameByAccountConditionViewForm
):
    query_template: Literal['AGGREGATION_BY_ANNOTATION_BY_SIGNAL_NAME_BY_ACCOUNT'] = (
        'AGGREGATION_BY_ANNOTATION_BY_SIGNAL_NAME_BY_ACCOUNT'
    )
    signals: Sequence[SignalViewFormStrict]
    aggregate_by_annotation_by_signal_name_function: AggregationFunctionViewFormStrict
    aggregate_by_account_function: AggregationFunctionViewFormStrict
    window: WindowViewFormStrict | None = None


AggregationViewFormStrict = (
    AggregationByAccountConditionViewFormStrict
    | AggregationByAnnotationByAccountConditionViewFormStrict
    | AggregationByAnnotationBySignalNameByAccountConditionViewFormStrict
)
