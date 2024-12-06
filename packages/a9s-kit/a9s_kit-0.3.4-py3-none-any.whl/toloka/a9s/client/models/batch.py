# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Sequence

from pydantic import BaseModel, Field

from toloka.a9s.client.models.annotation_process import UploadFormV1DataStrict, UploadFormV1Strict
from toloka.a9s.client.models.extension_id import ExtensionId
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.restriction.web.v0.form import GetRestrictionListQueryParamsV0
from toloka.a9s.client.models.generated.ai.toloka.a9s.services.batch.web.v1.model.form import (
    BatchCreateFormV1,
    BatchUpdateFormV1,
    BatchUpdateFormV1ExtensionInstanceConfigV1,
    BatchUpdateFormV1ExtensionsV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.services.batch.web.v1.model.view import (
    BatchListViewV1,
    BatchViewV1,
)
from toloka.a9s.client.models.types import BatchId, ProjectId
from toloka.a9s.client.models.utils import none_default_validator


class BatchUpdateFormV1ExtensionInstanceConfigV1Strict(BatchUpdateFormV1ExtensionInstanceConfigV1):
    extension_id: ExtensionId
    instance_id: str


class BatchUpdateFormV1ExtensionsV1Strict(BatchUpdateFormV1ExtensionsV1):
    instances: Annotated[
        Sequence[BatchUpdateFormV1ExtensionInstanceConfigV1Strict],
        Field(max_length=100, min_length=0, default_factory=list),
        none_default_validator(default_factory=list),
    ]


class BatchViewV1Strict(BatchViewV1):
    id: BatchId
    project_id: ProjectId
    private_name: str
    extensions: Annotated[
        BatchUpdateFormV1ExtensionsV1Strict,
        Field(default_factory=BatchUpdateFormV1ExtensionsV1Strict),
        none_default_validator(default_factory=BatchUpdateFormV1ExtensionsV1Strict),
    ]
    tags: Annotated[
        Sequence[str],
        none_default_validator(default_factory=list),
    ]


class BatchListViewV1Strict(BatchListViewV1):
    data: Sequence[BatchViewV1Strict]
    has_more: bool


class BatchCreateFormV1Strict(BatchCreateFormV1):
    extensions: Annotated[
        BatchUpdateFormV1ExtensionsV1Strict,
        Field(default_factory=BatchUpdateFormV1ExtensionsV1Strict),
        none_default_validator(default_factory=BatchUpdateFormV1ExtensionsV1Strict),
    ]
    tags: Annotated[
        Sequence[str],
        none_default_validator(default_factory=list),
    ]


class BatchUpdateFormV1Strict(BatchUpdateFormV1):
    extensions: Annotated[
        BatchUpdateFormV1ExtensionsV1Strict,
        Field(default_factory=BatchUpdateFormV1ExtensionsV1Strict),
        none_default_validator(default_factory=BatchUpdateFormV1ExtensionsV1Strict),
    ]
    tags: Annotated[
        Sequence[str],
        none_default_validator(default_factory=list),
    ]

    @classmethod
    def from_view(cls, view: BatchViewV1Strict) -> 'BatchUpdateFormV1Strict':
        return cls(
            private_name=view.private_name,
            metadata=view.metadata,
            extensions=view.extensions,
            tags=view.tags,
            hidden=view.hidden,
        )


class BatchUploadForm(BaseModel):
    data: Sequence[UploadFormV1DataStrict]
    skip_on_repeated_external_id_in_single_request: bool | None = None

    def to_upload_form(self, batch_id: BatchId) -> UploadFormV1Strict:
        return UploadFormV1Strict(
            batch_id=batch_id,
            data=self.data,
            skip_on_repeated_external_id_in_single_request=self.skip_on_repeated_external_id_in_single_request,
        )


class GetRestrictionsForm(GetRestrictionListQueryParamsV0):
    project_id: None = None
    batch_id: None = None
