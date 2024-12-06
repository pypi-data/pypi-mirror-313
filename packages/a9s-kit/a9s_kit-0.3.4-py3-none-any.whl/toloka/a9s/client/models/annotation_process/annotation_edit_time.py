from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model import (
    AnnotationEditTimeAnnotationProcessView,
)


class AnnotationEditTimeAnnotationProcessViewDataStrict(AnnotationEditTimeAnnotationProcessView):
    type: Literal['annotation-edit-time'] = 'annotation-edit-time'
