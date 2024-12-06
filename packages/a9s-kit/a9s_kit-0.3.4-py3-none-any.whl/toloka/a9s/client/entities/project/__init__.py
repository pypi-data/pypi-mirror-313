from __future__ import annotations

import datetime
import logging
from functools import partial
from typing import Any, AsyncGenerator, Generic, Literal, Mapping, Sequence, TypeGuard, overload
from uuid import UUID

from typing_extensions import Unpack

from toloka.a9s.client.client import AsyncKit
from toloka.a9s.client.entities.base import EntityApiBase, EntityApiBaseParams, LazyValue
from toloka.a9s.client.entities.builder.batch import BatchBuilder, ExpertsType, InitialBatchBuilder
from toloka.a9s.client.entities.money_config import (
    BaseAnnotationMoneyConfigFormParams,
    BaseBuildStatusWorkflowMoneyConfigFormParams,
    build_annotation_money_config_form,
    build_status_workflow_money_config_form,
)
from toloka.a9s.client.entities.project.types import (
    GT,
    MC,
    QM,
    QRM,
    SW,
    LazyFromId,
    LazyFromView,
    OptionalGT,
    OptionalMC,
    OptionalQM,
    OptionalQRM,
    OptionalSW,
    ProjectAnyEager,
    ProjectAnyLazy,
    ProjectView,
    ProjectWithGroundTruth,
    ProjectWithMoneyConfig,
    ProjectWithQualityManagement,
)
from toloka.a9s.client.models.annotation_process.status_workflow import StatusWorkflowConfigViewStrict
from toloka.a9s.client.models.batch import (
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
    with_ground_truth_extension_project,
    with_money_config_extension_project,
    with_quality_config_extension_project,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.view import (
    QuorumConfigView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.restriction.web.v0.form import (
    GetRestrictionListQueryParamsV0,
    RestrictionFormV0,
)
from toloka.a9s.client.models.generated.ai.toloka.gts.config.web.v0.form import GroundTruthConfigForm
from toloka.a9s.client.models.ground_truth import GroundTruthConfigViewV0Strict
from toloka.a9s.client.models.money_config import (
    MoneyConfigIdViewStrict,
    MoneyConfigViewStrict,
)
from toloka.a9s.client.models.project import (
    ProjectFormV1Strict,
    ProjectViewV1Strict,
)
from toloka.a9s.client.models.quality_management.config import (
    QualityConfigFormV0Strict,
    QualityConfigViewV0Strict,
)
from toloka.a9s.client.models.quality_management.restriction import RestrictionViewV0Strict
from toloka.a9s.client.models.types import GroundTruthConfigId, MoneyConfigId, ProjectId, QualityConfigId
from toloka.a9s.client.models.utils import DATETIME_ADAPTER

logger = logging.getLogger(__name__)


class Project(EntityApiBase, Generic[ProjectView, MC, GT, QM, QRM, SW]):
    """An `Annotation` Studio project that can be configured with various extensions.

    A project represents a collection of batches that can be configured with different extensions (money config,
    ground truth, quality management). The class supports both eager and lazy loading of configurations. General rule
    for extensions is following: batch extension takes priority over project extension, so project extension is used
    if batch extension is not set.

    Generic type parameters:

    * `ProjectView`: Type of the project API representation
    * `MC`: Type of money config extension
    * `GT`: Type of ground truth extension
    * `QM`: Type of quality management extension

    Each type parameter represents extension configuration, possible values are:

    * `None`: Not configured
    * `T`: Configured and loaded from the API
    * `LazyFrom*[T | None]`: Not loaded from API, instead loader is stored (may not be configured)

    Attributes:
        project_id: Identifier for the existing project
        view: API representation of the project
        money_config: Payment settings that serve as defaults for batches
        ground_truth: Ground truth storage connection settings
        quality_management: Quality control and restrictions settings

    Examples:
        Load project with all configurations:
        ```python
        project = await Project.get(project_id=ProjectId('existing-project-id-here'), lazy=False, kit=kit)
        print(project.view.id)
        ```

        Load project with lazy loading of configurations:
        ```python
        # no actual API calls are made in .get method
        project = await Project.get(project_id=ProjectId('existing-project-id-here'), lazy=True, kit=kit)
        loaded_project = await project.fetch_view()
        print(loaded_project.view.name)
        ```
    """

    project_id: ProjectId
    view: ProjectView

    money_config: MC
    ground_truth: GT
    quality_management: QM

    quorum: QRM
    status_workflow: SW

    def __init__(
        self,
        project_id: ProjectId,
        view: ProjectView,
        money_config: MC,
        ground_truth: GT,
        quality_management: QM,
        quorum: QRM,
        status_workflow: SW,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> None:
        super().__init__(**kwargs)
        self.project_id = project_id
        self.view = view

        self.money_config = money_config
        self.ground_truth = ground_truth
        self.quality_management = quality_management

        self.quorum = quorum
        self.status_workflow = status_workflow

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
                f'Inconsistency detected: {extension_id} extension ID in project ({extension_instance_id}) '
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

    @staticmethod
    async def _fetch_view(project_id: ProjectId, kit: AsyncKit) -> ProjectViewV1Strict:
        return await kit.annotation_studio.project.get(project_id=project_id)

    @staticmethod
    async def _fetch_money_config(view: ProjectViewV1Strict, kit: AsyncKit) -> OptionalMC:
        money_config_id = find_extension_instance_id(view.extensions, MONEY_CONFIG_EXTENSION_ID)
        if money_config_id:
            return await kit.experts_portal.money_config.get_last_version(
                config_id=MoneyConfigId(UUID(money_config_id))
            )
        return None

    @staticmethod
    async def _fetch_ground_truth(view: ProjectViewV1Strict, kit: AsyncKit) -> OptionalGT:
        ground_truth_config_id = find_extension_instance_id(view.extensions, GROUND_TRUTH_EXTENSION_ID)
        if ground_truth_config_id:
            return await kit.annotation_studio.ground_truth_config.get(id=GroundTruthConfigId(ground_truth_config_id))
        return None

    @staticmethod
    async def _fetch_quality_management(view: ProjectViewV1Strict, kit: AsyncKit) -> OptionalQM:
        quality_config_id = find_extension_instance_id(view.extensions, QUALITY_CONFIG_EXTENSION_ID)
        if quality_config_id:
            return await kit.quality_management.quality_config.get(id=QualityConfigId(quality_config_id))
        return None

    @staticmethod
    async def _fetch_quorum_config(id: ProjectId, kit: AsyncKit) -> OptionalQRM:
        return await kit.annotation_studio.quorum.get_project_defaults(project_id=id)

    @staticmethod
    async def _fetch_status_workflow_config(id: ProjectId, kit: AsyncKit) -> OptionalSW:
        return await kit.annotation_studio.status_workflow.get_project_defaults(project_id=id)

    @overload
    @classmethod
    async def get(
        cls: type[Project],
        project_id: ProjectId,
        lazy: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> ProjectAnyLazy: ...

    @overload
    @classmethod
    async def get(
        cls: type[Project],
        project_id: ProjectId,
        lazy: Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> ProjectAnyEager: ...

    @classmethod
    async def get(
        cls: type[Project],
        project_id: ProjectId,
        lazy: bool = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> ProjectAnyLazy | ProjectAnyEager:
        """Gets a project by its ID and loads its representation and extensions configurations.

        Args:
            project_id: ID of the project to get
            lazy: If True, no API requests will be made immediately. Instead, configurations will be loaded lazily when
                requested. Laziness is stored in type, later you can ensure that value is loaded using .fetch_* methods.
            kit (AsyncKit): `AsyncKit` instance

        Returns:
            If lazy=True:
                Project with lazy configurations that will be loaded on first access
            If lazy=False:
                Project with all available configurations loaded from API

        Examples:
            Load project with all configurations:
            ```python
            project = await Project.get(project_id=ProjectId('project-id'), lazy=False, kit=kit)
            print(project.view.name)
            ```

            Load project with lazy loading:
            ```python
            project = await Project.get(project_id=ProjectId('project-id'), lazy=True, kit=kit)
            print(project.view.name)  # will raise an error during type checking
            loaded = await project.fetch_view()
            print(loaded.view.name)
            ```
        """
        kit = kwargs['kit']

        if lazy:
            return Project[
                LazyFromId[ProjectViewV1Strict],
                LazyFromView[OptionalMC],
                LazyFromView[OptionalGT],
                LazyFromView[OptionalQM],
                LazyFromId[OptionalQRM],
                LazyFromId[OptionalSW],
            ](
                project_id=project_id,
                view=LazyValue(partial(cls._fetch_view, kit=kit)),
                money_config=LazyValue(partial(cls._fetch_money_config, kit=kit)),
                ground_truth=LazyValue(partial(cls._fetch_ground_truth, kit=kit)),
                quality_management=LazyValue(partial(cls._fetch_quality_management, kit=kit)),
                quorum=LazyValue(partial(cls._fetch_quorum_config, kit=kit)),
                status_workflow=LazyValue(partial(cls._fetch_status_workflow_config, kit=kit)),
                **kwargs,
            )
        else:
            view = await cls._fetch_view(project_id, kit)
            return Project[
                ProjectViewV1Strict,
                OptionalMC,
                OptionalGT,
                OptionalQM,
                OptionalQRM,
                OptionalSW,
            ](
                project_id=project_id,
                view=view,
                money_config=await cls._fetch_money_config(view, kit),
                ground_truth=await cls._fetch_ground_truth(view, kit),
                quality_management=await cls._fetch_quality_management(view, kit),
                quorum=await cls._fetch_quorum_config(project_id, kit),
                status_workflow=await cls._fetch_status_workflow_config(project_id, kit),
                **kwargs,
            )

    def get_batch_builder(
        self,
        private_name: str,
        jira_issue: str,
        experts_type: ExpertsType,
        monday_subitem_id: str,
        hidden: bool = False,
        metadata: Mapping[str, Any] | None = None,
        tags: Sequence[str] | None = None,
        completion: Literal['AUTO', 'MANUAL'] = 'AUTO',
        existing_extensions: Mapping[ExtensionId, str] | None = None,
    ) -> InitialBatchBuilder:
        """Create a new BatchBuilder for this project.

        Args:
            private_name: The name of created batch, that only shown to the author
            hidden: Whether to show or hide the batch in the list of batches. Project managers can control this
                parameter through UI. Hidden batches can be fully managed through A9S API but appear disabled in the UI.
            metadata: An arbitrary dictionary with additional information about the batch.
            tags: Tags on the project or batch, used in quality management async config.
            completion: Batch completion type, either "AUTO" or "MANUAL". If "AUTO" is set batch will be automatically
                moved to "COMPLETED" status when all tasks are done. Note that completed batch can't be opened for
                labeling again.
            existing_extensions: A dictionary with extension IDs as keys and extension instance IDs as values.
        """
        return BatchBuilder.from_parameters(
            kit=self.kit,
            project_id=self.project_id,
            private_name=private_name,
            jira_issue=jira_issue,
            experts_type=experts_type,
            monday_subitem_id=monday_subitem_id,
            hidden=hidden,
            metadata=metadata,
            tags=tags,
            completion=completion,
            existing_extensions=existing_extensions,
        )

    @overload
    async def refresh(self, lazy: Literal[True]) -> ProjectAnyLazy: ...

    @overload
    async def refresh(self, lazy: Literal[False] = False) -> ProjectAnyEager: ...

    async def refresh(self, lazy: Literal[True] | Literal[False] = False) -> ProjectAnyEager | ProjectAnyLazy:
        """Refreshes the project by reloading it from the API.

        Args:
            lazy: If `True`, configurations will be loaded lazily when accessed. If `False`, all available
                configurations will be loaded immediately.

        Returns:
            (ProjectAnyLazy): If `lazy=True`, fresh project instance with lazy configurations
            (ProjectAnyEager): If `lazy=False`, fresh project instance with all configurations loaded

        Examples:
            ```python
            project = await project.refresh(lazy=False)
            print(project.view.name)  # fresh data from API
            ```
        """
        return await self.get(
            project_id=self.project_id,
            lazy=lazy,
            kit=self.kit,
        )

    async def fetch_view(self) -> Project[ProjectViewV1Strict, MC, GT, QM, QRM, SW]:
        """Fetches the project view from the API if it was loaded lazily.

        Loads the project view from the API if it wasn't loaded initially (`lazy=True` was used). Returns the same
        project instance if view was already loaded.

        Returns:
            `Project` with view loaded from API

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), lazy=True, kit=kit)
            loaded = await project.fetch_view()
            print(loaded.view.name)
            ```
        """

        if is_view_loaded(self):
            return self
        assert isinstance(self.view, LazyValue)
        return Project(
            project_id=self.project_id,
            view=await self.view(self.project_id),
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum=self.quorum,
            status_workflow=self.status_workflow,
            kit=self.kit,
        )

    async def fetch_money_config(self) -> Project[ProjectViewV1Strict, OptionalMC, GT, QM, QRM, SW]:
        """Fetches the money config from the API if it was loaded lazily.

        Loads the money config from the API if it wasn't loaded initially (`lazy=True` was used).
        Returns the same project instance if money config was already loaded.

        Returns:
            `Project` with money config loaded from API if it exists

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), lazy=True, kit=kit)
            loaded = await project.fetch_money_config()
            if has_money_config(loaded):  # money config may not exists at all
                print(loaded.money_config.config_id)
            ```
        """

        if is_money_config_loaded(self):
            return await self.fetch_view()
        assert isinstance(self.money_config, LazyValue)
        project_with_view = await self.fetch_view()
        return Project(
            project_id=project_with_view.project_id,
            view=project_with_view.view,
            money_config=await self.money_config(project_with_view.view),
            ground_truth=project_with_view.ground_truth,
            quality_management=project_with_view.quality_management,
            quorum=project_with_view.quorum,
            status_workflow=project_with_view.status_workflow,
            kit=project_with_view.kit,
        )

    async def fetch_ground_truth(self) -> Project[ProjectViewV1Strict, MC, OptionalGT, QM, QRM, SW]:
        """Fetches the ground truth config from the API if it was loaded lazily.

        Loads the ground truth config from the API if it wasn't loaded initially (`lazy=True` was used).
        Returns the same project instance if ground truth config was already loaded.

        Returns:
            `Project` with ground truth config loaded from API if it exists

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), lazy=True, kit=kit)
            loaded = await project.fetch_ground_truth()
            if has_ground_truth(loaded):  # ground truth config may not exist at all
                print(loaded.ground_truth.id)
            ```
        """

        if is_ground_truth_loaded(self):
            return await self.fetch_view()
        assert isinstance(self.ground_truth, LazyValue)
        project_with_view = await self.fetch_view()
        return Project(
            project_id=project_with_view.project_id,
            view=project_with_view.view,
            money_config=project_with_view.money_config,
            ground_truth=await self.ground_truth(project_with_view.view),
            quality_management=project_with_view.quality_management,
            quorum=project_with_view.quorum,
            status_workflow=project_with_view.status_workflow,
            kit=project_with_view.kit,
        )

    async def fetch_quality_management(self) -> Project[ProjectViewV1Strict, MC, GT, OptionalQM, QRM, SW]:
        """Fetches the quality management config from the API if it was loaded lazily.

        Loads the quality management config from the API if it wasn't loaded initially (`lazy=True` was used).
        Returns the same project instance if quality management config was already loaded.

        Returns:
            `Project` with quality management config loaded from API if it exists

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), lazy=True, kit=kit)
            loaded = await project.fetch_quality_management()
            if has_quality_management(loaded):  # quality management config may not exist at all
                print(loaded.quality_management.id)
            ```
        """

        if is_quality_management_loaded(self):
            return await self.fetch_view()
        assert isinstance(self.quality_management, LazyValue)
        project_with_view = await self.fetch_view()
        return Project(
            project_id=project_with_view.project_id,
            view=project_with_view.view,
            money_config=project_with_view.money_config,
            ground_truth=project_with_view.ground_truth,
            quality_management=await self.quality_management(project_with_view.view),
            quorum=project_with_view.quorum,
            status_workflow=project_with_view.status_workflow,
            kit=project_with_view.kit,
        )

    async def fetch_quorum(self) -> Project[ProjectView, MC, GT, QM, OptionalQRM, SW]:
        """Fetches quorum config if loaded lazily.

        Loads quorum annotation process configuration from the API if it was not loaded yet. If quorum config
        is already loaded (either configured or not configured), returns `self`. Otherwise, loads quorum config
        from the API and returns new project instance with loaded config.

        Returns:
            `Project` instance with loaded quorum config (may be `None` if not configured)

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), lazy=True, kit=kit)
            loaded_project = await project.fetch_quorum()
            if has_quorum(loaded_project):
                print(loaded_project.quorum.config_id)  # Statically type checked
            ```
        """
        if is_quorum_loaded(self):
            return self
        assert isinstance(self.quorum, LazyValue)
        return Project(
            project_id=self.project_id,
            view=self.view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum=await self.quorum(self.project_id),
            status_workflow=self.status_workflow,
            kit=self.kit,
        )

    async def fetch_status_workflow(self) -> Project[ProjectView, MC, GT, QM, QRM, OptionalSW]:
        """Fetches status workflow config if loaded lazily.

        Loads status workflow annotation process configuration from the API if it was not loaded yet. If status workflow
        config is already loaded (either configured or not configured), returns `self`. Otherwise, loads status workflow
        config from the API and returns new project instance with loaded config.

        Returns:
            `Project` instance with loaded status workflow config (may be `None` if not configured)

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), lazy=True, kit=kit)
            loaded_project = await project.fetch_status_workflow()
            if has_status_workflow(loaded_project):
                print(loaded_project.status_workflow.config_id)  # Statically type checked
            ```
        """
        if is_status_workflow_loaded(self):
            return self
        assert isinstance(self.status_workflow, LazyValue)
        return Project(
            project_id=self.project_id,
            view=self.view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum=self.quorum,
            status_workflow=await self.status_workflow(self.project_id),
            kit=self.kit,
        )

    async def update(
        self: Project[ProjectView, MC, GT, QM, QRM, SW],
        form: ProjectFormV1Strict,
    ) -> Project[ProjectViewV1Strict, MC, GT, QM, QRM, SW]:
        """Updates project view from the form.

        Current extensions configurations remain unchanged. Updated view must be consistent with current extensions.

        Args:
            form: `Project` update parameters

        Returns:
            Updated `Project` with updated view and same extensions configurations

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), kit=kit)
            form = ProjectFormV1Strict.from_view(project.view)
            form.private_name = 'New name'
            updated_project = await project.update(form)
            print(updated_project.view.private_name)  # 'New name'
            ```
        """

        updated_view = await self.kit.annotation_studio.project.update(
            project_id=self.project_id,
            form=form,
        )
        return Project(
            project_id=self.project_id,
            view=updated_view,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum=self.quorum,
            status_workflow=self.status_workflow,
            kit=self.kit,
        )

    # region money config project API
    async def update_project_view_with_money_config(
        self: Project[ProjectViewV1Strict, None, GT, QM],
        money_config: MoneyConfigViewStrict | MoneyConfigIdViewStrict,
    ) -> ProjectViewV1Strict:
        """Updates project view to reference the provided money config.

        Links the money config to the project by adding its reference to project extensions.
        Should be called only for projects without money config - if project already has money config
        configured, use `upsert_money_config` instead.

        Args:
            money_config: `MoneyConfigViewStrict` or `MoneyConfigIdViewStrict` to reference in project extensions

        Returns:
            Updated project view with money config extension added

        Examples:

            ```python
            project = await project.fetch_money_config()
            if has_no_money_config(project):
                new_config = await kit.experts_portal.money_config.create(form)
                updated_view = await project.update_project_view_with_money_config(new_config)
            ```
        """

        update_form = with_money_config_extension_project(
            ProjectFormV1Strict.from_view(self.view),
            money_config_id=money_config.config_id,
        )
        return await self.kit.annotation_studio.project.update(
            project_id=self.view.id,
            form=update_form,
        )

    async def upsert_annotation_money_config(
        self,
        **kwargs: Unpack[BaseAnnotationMoneyConfigFormParams],
    ) -> ProjectWithMoneyConfig[ProjectViewV1Strict, GT, QM, QRM, SW]:
        """Creates or updates money config for annotation-based project pricing.

        If money config is already configured for the project, creates new version of existing config.
        If not configured, creates new config and adds it to project extensions.

        Args:
            price (float): Price per annotation in specified currency
            currency (Literal['BU', 'USD']): Currency code, either `BU` (Base Units) or `USD`
            tenant_id (NotRequired[str | None]): Optional tenant identifier
            skip_pending_balance (NotRequired[bool]): If `True`, payment will be processed without pending balance
                stage.

        Returns:
            Updated project with annotation-based money config

        Examples:

            ```python
            project = await project.upsert_annotation_money_config(
                price=0.5,
                currency='USD',
                skip_pending_balance=True,
            )
            print(project.money_config.config_id)
            ```
        """
        project_with_view = await self.fetch_view()
        money_config_form = build_annotation_money_config_form(
            **kwargs,
            requester_id=await self.kit.annotation_studio.get_account_id(),
            name=project_with_view.view.name,
        )

        project = await self.fetch_money_config()
        if has_money_config(project):
            money_config_response = await project.kit.experts_portal.money_config.create_new_version(
                config_id=project.money_config.config_id,
                form=money_config_form,
            )
            view = project.view
        elif has_no_money_config(project):
            money_config_response = await project.kit.experts_portal.money_config.create(form=money_config_form)
            view = await project.update_project_view_with_money_config(money_config=money_config_response)
        else:
            assert False, 'not reachable'

        money_config = await project.kit.experts_portal.money_config.get_version(
            config_id=money_config_response.config_id,
            version_id=money_config_response.version_id,
        )
        return Project(
            project_id=project.project_id,
            view=view,
            money_config=money_config,
            ground_truth=project.ground_truth,
            quality_management=project.quality_management,
            quorum=project.quorum,
            status_workflow=project.status_workflow,
            kit=project.kit,
        )

    async def upsert_status_workflow_money_config(
        self: Project[ProjectView, OptionalMC, GT, QM, QRM, StatusWorkflowConfigViewStrict],
        **kwargs: Unpack[BaseBuildStatusWorkflowMoneyConfigFormParams],
    ) -> ProjectWithMoneyConfig[ProjectViewV1Strict, GT, QM, QRM, StatusWorkflowConfigViewStrict]:
        """Creates or updates money config for status workflow based project pricing.

        If money config is already configured for the project, creates new version of existing config. If not
        configured, creates new config and adds it to project extensions. This method can be used only for
        projects with status workflow to configure payments for status transitions.

        Args:
            snippet_price (float): Price shown in tasks list
            currency (Literal['BU', 'USD']): Currency code, either BU (Base Units) or USD
            mutable_transitions (StatusTransitionMutablePayments): Mapping from status to payment settings when
                transitioning to that status. Specified amount will not be actually paid but will be added to an
                expected payment for the task when annotation is transitioned to that status.
            paid_transitions (StatusTransitionPayments): Mapping from status to payment settings when transitioning
                to that status. Specified amount will be actually paid to the annotator when annotation is
                transitioned to that status. Note that only the first transition to any of statuses specified in
                this parameter will be paid.
            tenant_id (NotRequired[str | None]): Optional tenant identifier
            skip_pending_balance (NotRequired[bool]): If `True`, payment will be processed without pending balance
                stage. Note that pending balance is different from the expected payment from `mutable_transitions`.

        Returns:
            Updated project with status workflow based money config

        Examples:

            ```python
            project = await project.assert_status_workflow()
            mutable = {'in_progress': StatusTransitionMutablePayment(price=0.4)}
            paid = {
                'accepted': StatusTransitionPayment(price=0.4, portal_review_result='ACCEPTED'),
                'rejected': StatusTransitionPayment(price=0.0, portal_review_result='REJECTED'),
            }
            project = await project.upsert_status_workflow_money_config(
                snippet_price=0.4, currency='USD', mutable_transitions=mutable, paid_transitions=paid
            )
            print(project.money_config.config_id)
            ```
        """
        project_with_view = await self.fetch_view()
        money_config_form = build_status_workflow_money_config_form(
            **kwargs,
            requester_id=await self.kit.annotation_studio.get_account_id(),
            name=project_with_view.view.name,
        )

        project = await self.fetch_money_config()
        if has_money_config(project):
            money_config_response = await project.kit.experts_portal.money_config.create_new_version(
                config_id=project.money_config.config_id,
                form=money_config_form,
            )
            view = project.view
        elif has_no_money_config(project):
            money_config_response = await project.kit.experts_portal.money_config.create(form=money_config_form)
            view = await project.update_project_view_with_money_config(money_config=money_config_response)
        else:
            assert False, 'not reachable'

        money_config = await project.kit.experts_portal.money_config.get_version(
            config_id=money_config_response.config_id,
            version_id=money_config_response.version_id,
        )
        return Project(
            project_id=project.project_id,
            view=view,
            money_config=money_config,
            ground_truth=project.ground_truth,
            quality_management=project.quality_management,
            quorum=project.quorum,
            status_workflow=project.status_workflow,
            kit=project.kit,
        )

    # endregion

    # region ground truth project API
    async def upsert_ground_truth(
        self,
        form: GroundTruthConfigForm,
    ) -> ProjectWithGroundTruth[ProjectViewV1Strict, MC, QM, QRM, SW]:
        """Creates or updates project ground truth extension.

        If ground truth is already configured for the project, updates existing configuration. If not configured,
        creates new configuration and adds it to project extensions.

        Args:
            form: `GroundTruthConfigForm` configuration parameters including connection settings to ground truth storage

        Returns:
            Updated `Project` with ground truth configuration

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), kit=kit)
            config_form = GroundTruthConfigForm(...)
            project_with_ground_truth = await project.upsert_ground_truth(config_form)
            print(project_with_ground_truth.ground_truth.id)
            ```
        """

        project = await self.fetch_ground_truth()

        if project.ground_truth is not None:
            ground_truth_config = await project.kit.annotation_studio.ground_truth_config.update(
                id=project.ground_truth.id,
                form=form,
            )
            view = project.view
        else:
            ground_truth_config = await project.kit.annotation_studio.ground_truth_config.create(
                form=form,
            )
            update_form = ProjectFormV1Strict.from_view(project.view)
            update_form = with_ground_truth_extension_project(
                project_form=update_form,
                ground_truth_config_id=str(ground_truth_config.id),
            )
            view = await project.kit.annotation_studio.project.update(
                project_id=project.view.id,
                form=update_form,
            )

        return Project(
            project_id=project.project_id,
            view=view,
            money_config=project.money_config,
            ground_truth=ground_truth_config,
            quality_management=project.quality_management,
            quorum=project.quorum,
            status_workflow=project.status_workflow,
            kit=project.kit,
        )

    # endregion

    # region quality management project API

    async def upsert_quality_management(
        self,
        form: QualityConfigFormV0Strict,
    ) -> ProjectWithQualityManagement[ProjectViewV1Strict, MC, GT, QRM, SW]:
        """Creates or updates project quality management extension.

        If quality management is already configured for the project, updates existing configuration. If not configured,
        creates new configuration and adds it to project extensions.

        Args:
            form: `QualityConfigFormV0Strict` configuration parameters

        Returns:
            Updated `Project` with quality management configuration

        Examples:

            ```python
            project = await Project.get(project_id=ProjectId('project-id'), kit=kit)
            config_form = QualityConfigFormV0Strict(...)
            project_with_quality_management = await project.upsert_quality_management(config_form)
            print(project_with_quality_management.quality_management.id)
            ```
        """

        project = await self.fetch_quality_management()

        if project.quality_management is not None:
            quality_config = await project.kit.quality_management.quality_config.update(
                id=project.quality_management.id,
                form=form,
            )
            view = project.view
        else:
            quality_config = await project.kit.quality_management.quality_config.create(
                form=form,
            )
            update_form = ProjectFormV1Strict.from_view(project.view)
            update_form = with_quality_config_extension_project(
                project_form=update_form,
                quality_config_id=str(quality_config.id),
            )
            view = await project.kit.annotation_studio.project.update(
                project_id=project.view.id,
                form=update_form,
            )

        return Project(
            project_id=project.project_id,
            view=view,
            money_config=project.money_config,
            ground_truth=project.ground_truth,
            quality_management=quality_config,
            quorum=project.quorum,
            status_workflow=project.status_workflow,
            kit=project.kit,
        )

    async def create_restriction(
        self: ProjectWithQualityManagement[ProjectView, MC, GT],
        account_id: str,
        scope_access_level: Literal['NO_ACCESS', 'ONLY_ASSIGNED'],
        expire_at: datetime.datetime | None = None,
        private_comment: str | None = None,
    ) -> RestrictionViewV0Strict:
        """Creates a restriction for specific account in this project.

        Creates a new restriction that limits account's access to this project. Note that project must have quality
        management configured to create restrictions.

        Args:
            account_id: ID of the account to restrict
            scope_access_level: Level of restriction:
                * `'NO_ACCESS'`: Account cannot access project at all
                * `'ONLY_ASSIGNED'`: Account can only access already assigned annotations in this project
            expire_at: When restriction should expire (optional)
            private_comment: Comment explaining restriction (optional)

        Returns:
            Created restriction details

        Examples:

            ```python
            project = await project.assert_project_quality_management()
            restriction = await project.create_restriction(
                account_id='user-1', scope_access_level='NO_ACCESS', private_comment='Too many errors'
            )
            print(restriction.id)
            ```
        """

        return await self.kit.quality_management.restriction.create(
            RestrictionFormV0(
                account_id=account_id,
                scope='PROJECT',
                scope_access_level=scope_access_level,
                expire_at=DATETIME_ADAPTER.dump_json(expire_at).decode() if expire_at else None,
                private_comment=private_comment,
                project_id=self.project_id,
            )
        )

    async def get_restrictions(
        self: ProjectWithQualityManagement[ProjectView, MC, GT],
        query: GetRestrictionsForm,
    ) -> AsyncGenerator[RestrictionViewV0Strict, None]:
        """Returns an asynchronous generator of project restrictions matching query parameters.

        Lists all restrictions created for this project that match provided query parameters. Note that project must
        have quality management configured to get restrictions. Only returns project scoped restrictions: account may be
        restricted from accessing specific batches in this project due to batch level restrictions.

        Args:
            query: Parameters to filter restrictions by

        Returns:
            AsyncGenerator yielding `RestrictionViewV0Strict` objects

        Examples:

            ```python
            project = await project.assert_project_quality_management()
            query = BatchGetRestrictionsForm(account_id='user-1')
            async for restriction in project.get_restrictions(query):
                print(f'Restriction {restriction.account_id}, expires at {restriction.expire_at}')
            ```
        """

        query_params = GetRestrictionListQueryParamsV0(
            **{key: value for key, value in dict(query).items() if key != 'project_id'},
            project_id=self.project_id,
        )

        async for restriction in self.kit.quality_management.restriction.get_all(query_params=query_params):
            yield restriction

    # endregion

    # region type assertions
    async def assert_project_money_config(
        self: Project[ProjectView, OptionalMC | LazyFromView[OptionalMC], GT, QM, QRM, SW],
        message: str | None = None,
    ) -> ProjectWithMoneyConfig[ProjectViewV1Strict, GT, QM, QRM, SW]:
        """Asserts that the project has a money config extension configured in its local state.

        If the project is lazy loaded, fetches the money config extension from the API. If the project does not have
        money config configured, raises a `ValueError` with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If `None`, a default message is used.

        Returns:
            The same project with a money config extension loaded from the API.

        Raises:
            `ValueError`: If money config is not configured in local representation of this project.

        Examples:
            ```python
            project = await project.assert_project_money_config()
            print(project.money_config.config_id)  # Statically type checked
            ```
        """

        self_with_mc = await self.fetch_money_config()
        if has_money_config(self_with_mc):
            return self_with_mc
        raise ValueError(message or 'Project does not have money config')

    async def assert_project_ground_truth(
        self: Project[ProjectView, MC, OptionalGT | LazyFromView[OptionalGT], QM, QRM, SW],
        message: str | None = None,
    ) -> ProjectWithGroundTruth[ProjectViewV1Strict, MC, QM, QRM, SW]:
        """Asserts that the project has a ground truth extension configured in its local state.

        If the project is lazy loaded, fetches the ground truth extension from the API. If the project does not have
        ground truth configured, raises a `ValueError` with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If `None`, a default message is used.

        Returns:
            The same project with a ground truth extension loaded from the API.

        Raises:
            `ValueError`: If ground truth is not configured in local representation of this project.

        Examples:
            ```python
            project = await project.assert_project_ground_truth()
            print(project.ground_truth.id)  # Statically type checked
            ```
        """

        self_with_gt = await self.fetch_ground_truth()
        if has_ground_truth(self_with_gt):
            return self_with_gt
        raise ValueError(message or 'Project does not have ground truth config')

    async def assert_project_quality_management(
        self: Project[ProjectView, MC, GT, OptionalQM | LazyFromView[OptionalQM], QRM, SW],
        message: str | None = None,
    ) -> ProjectWithQualityManagement[ProjectViewV1Strict, MC, GT, QRM, SW]:
        """Asserts that the project has a quality management extension configured in its local state.

        If the project is lazy loaded, fetches the quality management extension from the API. If the project does not
        have quality management configured, raises a `ValueError` with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If `None`, a default message is used.

        Returns:
            The same project with a quality management extension loaded from the API.

        Raises:
            `ValueError`: If quality management is not configured in local representation of this project.

        Examples:
            ```python
            project = await project.assert_project_quality_management()
            print(project.quality_management.id)  # Statically type checked
            ```
        """

        self_with_qm = await self.fetch_quality_management()
        if has_quality_management(self_with_qm):
            return self_with_qm
        raise ValueError(message or 'Project does not have quality management config')

    async def assert_project_quorum(
        self: Project[ProjectView, MC, GT, QM, OptionalQRM | LazyFromId[OptionalQRM], SW],
        message: str | None = None,
    ) -> Project[ProjectView, MC, GT, QM, QuorumConfigView, SW]:
        """Asserts that the project has a quorum annotation process configured in its local state.

        If the project is lazy loaded, fetches the quorum config from the API. If the project does not
        have quorum configured, raises a `ValueError` with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If `None`, a default message is used.

        Returns:
            The same project with quorum config loaded from the API.

        Raises:
            `ValueError`: If quorum is not configured in local representation of this project.

        Examples:
            ```python
            project = await project.assert_project_quorum()
            print(project.quorum.config_id)  # Statically type checked
            ```
        """

        self_with_quorum = await self.fetch_quorum()
        if has_quorum(self_with_quorum):
            return self_with_quorum
        raise ValueError(message or 'Project does not have quorum config')

    async def assert_project_status_workflow(
        self: Project[ProjectView, MC, GT, QM, QRM, OptionalSW | LazyFromId[OptionalSW]],
        message: str | None = None,
    ) -> Project[ProjectView, MC, GT, QM, QRM, StatusWorkflowConfigViewStrict]:
        """Asserts that the project has a status workflow annotation process configured in its local state.

        If the project is lazy loaded, fetches the status workflow config from the API. If the project does not
        have status workflow configured, raises a `ValueError` with a custom message or a default one.

        Args:
            message: Custom error message to use when assertion fails. If `None`, a default message is used.

        Returns:
            The same project with status workflow config loaded from the API.

        Raises:
            `ValueError`: If status workflow is not configured in local representation of this project.

        Examples:

            ```python
            project = await project.assert_project_status_workflow()
            print(project.status_workflow.config_id)  # Statically type checked
            ```
        """

        self_with_status_workflow = await self.fetch_status_workflow()
        if has_status_workflow(self_with_status_workflow):
            return self_with_status_workflow
        raise ValueError(message or 'Project does not have status workflow config')

    # endregion


def is_view_loaded(
    project: Project[ProjectViewV1Strict | LazyFromId[ProjectViewV1Strict], MC, GT, QM, QRM, SW],
) -> TypeGuard[Project[ProjectViewV1Strict, MC, GT, QM, QRM, SW]]:
    """Checks if project view is loaded from the API.

    Type guard function that checks if project view was loaded from the API or exists only as a lazy loader.
    Function is used to narrow project type from potentially lazy to concrete loaded type.

    Returns:
        `True` if project view is loaded, `False` if it exists as lazy loader

    Examples:

        ```python
        project = await `Project`.get(project_id=`ProjectId`('project-id'), lazy=`True`, kit=kit)
        if is_view_loaded(project):
            print(project.view.name)  # Statically type checked
        ```
    """

    return not isinstance(project.view, LazyValue)


def has_money_config(
    project: Project[ProjectView, OptionalMC, GT, QM, QRM, SW],
) -> TypeGuard[ProjectWithMoneyConfig[ProjectView, GT, QM, QRM, SW]]:
    """Checks if project has money config extension configured.

    Type guard function that checks if project has money config extension configured in its current local state.
    Function is used to narrow project type to concrete `ProjectWithMoneyConfig` type.

    Returns:
        `True` if project has money config configured, `False` if it doesn't

    Examples:

        ```python
        project = await project.fetch_money_config()
        if has_money_config(project):
            print(project.money_config.config_id)  # Statically type checked
        ```
    """

    return project.money_config is not None


def has_no_money_config(
    project: Project[ProjectView, OptionalMC, GT, QM, QRM, SW],
) -> TypeGuard[Project[ProjectView, None, GT, QM, QRM, SW]]:
    """Checks if project has no money config extension configured. See `has_money_config` for reference."""

    return project.money_config is None


def is_money_config_loaded(
    project: Project[ProjectView, OptionalMC | LazyFromView[OptionalMC], GT, QM, QRM, SW],
) -> TypeGuard[Project[ProjectView, OptionalMC, GT, QM, QRM, SW]]:
    """Checks if project money config is loaded from the API.

    Type guard function that checks if project money config was loaded from the API or exists only as a lazy loader.
    Function is used to narrow project type from potentially lazy to concrete loaded type.

    Returns:
        `True` if money config is loaded, `False` if it exists as lazy loader

    Examples:

        ```python
        project = await `Project`.get(project_id=`ProjectId`('project-id'), lazy=`True`, kit=kit)
        if is_money_config_loaded(project) and has_money_config(project):
            print(project.money_config.config_id)  # Statically type checked
        ```
    """

    return not isinstance(project.money_config, LazyValue)


def has_ground_truth(
    project: Project[ProjectView, MC, OptionalGT, QM, QRM, SW],
) -> TypeGuard[ProjectWithGroundTruth[ProjectView, MC, QM, QRM, SW]]:
    """Checks if project has ground truth extension configured.

    Type guard function that checks if project has ground truth extension configured in its current local state.
    Function is used to narrow project type to concrete `ProjectWithGroundTruth` type.

    Returns:
        `True` if project has ground truth configured, `False` if it doesn't

    Examples:

        ```python
        project = await project.fetch_ground_truth()
        if has_ground_truth(project):
            print(project.ground_truth.id)  # Statically type checked
        ```
    """

    return project.ground_truth is not None


def is_ground_truth_loaded(
    project: Project[ProjectView, MC, OptionalGT | LazyFromView[OptionalGT], QM, QRM, SW],
) -> TypeGuard[Project[ProjectView, MC, OptionalGT, QM, QRM, SW]]:
    """Checks if project ground truth config is loaded from the API.

    Type guard function that checks if project ground truth config was loaded from the API or exists only as a lazy
    loader. Function is used to narrow project type from potentially lazy to concrete loaded type.

    Returns:
        `True` if ground truth config is loaded, `False` if it exists as lazy loader

    Examples:

        ```python
        project = await `Project`.get(project_id=`ProjectId`('project-id'), lazy=`True`, kit=kit)
        if is_ground_truth_loaded(project) and has_ground_truth(project):
            print(project.ground_truth.id)  # Statically type checked
        ```
    """
    return not isinstance(project.ground_truth, LazyValue)


def has_quality_management(
    project: Project[ProjectView, MC, GT, OptionalQM, QRM, SW],
) -> TypeGuard[ProjectWithQualityManagement[ProjectView, MC, GT, QRM, SW]]:
    """Checks if project has quality management extension configured.

    Type guard function that checks if project has quality management extension configured in its current local state.
    Function is used to narrow project type to concrete `ProjectWithQualityManagement` type.

    Returns:
        `True` if project has quality management configured, `False` if it doesn't

    Examples:

        ```python
        project = await project.fetch_quality_management()
        if has_quality_management(project):
            print(project.quality_management.id)  # Statically type checked
        ```
    """

    return project.quality_management is not None


def is_quality_management_loaded(
    project: Project[ProjectView, MC, GT, OptionalQM | LazyFromView[OptionalQM], QRM, SW],
) -> TypeGuard[Project[ProjectView, MC, GT, OptionalQM, QRM, SW]]:
    """Checks if project quality management config is loaded from the API.

    Type guard function that checks if project quality management config was loaded from the API or exists only as a
    lazy loader. Function is used to narrow project type from potentially lazy to concrete loaded type.

    Returns:
        `True` if quality management config is loaded, `False` if it exists as lazy loader

    Examples:

        ```python
        project = await `Project`.get(project_id=`ProjectId`('project-id'), lazy=`True`, kit=kit)
        if is_quality_management_loaded(project) and has_quality_management(project):
            print(project.quality_management.id)  # Statically type checked
        ```
    """

    return not isinstance(project.quality_management, LazyValue)


def has_quorum(
    project: Project[ProjectView, MC, GT, QM, OptionalQRM, SW],
) -> TypeGuard[Project[ProjectView, MC, GT, QM, QuorumConfigView, SW]]:
    """Checks if project has quorum annotation process configured.

    Type guard function that checks if project has quorum annotation process configured in its current local state.
    Function is used to narrow project type to concrete `Project` type with `QuorumConfigView`.

    Returns:
        `True` if project has quorum configured, `False` if it doesn't

    Examples:

        ```python
        project = await project.fetch_quorum()
        if has_quorum(project):
            print(project.quorum.config_id)  # Statically type checked
        ```
    """
    return project.quorum is not None


def is_quorum_loaded(
    project: Project[ProjectView, MC, GT, QM, OptionalQRM | LazyFromId[OptionalQRM], SW],
) -> TypeGuard[Project[ProjectView, MC, GT, QM, OptionalQRM, SW]]:
    """Checks if project quorum config is loaded from the API.

    Type guard function that checks if project quorum config was loaded from the API or exists only as a lazy
    loader. Function is used to narrow project type from potentially lazy to concrete loaded type.

    Returns:
        `True` if quorum config is loaded, `False` if it exists as lazy loader

    Examples:

        ```python
        project = await `Project`.get(project_id=`ProjectId`('project-id'), lazy=`True`, kit=kit)
        if is_quorum_loaded(project) and has_quorum(project):
            print(project.quorum.config_id)  # Statically type checked
        ```
    """
    return not isinstance(project.quorum, LazyValue)


def has_status_workflow(
    project: Project[ProjectView, MC, GT, QM, QRM, OptionalSW],
) -> TypeGuard[Project[ProjectView, MC, GT, QM, QRM, StatusWorkflowConfigViewStrict]]:
    """Checks if project has status workflow annotation process configured.

    Type guard function that checks if project has status workflow annotation process configured in its current
    local state. Function is used to narrow project type to concrete `Project` type with
    `StatusWorkflowConfigViewStrict`.

    Returns:
        `True` if project has status workflow configured, `False` if it doesn't

    Examples:

        ```python
        project = await project.fetch_status_workflow()
        if has_status_workflow(project):
            print(project.status_workflow.config_id)  # Statically type checked
        ```
    """
    return project.status_workflow is not None


def is_status_workflow_loaded(
    project: Project[ProjectView, MC, GT, QM, QRM, OptionalSW | LazyFromId[OptionalSW]],
) -> TypeGuard[Project[ProjectView, MC, GT, QM, QRM, OptionalSW]]:
    """Checks if project status workflow config is loaded from the API.

    Type guard function that checks if project status workflow config was loaded from the API or exists only as a lazy
    loader. Function is used to narrow project type from potentially lazy to concrete loaded type.

    Returns:
        `True` if status workflow config is loaded, `False` if it exists as lazy loader

    Examples:

        ```python
        project = await `Project`.get(project_id=`ProjectId`('project-id'), lazy=`True`, kit=kit)
        if is_status_workflow_loaded(project) and has_status_workflow(project):
            print(project.status_workflow.config_id)  # Statically type checked
        ```
    """
    return not isinstance(project.status_workflow, LazyValue)
