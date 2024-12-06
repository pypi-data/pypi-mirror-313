# pyright: reportGeneralTypeIssues=false

from typing import Sequence

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_edit.web.v1.annotation_edits.view import (
    AnnotationEditListV1,
    AnnotationEditViewV1,
)
from toloka.a9s.client.models.types import AnnotationEditId


class AnnotationEditViewV1Strict(AnnotationEditViewV1):
    id: AnnotationEditId


class AnnotationEditListV1Strict(AnnotationEditListV1):
    data: Sequence[AnnotationEditViewV1Strict]
