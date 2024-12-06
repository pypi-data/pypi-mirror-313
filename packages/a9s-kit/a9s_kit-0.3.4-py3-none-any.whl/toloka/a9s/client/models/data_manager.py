# pyright: reportGeneralTypeIssues=false

from typing import Sequence

from toloka.a9s.client.models.generated.ai.toloka.a9s.data_manager.web.ui.assignee import AccountView
from toloka.a9s.client.models.generated.ai.toloka.a9s.data_manager.web.ui.search import (
    SearchViewRow,
    SearchViewRowElement,
    SearchViewRowQuorum,
)
from toloka.a9s.client.models.types import AnnotationGroupId, AnnotationId


class AccountViewStrict(AccountView):
    account_id: str
    display_name: str
    login: str
    username: str


class QuorumDataManagerView(SearchViewRowQuorum):
    id: str
    completed_count: int
    total_count: int


class SearchViewRowElementStrict(SearchViewRowElement):
    annotation_id: AnnotationId | None = None
    created_at: str
    assignee: AccountViewStrict | None = None


class AnnotationGroupDataManagerView(SearchViewRow):
    group_id: AnnotationGroupId
    created_at: str
    annotation_count: int
    quorum: QuorumDataManagerView | None
    elements: Sequence[SearchViewRowElementStrict]
