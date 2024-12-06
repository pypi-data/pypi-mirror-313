__all__ = [
    'AsyncAnnotationStudioClient',
    'AsyncExpertsPortalClient',
    'AsyncKit',
    'CustomEnvironment',
    'BaseUrl',
]


from typing import Literal

from typing_extensions import Self, Unpack, assert_never, deprecated

from toloka.a9s.client.base.client import (
    AsyncBaseAnnotationStudioClient,
    AsyncBaseExpertsPortalClient,
)
from toloka.a9s.client.base.converter import (
    is_preset_a9s_environment,
    is_preset_experts_portal_environment,
)
from toloka.a9s.client.base.types import (
    AnnotationStudioEnvironment,
    BaseUrl,
    CustomEnvironment,
    EnvironmentSpec,
    ExpertsPortalEnvironment,
    GlobalEnvironment,
    is_production_preset_a9s_environment,
)
from toloka.a9s.client.client.annotation import AsyncAnnotationStudioAnnotationsClient
from toloka.a9s.client.client.annotation_edit import AsyncAnnotationStudioAnnotationEditsClient
from toloka.a9s.client.client.annotation_metric import AsyncAnnotationStudioAnnotationMetricsClient
from toloka.a9s.client.client.batch import AsyncAnnotationStudioBatchesClient
from toloka.a9s.client.client.experimental.annotation_process import AsyncAnnotationProcessesClient
from toloka.a9s.client.client.experimental.annotation_process.post_acceptance import (
    AsyncAnnotationStudioPostAcceptanceClient,
)
from toloka.a9s.client.client.experimental.annotation_process.quorum import AsyncAnnotationStudioQuorumClient
from toloka.a9s.client.client.experimental.annotation_process.status_workflow import (
    AsyncAnnotationStudioStatusWorkflowClient,
)
from toloka.a9s.client.client.experimental.ground_truth import (
    AsyncGroundTruthBucketClient,
    AsyncGroundTruthClient,
    AsyncGroundTruthConfigClient,
)
from toloka.a9s.client.client.experimental.quality_management import AsyncQmsClient
from toloka.a9s.client.client.experts_portal.money_config import (
    AsyncExpertsPortalMoneyConfigClient,
    MoneyConfigFormStrict,
)
from toloka.a9s.client.client.experts_portal.pipeline.config import AsyncExpertsPortalPipelineConfigControllerClient
from toloka.a9s.client.client.experts_portal.pipeline.instance import AsyncExpertsPortalPipelineInstanceControllerClient
from toloka.a9s.client.client.experts_portal.pipeline.money_config import (
    AsyncExpertsPortalPipelineMoneyConfigControllerClient,
)
from toloka.a9s.client.client.experts_portal.qualification import AsyncExpertsPortalQualificationControllerClient
from toloka.a9s.client.client.experts_portal.qualification.filter import (
    AsyncExpertsPortalQualificationFilterControllerClient,
)
from toloka.a9s.client.client.experts_portal.qualification.user import (
    AsyncExpertsPortalUserQualificationControllerClient,
)
from toloka.a9s.client.client.functions import AsyncFunctionsClient
from toloka.a9s.client.client.project import AsyncAnnotationStudioProjectsClient
from toloka.a9s.client.models.batch import BatchCreateFormV1Strict, BatchViewV1Strict
from toloka.a9s.client.models.custom import AddFastResponsesBanForProjectResult
from toloka.a9s.client.models.data_manager import AnnotationGroupDataManagerView
from toloka.a9s.client.models.extension_id import QUALITY_CONFIG_EXTENSION_ID
from toloka.a9s.client.models.extensions import (
    with_ground_truth_extension_batch,
    with_ground_truth_extension_project,
    with_money_config_extension_batch,
    with_money_config_extension_project,
    with_quality_config_extension_batch,
    with_quality_config_extension_project,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.data_manager.web.ui.search import (
    SearchForm,
    SearchFormCondition,
    SearchFormPagination,
    SearchView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.project.web.v1.form import ProjectFormV1
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.rule_evaluation.web.v0.viewform import TagFilterViewForm
from toloka.a9s.client.models.generated.ai.toloka.a9s.services.batch.web.v1.model.form import BatchCreateFormV1
from toloka.a9s.client.models.generated.ai.toloka.gts.config.web.v0.form import GroundTruthConfigForm
from toloka.a9s.client.models.project import ProjectFormV1Strict, ProjectViewV1Strict
from toloka.a9s.client.models.quality_management.async_config import (
    AsyncQualityConfigFormV0Strict,
    CountQualityRuleViewForm,
    CreateRestrictionQualityActionParams,
    CreateRestrictionQualityActionViewForm,
)
from toloka.a9s.client.models.quality_management.config import (
    AnnotationEditTimeParams,
    AnnotationEditTimeViewFormStrict,
    QualityConfigFormV0Strict,
)
from toloka.a9s.client.models.quality_management.rules import CountRuleParams
from toloka.a9s.client.models.types import AnnotationId, QualityConfigId
from toloka.a9s.client.models.utils import model_dump_a9s
from toloka.common.http.args import BaseHttpClientNotRequiredArgs
from toloka.common.http.client import AsyncHttpClient


class AsyncAnnotationStudioClient(AsyncBaseAnnotationStudioClient):
    project: AsyncAnnotationStudioProjectsClient
    batch: AsyncAnnotationStudioBatchesClient
    annotation: AsyncAnnotationStudioAnnotationsClient
    annotation_edit: AsyncAnnotationStudioAnnotationEditsClient

    # unstable api
    annotation_process: AsyncAnnotationProcessesClient
    post_acceptance: AsyncAnnotationStudioPostAcceptanceClient
    quorum: AsyncAnnotationStudioQuorumClient
    status_workflow: AsyncAnnotationStudioStatusWorkflowClient
    ground_truth: AsyncGroundTruthClient
    ground_truth_bucket: AsyncGroundTruthBucketClient
    ground_truth_config: AsyncGroundTruthConfigClient

    def __init__(self, transport: AsyncHttpClient) -> None:
        super().__init__(transport)
        self.project = AsyncAnnotationStudioProjectsClient(transport)
        self.batch = AsyncAnnotationStudioBatchesClient(transport)
        self.annotation = AsyncAnnotationStudioAnnotationsClient(transport)
        self.annotation_edit = AsyncAnnotationStudioAnnotationEditsClient(transport)
        self.annotation_metric = AsyncAnnotationStudioAnnotationMetricsClient(transport)
        self.annotation_process = AsyncAnnotationProcessesClient(transport)
        self.post_acceptance = AsyncAnnotationStudioPostAcceptanceClient(transport)
        self.quorum = AsyncAnnotationStudioQuorumClient(transport)
        self.status_workflow = AsyncAnnotationStudioStatusWorkflowClient(transport)
        self.ground_truth = AsyncGroundTruthClient(transport)
        self.ground_truth_bucket = AsyncGroundTruthBucketClient(transport)
        self.ground_truth_config = AsyncGroundTruthConfigClient(transport)

    @classmethod
    def from_credentials(
        cls,
        environment: AnnotationStudioEnvironment | BaseUrl,
        api_key: str,
        **kwargs: Unpack[BaseHttpClientNotRequiredArgs],
    ) -> Self:
        if is_preset_a9s_environment(environment):
            base_url = AsyncBaseAnnotationStudioClient.environment_to_url(environment)
        else:
            base_url = environment
        return cls(
            transport=AsyncHttpClient.from_api_key(
                base_url=base_url,
                api_key=api_key,
                **kwargs,
            )
        )

    # unstable api
    async def get_account_id(self) -> str:
        return str(
            (await self.client.make_retriable_request('GET', f'{self.UI_API_PREFIX}/account')).json()['account_id']
        )

    async def get_annotation_group_data_manager_view(
        self,
        annotation_group_id: str,
        batch_id: str,
    ) -> AnnotationGroupDataManagerView | None:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.UI_API_PREFIX}/data-manager/search',
            body=model_dump_a9s(
                SearchForm(
                    batch_id=batch_id,
                    conditions=[
                        SearchFormCondition(
                            field='group_id',
                            operator='EQUALS',
                            value=annotation_group_id,
                        )
                    ],
                    pagination=SearchFormPagination(
                        offset=0,
                        limit=1,
                    ),
                ),
            ),
        )
        search_view = SearchView.model_validate(response.json())

        if search_view.data is None or len(search_view.data) == 0:
            return None

        assert len(search_view.data) == 1, 'there is at most one search view row per annotation group'
        return AnnotationGroupDataManagerView.model_validate(search_view.data[0], from_attributes=True)

    async def get_all_annotation_ids_by_annotation_group_id(
        self,
        annotation_group_id: str,
        batch_id: str,
    ) -> set[AnnotationId]:
        search_view = await self.get_annotation_group_data_manager_view(
            annotation_group_id=annotation_group_id,
            batch_id=batch_id,
        )
        if search_view is None:
            return set()

        annotation_ids = set(
            element.annotation_id for element in search_view.elements if element.annotation_id is not None
        )
        return {AnnotationId(annotation_id) for annotation_id in annotation_ids}


