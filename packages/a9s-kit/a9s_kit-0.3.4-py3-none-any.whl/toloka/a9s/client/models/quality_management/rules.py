from typing import Literal, Sequence

from pydantic import BaseModel
from typing_extensions import deprecated

AVERAGE_RULE_NAME: Literal['AVERAGE'] = 'AVERAGE'


WindowType = Literal['SLIDING', 'CURRENT_DAY_UTC']


@deprecated('Rules are deprecated, use filters instead')
class AverageRuleParams(BaseModel):
    metric_names: Sequence[str] | None = None
    metric_name: str | None = None
    history_threshold: int
    quality_threshold_lower_bound: float
    quality_threshold_upper_bound: float
    window_type: WindowType | None = None
    window_length_days: int | None = None
    history_size: int | None = None
    history_threshold_condition: str | None = None


COUNT_RULE_NAME: Literal['COUNT'] = 'COUNT'


@deprecated('Rules are deprecated, use filters instead')
class CountRuleParams(BaseModel):
    metric_names: Sequence[str] | None = None
    metric_name: str | None = None
    history_threshold: int
    quality_threshold_lower_bound: float
    quality_threshold_upper_bound: float
    count_threshold: int
    window_type: WindowType | None = None
    window_length_days: int | None = None
    history_size: int | None = None
    history_threshold_condition: str | None = None
