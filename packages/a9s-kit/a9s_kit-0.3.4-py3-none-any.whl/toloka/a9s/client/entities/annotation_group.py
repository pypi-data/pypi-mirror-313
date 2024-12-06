from __future__ import annotations

import datetime
from typing import Any, Generic, Mapping, Sequence, TypeAlias, TypeVar, overload

from typing_extensions import TypeIs, Unpack

from toloka.a9s.client.entities.annotation import Annotation
from toloka.a9s.client.entities.annotation.types import OptionalSW
from toloka.a9s.client.entities.base import EntityApiBase, EntityApiBaseParams
from toloka.a9s.client.models.annotation import ValuesType
from toloka.a9s.client.models.annotation_process.view import QuorumAnnotationProcessViewStrict
from toloka.a9s.client.models.types import (
    AnnotationGroupId,
    AnnotationId,
    BatchId,
    ProjectId,
)
from toloka.a9s.client.models.utils import DATETIME_ADAPTER

OptionalQRM = QuorumAnnotationProcessViewStrict | None
QRM = TypeVar('QRM', QuorumAnnotationProcessViewStrict, None, OptionalQRM, covariant=True)
AnnotationGroupAny: TypeAlias = 'AnnotationGroup[OptionalQRM]'


class AnnotationGroup(EntityApiBase, Generic[QRM]):
    """A group of annotations in Annotation Studio related by some annotation process.

    An annotation group represents multiple annotations originating from the same annotation process.

    Generic type parameters:

    * `QRM`: Type of quorum annotation process. Can be:
        * `None`: process is not configured
        * `QuorumAnnotationProcessViewStrict`: process is configured and loaded from the API

    Attributes:
        annotation_group_id: Unique identifier of the group.
        quorum: Quorum parameters of the annotation group.
        batch_id: ID of the batch this group belongs to.
        project_id: ID of the project this group belongs to.
        annotation_ids: Set of IDs of annotations in this group.
        created_at: Group creation time.
    """

    annotation_group_id: AnnotationGroupId
    quorum: QRM
    batch_id: BatchId
    project_id: ProjectId
    annotation_ids: set[AnnotationId]
    created_at: datetime.datetime

    def __init__(
        self,
        annotation_group_id: AnnotationGroupId,
        quorum: QRM,
        batch_id: BatchId,
        project_id: ProjectId,
        annotation_ids: set[AnnotationId],
        created_at: datetime.datetime,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> None:
        super().__init__(**kwargs)
        self.quorum = quorum
        self.annotation_group_id = annotation_group_id
        self.batch_id = batch_id
        self.project_id = project_id
        self.annotation_ids = annotation_ids
        self.created_at = created_at

    @classmethod
    async def get(
        cls: type[AnnotationGroupAny],
        id: AnnotationGroupId,
        batch_id: BatchId,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationGroupAny:
        """Gets an annotation group and its annotation processes from the API by its ID and batch ID.

        Args:
            id: ID of the annotation group to get.
            batch_id: ID of the batch containing the group.
            kit (AsyncKit): `AsyncKit` instance.

        Returns:
            `AnnotationGroup` that may or may not have quorum process configured.

        Raises:
            ValueError: If annotation group with given ID is not found.

        Examples:
            ```python
            group = await AnnotationGroup.get(id='group123', batch_id='batch456', kit=kit)
            ```
        """

        kit = kwargs['kit']

        data_manager_view = await kit.annotation_studio.get_annotation_group_data_manager_view(
            annotation_group_id=id,
            batch_id=batch_id,
        )
        if data_manager_view is None:
            raise ValueError(f'Annotation group with id {id} not found')

        annotation_ids = set(
            elem.annotation_id for elem in data_manager_view.elements if elem.annotation_id is not None
        )
        quorum = await kit.annotation_studio.annotation_process.get_quorum(annotation_group_id=id)
        if quorum is not None:
            project_id = quorum.project_id
        else:
            project_id = (await kit.annotation_studio.batch.get(batch_id)).project_id

        return cls(
            annotation_group_id=id,
            quorum=quorum,
            batch_id=batch_id,
            project_id=project_id,
            annotation_ids=annotation_ids,
            created_at=DATETIME_ADAPTER.validate_python(data_manager_view.created_at),
            **kwargs,
        )

    @classmethod
    async def get_with_quorum_or_fail(
        cls: type[AnnotationGroupAny],
        id: AnnotationGroupId,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationGroup[QuorumAnnotationProcessViewStrict]:
        """Gets an annotation group by its ID, ensuring it has quorum process configured.

        Args:
            id: ID of the annotation group to get.
            kit (AsyncKit): `AsyncKit` instance.

        Returns:
            `AnnotationGroup` with concrete `QuorumAnnotationProcessViewStrict` type.

        Raises:
            ValueError: If annotation group with given ID is not found or doesn't have quorum configured.

        Examples:
            ```python
            group = await AnnotationGroup.get_with_quorum_or_fail(id='group123', kit=kit)
            # Statically type checked
            print(f'Quorum remaining annotations: {group.quorum.data.remaining_annotations}')
            ```
        """

        kit = kwargs['kit']

        quorum = await kit.annotation_studio.annotation_process.get_quorum(annotation_group_id=id)
        if quorum is None:
            raise ValueError(f'Annotation group with id {id} does not have a quorum')

        batch_id = quorum.batch_id
        project_id = quorum.project_id

        data_manager_view = await kit.annotation_studio.get_annotation_group_data_manager_view(
            annotation_group_id=id,
            batch_id=batch_id,
        )
        assert data_manager_view is not None, "Quorum can't exist without annotation group"

        # elements can contain edits without annotations
        annotation_ids = set(
            elem.annotation_id for elem in data_manager_view.elements if elem.annotation_id is not None
        )

        return AnnotationGroup[QuorumAnnotationProcessViewStrict](
            annotation_group_id=id,
            quorum=quorum,
            batch_id=batch_id,
            project_id=project_id,
            annotation_ids=annotation_ids,
            created_at=DATETIME_ADAPTER.validate_python(data_manager_view.created_at),
            **kwargs,
        )

    async def refresh(self) -> AnnotationGroupAny:
        """Refreshes the group by fetching its latest state from the API.

        Returns:
            A new `AnnotationGroup` instance with the latest state.

        Examples:
            ```python
            group = await group.refresh()
            print(len(group.annotation_ids))  # Current number of annotations
            ```
        """
        return await self.get(id=self.annotation_group_id, batch_id=self.batch_id, kit=self.kit)

    @overload
    async def get_annotations(
        self: AnnotationGroup[QRM],
        values_type: type[ValuesType],
    ) -> list[Annotation[QRM, OptionalSW, ValuesType]]: ...

    @overload
    async def get_annotations(
        self: AnnotationGroup[QRM],
        values_type: None = None,
    ) -> list[Annotation[QRM, OptionalSW, Mapping[str, Any]]]: ...

    async def get_annotations(
        self: AnnotationGroup[QRM],
        values_type: type[ValuesType] | None = None,
    ) -> (
        Sequence[Annotation[OptionalQRM, OptionalSW, ValuesType]]
        | Sequence[Annotation[OptionalQRM, OptionalSW, Mapping[str, Any]]]
    ):
        """Returns all annotations in this group.

        Args:
            values_type: Optional type for annotation values. If None, values will be returned as dict.

        Returns:
            List of `Annotation` instances belonging to this group.

        Examples:
            ```python
            annotations = await group.get_annotations()
            for annotation in annotations:
                print(annotation.view.values)


            class MyValues(BaseModel):
                label: str


            annotations = await group.get_annotations(values_type=MyValues)
            for annotation in annotations:
                print(annotation.view.values.label)
            ```
        """

        # TODO: use from_view and batch get annotations by group id when endpoint is ready

        # this check is needed just for values_type type narrowing
        if values_type is None:
            return [
                await Annotation.get(annotation_id, values_type=values_type, kit=self.kit)
                for annotation_id in self.annotation_ids
            ]
        else:
            return [
                await Annotation.get(annotation_id, values_type=values_type, kit=self.kit)
                for annotation_id in self.annotation_ids
            ]

    def assert_quorum(
        self: AnnotationGroup[OptionalQRM],
    ) -> AnnotationGroup[QuorumAnnotationProcessViewStrict]:
        """Asserts that the group has a quorum process configured in its local state.

        Verifies that the group has a quorum annotation process configured in its current local
        representation, without fetching new data from the API. Returns the same group with a concrete
        `QuorumAnnotationProcessViewStrict` type instead of `OptionalQRM` or fails.

        Returns:
            The same group with a concrete `QuorumAnnotationProcessViewStrict` type.

        Raises:
            ValueError: If quorum process is not configured in the local representation of this group.

        Examples:
            ```python
            group = group.assert_quorum()
            print(group.quorum.data.threshold)  # Statically type checked
            ```
        """

        if has_quorum(self):
            return self
        raise ValueError('Annotation group does not have a quorum')

    # quorum annotation group API

    def is_quorum_completed(self: 'AnnotationGroup[QuorumAnnotationProcessViewStrict]') -> bool:
        """Checks if the quorum process is completed for this group, i.e. there are enough annotations.

        Returns:
            True if required number of annotations is reached, False otherwise.
        """

        return self.quorum.completed


def has_quorum(
    annotation_group: AnnotationGroup[OptionalQRM],
) -> TypeIs[AnnotationGroup[QuorumAnnotationProcessViewStrict]]:
    return annotation_group.quorum is not None
