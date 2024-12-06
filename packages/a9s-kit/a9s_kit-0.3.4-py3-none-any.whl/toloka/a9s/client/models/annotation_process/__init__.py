# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Sequence, TypeGuard

from pydantic import Field

from toloka.a9s.client.models.annotation_process.agreement import AgreementAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.annotation_edit_time import (
    AnnotationEditTimeAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.metric_provider import MetricProviderAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.post_acceptance import PostAcceptanceAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.quorum import (
    QuorumAnnotationProcessParametersStrict,
    QuorumAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowAnnotationProcessParametersStrict,
    StatusWorkflowAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    AnnotationProcessDataType,
    AnnotationProcessViewStrict,
    UnrecognizedAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model_object.ParticularAnnotationProcessDataViewJava.lang.ObjectJava.lang import (  # noqa
    Object,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.web.ui.view import (
    AnnotationProcessListView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.web.v1.upload import (
    UploadFormV1,
    UploadFormV1Data,
    UploadViewV1,
    UploadViewV1Data,
)
from toloka.a9s.client.models.types import AnnotationGroupId, AnnotationId
from toloka.a9s.client.models.utils import none_default_validator

AnnotationProcessViewStrictVariant = AnnotationProcessViewStrict[
    Annotated[
        MetricProviderAnnotationProcessViewDataStrict
        | StatusWorkflowAnnotationProcessViewDataStrict
        | PostAcceptanceAnnotationProcessViewDataStrict
        | QuorumAnnotationProcessViewDataStrict
        | AgreementAnnotationProcessViewDataStrict
        | AnnotationEditTimeAnnotationProcessViewDataStrict,
        Field(discriminator='type'),
    ]
    | UnrecognizedAnnotationProcessViewDataStrict
]


class AnnotationProcessListViewStrict(AnnotationProcessListView):
    processes: Annotated[
        Sequence[AnnotationProcessViewStrictVariant],
        none_default_validator(default_factory=list),
    ]


class UploadViewV1DataStrict(UploadViewV1Data):
    annotation_id: AnnotationId | None = None
    annotation_group_id: AnnotationGroupId


class UploadViewV1Strict(UploadViewV1):
    data: Sequence[UploadViewV1DataStrict]


def is_annotation_process_instance(
    process: AnnotationProcessViewStrictVariant,
    data_type: type[AnnotationProcessDataType],
) -> TypeGuard[AnnotationProcessViewStrict[AnnotationProcessDataType]]:
    return isinstance(process.data, data_type)


class UploadFormV1DataStrict(UploadFormV1Data):
    params: (
        Sequence[QuorumAnnotationProcessParametersStrict | StatusWorkflowAnnotationProcessParametersStrict] | None
    ) = None


class UploadFormV1Strict(UploadFormV1):
    data: Sequence[UploadFormV1DataStrict]
