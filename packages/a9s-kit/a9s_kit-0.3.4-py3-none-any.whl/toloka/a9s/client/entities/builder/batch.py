from __future__ import annotations

import uuid
from typing import Any, Generic, Literal, Mapping, Sequence, cast

from typing_extensions import TypeVar, Unpack

from toloka.a9s.client.client import AsyncKit
from toloka.a9s.client.client.experts_portal.money_config import MoneyConfigFormStrict
from toloka.a9s.client.entities.batch import Batch
from toloka.a9s.client.entities.builder.common import QuorumForm, StatusWorkflowForm
from toloka.a9s.client.entities.money_config import (
    BaseAnnotationMoneyConfigFormParams,
    BaseBuildStatusWorkflowMoneyConfigFormParams,
    build_form_from_base_parameters,
)
from toloka.a9s.client.models.annotation_process.quorum import QuorumConfigBatchForm
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowConfigBatchForm,
    StatusWorkflowConfigViewStrict,
)
from toloka.a9s.client.models.batch import (
    BatchCreateFormV1Strict,
    BatchUpdateFormV1ExtensionInstanceConfigV1Strict,
    BatchUpdateFormV1ExtensionsV1Strict,
    BatchViewV1Strict,
)
from toloka.a9s.client.models.extension_id import ExtensionId
from toloka.a9s.client.models.extensions import (
    with_ground_truth_extension_batch,
    with_money_config_extension_batch,
    with_quality_config_extension_batch,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.view import (
    QuorumConfigView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.services.batch.web.v1.model.form import BatchCompletionFormV1
from toloka.a9s.client.models.generated.ai.toloka.gts.config.web.v0.form import GroundTruthConfigForm
from toloka.a9s.client.models.ground_truth import GroundTruthConfigViewV0Strict
from toloka.a9s.client.models.money_config import MoneyConfigViewStrict
from toloka.a9s.client.models.quality_management.config import (
    QualityConfigFormV0Strict,
    QualityConfigViewV0Strict,
)
from toloka.a9s.client.models.types import GroundTruthConfigId, MoneyConfigId, ProjectId, QualityConfigId

MCFOpt = TypeVar(
    'MCFOpt',
    bound=BaseAnnotationMoneyConfigFormParams
    | BaseBuildStatusWorkflowMoneyConfigFormParams
    | MoneyConfigFormStrict
    | MoneyConfigId
    | None,
    covariant=True,
)
GTFOpt = TypeVar('GTFOpt', bound=GroundTruthConfigForm | GroundTruthConfigId | None, covariant=True)
QMFOpt = TypeVar('QMFOpt', bound=QualityConfigFormV0Strict | QualityConfigId | None, covariant=True)
QrmFOpt = TypeVar('QrmFOpt', bound=QuorumForm | None, covariant=True)
SWFOpt = TypeVar('SWFOpt', bound=StatusWorkflowForm | None, covariant=True)

ResMC = TypeVar('ResMC', bound=MoneyConfigViewStrict | None, covariant=True, default=None)
ResGT = TypeVar('ResGT', bound=GroundTruthConfigViewV0Strict | None, covariant=True, default=None)
ResQM = TypeVar('ResQM', bound=QualityConfigViewV0Strict | None, covariant=True, default=None)
ResQrm = TypeVar('ResQrm', bound=QuorumConfigView | None, covariant=True, default=None)
ResSW = TypeVar('ResSW', bound=StatusWorkflowConfigViewStrict | None, covariant=True, default=None)

ExpertsType = Literal[
    'ai_tutors_writing',
    'team_lead_writers_team',
    'expert_annotators',
    'team_lead_annotators_team',
    'domain_experts',
    'all_experts',
    'bpo',
]


class BatchBuilder(
    Generic[
        MCFOpt,
        GTFOpt,
        QMFOpt,
        QrmFOpt,
        SWFOpt,
        ResMC,
        ResGT,
        ResQM,
        ResQrm,
        ResSW,
    ]
):
    """Builder for creating new Annotation Studio batches with various configurations.

    The BatchBuilder provides an interface for configuring and creating new batches with different extensions
    (money config, ground truth, quality management) and annotation processes (quorum, status workflow).

    Generic type parameters:

    * MCFOpt: Type of money config form or existing config ID
    * GTFOpt: Type of ground truth form or existing config ID
    * QMFOpt: Type of quality management form or existing config ID
    * QrmFOpt: Type of quorum form
    * SWFOpt: Type of status workflow form
    * ResMC: Money config view type after build
    * ResGT: Ground truth config view type after build
    * ResQM: Quality management config view type after build
    * ResQrm: Quorum config view type after build
    * ResSW: Status workflow type after build

    Attributes:
        kit: AsyncKit instance for making API calls
        form: Batch creation form with basic parameters
        money_config: Money config form or ID
        ground_truth: Ground truth config form or ID
        quality_management: Quality management config form or ID
        quorum_config: Quorum config form
        status_workflow_config: Status workflow config form

    Examples:
        Create a basic batch:
        ```python
        builder = BatchBuilder.from_parameters(
            kit=kit,
            project_id=ProjectId('project-1'),
            private_name='Test batch',
            jira_issue='ANNO-123',
            experts_type='expert_annotators',
            monday_subitem_id='123',
        )
        batch = await builder.build()
        ```

        Create batch with money config:
        ```python
        batch = await builder.with_annotation_money_config(price=0.5, currency='USD').build()
        ```

        Create batch with quorum:
        ```python
        batch = await builder.with_quorum(QuorumForm(max_annotations=3)).build()
        ```
    """

    def __init__(
        self,
        kit: AsyncKit,
        form: BatchCreateFormV1Strict,
        money_config: MCFOpt,
        ground_truth: GTFOpt,
        quality_management: QMFOpt,
        quorum_config: QrmFOpt,
        status_workflow_config: SWFOpt,
    ) -> None:
        self.kit = kit
        self.form = form
        self.money_config = money_config
        self.ground_truth = ground_truth
        self.quality_management = quality_management
        self.quorum_config = quorum_config
        self.status_workflow_config = status_workflow_config

    @classmethod
    def from_parameters(
        cls,
        kit: AsyncKit,
        project_id: ProjectId,
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
        """Creates a new BatchBuilder with basic batch parameters.

        Creates an initial BatchBuilder instance that can be used to configure and create a new batch. The builder
        starts with basic batch parameters and can be further configured with extensions and annotation processes
        using with_* methods.

        Args:
            kit: AsyncKit instance for making API calls
            project_id: ID of the project to create batch in
                        private_name: The name of created batch, that only shown to the author
            hidden: Whether to show or hide the batch in the list of batches. Project managers can control this
                parameter through UI. Hidden batches can be fully managed through A9S API but appear disabled in the UI.
            metadata: An arbitrary dictionary with additional information about the batch.
            tags: Tags on the project or batch, used in quality management async config.
            completion: Batch completion type, either "AUTO" or "MANUAL". If "AUTO" is set batch will be automatically
                moved to "COMPLETED" status when all tasks are done. Note that completed batch can't be opened for
                labeling again.
            existing_extensions: A dictionary with extension IDs as keys and extension instance IDs as values.

        Returns:
            New BatchBuilder instance with basic parameters set

        Examples:
            Create builder with minimal params:
            ```python
            builder = BatchBuilder.from_parameters(
                kit=kit,
                project_id='project-1',
                private_name='Test batch',
                jira_issue='ANNO-123',
                experts_type='expert_annotators',
                monday_subitem_id='123',
            )
            ```
        """

        runnable_batch_meta = {
            'jira_issue': jira_issue,
            'experts_type': experts_type,
            'monday_subitem_id': monday_subitem_id,
        }
        if metadata is None:
            metadata = runnable_batch_meta
        else:
            metadata = {**runnable_batch_meta, **metadata}

        return BatchBuilder(
            kit=kit,
            form=BatchCreateFormV1Strict(
                project_id=project_id,
                private_name=private_name,
                hidden=hidden,
                metadata=metadata,
                tags=tags or [],
                completion=BatchCompletionFormV1(type=completion),
                extensions=BatchUpdateFormV1ExtensionsV1Strict(
                    instances=[
                        BatchUpdateFormV1ExtensionInstanceConfigV1Strict(
                            extension_id=extension_id,
                            instance_id=instance_id,
                        )
                        for extension_id, instance_id in (existing_extensions or {}).items()
                    ]
                ),
            ),
            money_config=None,
            ground_truth=None,
            quality_management=None,
            quorum_config=None,
            status_workflow_config=None,
        )

    async def build(self) -> Batch[BatchViewV1Strict, ResMC, ResGT, ResQM, ResQrm, ResSW]:
        """Creates a new batch with all configured extensions and annotation processes.

        Makes API calls to create the batch and any configured extensions (`money_config`, `ground_truth`,
        `quality_management`) and annotation processes (`quorum`, `status_workflow`). Any configurations provided
        as IDs will be
        fetched from the API. All configured extensions and processes will be linked to the created batch.

        Returns:
            New `Batch` instance with all configured extensions and annotation processes. The batch type will reflect
            which configurations were enabled:

                * `BatchWithMoneyConfig`: if money config was configured
                * `BatchWithGroundTruth`: if ground truth was configured
                * `BatchWithQualityManagement`: if quality management was configured
                * `BatchWithQuorum`: if quorum was configured
                * `BatchWithStatusWorkflow`: if status workflow was configured

        Raises:
            `ValueError`: If any API call fails or if extension configurations are inconsistent with the batch.

        Examples:

            Create basic batch:

            ```python
            builder = BatchBuilder.from_parameters(
                kit=kit,
                project_id='project-1',
                private_name='Test batch',
                jira_issue='ANNO-123',
                experts_type='expert_annotators',
                monday_subitem_id='123',
            )
            batch = await builder.build()
            ```

            Create batch with multiple configurations:
            ```python
            batch = await builder
                .with_annotation_money_config(price=0.5, currency='USD')
                .with_quorum(QuorumForm(max_annotations=3))
                .with_status_workflow(StatusWorkflowForm(...))
                .build()
            ```

            Create batch with existing configurations:
            ```python
            batch = await builder
                .with_money_config(MoneyConfigId('existing-config-id'))
                .with_quality_management(QualityConfigId('existing-config-id'))
                .build()
            ```
        """

        money_config_params: (
            BaseAnnotationMoneyConfigFormParams
            | BaseBuildStatusWorkflowMoneyConfigFormParams
            | MoneyConfigFormStrict
            | MoneyConfigId
            | None
        ) = self.money_config
        if money_config_params is None:
            money_config = None
        else:
            if isinstance(money_config_params, (MoneyConfigFormStrict, dict)):
                money_config_form: MoneyConfigFormStrict
                if isinstance(money_config_params, dict):
                    money_config_form = build_form_from_base_parameters(
                        name=str(uuid.uuid4()),
                        requester_id=await self.kit.annotation_studio.get_account_id(),
                        **money_config_params,
                    )
                else:
                    money_config_form = money_config_params

                money_config_id = (await self.kit.experts_portal.money_config.create(money_config_form)).config_id
            else:
                assert isinstance(money_config_params, uuid.UUID)
                money_config_id = money_config_params

            money_config = await self.kit.experts_portal.money_config.get_last_version(money_config_id)

        ground_truth_form: GroundTruthConfigForm | GroundTruthConfigId | None = self.ground_truth
        if ground_truth_form is None:
            ground_truth = None
        elif isinstance(ground_truth_form, GroundTruthConfigForm):
            ground_truth = await self.kit.annotation_studio.ground_truth_config.create(ground_truth_form)
        else:
            ground_truth = await self.kit.annotation_studio.ground_truth_config.get(ground_truth_form)

        quality_management_form: QualityConfigFormV0Strict | QualityConfigId | None = self.quality_management
        if quality_management_form is None:
            quality_management = None
        elif isinstance(quality_management_form, QualityConfigFormV0Strict):
            quality_management = await self.kit.quality_management.quality_config.create(quality_management_form)
        else:
            quality_management = await self.kit.quality_management.quality_config.get(quality_management_form)

        form = self.form
        if money_config is not None:
            form = with_money_config_extension_batch(batch_form=form, money_config_id=money_config.config_id)
        if ground_truth is not None:
            form = with_ground_truth_extension_batch(batch_form=form, ground_truth_config_id=ground_truth.id)
        if quality_management is not None:
            form = with_quality_config_extension_batch(batch_form=form, quality_config_id=quality_management.id)

        batch = await self.kit.annotation_studio.batch.create(form)

        if isinstance(self.quorum_config, QuorumForm):
            quorum_config = await self.kit.annotation_studio.quorum.set_batch_defaults(
                QuorumConfigBatchForm(
                    batch_id=batch.id,
                    max_annotations=self.quorum_config.max_annotations,
                    max_annotation_per_annotator=self.quorum_config.max_annotation_per_annotator,
                    skip_allowed=self.quorum_config.skip_allowed,
                )
            )
        else:
            quorum_config = None

        status_workflow_form: StatusWorkflowForm | None = self.status_workflow_config
        if isinstance(status_workflow_form, StatusWorkflowForm):
            await self.kit.annotation_studio.status_workflow.set_batch_defaults(
                StatusWorkflowConfigBatchForm(
                    batch_id=batch.id,
                    statuses=status_workflow_form.statuses,
                    timeouts=status_workflow_form.timeouts,
                )
            )
            status_workflow_config = await self.kit.annotation_studio.status_workflow.get_possible_statuses(batch.id)
        else:
            status_workflow_config = None

        return Batch(
            batch_id=batch.id,
            view=batch,
            money_config=cast(ResMC, money_config),
            ground_truth=cast(ResGT, ground_truth),
            quality_management=cast(ResQM, quality_management),
            quorum_config=cast(ResQrm, quorum_config),
            status_workflow_config=cast(ResSW, status_workflow_config),
            kit=self.kit,
        )

    def with_money_config(
        self: BatchBuilderWithoutMoneyConfig[GTFOpt, QMFOpt, QrmFOpt, SWFOpt, ResGT, ResQM, ResQrm, ResSW],
        money_config: BaseAnnotationMoneyConfigFormParams
        | BaseBuildStatusWorkflowMoneyConfigFormParams
        | MoneyConfigId,
    ) -> BatchBuilderWithMoneyConfig[GTFOpt, QMFOpt, QrmFOpt, SWFOpt, ResGT, ResQM, ResQrm, ResSW]:
        """Configures money config extension for the batch being built.

        Adds money config configuration to the builder, either as parameters for a new config or an existing config ID.
        This is a generic method that accepts both annotation-based and status workflow-based money configs.
        Consider using `with_annotation_money_config` or `with_status_workflow_money_config` for simpler interfaces.

        Args:
            money_config: Either parameters for creating new money config or ID of existing config to use.
                Can be annotation-based or status workflow-based parameters.

        Returns:
            Updated builder with money config configuration added. The return type reflects that money config
            will be available after build.

        Examples:

            Use existing money config:

            ```python
            builder = builder.with_money_config(MoneyConfigId('existing-config'))
            ```

            Create new annotation money config:

            ```python
            params = BaseAnnotationMoneyConfigFormParams(price=0.5, currency='USD')
            builder = builder.with_money_config(params)
            ```
        """

        return BatchBuilderWithMoneyConfig[GTFOpt, QMFOpt, QrmFOpt, SWFOpt, ResGT, ResQM, ResQrm, ResSW](
            kit=self.kit,
            form=self.form,
            money_config=money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=self.status_workflow_config,
        )

    def with_status_workflow_money_config(
        self: BatchBuilderWithoutMoneyConfig[GTFOpt, QMFOpt, QrmFOpt, StatusWorkflowForm, ResGT, ResQM, ResQrm, ResSW],
        **kwargs: Unpack[BaseBuildStatusWorkflowMoneyConfigFormParams],
    ) -> BatchBuilderWithMoneyConfig[GTFOpt, QMFOpt, QrmFOpt, StatusWorkflowForm, ResGT, ResQM, ResQrm, ResSW]:
        """Configures status workflow-based money config extension for the batch being built.

        Adds money config configuration to the builder, with parameters specific to status workflow-based payments.
        This method can only be used when status workflow is also configured for the batch.

        Args:
            snippet_price (float): Price shown in tasks list
            currency (Literal['BU', 'USD']): Currency code, either 'BU' (Base Units) or 'USD'
            mutable_transitions (StatusTransitionMutablePayments): Mapping from status to expected payment settings
            paid_transitions (StatusTransitionPayments): Mapping from status to actual payment settings
            tenant_id (NotRequired[str | None]): Optional tenant identifier
            skip_pending_balance (NotRequired[bool]): If True, payment will be processed without pending balance stage

        Returns:
            Updated builder with status workflow money config configuration added. The return type reflects that
            money config will be available after build.

        Examples:
            ```python
            builder = builder.with_status_workflow(status_workflow_form)
            mutable = {'in_progress': StatusTransitionMutablePayment(price=0.4)}
            paid = {'accepted': StatusTransitionPayment(price=0.4)}
            builder = builder.with_status_workflow_money_config(
                snippet_price=0.4, currency='USD', mutable_transitions=mutable, paid_transitions=paid
            )
            ```
        """

        return self.with_money_config(kwargs)

    def with_annotation_money_config(
        self: BatchBuilderWithoutMoneyConfig[GTFOpt, QMFOpt, QrmFOpt, SWFOpt, ResGT, ResQM, ResQrm, ResSW],
        **kwargs: Unpack[BaseAnnotationMoneyConfigFormParams],
    ) -> BatchBuilderWithMoneyConfig[GTFOpt, QMFOpt, QrmFOpt, SWFOpt, ResGT, ResQM, ResQrm, ResSW]:
        """Configures annotation-based money config extension for the batch being built.

        Adds money config configuration to the builder, with parameters for simple per-annotation payments.

        Args:
            price (float): Price per annotation in specified currency
            currency (Literal['BU', 'USD']): Currency code, either 'BU' (Base Units) or 'USD'
            tenant_id (NotRequired[str | None]): Optional tenant identifier
            skip_pending_balance (NotRequired[bool]): If True, payment will be processed without pending balance stage

        Returns:
            Updated builder with annotation-based money config configuration added. The return type reflects that
            money config will be available after build.

        Examples:
            ```python
            builder = builder.with_annotation_money_config(price=0.5, currency='USD', skip_pending_balance=True)
            ```
        """

        return self.with_money_config(kwargs)

    def with_ground_truth(
        self: BatchBuilderWithoutGroundTruth[MCFOpt, QMFOpt, QrmFOpt, SWFOpt, ResMC, ResQM, ResQrm, ResSW],
        ground_truth: GroundTruthConfigForm | GroundTruthConfigId,
    ) -> BatchBuilderWithGroundTruth[MCFOpt, QMFOpt, QrmFOpt, SWFOpt, ResMC, ResQM, ResQrm, ResSW]:
        """Configures ground truth extension for the batch being built.

        Adds ground truth configuration to the builder, either as parameters for a new config or an existing config ID.

        Args:
            ground_truth: Either parameters for creating new ground truth config or ID of existing config to use

        Returns:
            Updated builder with ground truth configuration added. The return type reflects that ground truth
            will be available after build.

        Examples:

            Use existing ground truth config:

            ```python
            builder = builder.with_ground_truth(GroundTruthConfigId('existing-config'))
            ```

            Create new ground truth config:

            ```python
            form = GroundTruthConfigForm(...)
            builder = builder.with_ground_truth(form)
            ```
        """

        return BatchBuilderWithGroundTruth[MCFOpt, QMFOpt, QrmFOpt, SWFOpt, ResMC, ResQM, ResQrm, ResSW](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=self.status_workflow_config,
        )

    def with_quality_management(
        self: BatchBuilderWithoutQualityManagement[MCFOpt, GTFOpt, QrmFOpt, SWFOpt, ResMC, ResGT, ResQrm, ResSW],
        quality_management: QualityConfigFormV0Strict | QualityConfigId,
    ) -> BatchBuilderWithQualityManagement[MCFOpt, GTFOpt, QrmFOpt, SWFOpt, ResMC, ResGT, ResQrm, ResSW]:
        """Configures quality management extension for the batch being built.

        Adds quality management configuration to the builder, either as parameters for a new config or an existing
        config ID. Quality management allows setting restrictions on annotators' access to the batch.

        Args:
            quality_management: Either parameters for creating new quality management config or ID of existing config
                to use

        Returns:
            Updated builder with quality management configuration added. The return type reflects that quality
                management will be available after build.

        Examples:

            Use existing quality management config:

            ```python
            builder = builder.with_quality_management(QualityConfigId('existing-config'))
            ```

            Create new quality management config:

            ```python
            form = QualityConfigFormV0Strict(...)
            builder = builder.with_quality_management(form)
            ```
        """

        return BatchBuilderWithQualityManagement[MCFOpt, GTFOpt, QrmFOpt, SWFOpt, ResMC, ResGT, ResQrm, ResSW](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=self.status_workflow_config,
        )

    def with_quorum(
        self: BatchBuilderWithoutQuorum[MCFOpt, GTFOpt, QMFOpt, SWFOpt, ResMC, ResGT, ResQM, ResSW],
        quorum_config: QuorumForm,
    ) -> BatchBuilderWithQuorum[MCFOpt, GTFOpt, QMFOpt, SWFOpt, ResMC, ResGT, ResQM, ResSW]:
        """Configures quorum annotation process for the batch being built.

        Adds quorum configuration to create annotation groups that require multiple annotations per task.

        Args:
            quorum_config: Parameters for quorum process.

        Returns:
            Updated builder with quorum configuration added. The return type reflects that quorum process
            will be available after build.

        Examples:
            ```python
            builder = builder.with_quorum(
                QuorumForm(
                    max_annotations=3,
                    max_annotation_per_annotator=1,
                    skip_allowed=True,
                )
            )
            ```
        """

        return BatchBuilderWithQuorum[MCFOpt, GTFOpt, QMFOpt, SWFOpt, ResMC, ResGT, ResQM, ResSW](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=quorum_config,
            status_workflow_config=self.status_workflow_config,
        )

    def with_status_workflow(
        self: BatchBuilderWithoutStatusWorkflow[MCFOpt, GTFOpt, QMFOpt, QrmFOpt, ResMC, ResGT, ResQM, ResQrm],
        status_workflow_config: StatusWorkflowForm,
    ) -> BatchBuilderWithStatusWorkflow[MCFOpt, GTFOpt, QMFOpt, QrmFOpt, ResMC, ResGT, ResQM, ResQrm]:
        """Configures status workflow annotation process for the batch being built.

        Adds status workflow configuration to track annotation states and transitions between them.
        Status workflow enables features like review stages and conditional payments based on status.

        Args:
            status_workflow_config: Parameters for status workflow process.

        Returns:
            Updated builder with status workflow configuration added. The return type reflects that status workflow
            will be available after build.

        Examples:
            ```python
            statuses = {'in_progress': StatusForm(...), 'review': StatusForm(...), 'accepted': StatusForm(...)}
            builder = builder.with_status_workflow(
                StatusWorkflowForm(
                    statuses=statuses,
                    timeouts={
                        'in_progress': StatusWorkflowTimeoutForm(duration=3600),
                    },
                )
            )
            ```
        """

        return BatchBuilderWithStatusWorkflow[MCFOpt, GTFOpt, QMFOpt, QrmFOpt, ResMC, ResGT, ResQM, ResQrm](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum_config=self.quorum_config,
            status_workflow_config=status_workflow_config,
        )


InitialBatchBuilder = BatchBuilder[None, None, None, None, None]
BatchBuilderWithoutMoneyConfig = BatchBuilder[None, GTFOpt, QMFOpt, QrmFOpt, SWFOpt, None, ResGT, ResQM, ResQrm, ResSW]
BatchBuilderWithMoneyConfig = BatchBuilder[
    BaseAnnotationMoneyConfigFormParams
    | BaseBuildStatusWorkflowMoneyConfigFormParams
    | MoneyConfigFormStrict
    | MoneyConfigId
    | None,
    GTFOpt,
    QMFOpt,
    QrmFOpt,
    SWFOpt,
    MoneyConfigViewStrict,
    ResGT,
    ResQM,
    ResQrm,
    ResSW,
]
BatchBuilderWithoutGroundTruth = BatchBuilder[MCFOpt, None, QMFOpt, QrmFOpt, SWFOpt, ResMC, None, ResQM, ResQrm, ResSW]
BatchBuilderWithGroundTruth = BatchBuilder[
    MCFOpt,
    GroundTruthConfigForm | GroundTruthConfigId,
    QMFOpt,
    QrmFOpt,
    SWFOpt,
    ResMC,
    GroundTruthConfigViewV0Strict,
    ResQM,
    ResQrm,
    ResSW,
]
BatchBuilderWithoutQualityManagement = BatchBuilder[
    MCFOpt, GTFOpt, None, QrmFOpt, SWFOpt, ResMC, ResGT, None, ResQrm, ResSW
]
BatchBuilderWithQualityManagement = BatchBuilder[
    MCFOpt,
    GTFOpt,
    QualityConfigFormV0Strict | QualityConfigId,
    QrmFOpt,
    SWFOpt,
    ResMC,
    ResGT,
    QualityConfigViewV0Strict,
    ResQrm,
    ResSW,
]
BatchBuilderWithoutQuorum = BatchBuilder[MCFOpt, GTFOpt, QMFOpt, None, SWFOpt, ResMC, ResGT, ResQM, None, ResSW]
BatchBuilderWithQuorum = BatchBuilder[
    MCFOpt, GTFOpt, QMFOpt, QuorumForm, SWFOpt, ResMC, ResGT, ResQM, QuorumConfigView, ResSW
]
BatchBuilderWithoutStatusWorkflow = BatchBuilder[
    MCFOpt, GTFOpt, QMFOpt, QrmFOpt, None, ResMC, ResGT, ResQM, ResQrm, None
]
BatchBuilderWithStatusWorkflow = BatchBuilder[
    MCFOpt, GTFOpt, QMFOpt, QrmFOpt, StatusWorkflowForm, ResMC, ResGT, ResQM, ResQrm, StatusWorkflowConfigViewStrict
]