class AsyncExpertsPortalClient:
    money_config: AsyncExpertsPortalMoneyConfigClient
    pipeline_config: AsyncExpertsPortalPipelineConfigControllerClient
    pipeline_instance: AsyncExpertsPortalPipelineInstanceControllerClient
    pipeline_money_config: AsyncExpertsPortalPipelineMoneyConfigControllerClient
    qualification: AsyncExpertsPortalQualificationControllerClient
    qualification_filter: AsyncExpertsPortalQualificationFilterControllerClient
    user_qualification: AsyncExpertsPortalUserQualificationControllerClient

    def __init__(self, transport: AsyncHttpClient) -> None:
        self.money_config = AsyncExpertsPortalMoneyConfigClient(transport)
        self.pipeline_config = AsyncExpertsPortalPipelineConfigControllerClient(transport)
        self.pipeline_instance = AsyncExpertsPortalPipelineInstanceControllerClient(transport)
        self.pipeline_money_config = AsyncExpertsPortalPipelineMoneyConfigControllerClient(transport)
        self.qualification = AsyncExpertsPortalQualificationControllerClient(transport)
        self.qualification_filter = AsyncExpertsPortalQualificationFilterControllerClient(transport)
        self.user_qualification = AsyncExpertsPortalUserQualificationControllerClient(transport)

    @classmethod
    def from_credentials(
        cls,
        environment: BaseUrl | ExpertsPortalEnvironment,
        api_key: str,
        **kwargs: Unpack[BaseHttpClientNotRequiredArgs],
    ) -> Self:
        if is_preset_experts_portal_environment(environment):
            base_url = AsyncBaseExpertsPortalClient.environment_to_url(environment)
        else:
            base_url = environment
        return cls(
            transport=AsyncHttpClient.from_api_key(
                base_url=base_url,
                api_key=api_key,
                **kwargs,
            ),
        )


