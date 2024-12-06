from __future__ import annotations

import datetime
import logging
from functools import partial
from typing import Any, AsyncGenerator, Generic, Literal, Mapping, Sequence, TypeGuard, overload
from uuid import UUID

from pydantic import BaseModel
from typing_extensions import Unpack

from toloka.a9s.client.client import AsyncKit
from toloka.a9s.client.entities.annotation import Annotation
from toloka.a9s.client.entities.annotation import has_no_quorum as annotation_has_no_quorum
from toloka.a9s.client.entities.annotation.types import OptionalQRM as AnnotationOptionalQRM
from toloka.a9s.client.entities.annotation.types import OptionalSW as AnnotationOptionalSW
from toloka.a9s.client.entities.annotation_group import AnnotationGroup
from toloka.a9s.client.entities.base import EntityApiBase, EntityApiBaseParams, LazyValue
from toloka.a9s.client.entities.batch.types import (
    GT,
    MC,
    QM,
    QRM,
    SW,
    BatchAnyEager,
    BatchAnyLazy,
    BatchView,
    BatchWithGroundTruth,
    BatchWithMoneyConfig,
    BatchWithoutQuorum,
    BatchWithQualityManagement,
    BatchWithQuorum,
    BatchWithStatusWorkflow,
    LazyFromId,
    LazyFromView,
    OptionalGT,
    OptionalMC,
    OptionalQM,
    OptionalQRM,
    OptionalSW,
)
from toloka.a9s.client.entities.money_config import (
    BaseAnnotationMoneyConfigFormParams,
    BaseBuildStatusWorkflowMoneyConfigFormParams,
    build_annotation_money_config_form,
    build_status_workflow_money_config_form,
)
from toloka.a9s.client.models.annotation_process import UploadFormV1DataStrict
from toloka.a9s.client.models.annotation_process.quorum import (
    QuorumAnnotationProcessParametersStrict,
)
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowConfigViewStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    QuorumAnnotationProcessViewStrict,
    StatusWorkflowAnnotationProcessViewStrict,
)
from toloka.a9s.client.models.batch import (
    BatchUpdateFormV1Strict,
    BatchUploadForm,
    BatchViewV1Strict,
    GetRestrictionsForm,
)
from toloka.a9s.client.models.extension_id import (
    GROUND_TRUTH_EXTENSION_ID,
    MONEY_CONFIG_EXTENSION_ID,
    QUALITY_CONFIG_EXTENSION_ID,
    ExtensionId,
)
from toloka.a9s.client.models.extensions import (
    find_extension_instance_id,
    with_ground_truth_extension_batch,
    with_money_config_extension_batch,
    with_quality_config_extension_batch,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.form import (
    AnnotationFormV1,
    UploadAnnotationFormV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_params import (
    StatusWorkflowAnnotationProcessParameters,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.restriction.web.v0.form import (
    GetRestrictionListQueryParamsV0,
    RestrictionFormV0,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.services.batch.web.v1.model.form import BatchUpdateFormV1
from toloka.a9s.client.models.generated.ai.toloka.gts.config.web.v0.form import GroundTruthConfigForm
from toloka.a9s.client.models.ground_truth import GroundTruthConfigViewV0Strict
from toloka.a9s.client.models.money_config import (
    MoneyConfigFormStrict,
    MoneyConfigIdViewStrict,
    MoneyConfigViewStrict,
)
from toloka.a9s.client.models.quality_management.config import (
    QualityConfigFormV0Strict,
    QualityConfigViewV0Strict,
)
from toloka.a9s.client.models.quality_management.restriction import RestrictionViewV0Strict
from toloka.a9s.client.models.types import BatchId, GroundTruthConfigId, MoneyConfigId, QualityConfigId
from toloka.a9s.client.models.utils import DATETIME_ADAPTER

logger = logging.getLogger(__name__)


class Batch(EntityApiBase, Generic[BatchView, MC, GT, QM, QRM, SW]):
    """
    An Annotation Studio batch that can be configured with various extensions and annotation processes.

    A batch represents a collection of annotations that can be configured with different extensions
    (money config, ground truth, quality management) and annotation processes (quorum, status workflow).
    The class supports both eager and lazy loading of configurations. Usually you don't need to create
    instances of this class directly, use `Batch.get` method to load batch
    from the API.

    Generic type parameters:

    * `BatchView`: Type of the batch API representation
    * `MC`: Type of money config extension
    * `GT`: Type of ground truth extension
    * `QM`: Type of quality management extension
    * `QRM`: Type of quorum annotation process
    * `SW`: Type of status workflow annotation process

    Each type parameter represents extension or annotation process configuration, possible values are:

    * `None`: Not configured
    * `T`: Configured and loaded from the API
    * `LazyFrom*[T | None]`: Not loaded from API (may either be configured or not)

    Attributes:
        batch_id: Identifier for the existing batch
        view: API representation of the batch
        money_config: Payment settings for annotators
        ground_truth: Ground truth storage connection settings
        quality_management: Quality control and restrictions settings
        quorum_config: Quorum settings - how many annotations required per group
        status_workflow_config: Configuration for annotation status transitions

    Examples:
        Load batch with all configurations (default):
        ```python
        batch = await Batch.get(batch_id=BatchId('existing-batch-id-here'), lazy=False, kit=kit)
        print(batch.view.status)
        ```

        Load batch with lazy loading of configurations:
        ```python
        # no actual API calls are made in .get method
        batch = await Batch.get(batch_id=BatchId('existing-batch-id-here'), lazy=True, kit=kit)
        loaded_batch = await batch.fetch_view()
        print(loaded_batch.view.status)
        ```
    """

    batch_id: BatchId
    view: BatchView

    money_config: MC
    ground_truth: GT
    quality_management: QM
    quorum_config: QRM
    status_workflow_config: SW

    def __init__(
        self,
        batch_id: BatchId,
        view: BatchView,
        money_config: MC,
        ground_truth: GT,
        quality_management: QM,
        quorum_config: QRM,
        status_workflow_config: SW,
        **kwargs: Unpack[EntityApiBaseParams],
    ):
        super().__init__(**kwargs)
        self.batch_id = batch_id
        self.view = view
        self.money_config = money_config
        self.ground_truth = ground_truth
        self.quality_management = quality_management
        self.quorum_config = quorum_config
        self.status_workflow_config = status_workflow_config

        self.validate_view_is_consistent_with_extensions()

    def _validate_extension_consistency(
        self,
        config_id: str | UUID,
        extension_id: ExtensionId,
    ) -> None:
        if not is_view_loaded(self):
            return

        extension_instance_id = find_extension_instance_id(self.view.extensions, extension_id)
        if str(config_id) != str(extension_instance_id):
            raise ValueError(
                f'Inconsistency detected: {MONEY_CONFIG_EXTENSION_ID} extension ID in batch ({extension_instance_id}) '
                f'does not match the config ID ({config_id})'
            )

    def validate_ground_truth_is_consistent_with_extensions(self) -> None:
        if not is_view_loaded(self):
            return

        if isinstance(self.ground_truth, GroundTruthConfigViewV0Strict):
            self._validate_extension_consistency(
                extension_id=GROUND_TRUTH_EXTENSION_ID,
                config_id=self.ground_truth.id,
            )

    def validate_money_config_is_consistent_with_extensions(self) -> None:
        if not is_view_loaded(self):
            return

        if isinstance(self.money_config, MoneyConfigViewStrict):
            self._validate_extension_consistency(
                extension_id=MONEY_CONFIG_EXTENSION_ID,
                config_id=self.money_config.config_id,
            )

    def validate_quality_management_is_consistent_with_extensions(self) -> None:
        if not is_view_loaded(self):
            return

        if isinstance(self.quality_management, QualityConfigViewV0Strict):
            self._validate_extension_consistency(
                extension_id=QUALITY_CONFIG_EXTENSION_ID,
                config_id=self.quality_management.id,
            )

    def validate_view_is_consistent_with_extensions(self) -> None:
        self.validate_ground_truth_is_consistent_with_extensions()
        self.validate_money_config_is_consistent_with_extensions()
        self.validate_quality_management_is_consistent_with_extensions()

    async def update(
        self: Batch[BatchView, MC, GT, QM, QRM, SW],
        form: BatchUpdateFormV1,
    ) -> Batch[BatchViewV1Strict, MC, GT, QM, QRM, SW]:
        """Updates batch view from the form.

        Current extensions configurations remain unchanged. Updated view must be consistent with current extensions
        (i.e. it should not remove or introduce any extensions to the `extensions` field which are aknowledged by this
        class).

        Args:
            form: Batch update parameters

        Returns:
            Updated batch with updated view and same extensions configurations

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), kit=kit)
            form = BatchUpdateFormV1Strict.from_view(batch.view)
            form.private_name = 'New name'
            updated_batch = await batch.update(form)
            print(updated_batch.view.private_name)  # 'New name'
            ```
        """

        updated_view = await self.kit.annotation_studio.batch.update(
            batch_id=self.batch_id,
            form=form,
        )
        return Batch(
            batch_id=self.batch_id,
            view=updated_view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=self.status_workflow_config,
            kit=self.kit,
        )

    @staticmethod
    async def _fetch_view(batch_id: BatchId, kit: AsyncKit) -> BatchViewV1Strict:
        return await kit.annotation_studio.batch.get(batch_id)

    @staticmethod
    async def _fetch_money_config(view: BatchViewV1Strict, kit: AsyncKit) -> OptionalMC:
        money_config_id = find_extension_instance_id(view.extensions, MONEY_CONFIG_EXTENSION_ID)
        if money_config_id:
            return await kit.experts_portal.money_config.get_last_version(
                config_id=MoneyConfigId(UUID(money_config_id))
            )
        return None

    @staticmethod
    async def _fetch_ground_truth(view: BatchViewV1Strict, kit: AsyncKit) -> OptionalGT:
        ground_truth_config_id = find_extension_instance_id(view.extensions, GROUND_TRUTH_EXTENSION_ID)
        if ground_truth_config_id:
            return await kit.annotation_studio.ground_truth_config.get(id=GroundTruthConfigId(ground_truth_config_id))
        return None

    @staticmethod
    async def _fetch_quality_management(view: BatchViewV1Strict, kit: AsyncKit) -> OptionalQM:
        quality_config_id = find_extension_instance_id(view.extensions, QUALITY_CONFIG_EXTENSION_ID)
        if quality_config_id:
            return await kit.quality_management.quality_config.get(id=QualityConfigId(quality_config_id))
        return None

    @staticmethod
    async def _fetch_quorum_config(view: BatchViewV1Strict, kit: AsyncKit) -> OptionalQRM:
        sw = await kit.annotation_studio.quorum.get_batch_defaults(batch_id=view.id)
        if sw is None:
            return await kit.annotation_studio.quorum.get_project_defaults(project_id=view.project_id)
        return sw

    @staticmethod
    async def _fetch_status_workflow_config(view: BatchViewV1Strict, kit: AsyncKit) -> OptionalSW:
        sw = await kit.annotation_studio.status_workflow.get_batch_defaults(batch_id=view.id)
        if sw is None:
            return await kit.annotation_studio.status_workflow.get_project_defaults(project_id=view.project_id)
        return sw

    @overload
    @classmethod
    async def get(
        cls: type[Batch],
        batch_id: BatchId,
        lazy: Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> BatchAnyEager: ...

    @overload
    @classmethod
    async def get(
        cls: type[Batch],
        batch_id: BatchId,
        lazy: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> BatchAnyLazy: ...

    @classmethod
    async def get(
        cls: type[Batch],
        batch_id: BatchId,
        lazy: Literal[True] | Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> BatchAnyEager | BatchAnyLazy:
        """Gets a batch by its ID and loads its representation and extensions configurations.

        Args:
            batch_id: ID of the batch to get
            lazy: If True, no API requests will be made immediately. Instead, configurations will be loaded lazily when
                requested. Lazyness is stored in type, later you can ensure that value is loaded using .fetch_* methods.
            kit (AsyncKit): AsyncKit instance

        Returns:
            (BatchAnyEager): If `lazy=True`, batch with lazy configurations that will be loaded on first access
            (BatchAnyLazy): If `lazy=False`, batch with all available configurations loaded from API

        Examples:
            Load batch with all configurations:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=False, kit=kit)
            print(batch.view.status)
            ```

            Load batch with lazy loading:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
            print(batch.view.status)  # will raise an error during type checking
            loaded = await batch.fetch_view()
            print(loaded.view.status)
            ```
        """

        kit = kwargs['kit']

        if lazy:
            return Batch[
                LazyFromId[BatchViewV1Strict],
                LazyFromView[OptionalMC],
                LazyFromView[OptionalGT],
                LazyFromView[OptionalQM],
                LazyFromView[OptionalQRM],
                LazyFromView[OptionalSW],
            ](
                batch_id=batch_id,
                view=LazyValue(partial(cls._fetch_view, kit=kit)),
                money_config=LazyValue(partial(cls._fetch_money_config, kit=kit)),
                ground_truth=LazyValue(partial(cls._fetch_ground_truth, kit=kit)),
                quality_management=LazyValue(partial(cls._fetch_quality_management, kit=kit)),
                quorum_config=LazyValue(partial(cls._fetch_quorum_config, kit=kit)),
                status_workflow_config=LazyValue(partial(cls._fetch_status_workflow_config, kit=kit)),
                **kwargs,
            )
        else:
            view = await cls._fetch_view(batch_id, kit)
            return Batch[
                BatchViewV1Strict,
                OptionalMC,
                OptionalGT,
                OptionalQM,
                OptionalQRM,
                OptionalSW,
            ](
                batch_id=batch_id,
                view=view,
                money_config=await cls._fetch_money_config(view, kit),
                ground_truth=await cls._fetch_ground_truth(view, kit),
                quality_management=await cls._fetch_quality_management(view, kit),
                quorum_config=await cls._fetch_quorum_config(view, kit),
                status_workflow_config=await cls._fetch_status_workflow_config(view, kit),
                **kwargs,
            )

    @overload
    async def refresh(self, lazy: Literal[True]) -> BatchAnyLazy: ...

    @overload
    async def refresh(self, lazy: Literal[False] = False) -> BatchAnyEager: ...

    async def refresh(self, lazy: Literal[True] | Literal[False] = False) -> BatchAnyEager | BatchAnyLazy:
        if lazy:
            return await self.get(
                self.batch_id,
                lazy,
                kit=self.kit,
            )
        else:
            return await self.get(
                self.batch_id,
                lazy,
                kit=self.kit,
            )

    async def fetch_view(self) -> Batch[BatchViewV1Strict, MC, GT, QM, QRM, SW]:
        """Fetches the batch view from the API if it was loaded lazily.

        Loads the batch view from the API if it wasn't loaded initially (lazy=True was used). Returns the same batch
        instance if view was already loaded.

        Returns:
            Batch with view loaded from API

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
            loaded = await batch.fetch_view()
            print(loaded.view.status)
            ```
        """

        if is_view_loaded(self):
            return self
        # make check TypeIs after https://github.com/python/mypy/pull/17232 is merged
        assert isinstance(self.view, LazyValue)
        return Batch(
            batch_id=self.batch_id,
            view=await self.view(self.batch_id),
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=self.status_workflow_config,
            kit=self.kit,
        )

    async def fetch_money_config(self) -> Batch[BatchViewV1Strict, OptionalMC, GT, QM, QRM, SW]:
        """Fetches the money config from the API if it was loaded lazily.

        Loads the money config from the API if it wasn't loaded initially (lazy=True was used).
        Returns the same batch instance if money config was already loaded.

        Returns:
            Batch with money config loaded from API if it exists

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
            loaded = await batch.fetch_money_config()
            if has_batch_money_config(loaded):  # money config may not exists at all
                print(loaded.money_config.config_id)
            ```
        """

        if is_money_config_loaded(self):
            return await self.fetch_view()
        # make check TypeIs after https://github.com/python/mypy/pull/17232 is merged
        assert isinstance(self.money_config, LazyValue)
        batch_with_view = await self.fetch_view()
        return Batch(
            batch_id=batch_with_view.batch_id,
            view=batch_with_view.view,
            money_config=await self.money_config(batch_with_view.view),
            ground_truth=batch_with_view.ground_truth,
            quality_management=batch_with_view.quality_management,
            quorum_config=batch_with_view.quorum_config,
            status_workflow_config=batch_with_view.status_workflow_config,
            kit=batch_with_view.kit,
        )

    async def fetch_ground_truth(self) -> Batch[BatchViewV1Strict, MC, OptionalGT, QM, QRM, SW]:
        """Fetches the ground truth config from the API if it was loaded lazily.

        Loads the ground truth config from the API if it wasn't loaded initially (lazy=True was used).
        Returns the same batch instance if ground truth config was already loaded.

        Returns:
            Batch with ground truth config loaded from API if it exists

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
            loaded = await batch.fetch_ground_truth()
            if has_batch_ground_truth(loaded):  # ground truth config may not exist at all
                print(loaded.ground_truth.id)
            ```
        """

        if is_ground_truth_loaded(self):
            return await self.fetch_view()
        # make check TypeIs after https://github.com/python/mypy/pull/17232 is merged
        assert isinstance(self.ground_truth, LazyValue)
        batch_with_view = await self.fetch_view()
        return Batch(
            batch_id=batch_with_view.batch_id,
            view=batch_with_view.view,
            money_config=batch_with_view.money_config,
            ground_truth=await self.ground_truth(batch_with_view.view),
            quality_management=batch_with_view.quality_management,
            quorum_config=batch_with_view.quorum_config,
            status_workflow_config=batch_with_view.status_workflow_config,
            kit=batch_with_view.kit,
        )

    async def fetch_quality_management(self) -> Batch[BatchViewV1Strict, MC, GT, OptionalQM, QRM, SW]:
        """Fetches the quality management config from the API if it was loaded lazily.

        Loads the quality management config from the API if it wasn't loaded initially (lazy=True was used).
        Returns the same batch instance if quality management config was already loaded.

        Returns:
            Batch with quality management config loaded from API if it exists

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
            loaded = await batch.fetch_quality_management()
            if has_batch_quality_management(loaded):  # quality management config may not exist at all
                print(loaded.quality_management.id)
            ```
        """

        if is_quality_management_loaded(self):
            return await self.fetch_view()
        # make check TypeIs after https://github.com/python/mypy/pull/17232 is merged
        assert isinstance(self.quality_management, LazyValue)
        batch_with_view = await self.fetch_view()
        return Batch(
            batch_id=batch_with_view.batch_id,
            view=batch_with_view.view,
            money_config=batch_with_view.money_config,
            ground_truth=batch_with_view.ground_truth,
            quality_management=await self.quality_management(batch_with_view.view),
            quorum_config=batch_with_view.quorum_config,
            status_workflow_config=batch_with_view.status_workflow_config,
            kit=batch_with_view.kit,
        )

    async def fetch_quorum_config(self) -> Batch[BatchView, MC, GT, QM, OptionalQRM, SW]:
        """Fetches the quorum config from the API if it was loaded lazily.

        Loads the quorum config from the API if it wasn't loaded initially (lazy=True was used).
        Returns the same batch instance if quorum config was already loaded.

        Returns:
            Batch with quorum config loaded from API if it exists

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
            loaded = await batch.fetch_quorum_config()
            if has_quorum(loaded):  # quorum config may not exist at all
                print(loaded.quorum_config.data)
            ```
        """

        if is_quorum_loaded(self):
            return self
        # make check TypeIs after https://github.com/python/mypy/pull/17232 is merged
        assert isinstance(self.quorum_config, LazyValue)
        batch_with_view = await self.fetch_view()
        return Batch(
            batch_id=self.batch_id,
            view=self.view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=await self.quorum_config(batch_with_view.view),
            status_workflow_config=self.status_workflow_config,
            kit=self.kit,
        )

    async def fetch_status_workflow_config(self) -> Batch[BatchView, MC, GT, QM, QRM, OptionalSW]:
        """Fetches the status workflow config from the API if it was loaded lazily.

        Loads the status workflow config from the API if it wasn't loaded initially (lazy=True was used).
        Returns the same batch instance if status workflow config was already loaded.

        Returns:
            Batch with status workflow config loaded from API if it exists

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
            loaded = await batch.fetch_status_workflow_config()
            if has_status_workflow(loaded):  # status workflow config may not exist at all
                print(loaded.status_workflow_config)
            ```
        """

        if is_status_workflow_loaded(self):
            return self
        # make check TypeIs after https://github.com/python/mypy/pull/17232 is merged
        assert isinstance(self.status_workflow_config, LazyValue)
        batch_with_view = await self.fetch_view()
        return Batch(
            batch_id=self.batch_id,
            view=self.view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=await self.status_workflow_config(batch_with_view.view),
            kit=self.kit,
        )

    # region uploading data API

    @overload
    async def upload(
        self: BatchWithQuorum[BatchView, MC, GT, QM, SW], form: BatchUploadForm
    ) -> list[AnnotationGroup[QuorumAnnotationProcessViewStrict]]: ...

    @overload
    async def upload(
        self: BatchWithoutQuorum[BatchView, MC, GT, QM, StatusWorkflowConfigViewStrict],
        form: BatchUploadForm,
    ) -> list[Annotation[None, StatusWorkflowAnnotationProcessViewStrict, Mapping[str, Any]]]: ...

    @overload
    async def upload(
        self: BatchWithoutQuorum[BatchView, MC, GT, QM, None], form: BatchUploadForm
    ) -> list[Annotation[None, None, Mapping[str, Any]]]: ...

    @overload
    async def upload(
        self: BatchWithoutQuorum[BatchView, MC, GT, QM, OptionalSW], form: BatchUploadForm
    ) -> list[Annotation[None, AnnotationOptionalSW, Mapping[str, Any]]]: ...

    async def upload(
        self: Batch, form: BatchUploadForm
    ) -> (
        list[AnnotationGroup[QuorumAnnotationProcessViewStrict]]
        | list[AnnotationGroup[QuorumAnnotationProcessViewStrict | None]]
        | list[Annotation[None, StatusWorkflowAnnotationProcessViewStrict, Mapping[str, Any]]]
        | list[Annotation[None, None, Mapping[str, Any]]]
        | list[Annotation[None, StatusWorkflowAnnotationProcessViewStrict | None, Mapping[str, Any]]]
    ):
        """Upload data to create annotations or annotation groups in the batch.

        Based on the batch configuration, this method will create either annotations or annotation groups:
        * for batches with quorum configured: creates annotation groups that require multiple annotations;
        * for batches without quorum: сreates individual annotations.

        Return type can be statically inferred if batch configuration is known.

        Args:
            form: BatchUploadForm containing the data to upload.

        Returns:
            (list[AnnotationGroup[QuorumAnnotationProcessViewStrict]]): list of `AnnotationGroup` with quorum process
                for batches with quorum
            (list[Annotation[None, StatusWorkflowAnnotationProcessViewStrict | None, Mapping[str, Any]]]): list of
                `Annotation` (with status workflow if status workflow is configured for batch)

        Examples:
            Upload data to a batch:
            ```python
            from toloka.a9s.client.models.annotation_process import UploadFormV1DataStrict

            batch = await Batch.get(batch_id=BatchId('existing-batch-id-here'), kit=kit)
            form = BatchUploadForm(data=[UploadFormV1DataStrict(draft_values={'text': 'Sample text'})])
            if has_quorum(batch):
                # annotation_groups type is list[AnnotationGroup[QuorumAnnotationProcessViewStrict]] here
                annotation_groups = await batch.upload(form)
            elif has_no_quorum(batch):
                # annotations type is list[Annotation[None, OptionalSW, Mapping[str, Any]]] here
                annotations = await batch.upload(form)
            ```
        """

        uploaded_data = await self.kit.annotation_studio.annotation_process.upload_data(
            form.to_upload_form(self.batch_id)
        )
        if len(uploaded_data.data) == 0:
            return []

        annotations_created = uploaded_data.data[0].annotation_id is not None
        if annotations_created:
            annotations: list[
                Annotation[None, StatusWorkflowAnnotationProcessViewStrict | None, Mapping[str, Any]]
            ] = []
            for item in uploaded_data.data:
                assert (
                    item.annotation_id is not None
                ), 'Either all uploaded items are annotations or all are annotation groups'
                annotation = await Annotation.get(id=item.annotation_id, kit=self.kit)
                assert annotation_has_no_quorum(annotation), 'Otherwise annotation groups would have been created'
                annotations.append(annotation)
            self_with_sw = await self.fetch_status_workflow_config()
            if has_status_workflow(self_with_sw):
                return [annotation.assert_status_workflow() for annotation in annotations]
            return annotations
        else:
            annotation_groups = [
                await AnnotationGroup.get(id=item.annotation_group_id, batch_id=self.batch_id, kit=self.kit)
                for item in uploaded_data.data
            ]
            self_with_quorum = await self.fetch_quorum_config()
            if has_quorum(self_with_quorum):
                return [group.assert_quorum() for group in annotation_groups]
            return annotation_groups

    async def upload_to_quorum(
        self: BatchWithQuorum[BatchView, MC, GT, QM, SW],
        values: Mapping[str, Any] | BaseModel,
        external_id: str | None,
        unavailable_for: list[str] | None = None,
    ) -> AnnotationGroup[QuorumAnnotationProcessViewStrict]:
        """Upload a single item to create an annotation group in a batch with quorum.

        Args:
            values: Initial values for the annotation, either as a mapping or BaseModel instance.
            external_id: External identifier for the uploaded item. If annotation group with the same external_id
                exists it will be returned unchanged from this method.
            unavailable_for: Optional list of account IDs for whom this annotation should be unavailable for labeling.

        Returns:
            AnnotationGroup with quorum process configuration.

        Raises:
            ValueError: If called on a batch without quorum configuration.

        Examples:
            Upload single item to a batch with quorum:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-with-quorum'), kit=kit)
            batch_with_quorum = await batch.assert_quorum()
            group = await batch_with_quorum.upload_to_quorum(values={'text': 'Sample text'}, external_id='text-1')
            ```
        """

        form = BatchUploadForm(
            data=[
                UploadFormV1DataStrict(
                    external_id=external_id,
                    draft_values=values,
                )
            ]
        )
        if unavailable_for:
            form.data[0].params = [
                QuorumAnnotationProcessParametersStrict(
                    unavailable_for=unavailable_for,
                ),
            ]

        result = (await self.upload(form))[0]
        if not isinstance(result, AnnotationGroup):
            raise ValueError(
                'Expected an annotation group, but got an annotation. Batch configuration may have changed.'
            )
        return result

    @overload
    async def upload_annotation(
        self: BatchWithStatusWorkflow[BatchView, MC, GT, QM, QRM],
        values: Mapping[str, Any],
        external_id: str | None = None,
        unavailable_for: Sequence[str] | None = None,
    ) -> Annotation[AnnotationOptionalQRM, StatusWorkflowAnnotationProcessViewStrict, Mapping[str, Any]]: ...

    @overload
    async def upload_annotation(
        self,
        values: Mapping[str, Any],
        external_id: str | None = None,
        unavailable_for: None = None,
    ) -> Annotation[AnnotationOptionalQRM, AnnotationOptionalSW, Mapping[str, Any]]: ...

    async def upload_annotation(
        self,
        values: Mapping[str, Any],
        external_id: str | None = None,
        unavailable_for: Sequence[str] | None = None,
    ) -> Annotation[AnnotationOptionalQRM, AnnotationOptionalSW, Mapping[str, Any]]:
        """Upload a single annotation to a batch.

        This method allows uploading individual annotations to batches. Any annotation group level annotation processes
        configured for the batch will not be created.

        Args:
            values: Initial values for the annotation as a mapping
            external_id: Optional external identifier for the uploaded annotation. If an annotation with the same
                external_id exists in the batch, it will be returned unchanged.
            unavailable_for: Optional list of account IDs for whom this annotation should be unavailable for labeling.
                Only valid for batches with status workflow configured.

        Returns:
            Annotation (with status workflow if status workflow is configured for batch).

        Examples:
            Upload single annotation to a batch:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), kit=kit)
            annotation = await batch.upload_annotation(values={'text': 'Sample text'}, external_id='text-1')
            ```
        """

        if unavailable_for is None:
            params = None
        else:
            params = [
                StatusWorkflowAnnotationProcessParameters(
                    unavailable_for=unavailable_for,
                    type='status-workflow',
                )
            ]

        uploaded = await self.kit.annotation_studio.annotation.upload(
            form=UploadAnnotationFormV1(
                batch_id=self.batch_id,
                annotations=[
                    AnnotationFormV1(
                        external_id=external_id,
                        values=values,
                        params=params,
                    )
                ],
            )
        )
        return await Annotation.from_view(
            view=uploaded.annotations[0],
            kit=self.kit,
        )

    # endregion

    # region batch status API

    async def start(self) -> Batch[BatchViewV1Strict, MC, GT, QM, QRM, SW]:
        """Changes batch status to 'STARTED' to allow submiting annotation edits or quorum annotations.

        Returns:
            Updated batch with updated view containing 'STARTED' status.

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), kit=kit, lazy=True)
            started_batch = await batch.start()
            print(started_batch.view.status)  # 'STARTED'
            ```
        """

        updated_view = await self.kit.annotation_studio.batch.start(batch_id=self.batch_id)
        return Batch(
            batch_id=self.batch_id,
            view=updated_view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=self.status_workflow_config,
            kit=self.kit,
        )

    async def stop(self) -> Batch[BatchViewV1Strict, MC, GT, QM, QRM, SW]:
        """Changes batch status to 'STOPPED' to prevent submiting annotation edits or quorum annotations.

        Returns:
            Updated batch with updated view containing 'STOPPED' status.

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), kit=kit, lazy=True)
            stopped_batch = await batch.stop()
            print(stopped_batch.view.status)  # 'STOPPED'
            ```
        """
        updated_view = await self.kit.annotation_studio.batch.stop(batch_id=self.batch_id)
        return Batch(
            batch_id=self.batch_id,
            view=updated_view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=self.status_workflow_config,
            kit=self.kit,
        )

    async def complete(self) -> Batch[BatchViewV1Strict, MC, GT, QM, QRM, SW]:
        """Changes batch status to 'COMPLETED' to mark batch as finished.

        Note:
            batch in 'COMPLETED' status can't be changed to any other status.

        Returns:
            Updated batch with updated view containing 'COMPLETED' status.

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), kit=kit, lazy=True)
            completed_batch = await batch.complete()
            print(completed_batch.view.status)  # 'COMPLETED'
            ```
        """

        updated_view = await self.kit.annotation_studio.batch.complete(batch_id=self.batch_id)
        return Batch(
            batch_id=self.batch_id,
            view=updated_view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=self.status_workflow_config,
            kit=self.kit,
        )

    # endregion

    # region money config batch API

    async def update_batch_view_with_money_config(
        self: Batch[BatchViewV1Strict, None, GT, QM, QRM, SW],
        money_config: MoneyConfigViewStrict | MoneyConfigIdViewStrict,
    ) -> BatchViewV1Strict:
        """Updates batch view to reference the provided money config.

        Links the money config to the batch by adding its reference to batch extensions.

        Args:
            money_config: Money config to reference in batch extensions

        Returns:
            Updated batch view with money config extension added
        """

        update_form = with_money_config_extension_batch(
            BatchUpdateFormV1Strict.from_view(self.view),
            money_config_id=money_config.config_id,
        )
        return await self.kit.annotation_studio.batch.update(
            batch_id=self.view.id,
            form=update_form,
        )

    async def upsert_money_config(
        self, form: MoneyConfigFormStrict
    ) -> BatchWithMoneyConfig[BatchViewV1Strict, GT, QM, QRM, SW]:
        """Creates or updates batch money config extension.

        If money config is already configured for the batch, creates new version of existing config. If not configured,
        creates new config and adds it to batch extensions.

        Args:
            form: Money config parameters including pricing settings

        Returns:
            Updated batch with money config extension

        Examples:
            ```python
            config_form = MoneyConfigCreateVersionRequestStrict(...)
            batch_with_money_config = await batch.upsert_money_config(config_form)
            print(batch_with_money_config.money_config.config_id)
            ```
        """

        batch = await self.fetch_money_config()

        if has_batch_money_config(batch):
            money_config_response = await batch.kit.experts_portal.money_config.create_new_version(
                config_id=batch.money_config.config_id,
                form=form,
            )
            view = batch.view
        elif has_no_batch_money_config(batch):
            money_config_response = await batch.kit.experts_portal.money_config.create(form=form)
            view = await batch.update_batch_view_with_money_config(money_config=money_config_response)
        else:
            assert False, 'not reachable'
        money_config = await batch.kit.experts_portal.money_config.get_version(
            config_id=money_config_response.config_id,
            version_id=money_config_response.version_id,
        )
        return Batch(
            batch_id=batch.batch_id,
            view=view,
            money_config=money_config,
            ground_truth=batch.ground_truth,
            quality_management=batch.quality_management,
            quorum_config=batch.quorum_config,
            status_workflow_config=batch.status_workflow_config,
            kit=batch.kit,
        )

    async def upsert_annotation_money_config(
        self,
        **kwargs: Unpack[BaseAnnotationMoneyConfigFormParams],
    ) -> BatchWithMoneyConfig[BatchViewV1Strict, GT, QM, QRM, SW]:
        """Creates or updates money config for annotation-based batch pricing.

        If money config is already configured for the batch, creates new version of existing config. If not configured,
        creates new config and adds it to batch extensions.

        Args:
            price (float): Price per annotation in specified currency
            currency (Literal['BU', 'USD']): Currency code, either 'BU' (Base Units) or 'USD'
            tenant_id (NotRequired[str | None]): Optional tenant identifier
            skip_pending_balance (NotRequired[bool]): If True, payment will be processed without pending balance stage.

        Returns:
            Updated batch with annotation-based money config

        Examples:
            ```python
            batch = await batch.upsert_annotation_money_config(price=0.5, currency='USD', skip_pending_balance=True)
            print(batch.money_config.config_id)
            ```
        """

        batch_with_view = await self.fetch_view()
        money_config_form = build_annotation_money_config_form(
            **kwargs,
            requester_id=await self.kit.annotation_studio.get_account_id(),
            name=batch_with_view.view.private_name,
        )
        return await batch_with_view.upsert_money_config(money_config_form)

    async def upsert_status_workflow_money_config(
        self: BatchWithStatusWorkflow[BatchView, OptionalMC, GT, QM, QRM],
        **kwargs: Unpack[BaseBuildStatusWorkflowMoneyConfigFormParams],
    ) -> BatchWithMoneyConfig[BatchViewV1Strict, GT, QM, QRM, StatusWorkflowConfigViewStrict]:
        """Creates or updates money config for status workflow based batch pricing.

        If money config is already configured for the batch, creates new version of existing config. If not configured,
        creates new config and adds it to batch extensions. This method can be used only for batches with status
        workflow to configure payments for status transitions.

        Args:
            snippet_price (float): Price shown in tasks list
            currency (Literal['BU', 'USD']): Currency code, either 'BU' (Base Units) or 'USD'
            mutable_transitions (StatusTransitionMutablePayments): Mapping from status to payment settings when
                transitioning to that status. Specified amount will not be actually paid but will be added to an
                expected payment for the task when annotation
                is transitioned to that status.
            paid_transitions (StatusTransitionPayments): Mapping from status to payment settings when transitioning to
                that status. Specified amount will be actually paid to the annotator when annotation is transitioned to
                that status. Note that only the first transition to any of statuses specified in this parameter will be
                paid.
            tenant_id (NotRequired[str | None]): Optional tenant identifier
            skip_pending_balance (NotRequired[bool]): If True, payment will be processed without pending balance stage.
                Note that pending balance is different from the expected payment from mutable_transitions.

        Returns:
            Updated batch with status workflow based money config

        Examples:
            ```python
            batch = await batch.assert_status_workflow()
            mutable = {'in_progress': StatusTransitionMutablePayment(price=0.4)}
            paid = {
                'accepted': StatusTransitionPayment(price=0.4, portal_review_result='ACCEPTED'),
                'rejected': StatusTransitionPayment(price=0.0, portal_review_result='REJECTED'),
            }
            batch = await batch.upsert_status_workflow_money_config(
                snippet_price=0.4, currency='USD', mutable_transitions=mutable, paid_transitions=paid
            )
            print(batch.money_config.config_id)
            ```
        """

        batch_with_view = await self.fetch_view()
        money_config_form = build_status_workflow_money_config_form(
            **kwargs,
            requester_id=await self.kit.annotation_studio.get_account_id(),
            name=batch_with_view.view.private_name,
        )
        return await batch_with_view.upsert_money_config(money_config_form)

    # endregion

    # region ground truth batch API

    async def upsert_ground_truth(
        self,
        form: GroundTruthConfigForm,
    ) -> BatchWithGroundTruth[BatchViewV1Strict, MC, QM, QRM, SW]:
        """Creates or updates batch ground truth extension.

        If ground truth is already configured for the batch, updates existing configuration. If not configured,
        creates new configuration and adds it to batch extensions.

        Args:
            form: Ground truth configuration parameters including connection settings to ground truth storage

        Returns:
            Updated batch with ground truth configuration

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), kit=kit)
            config_form = GroundTruthConfigForm(...)
            batch_with_ground_truth = await batch.upsert_ground_truth(config_form)
            print(batch_with_ground_truth.ground_truth.id)
            ```
        """

        batch = await self.fetch_ground_truth()

        if batch.ground_truth is not None:
            ground_truth_config = await batch.kit.annotation_studio.ground_truth_config.update(
                id=batch.ground_truth.id,
                form=form,
            )
            view = batch.view
        else:
            ground_truth_config = await batch.kit.annotation_studio.ground_truth_config.create(
                form=form,
            )
            update_form = BatchUpdateFormV1Strict.from_view(batch.view)
            update_form = with_ground_truth_extension_batch(
                batch_form=update_form,
                ground_truth_config_id=str(ground_truth_config.id),
            )
            view = await batch.kit.annotation_studio.batch.update(
                batch_id=batch.view.id,
                form=update_form,
            )

        return Batch(
            batch_id=batch.batch_id,
            view=view,
            money_config=batch.money_config,
            ground_truth=ground_truth_config,
            quality_management=batch.quality_management,
            quorum_config=batch.quorum_config,
            status_workflow_config=batch.status_workflow_config,
            kit=batch.kit,
        )

    # endregion

    # region quality management batch API

    async def upsert_batch_quality_management(
        self,
        form: QualityConfigFormV0Strict,
    ) -> BatchWithQualityManagement[BatchViewV1Strict, MC, GT, QRM, SW]:
        """Creates or updates batch quality management extension.

        If quality management is already configured for the batch, updates existing configuration. If not configured,
        creates new configuration and adds it to batch extensions.

        Args:
            form: Quality management configuration parameters

        Returns:
            Updated batch with quality management configuration

        Examples:
            ```python
            batch = await Batch.get(batch_id=BatchId('batch-id'), kit=kit)
            config_form = QualityConfigFormV0Strict(...)
            batch_with_quality_management = await batch.upsert_batch_quality_management(config_form)
            print(batch_with_quality_management.quality_management.id)
            ```
        """

        batch = await self.fetch_quality_management()

        if batch.quality_management is not None:
            quality_config = await batch.kit.quality_management.quality_config.update(
                id=batch.quality_management.id,
                form=form,
            )
            view = batch.view
        else:
            quality_config = await batch.kit.quality_management.quality_config.create(
                form=form,
            )
            update_form = BatchUpdateFormV1Strict.from_view(batch.view)
            update_form = with_quality_config_extension_batch(
                batch_form=update_form,
                quality_config_id=str(quality_config.id),
            )
            view = await batch.kit.annotation_studio.batch.update(
                batch_id=batch.view.id,
                form=update_form,
            )

        return Batch(
            batch_id=batch.batch_id,
            view=view,
            money_config=batch.money_config,
            ground_truth=batch.ground_truth,
            quality_management=quality_config,
            quorum_config=batch.quorum_config,
            status_workflow_config=batch.status_workflow_config,
            kit=batch.kit,
        )

    async def create_restriction(
        self: BatchWithQualityManagement[BatchView, MC, GT, QRM, SW],
        account_id: str,
        scope_access_level: Literal['NO_ACCESS', 'ONLY_ASSIGNED'],
        expire_at: datetime.datetime | None = None,
        private_comment: str | None = None,
    ) -> RestrictionViewV0Strict:
        """Creates a restriction for specific account in this batch.

        Creates a new restriction that limits account's access to this batch. Note that batch must have quality
        management configured to create restrictions.

        Args:
            account_id: ID of the account to restrict
            scope_access_level: Level of restriction:
                * 'NO_ACCESS': Account cannot access batch at all
                * 'ONLY_ASSIGNED': Account can only access already assigned annotations in this batch
            expire_at: When restriction should expire (optional)
            private_comment: Comment explaining restriction (optional)

        Returns:
            Created restriction details

        Examples:
            ```python
            batch = await new_batch.assert_batch_quality_management()
            restriction = await batch.create_restriction(
                account_id='user-1', scope_access_level='NO_ACCESS', private_comment='Too many errors'
            )
            print(restriction.id)
            ```
        """

        return await self.kit.quality_management.restriction.create(
            RestrictionFormV0(
                account_id=account_id,
                scope='BATCH',
                scope_access_level=scope_access_level,
                expire_at=DATETIME_ADAPTER.dump_json(expire_at).decode() if expire_at else None,
                private_comment=private_comment,
                batch_id=self.batch_id,
            )
        )

    async def get_restrictions(
        self: BatchWithQualityManagement[BatchView, MC, GT, QRM, SW],
        query: GetRestrictionsForm,
    ) -> AsyncGenerator[RestrictionViewV0Strict, None]:
        """Returns an asynchronous generator of batch restrictions matching query parameters.

        Lists all restrictions created for this batch that match provided query parameters. Note that batch must have
        quality management configured to get restrictions. This methods returns only batch scoped restrictions: account
        may not have access to the batch due to project level restrictions.


        Args:
            query: Parameters to filter restrictions by

        Returns:
            AsyncGenerator yielding RestrictionViewV0Strict objects

        Examples:
            ```python
            batch = await batch.assert_batch_quality_management()
            query = BatchGetRestrictionsForm(account_id='user-1')
            async for restriction in batch.get_restrictions(query):
                print(f'Restriction {restriction.account_id}, expires at {restriction.expire_at}')
            ```
        """

        query_params = GetRestrictionListQueryParamsV0(
            **{key: value for key, value in dict(query).items() if key != 'batch_id'},
            batch_id=self.batch_id,
        )

        async for restriction in self.kit.quality_management.restriction.get_all(query_params=query_params):
            yield restriction

    # endregion

    # region type assertions

    async def assert_batch_money_config(
        self: Batch[BatchView, OptionalMC | LazyFromView[OptionalMC], GT, QM, QRM, SW],
        message: str | None = None,
    ) -> BatchWithMoneyConfig[BatchViewV1Strict, GT, QM, QRM, SW]:
        """Asserts that the batch has a money config extension configured in its local state.

        If the batch is lazy loaded, fetches the money config extension from the API.
        If the batch does not have money config configured, raises a ValueError with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If None, a default message is used.

        Returns:
            The same batch with a money config extension loaded from the API.

        Raises:
            ValueError: If money config is not configured in local representation of this batch.

        Examples:
            ```python
            batch = await batch.assert_batch_money_config()
            print(batch.money_config.config_id)  # Statically type checked
            ```
        """

        self_with_mc = await self.fetch_money_config()
        if has_batch_money_config(self_with_mc):
            return self_with_mc
        raise ValueError(message or 'Batch does not have money config')

    async def assert_batch_ground_truth(
        self: Batch[BatchView, MC, OptionalGT | LazyFromView[OptionalGT], QM, QRM, SW],
        message: str | None = None,
    ) -> BatchWithGroundTruth[BatchViewV1Strict, MC, QM, QRM, SW]:
        """Asserts that the batch has a ground truth extension configured in its local state.

        If the batch is lazy loaded, fetches the ground truth extension from the API. If the batch does not have ground
        truth configured, raises a ValueError with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If None, a default message is used.

        Returns:
            The same batch with a ground truth extension loaded from the API.

        Raises:
            ValueError: If ground truth is not configured in local representation of this batch.

        Examples:
            ```python
            batch = await batch.assert_batch_ground_truth()
            print(batch.ground_truth.id)  # Statically type checked
            ```
        """

        self_with_gt = await self.fetch_ground_truth()
        if has_batch_ground_truth(self_with_gt):
            return self_with_gt
        raise ValueError(message or 'Batch does not have ground truth config')

    async def assert_batch_quality_management(
        self: Batch[BatchView, MC, GT, OptionalQM | LazyFromView[OptionalQM], QRM, SW],
        message: str | None = None,
    ) -> BatchWithQualityManagement[BatchViewV1Strict, MC, GT, QRM, SW]:
        """Asserts that the batch has a quality management extension configured in its local state.

        If the batch is lazy loaded, fetches the quality management extension from the API. If the batch does not have
        quality management configured, raises a ValueError with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If None, a default message is used.

        Returns:
            The same batch with a quality management extension loaded from the API.

        Raises:
            ValueError: If quality management is not configured in local representation of this batch.

        Examples:
            ```python
            batch = await batch.assert_batch_quality_management()
            print(batch.quality_management.id)  # Statically type checked
            ```
        """

        self_with_qm = await self.fetch_quality_management()
        if has_batch_quality_management(self_with_qm):
            return self_with_qm
        raise ValueError(message or 'Batch does not have quality management config')

    async def assert_quorum(
        self: Batch[BatchView, MC, GT, QM, OptionalQRM | LazyFromView[OptionalQRM], SW],
        message: str | None = None,
    ) -> BatchWithQuorum[BatchView, MC, GT, QM, SW]:
        """Asserts that the batch has a quorum annotation process configured in its local state.

        If the batch is lazy loaded, fetches the quorum config from the API.
        If the batch does not have quorum configured, raises a ValueError with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If None, a default message is used.

        Returns:
            The same batch with a quorum config loaded from the API.

        Raises:
            ValueError: If quorum is not configured in local representation of this batch.

        Examples:
            ```python
            batch = await batch.assert_quorum()
            print(batch.quorum_config.data)  # Statically type checked
            ```
        """

        self_with_quorum = await self.fetch_quorum_config()
        if has_quorum(self_with_quorum):
            return self_with_quorum
        raise ValueError(message or 'Batch does not have quorum config')

    async def assert_status_workflow(
        self: Batch[BatchView, MC, GT, QM, QRM, OptionalSW | LazyFromView[OptionalSW]],
        message: str | None = None,
    ) -> BatchWithStatusWorkflow[BatchView, MC, GT, QM, QRM]:
        """Asserts that the batch has a status workflow annotation process configured in its local state.

        If the batch is lazy loaded, fetches the status workflow config from the API. If the batch does not have status
        workflow configured, raises a ValueError with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If None, a default message is used.

        Returns:
            The same batch with a status workflow config loaded from the API.

        Raises:
            ValueError: If status workflow is not configured in local representation of this batch.

        Examples:
            ```python
            batch = await batch.assert_status_workflow()
            print(batch.status_workflow_config)  # Statically type checked
            ```
        """

        self_with_sw = await self.fetch_status_workflow_config()

        if has_status_workflow(self_with_sw):
            return self_with_sw

        raise ValueError(message or 'Batch does not have status workflow')

    # endregion


def is_view_loaded(
    batch: Batch[BatchViewV1Strict | LazyFromId[BatchViewV1Strict], MC, GT, QM, QRM, SW],
) -> TypeGuard[Batch[BatchViewV1Strict, MC, GT, QM, QRM, SW]]:
    """Checks if batch view is loaded from the API.

    Type guard function that checks if batch view was loaded from the API or exists only as a lazy loader.
    Function is used to narrow batch type from potentially lazy to concrete loaded type.

    Returns:
        True if batch view is loaded, False if it exists as lazy loader

    Examples:
        ```python
        batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
        if is_view_loaded(batch):
            print(batch.view.status)  # Statically type checked
        ```
    """

    return not isinstance(batch.view, LazyValue)


def has_batch_money_config(
    batch: Batch[BatchView, OptionalMC, GT, QM, QRM, SW],
) -> TypeGuard[BatchWithMoneyConfig[BatchView, GT, QM, QRM, SW]]:
    """Checks if batch has money config extension configured.

    Type guard function that checks if batch has money config extension configured in its current local state.
    Function is used to narrow batch type to concrete BatchWithMoneyConfig type. Note that if batch has no money config
    configured project level money config may still be used.

    Returns:
        True if batch has money config configured, False if it doesn't

    Examples:
        ```python
        batch = await batch.fetch_money_config()
        if has_batch_money_config(batch):
            print(batch.money_config.config_id)  # Statically type checked
        ```
    """

    return batch.money_config is not None


def has_no_batch_money_config(
    batch: Batch[BatchView, OptionalMC, GT, QM, QRM, SW],
) -> TypeGuard[Batch[BatchView, None, GT, QM, QRM, SW]]:
    """Checks if batch has no money config extension configured. See has_batch_money_config for reference."""

    return batch.money_config is None


def is_money_config_loaded(
    batch: Batch[BatchView, OptionalMC | LazyFromView[OptionalMC], GT, QM, QRM, SW],
) -> TypeGuard[Batch[BatchView, OptionalMC, GT, QM, QRM, SW]]:
    """Checks if batch money config is loaded from the API.

    Type guard function that checks if batch money config was loaded from the API or exists only as a lazy loader.
    Function is used to narrow batch type from potentially lazy to concrete loaded type.

    Returns:
        True if money config is loaded, False if it exists as lazy loader

    Examples:
        ```python
        batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
        if is_money_config_loaded(batch) and has_batch_money_config(batch):
            print(batch.money_config.config_id)  # Statically type checked
        ```
    """

    return not isinstance(batch.money_config, LazyValue)


def has_batch_ground_truth(
    batch: Batch[BatchView, MC, OptionalGT, QM, QRM, SW],
) -> TypeGuard[BatchWithGroundTruth[BatchView, MC, QM, QRM, SW]]:
    """Checks if batch has ground truth extension configured.

    Type guard function that checks if batch has ground truth extension configured in its current local state.
    Function is used to narrow batch type to concrete BatchWithGroundTruth type.

    Returns:
        True if batch has ground truth configured, False if it doesn't

    Examples:
        ```python
        batch = await batch.fetch_ground_truth()
        if has_batch_ground_truth(batch):
            print(batch.ground_truth.id)  # Statically type checked
        ```
    """

    return batch.ground_truth is not None


def is_ground_truth_loaded(
    batch: Batch[BatchView, MC, OptionalGT | LazyFromView[OptionalGT], QM, QRM, SW],
) -> TypeGuard[Batch[BatchView, MC, OptionalGT, QM, QRM, SW]]:
    """Checks if batch ground truth config is loaded from the API.

    Type guard function that checks if batch ground truth config was loaded from the API or exists only as a lazy
    loader. Function is used to narrow batch type from potentially lazy to concrete loaded type.

    Returns:
        True if ground truth config is loaded, False if it exists as lazy loader

    Examples:
        ```python
        batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
        if is_ground_truth_loaded(batch) and has_batch_ground_truth(batch):
            print(batch.ground_truth.id)  # Statically type checked
        ```
    """

    return not isinstance(batch.ground_truth, LazyValue)


def has_batch_quality_management(
    batch: Batch[BatchView, MC, GT, OptionalQM, QRM, SW],
) -> TypeGuard[BatchWithQualityManagement[BatchView, MC, GT, QRM, SW]]:
    """Checks if batch has quality management extension configured.

    Type guard function that checks if batch has quality management extension configured in its current local state.
    Function is used to narrow batch type to concrete BatchWithQualityManagement type.

    Returns:
        True if batch has quality management configured, False if it doesn't

    Examples:
        ```python
        batch = await batch.fetch_quality_management()
        if has_batch_quality_management(batch):
            print(batch.quality_management.id)  # Statically type checked
        ```
    """

    return batch.quality_management is not None


def is_quality_management_loaded(
    batch: Batch[BatchView, MC, GT, OptionalQM | LazyFromView[OptionalQM], QRM, SW],
) -> TypeGuard[Batch[BatchView, MC, GT, OptionalQM, QRM, SW]]:
    """Checks if batch quality management config is loaded from the API.

    Type guard function that checks if batch quality management config was loaded from the API or exists only as a lazy
    loader. Function is used to narrow batch type from potentially lazy to concrete loaded type.

    Returns:
        True if quality management config is loaded, False if it exists as lazy loader

    Examples:
        ```python
        batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
        if is_quality_management_loaded(batch) and has_batch_quality_management(batch):
            print(batch.quality_management.id)  # Statically type checked
        ```
    """

    return not isinstance(batch.quality_management, LazyValue)


def has_quorum(
    batch: Batch[BatchView, MC, GT, QM, OptionalQRM, SW],
) -> TypeGuard[BatchWithQuorum[BatchView, MC, GT, QM, SW]]:
    """Checks if batch has quorum annotation process configured.

    Type guard function that checks if batch has quorum annotation process configured in its current local state.
    Function is used to narrow batch type to concrete BatchWithQuorum type.

    Returns:
        True if batch has quorum configured, False if it doesn't

    Examples:
        ```python
        batch = await batch.fetch_quorum_config()
        if has_quorum(batch):
            print(batch.quorum_config.data)  # Statically type checked
        ```
    """

    return batch.quorum_config is not None


def has_no_quorum(
    batch: Batch[BatchView, MC, GT, QM, OptionalQRM, SW],
) -> TypeGuard[Batch[BatchView, MC, GT, QM, None, SW]]:
    """Checks if batch has no quorum annotation process configured. See has_quorum for reference."""

    return batch.quorum_config is None


def is_quorum_loaded(
    batch: Batch[BatchView, MC, GT, QM, OptionalQRM | LazyFromView[OptionalQRM], SW],
) -> TypeGuard[Batch[BatchView, MC, GT, QM, OptionalQRM, SW]]:
    """Checks if batch quorum config is loaded from the API.

    Type guard function that checks if batch quorum config was loaded from the API or exists only as a lazy loader.
    Function is used to narrow batch type from potentially lazy to concrete loaded type.

    Returns:
        True if quorum config is loaded, False if it exists as lazy loader

    Examples:
        ```python
        batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
        if is_quorum_loaded(batch) and has_quorum(batch):
            print(batch.quorum_config.max_annotations)  # Statically type checked
        ```
    """

    return not isinstance(batch.quorum_config, LazyValue)


def has_status_workflow(
    batch: Batch[BatchView, MC, GT, QM, QRM, OptionalSW],
) -> TypeGuard[BatchWithStatusWorkflow[BatchView, MC, GT, QM, QRM]]:
    """Checks if batch has status workflow annotation process configured.

    Type guard function that checks if batch has status workflow annotation process configured in its current local
    state. Function is used to narrow batch type to concrete BatchWithStatusWorkflow type.

    Returns:
        True if batch has status workflow configured, False if it doesn't

    Examples:
        ```python
        batch = await batch.fetch_status_workflow_config()
        if has_status_workflow(batch):
            print(batch.status_workflow_config)  # Statically type checked
        ```
    """

    return batch.status_workflow_config is not None


def is_status_workflow_loaded(
    batch: Batch[BatchView, MC, GT, QM, QRM, OptionalSW | LazyFromView[OptionalSW]],
) -> TypeGuard[Batch[BatchView, MC, GT, QM, QRM, OptionalSW]]:
    """Checks if batch status workflow config is loaded from the API.

    Type guard function that checks if batch status workflow config was loaded from the API or exists only as a lazy
    loader. Function is used to narrow batch type from potentially lazy to concrete loaded type.

    Returns:
        True if status workflow config is loaded, False if it exists as lazy loader

    Examples:
        ```python
        batch = await Batch.get(batch_id=BatchId('batch-id'), lazy=True, kit=kit)
        if is_status_workflow_loaded(batch) and has_status_workflow(batch):
            print(batch.status_workflow_config)
        ```
    """

    return not isinstance(batch.status_workflow_config, LazyValue)
