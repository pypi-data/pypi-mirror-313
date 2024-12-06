# pyright: reportGeneralTypeIssues=false

from toloka.a9s.client.models.generated.ai.toloka.experts.portal.qualification.web.v0.model import (
    UserQualificationForm,
    UserQualificationView,
)
from toloka.a9s.client.models.types import QualificationId, UserQualificationId


class UserQualificationViewStrict(UserQualificationView):
    id: UserQualificationId
    account_id: str
    qualification_id: QualificationId


class UserQualificationFormStrict(UserQualificationForm):
    account_id: str
    qualification_id: QualificationId
