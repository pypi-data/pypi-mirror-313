# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Literal

from pydantic import Field

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.metric import (
    AnnotationMetricCreateFormV1,
    AnnotationMetricUpdateFormV1,
    AnnotationMetricViewV1,
)
from toloka.a9s.client.models.types import AnnotationMetricId


class AnnotationMetricUpdateFormV1StrictUnitInterval(AnnotationMetricUpdateFormV1):
    type: Literal['UNIT_INTERVAL'] = 'UNIT_INTERVAL'
    value: Annotated[float, Field(ge=0, le=1)]


class AnnotationMetricUpdateFormV1StrictLong(AnnotationMetricUpdateFormV1):
    type: Literal['LONG'] = 'LONG'
    value: int


AnnotationMetricUpdateFormV1Strict = (
    AnnotationMetricUpdateFormV1StrictUnitInterval | AnnotationMetricUpdateFormV1StrictLong
)


class AnnotationMetricCreateFormV1FormStrictUnitInterval(AnnotationMetricCreateFormV1):
    type: Literal['UNIT_INTERVAL'] = 'UNIT_INTERVAL'
    value: Annotated[float, Field(ge=0, le=1)]


class AnnotationMetricCreateFormV1FormStrictLong(AnnotationMetricCreateFormV1):
    type: Literal['LONG'] = 'LONG'
    value: int


AnnotationMetricCreateFormV1Strict = (
    AnnotationMetricCreateFormV1FormStrictUnitInterval | AnnotationMetricCreateFormV1FormStrictLong
)


class AnnotationMetricViewV1Strict(AnnotationMetricViewV1):
    id: AnnotationMetricId
