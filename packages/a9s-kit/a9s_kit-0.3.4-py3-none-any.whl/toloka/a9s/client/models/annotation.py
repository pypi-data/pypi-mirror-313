# pyright: reportGeneralTypeIssues=false

from typing import TYPE_CHECKING, Annotated, Any, Generic, Mapping, Sequence, cast

from pydantic import BaseModel, Field
from typing_extensions import Self, TypeVar

from toloka.a9s.client.models.annotation_process.quorum import QuorumAnnotationProcessParametersStrict
from toloka.a9s.client.models.annotation_process.status_workflow import StatusWorkflowAnnotationProcessParametersStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.form import (
    AnnotationFormV1,
    EditAnnotationFormV1,
    UploadAnnotationFormV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.param import AnnotationFilterParamV1
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.view import (
    AnnotationListViewV1,
    AnnotationViewV1,
    UploadAnnotationViewV1,
)
from toloka.a9s.client.models.types import AnnotationGroupId, AnnotationId, BatchId

if TYPE_CHECKING:
    ValuesType = TypeVar('ValuesType', Mapping[str, Any], BaseModel, covariant=True, default=Mapping[str, Any])
else:
    # waiting for pydantic 2.11: https://github.com/pydantic/pydantic/issues/9418
    ValuesType = TypeVar('ValuesType', covariant=True, default=Mapping[str, Any])


class AnnotationFormV1Strict(AnnotationFormV1, Generic[ValuesType]):
    values: ValuesType
    params: (
        Sequence[QuorumAnnotationProcessParametersStrict | StatusWorkflowAnnotationProcessParametersStrict] | None
    ) = None


class AnnotationViewV1Strict(AnnotationViewV1, Generic[ValuesType]):
    id: AnnotationId
    annotation_group_id: AnnotationGroupId
    values: ValuesType
    batch_id: BatchId
    created_at: Annotated[str, Field(examples=['2024-08-12T12:41:07.629'])]


class UploadAnnotationFormV1Strict(UploadAnnotationFormV1, Generic[ValuesType]):
    annotations: Sequence[AnnotationFormV1Strict[ValuesType]]


class UploadAnnotationViewV1Strict(UploadAnnotationViewV1, Generic[ValuesType]):
    batch_id: BatchId
    annotations: Sequence[AnnotationViewV1Strict[ValuesType]]


class AnnotationListViewV1Strict(AnnotationListViewV1, Generic[ValuesType]):
    data: Sequence[AnnotationViewV1Strict[ValuesType]]
    has_more: bool


class EditAnnotationFormV1Strict(EditAnnotationFormV1, Generic[ValuesType]):
    values: ValuesType


class AnnotationFilterParamV1Strict(AnnotationFilterParamV1):
    def with_tags(
        self,
        tag_any_of: Sequence[str] | None = None,
        tag_all_of: Sequence[str] | None = None,
        tag_none_of: Sequence[str] | None = None,
    ) -> Self:
        return self.model_copy(
            update={
                'tag_any_of': ','.join(tag_any_of) if tag_any_of else None,
                'tag_all_of': ','.join(tag_all_of) if tag_all_of else None,
                'tag_none_of': ','.join(tag_none_of) if tag_none_of else None,
            }
        )


def get_annotation_values_type(
    cls: type[
        AnnotationFormV1Strict[ValuesType]
        | AnnotationViewV1Strict[ValuesType]
        | UploadAnnotationFormV1Strict[ValuesType]
        | UploadAnnotationViewV1Strict[ValuesType]
        | AnnotationListViewV1Strict[ValuesType]
        | EditAnnotationFormV1Strict[ValuesType]
    ],
) -> type[ValuesType] | None:
    args = cls.__pydantic_generic_metadata__['args']
    if args:
        return cast(type[ValuesType], args[0])
    return None