class AsyncKit:
    annotation_studio: AsyncAnnotationStudioClient
    experts_portal: AsyncExpertsPortalClient
    quality_management: AsyncQmsClient
    functions: AsyncFunctionsClient

    def __init__(
        self,
        a9s_client: AsyncAnnotationStudioClient,
        experts_portal: AsyncExpertsPortalClient,
        quality_management: AsyncQmsClient,
        functions: AsyncFunctionsClient,
    ) -> None:
        self.annotation_studio = a9s_client
        self.experts_portal = experts_portal
        self.quality_management = quality_management
        self.functions = functions

    @staticmethod
    def resolve_global_environment(environment: GlobalEnvironment) -> EnvironmentSpec:
        if is_production_preset_a9s_environment(environment):
            return EnvironmentSpec(
                annotation_studio=environment, experts_portal='production', functions_environment='production'
            )
        elif environment == 'staging' or environment == 'prestable':
            return EnvironmentSpec(
                annotation_studio=environment, experts_portal='prestable', functions_environment='prestable'
            )
        elif environment == 'regress-release':
            return EnvironmentSpec(
                annotation_studio=environment,
                experts_portal='regress-release',
                functions_environment='regress-release',
            )
        else:
            assert_never(environment)

    @classmethod
    def from_credentials(
        cls,
        environment: GlobalEnvironment | CustomEnvironment,
        api_key: str,
        **kwargs: Unpack[BaseHttpClientNotRequiredArgs],
    ) -> Self:
        if isinstance(environment, CustomEnvironment):
            return cls(
                a9s_client=AsyncAnnotationStudioClient.from_credentials(
                    environment=environment.a9s_base_url,
                    api_key=api_key,
                    **kwargs,
                ),
                experts_portal=AsyncExpertsPortalClient.from_credentials(
                    environment=environment.experts_portal_base_url,
                    api_key=api_key,
                    **kwargs,
                ),
                quality_management=AsyncQmsClient.from_credentials(
                    environment=environment.a9s_base_url,
                    api_key=api_key,
                    **kwargs,
                ),
                functions=AsyncFunctionsClient.from_credentials(
                    environment=environment.functions_base_url,
                    api_key=api_key,
                    **kwargs,
                ),
            )
        else:
            environment_spec = cls.resolve_global_environment(environment)
            return cls(
                a9s_client=AsyncAnnotationStudioClient.from_credentials(
                    api_key=api_key,
                    environment=environment_spec.annotation_studio,
                    **kwargs,
                ),
                experts_portal=AsyncExpertsPortalClient.from_credentials(
                    api_key=api_key,
                    environment=environment_spec.experts_portal,
                    **kwargs,
                ),
                quality_management=AsyncQmsClient.from_credentials(
                    environment=environment_spec.annotation_studio,
                    api_key=api_key,
                    **kwargs,
                ),
                functions=AsyncFunctionsClient.from_credentials(
                    environment=environment_spec.functions_environment,
                    api_key=api_key,
                    **kwargs,
                ),
            )

    DEFAULT_ANNOTATION_EDIT_TIME_METRIC_NAME: Literal['answer-time'] = 'answer-time'
    DEFAULT_ANNOTATION_EDIT_TIME_CUMULATIVE_METRIC_NAME: Literal['total-answer-time'] = 'total-answer-time'

    @deprecated('Use AsyncQualityConfigFormV0Strict.project_fast_answers(...) instead')
    async def add_fast_responses_ban_for_project_legacy(
        self,
        project_view: ProjectViewV1Strict,
        restriction_form: CreateRestrictionQualityActionParams,
        history_threshold: int,
        quality_threshold_lower_bound: float,
        quality_threshold_upper_bound: float,
        count_threshold: int,
        window_length_days: int | None = None,
        history_size: int | None = None,
        metric_name: str = DEFAULT_ANNOTATION_EDIT_TIME_METRIC_NAME,
        cumulative_metric_name: str = DEFAULT_ANNOTATION_EDIT_TIME_CUMULATIVE_METRIC_NAME,
    ) -> AddFastResponsesBanForProjectResult:
        filter_tag = project_view.id

        quality_configs = [
            await self.quality_management.quality_config.get(QualityConfigId(extension_instance.instance_id))
            for extension_instance in project_view.extensions.instances
            if extension_instance.extension_id == QUALITY_CONFIG_EXTENSION_ID
        ]
        if len(quality_configs) > 1:
            raise ValueError('There should be at most one quality config for a project')
        annotation_edit_time_metrics = [
            metric
            for config in quality_configs
            for metric in config.metrics
            if (
                metric.type == 'ANNOTATION_EDIT_TIME'
                and metric.params.metric_name == metric_name
                and metric.params.cumulative_metric_name == cumulative_metric_name
            )
        ]

        need_update = False
        project_form = ProjectFormV1Strict.from_view(project_view)

        if len(annotation_edit_time_metrics) == 0:
            if quality_configs:
                quality_config = quality_configs[0]
                quality_config.metrics = [
                    *quality_config.metrics,
                    AnnotationEditTimeViewFormStrict(
                        params=AnnotationEditTimeParams(
                            metric_name=metric_name,
                            cumulative_metric_name=cumulative_metric_name,
                        ),
                    ),
                ]
                quality_config_form = QualityConfigFormV0Strict(
                    metrics=quality_config.metrics,
                    filters=quality_config.filters,
                )
                quality_config = await self.quality_management.quality_config.update(
                    quality_config.id, quality_config_form
                )
            else:
                quality_config = await self.quality_management.quality_config.create(
                    QualityConfigFormV0Strict(
                        filters=[],
                        metrics=[
                            AnnotationEditTimeViewFormStrict(
                                params=AnnotationEditTimeParams(
                                    metric_name=metric_name,
                                    cumulative_metric_name=cumulative_metric_name,
                                ),
                            )
                        ],
                    )
                )
                project_form = with_quality_config_extension_project(
                    project_form=project_form,
                    quality_config_id=quality_config.id,
                )
                need_update = True
        else:
            assert len(annotation_edit_time_metrics) == 1, 'there is at most one metric with given names'
            quality_config = quality_configs[0]

        if filter_tag not in project_view.tags:
            project_form.add_tag(filter_tag)
            need_update = True

        if need_update:
            project_view = await self.annotation_studio.project.update(project_view.id, project_form)

        # TODO: find async configs with this tag and same rule if present and update instead when API allows that
        async_config = await self.quality_management.async_quality_config.create(
            AsyncQualityConfigFormV0Strict(
                rules=[
                    CountQualityRuleViewForm(
                        params=CountRuleParams(
                            metric_names=[metric_name],
                            history_threshold=history_threshold,
                            quality_threshold_lower_bound=quality_threshold_lower_bound,
                            quality_threshold_upper_bound=quality_threshold_upper_bound,
                            count_threshold=count_threshold,
                            window_length_days=window_length_days,
                            history_size=history_size,
                        ),
                        actions=[CreateRestrictionQualityActionViewForm(params=restriction_form)],
                        filter=TagFilterViewForm(any_of=[filter_tag]),
                    )
                ],
                triggers=[],
            )
        )

        return AddFastResponsesBanForProjectResult(
            project=project_view,
            quality_config=quality_config,
            async_quality_config=async_config,
        )

    async def create_project_with_extensions(
        self,
        project_form: ProjectFormV1,
        money_config_form: MoneyConfigFormStrict | None = None,
        ground_truth_config_form: GroundTruthConfigForm | None = None,
        quality_config_form: QualityConfigFormV0Strict | None = None,
    ) -> ProjectViewV1Strict:
        if money_config_form is not None:
            money_config = await self.experts_portal.money_config.create(form=money_config_form)
            project_form = with_money_config_extension_project(
                project_form,
                money_config_id=money_config.config_id,
            )
        if ground_truth_config_form is not None:
            ground_truth_config = await self.annotation_studio.ground_truth_config.create(form=ground_truth_config_form)
            project_form = with_ground_truth_extension_project(
                project_form,
                ground_truth_config_id=ground_truth_config.id,
            )
        if quality_config_form is not None:
            quality_config = await self.quality_management.quality_config.create(form=quality_config_form)
            project_form = with_quality_config_extension_project(
                project_form,
                quality_config_id=quality_config.id,
            )

        return await self.annotation_studio.project.create(form=project_form)

    async def create_batch_with_extensions(
        self,
        batch_form: BatchCreateFormV1,
        money_config_form: MoneyConfigFormStrict | None = None,
        ground_truth_config_form: GroundTruthConfigForm | None = None,
        quality_config_form: QualityConfigFormV0Strict | None = None,
    ) -> BatchViewV1Strict:
        if money_config_form is not None:
            money_config = await self.experts_portal.money_config.create(form=money_config_form)
            batch_form = with_money_config_extension_batch(
                batch_form=BatchCreateFormV1Strict.model_validate(batch_form, from_attributes=True),
                money_config_id=money_config.config_id,
            )
        if ground_truth_config_form is not None:
            ground_truth_config = await self.annotation_studio.ground_truth_config.create(form=ground_truth_config_form)
            batch_form = with_ground_truth_extension_batch(
                batch_form=BatchCreateFormV1Strict.model_validate(batch_form, from_attributes=True),
                ground_truth_config_id=ground_truth_config.id,
            )
        if quality_config_form is not None:
            quality_config = await self.quality_management.quality_config.create(form=quality_config_form)
            batch_form = with_quality_config_extension_batch(
                batch_form=BatchCreateFormV1Strict.model_validate(batch_form, from_attributes=True),
                quality_config_id=quality_config.id,
            )
        return await self.annotation_studio.batch.create(form=batch_form)
