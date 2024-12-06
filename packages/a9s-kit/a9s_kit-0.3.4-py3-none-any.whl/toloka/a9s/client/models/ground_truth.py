# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Any, Mapping, Sequence

from toloka.a9s.client.models.generated.ai.toloka.gts.config.web.v0.view import GroundTruthConfigViewV0
from toloka.a9s.client.models.generated.ai.toloka.gts.web.v0.view import (
    GroundTruthBucketViewV0,
    GroundTruthListViewV0,
    GroundTruthOutputValueViewV0,
    GroundTruthViewV0,
)
from toloka.a9s.client.models.types import (
    GroundTruthBucketId,
    GroundTruthConfigId,
    GroundTruthId,
    GroundTruthOutputValueId,
)
from toloka.a9s.client.models.utils import none_default_validator


class GroundTruthOutputValueViewV0Strict(GroundTruthOutputValueViewV0):
    id: GroundTruthOutputValueId
    ground_truth_id: str
    output_value: Mapping[str, Any]


class GroundTruthBucketViewV0Strict(GroundTruthBucketViewV0):
    id: GroundTruthBucketId
    created_at: str
    name: str
    input_spec: Mapping[str, Any]
    output_spec: Mapping[str, Any]


class GroundTruthViewV0Strict(GroundTruthViewV0):
    id: GroundTruthId
    ground_truth_bucket_id: str
    created_at: str
    input_value: Mapping[str, Any]
    output_values: Annotated[Sequence[GroundTruthOutputValueViewV0Strict], none_default_validator(default_factory=list)]


class GroundTruthListViewV0Strict(GroundTruthListViewV0):
    data: Sequence[GroundTruthViewV0Strict]


class GroundTruthConfigViewV0Strict(GroundTruthConfigViewV0):
    id: GroundTruthConfigId
    bucket_id: str
    created_at: str
