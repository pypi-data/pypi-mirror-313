# pyright: reportGeneralTypeIssues=false

from typing import Literal, Sequence

from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.domain import MatchFilterResult
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import (
    QualificationFilterForm,
    QualificationFilterView,
    QualificationForm,
    QualificationLegacyForm,
    QualificationLegacyListView,
    QualificationLegacyView,
    QualificationListView,
    QualificationView,
)
from toloka.a9s.client.models.types import (
    QualificationFilterId,
    QualificationId,
)


class QualificationViewStrict(QualificationView):
    id: QualificationId
    title: str


class QualificationFormStrict(QualificationForm):
    title: str


class QualificationListViewStrict(QualificationListView):
    qualifications: Sequence[QualificationViewStrict]


class QualificationLegacyViewStrict(QualificationLegacyView):
    id: QualificationId
    qualification_id: QualificationId
    toloka_skill_id: int
    pass_on_no_value: bool
    operator: Literal['EQ', 'NE', 'GT', 'GTE', 'LT', 'LTE']
    value: float


class QualificationLegacyFormStrict(QualificationLegacyForm):
    qualification_id: QualificationId
    toloka_skill_id: int
    pass_on_no_value: bool
    operator: Literal['EQ', 'NE', 'GT', 'GTE', 'LT', 'LTE']
    value: float


class QualificationLegacyListViewStrict(QualificationLegacyListView):
    legacy_qualifications: Sequence[QualificationLegacyViewStrict]


class QualificationFilterViewStrict(QualificationFilterView):
    id: QualificationFilterId
    created_at: str
    created_by: str
    title: str


class QualificationFilterFormStrict(QualificationFilterForm):
    title: str


class MatchFilterResultStrict(MatchFilterResult):
    missedRequiredQualificationIds: Sequence[QualificationId] | None = None
    qualified: bool
