from __future__ import annotations

import datetime
import logging
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Generic,
    Literal,
    Mapping,
    Sequence,
    TypeAlias,
    TypeGuard,
    cast,
    overload,
)

from pydantic import BaseModel
from typing_extensions import TypeVar, Unpack

from toloka.a9s.client.entities.annotation.types import QRM, SW, OptionalQRM, OptionalSW
from toloka.a9s.client.entities.base import EntityApiBase, EntityApiBaseParams
from toloka.a9s.client.models.annotation import (
    AnnotationViewV1Strict,
    EditAnnotationFormV1Strict,
    ValuesType,
)
from toloka.a9s.client.models.annotation_edit import AnnotationEditViewV1Strict
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowAnnotationProcessViewUserViewStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    QuorumAnnotationProcessViewStrict,
    StatusWorkflowAnnotationProcessViewStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.param import AnnotationFilterParamV1
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_edit.web.v1.annotation_edits.form import (
    AnnotationEditQueryParamsV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.status_workflow.web.ui.form import (
    UpdateStatusWorkflowForm,
)
from toloka.a9s.client.models.types import AnnotationId, BatchId
from toloka.a9s.client.models.utils import DATETIME_ADAPTER, OPTIONAL_DATETIME_ADAPTER
from toloka.a9s.client.sort import SortValue, to_sort_string

if TYPE_CHECKING:
    from toloka.a9s.client.entities.annotation_group import AnnotationGroupAny

logger = logging.getLogger()


NewValuesType = TypeVar('NewValuesType', Mapping[str, Any], BaseModel, covariant=True)

AnnotationAny: TypeAlias = 'Annotation[OptionalQRM, OptionalSW, ValuesType]'


class Annotation(
    EntityApiBase,
    Generic[QRM, SW, ValuesType],
):
    """An `Annotation` Studio annotation that can be configured with annotation processes.

    An annotation represents a single labeling result that can be configured with different annotation processes
    (quorum, status workflow). Each annotation contains values - the current state of the
    labeling result.

    Generic type parameters:

    * `QRM`: Type of quorum annotation process
    * `SW`: Type of status workflow annotation process
    * `ValuesType`: Type of annotation values (labeling result)

    Each annotation process type parameter can be:

    * `None`: process is not configured
    * `T`: process is configured and loaded from the API

    Values type parameter can be any mapping or `BaseModel`.

    Attributes:
        view: API representation of the annotation.
        quorum: Quorum annotation process settings.
        status_workflow: Status workflow annotation process settings.

    Examples:

        Get annotation with specific values type:
        ```python
        class MyValues(BaseModel):
            label: str


        annotation = await Annotation.get(id=AnnotationId('existing-annotation-id'), values_type=MyValues, kit=kit)
        print(annotation.view.values.label)
        ```

        Get annotation with dict values:
        ```python
        annotation = await Annotation.get(id=AnnotationId('existing-annotation-id'), kit=kit)
        print(annotation.view.values['label'])
        ```
    """

    status_workflow: SW
    quorum: QRM

    view: AnnotationViewV1Strict[ValuesType]

    def __init__(
        self,
        view: AnnotationViewV1Strict[ValuesType],
        quorum: QRM,
        status_workflow: SW,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> None:
        super().__init__(**kwargs)
        self.view = view

        self.status_workflow = status_workflow
        self.quorum = quorum

    @overload
    @classmethod
    async def from_view(
        cls: type[AnnotationAny[ValuesType]],
        view: AnnotationViewV1Strict[ValuesType],
        assert_status_workflow: Literal[True] = ...,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> Annotation[OptionalQRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType]: ...

    @overload
    @classmethod
    async def from_view(
        cls: type[AnnotationAny[ValuesType]],
        view: AnnotationViewV1Strict[ValuesType],
        assert_status_workflow: bool = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationAny[ValuesType]: ...

    @classmethod
    async def from_view(
        cls: type[AnnotationAny[ValuesType]],
        view: AnnotationViewV1Strict[ValuesType],
        assert_status_workflow: bool = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationAny[ValuesType]:
        """Creates an `Annotation` entity from its API representation, loading annotation processes.

        Creates an `Annotation` entity and loads its annotation processes (quorum, status workflow)
        from the API.

        Args:
            view: API representation of the annotation.
            assert_status_workflow: If `True`, verifies that status workflow is configured and returns an `Annotation`
                with concrete `StatusWorkflowAnnotationProcessViewStrict` type instead of `OptionalSW`. Raises
                `ValueError` if status workflow is not configured.
            kit (AsyncKit): `AsyncKit` instance.

        Returns:
            (Annotation[OptionalQRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType]): If assert_status_workflow
                is True, `Annotation` with concrete `StatusWorkflowAnnotationProcessViewStrict` type.
            (AnnotationAny[ValuesType]): If assert_status_workflow is False, `Annotation` that may or may not have
                status workflow configured.

        Raises:
            ValueError: If assert_status_workflow is True and status workflow is not configured.

        Examples:
            Create annotation with status workflow assertion:
            ```python
            view = await kit.annotation_studio.annotation.get(id='123')
            annotation = await Annotation.from_view(view=view, assert_status_workflow=True, kit=kit)
            await annotation.get_status_workflow_responsible()  # Statically type checked
            ```
        """

        kit = kwargs['kit']
        status_workflow = await kit.annotation_studio.annotation_process.get_status_workflow(annotation_id=view.id)
        if view.annotation_group_id is not None:
            quorum = await kit.annotation_studio.annotation_process.get_quorum(
                annotation_group_id=view.annotation_group_id
            )
        else:
            quorum = None

        annotation = cls(
            view=view,
            status_workflow=status_workflow,
            quorum=quorum,
            **kwargs,
        )
        if assert_status_workflow:
            return annotation.assert_status_workflow()
        return annotation

    @overload
    @classmethod
    async def get(
        cls: type[AnnotationAny[ValuesType]],
        id: AnnotationId,
        *,
        values_type: type[ValuesType],
        assert_status_workflow: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> Annotation[OptionalQRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType]: ...

    @overload
    @classmethod
    async def get(
        cls: type[AnnotationAny[ValuesType]],
        id: AnnotationId,
        *,
        values_type: type[ValuesType],
        assert_status_workflow: bool = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationAny[ValuesType]: ...

    @overload
    @classmethod
    async def get(
        cls: type[AnnotationAny[Any]],
        id: AnnotationId,
        *,
        values_type: None = None,
        assert_status_workflow: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> Annotation[OptionalQRM, StatusWorkflowAnnotationProcessViewStrict, Mapping[str, Any]]: ...

    @overload
    @classmethod
    async def get(
        cls: type[AnnotationAny[Any]],
        id: AnnotationId,
        *,
        values_type: None = None,
        assert_status_workflow: bool = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationAny[Mapping[str, Any]]: ...

    @classmethod
    async def get(
        cls: type[AnnotationAny[Any]],
        id: AnnotationId,
        *,
        values_type: type[ValuesType] | None = None,
        assert_status_workflow: bool = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationAny[ValuesType] | AnnotationAny[Mapping[str, Any]]:
        """Gets an annotation by its ID and loads its annotation processes.

        Fetches an annotation from the API by its ID and loads its annotation processes (quorum, status workflow).

        Args:
            id: ID of the annotation to get.
            values_type: Type of annotation values. If None, values will be returned as a dict.
            assert_status_workflow: If `True`, verifies that status workflow is configured and returns an
                `Annotation` with concrete `StatusWorkflowAnnotationProcessViewStrict` type instead of
                `OptionalSW`. Raises `ValueError` if status workflow is not configured.
            kit (AsyncKit): `AsyncKit` instance.

        Returns:
            (Annotation[OptionalQRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType]): If assert_status_workflow
                is True, `Annotation` with concrete `StatusWorkflowAnnotationProcessViewStrict` type.
            (AnnotationAny[ValuesType]): If assert_status_workflow is False, `Annotation` that may or may not have
                status workflow configured.

        Raises:
            ValueError: If `assert_status_workflow` is `True` and status workflow is not configured.

        Examples:
            Get annotation with specific values type:
            ```python
            class MyValues(BaseModel):
                label: str


            annotation = await Annotation.get(id=AnnotationId('123'), values_type=MyValues, kit=kit)
            print(annotation.view.values.label)
            ```

            Get annotation with dict values:
            ```python
            annotation = await Annotation.get(id=AnnotationId('123'), kit=kit)
            print(annotation.view.values['label'])
            ```

            Get annotation with status workflow assertion:
            ```python
            annotation = await Annotation.get(id=AnnotationId('123'), assert_status_workflow=True, kit=kit)
            await annotation.get_status_workflow_responsible()  # Statically type checked
            ```
        """
        kit = kwargs['kit']
        return await cls.from_view(
            view=await kit.annotation_studio.annotation.get(annotation_id=id, values_type=values_type),
            assert_status_workflow=assert_status_workflow,
            **kwargs,
        )

    @overload
    @classmethod
    async def get_by_external_id(
        cls: type[AnnotationAny[ValuesType]],
        external_id: str,
        batch_id: BatchId,
        values_type: type[ValuesType],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationAny[ValuesType] | None: ...

    @overload
    @classmethod
    async def get_by_external_id(
        cls: type[AnnotationAny[Any]],
        external_id: str,
        batch_id: BatchId,
        values_type: None = None,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationAny[Mapping[str, Any]] | None: ...

    @classmethod
    async def get_by_external_id(
        cls: type[AnnotationAny[Any]],
        external_id: str,
        batch_id: BatchId,
        values_type: type[ValuesType] | None = None,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationAny[ValuesType] | AnnotationAny[Mapping[str, Any]] | None:
        """Gets an annotation by its external ID and batch ID, and loads its annotation processes.

        Fetches an annotation from the API by its external ID and batch ID combination, and loads its annotation
        processes (quorum, status workflow). If no annotation is found with the given external ID in the batch, returns
        None.

        Args:
            external_id: External ID of the annotation to get.
            batch_id: ID of the batch containing the annotation.
            values_type: Type of annotation values. If `None`, values will be returned as a dict.
            kit (AsyncKit): `AsyncKit` instance.

        Returns:
            `Annotation` that may or may not have annotation processes configured, or `None` if no annotation is found
                with the given external_id in the batch.

        Examples:
            ```python
            annotation = await Annotation.get_by_external_id(external_id='task1', batch_id='batch123', kit=kit)
            ```
        """
        kit = kwargs['kit']
        annotation_view = await kit.annotation_studio.annotation.find(
            query_params=AnnotationFilterParamV1(
                batch_id=batch_id,
                external_id=external_id,
                limit=1,
            ),
            values_type=values_type,
        )
        if len(annotation_view.data) < 1:
            return None
        assert len(annotation_view.data) == 1, 'There is only one annotation with the same external_id in the batch'

        return await cls.from_view(view=annotation_view.data[0], kit=kit)

    async def refresh(self: Annotation[QRM, SW, ValuesType]) -> Annotation[QRM, SW, ValuesType]:
        """Refreshes the annotation by fetching its latest state from the API.

        Fetches the latest state of the annotation from the API, including its annotation processes
        (quorum, status workflow) and values.

        Returns:
            A new `Annotation` instance with the latest state.

        Examples:
            ```python
            annotation = await annotation.refresh()
            print(annotation.view.values)  # Latest values from the API
            ```
        """

        return cast(
            Annotation[QRM, SW, ValuesType],  # quorum or status_workflow can't disappear from annotation
            await self.get(
                id=self.view.id,
                values_type=type(self.view.values),
                kit=self.kit,
            ),
        )

    def assert_status_workflow(
        self: Annotation[QRM, OptionalSW, ValuesType],
        message: str | None = None,
    ) -> Annotation[QRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType]:
        """Asserts that the annotation has a status workflow configured in its local state.

        Verifies that the annotation has a status workflow process configured in its current local representation,
        without fetching new data from the API. Returns the same annotation with a concrete
        `StatusWorkflowAnnotationProcessViewStrict` type instead of `OptionalSW` or fails.

        Returns:
            The same annotation with a concrete `StatusWorkflowAnnotationProcessViewStrict` type.

        Args:
            message: Custom error message to use when the assertion fails. If None, a default message is used.

        Raises:
            ValueError: If status workflow is not configured in the local representation of this annotation.

        Examples:
            ```python
            annotation = annotation.assert_status_workflow()
            await annotation.get_status_workflow_responsible()  # Statically type checked
            ```
        """
        if has_status_workflow(self):
            return self
        raise ValueError(message or 'Annotation does not have a status workflow')

    def assert_quorum(
        self: Annotation[OptionalQRM, SW, ValuesType],
        message: str | None = None,
    ) -> Annotation[QuorumAnnotationProcessViewStrict, SW, ValuesType]:
        """Asserts that the annotation has a quorum process configured in its local state.

        Verifies that the annotation has a quorum annotation process configured in its current local representation,
        without fetching new data from the API. Returns the same annotation with a concrete
        `QuorumAnnotationProcessViewStrict` type instead of `OptionalQRM` or fails.

        Returns:
            The same annotation with a concrete `QuorumAnnotationProcessViewStrict` type.

        Args:
            message: Custom error message to use when the assertion fails. If None, a default message is used.

        Raises:
            ValueError: If quorum process is not configured in the local representation of this annotation.

        Examples:
            ```python
            annotation = annotation.assert_quorum()
            print(annotation.quorum.data)  # Statically type checked
            ```
        """
        if has_quorum(self):
            return self
        raise ValueError('Annotation does not have a quorum')

    async def get_annotation_edits(
        self,
        sort: Mapping[str, SortValue] | None = None,
    ) -> AsyncGenerator[AnnotationEditViewV1Strict, None]:
        """Returns an asynchronous generator of annotation edit history entries.

        Fetches the history of edits made to this annotation from the API.

        Args:
            sort: Optional mapping of field names to sort orders ('asc' or 'desc'). For example: {'created_at': 'desc'}.

        Returns:
            AsyncGenerator yielding `AnnotationEditViewV1Strict` objects representing each edit in sorted order.

        Examples:
            ```python
            async for edit in annotation.get_annotation_edits(sort={'created_at': 'desc'}):
                print(f'Edit at {edit.created_at}: {edit.values}')
            ```
        """

        async for annotation in self.kit.annotation_studio.annotation_edit.get_all(
            AnnotationEditQueryParamsV1(
                annotation_id=self.view.id,
                batch_id=self.view.batch_id,
                sort=to_sort_string(sort) if sort is not None else None,
            )
        ):
            yield annotation

    async def get_last_annotation_edit(
        self, sort_by: Literal['created_at', 'modified_at'] = 'modified_at'
    ) -> AnnotationEditViewV1Strict | None:
        """Returns the most recent edit made to this annotation.

        Fetches the last edit based on either creation or modification time.

        Args:
            sort_by: Field to use for determining the most recent edit.

                * `'created_at'`: Sort by creation time
                * `'modified_at'`: Sort by modification time (default)

        Returns:
            The most recent `AnnotationEditViewV1Strict` or None if no edits exist.

        Examples:
            ```python
            last_edit = await annotation.get_last_annotation_edit()
            if last_edit:
                print(f'Last edited at: {last_edit.modified_at}')
            ```
        """

        annotation_edits = await self.kit.annotation_studio.annotation_edit.find(
            AnnotationEditQueryParamsV1(annotation_id=self.view.id, sort=to_sort_string({sort_by: 'desc'}), limit=1),
        )

        return annotation_edits.data[0] if len(annotation_edits.data) >= 1 else None

    async def get_last_version(self) -> int | None:
        annotation_edit = await self.get_last_annotation_edit(sort_by='modified_at')
        if annotation_edit is None:
            return None
        return annotation_edit.annotation_version

    @property
    def status(self: AnnotationWithStatusWorkflow[QRM, ValuesType]) -> str:
        assert self.status_workflow.data.status is not None
        return self.status_workflow.data.status

    async def update_status(
        self: AnnotationWithStatusWorkflow[QRM, ValuesType],
        status: str,
        active_edit_action: Literal['SUBMIT', 'SKIP', 'EXPIRE', 'FAIL'] = 'SUBMIT',
        comment: str | None = None,
        unavailable_for: Sequence[str] | None = None,
        responsible: Literal['client_requester', 'previous'] | str | None = 'previous',
    ) -> Annotation[QRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType]:
        """Updates the status of an annotation in its status workflow.

        Changes the current status of the annotation to a new one or updates the current status. Only statuses listed in
        allowed_transitions or current status can be set.

        Args:
            status: New status to set.
            active_edit_action: What to do with the active annotation edit when changing status:

                * `'SUBMIT'`: Submit the active annotation edit
                * `'SKIP'`: Cancel the active edit with "SKIPPED" cancellation_reason
                * `'EXPIRE'`: Cancel the active edit with "EXPIRED" cancellation_reason
                * `'FAIL'`: Raise an error if there is an active edit and do not change the status
            comment: Optional comment explaining the status change. It will appear in performers' Activity History.
            unavailable_for: list of account IDs, if specified, the annotation will be unavailable for these accounts
                after the status change.
            responsible: Account ID that will be responsible for the annotation after the status change. Can be:
                'previous': Keep current responsible
                'client_requester': Set current requester as responsible. Requester will be inferred from the configured
                    `AsyncKit` instance.
                None: Unassign the current responsible account.
                If the status is set to `in_progress`,
                the annotation will revert to its initial state without a responsible account.
                str: Set specific account ID as responsible

        Returns:
            Updated annotation with new status workflow state.

        Raises:
            RuntimeError: If the requested status transition is not allowed.

        Examples:
            ```python
            annotation = await annotation.update_status(
                status='accepted', comment='Looks good', responsible='client_requester'
            )
            ```
        """

        if self.status_workflow.data.status != status and (
            self.status_workflow.data.allowed_transitions is None
            or status not in self.status_workflow.data.allowed_transitions
        ):
            raise RuntimeError(f'Status {status} is not available for annotation {self.view.id}')

        if responsible == 'previous':
            if self.status_workflow.data.responsible is None:
                responsible_account_id = None
            else:
                responsible_account_id = self.status_workflow.data.responsible.account_id
        elif responsible == 'client_requester':
            responsible_account_id = await self.kit.annotation_studio.get_account_id()
        elif responsible is None and self.status_workflow.data.status != status:
            raise RuntimeError('Cannot remove responsible account while changing status.')
        else:
            responsible_account_id = responsible

        request = UpdateStatusWorkflowForm(
            annotation_process_id=self.status_workflow.id,
            status=status,
            active_edit_action=active_edit_action,
            responsible_account_id=responsible_account_id,
            comment=comment,
            unavailable_for=unavailable_for,
        )
        updated_status_workflow = (await self.kit.annotation_studio.status_workflow.update_statuses(forms=[request]))[0]
        return Annotation(
            view=self.view,
            status_workflow=updated_status_workflow,
            quorum=self.quorum,
            kit=self.kit,
        )

    async def remove_responsible(
        self: AnnotationWithStatusWorkflow[QRM, ValuesType],
        active_edit_action: Literal['SUBMIT', 'SKIP', 'EXPIRE', 'FAIL'] = 'SKIP',
    ) -> Annotation[QRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType]:
        """Removes the current responsible account from the annotation, setting the responsible field to None.

        Args:
            active_edit_action: What to do with the active annotation edit when changing status:

                * `'SUBMIT'`: Submit the active annotation edit
                * `'SKIP'`: Cancel the active edit with "SKIPPED" cancellation_reason
                * `'EXPIRE'`: Cancel the active edit with "EXPIRED" cancellation_reason
                * `'FAIL'`: Raise an error if there is an active edit and do not change the status

        Returns:
            Updated annotation without a responsible account. If the current status is set to `in_progress`,
                the annotation will revert to its initial state without a responsible account.

        Raises:
            RuntimeError: If the removal of the responsible account is not allowed for the current status.

        Examples:
            ```python
            annotation = await annotation.remove_responsible()
            ```
        """
        return await self.update_status(
            status=self.status,
            active_edit_action=active_edit_action,
            responsible=None,
        )

    def get_status_workflow_responsible(
        self: Annotation[QRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType],
    ) -> StatusWorkflowAnnotationProcessViewUserViewStrict | None:
        """Returns the account currently responsible for this annotation.

        Returns:
            User view of the currently responsible account or None if no one is specified as responsible.

        Examples:
            ```python
            responsible = annotation.get_status_workflow_responsible()
            if responsible:
                print(f'Assigned to: {responsible.account_id}')
            ```
        """
        return self.status_workflow.data.responsible

    async def update(self: Annotation[QRM, SW, Any], values: NewValuesType) -> Annotation[QRM, SW, NewValuesType]:
        """Updates the values of this annotation.

        Updates current values of annotation. This will not create new `Annotation` Edit but will update the current
        values of the annotation. If there is an active annotation edit (with `'IN_PROGRESS'` status) for this
        annotation this operation will fail.

        Args:
            values: New values for the annotation. Can be either a mapping or a `BaseModel` subclass instance.

        Returns:
            Updated annotation with new values of possibly different type.

        Examples:
            ```python
            annotation = await annotation.edit({'label': 'cat'})
            print(annotation.view.values['label'])


            class NewValues(BaseModel):
                label: str = 'cat'


            annotation = await annotation.edit(NewValues())
            print(annotation.view.values.label)
            ```
        """
        updated_view = await self.kit.annotation_studio.annotation.edit(
            self.view.id, form=EditAnnotationFormV1Strict(values=values)
        )
        return Annotation(
            updated_view,
            quorum=self.quorum,
            status_workflow=self.status_workflow,
            kit=self.kit,
        )

    @property
    def created_at(self) -> datetime.datetime:
        return DATETIME_ADAPTER.validate_python(self.view.created_at)

    @property
    def modified_at(self) -> datetime.datetime | None:
        return OPTIONAL_DATETIME_ADAPTER.validate_python(self.view.modified_at)

    async def get_annotation_group(self) -> AnnotationGroupAny:
        """Returns the annotation group this annotation belongs to.

        Returns:
            `AnnotationGroup` instance or None if annotation doesn't belong to a group.
        """

        from toloka.a9s.client.entities.annotation_group import AnnotationGroup

        return await AnnotationGroup.get(
            id=self.view.annotation_group_id,
            batch_id=self.view.batch_id,
            kit=self.kit,
        )


AnnotationWithStatusWorkflow: TypeAlias = Annotation[QRM, StatusWorkflowAnnotationProcessViewStrict, ValuesType]


def has_status_workflow(
    annotation: Annotation[QRM, OptionalSW, ValuesType],
) -> TypeGuard[AnnotationWithStatusWorkflow[QRM, ValuesType]]:
    return annotation.status_workflow is not None


def has_no_status_workflow(
    annotation: Annotation[QRM, OptionalSW, ValuesType],
) -> TypeGuard[Annotation[QRM, None, ValuesType]]:
    return annotation.status_workflow is None


AnnotationWithQuorum: TypeAlias = Annotation[QuorumAnnotationProcessViewStrict, SW, ValuesType]


def has_quorum(
    annotation: Annotation[OptionalQRM, SW, ValuesType],
) -> TypeGuard[AnnotationWithQuorum[SW, ValuesType]]:
    return annotation.quorum is not None


def has_no_quorum(
    annotation: Annotation[OptionalQRM, SW, ValuesType],
) -> TypeGuard[Annotation[None, SW, ValuesType]]:
    return annotation.quorum is None
