# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Literal, Sequence

from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.restriction.web.v0.view import (
    RestrictionListViewV0,
    RestrictionViewV0,
)
from toloka.a9s.client.models.types import RestrictionId
from toloka.a9s.client.models.utils import none_default_validator


class RestrictionViewV0Strict(RestrictionViewV0):
    id: RestrictionId
    account_id: str
    created_at: str
    created_by: str
    private_comment: str | None = None
    scope: Literal['PROJECT', 'BATCH', 'ALL_PROJECTS']


class RestrictionListViewV0Strict(RestrictionListViewV0):
    data: Annotated[Sequence[RestrictionViewV0Strict], none_default_validator(default_factory=list)]
