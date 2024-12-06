from typing_extensions import TypeVar

from toloka.a9s.client.models.annotation_process.view import (
    QuorumAnnotationProcessViewStrict,
    StatusWorkflowAnnotationProcessViewStrict,
)

OptionalQRM = QuorumAnnotationProcessViewStrict | None
QRM = TypeVar('QRM', bound=OptionalQRM, covariant=True, default=OptionalQRM)
OptionalSW = StatusWorkflowAnnotationProcessViewStrict | None
SW = TypeVar('SW', bound=OptionalSW, covariant=True, default=OptionalSW)
