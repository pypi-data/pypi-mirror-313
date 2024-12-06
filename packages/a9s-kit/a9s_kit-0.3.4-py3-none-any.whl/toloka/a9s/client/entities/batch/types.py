from typing import TYPE_CHECKING, TypeAlias

from typing_extensions import TypeVar

from toloka.a9s.client.models.annotation_process.status_workflow import StatusWorkflowConfigViewStrict

if TYPE_CHECKING:
    from toloka.a9s.client.entities.batch import Batch

from toloka.a9s.client.entities.base import LazyValue
from toloka.a9s.client.models.batch import BatchViewV1Strict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.view import (
    QuorumConfigView,
)
from toloka.a9s.client.models.ground_truth import GroundTruthConfigViewV0Strict
from toloka.a9s.client.models.money_config import MoneyConfigViewStrict
from toloka.a9s.client.models.quality_management.config import QualityConfigViewV0Strict
from toloka.a9s.client.models.types import BatchId

LazyType = TypeVar('LazyType')
LazyFromId = LazyValue[[BatchId], LazyType]
LazyFromView = LazyValue[[BatchViewV1Strict], LazyType]

BatchView = TypeVar(
    'BatchView',
    bound=BatchViewV1Strict | LazyFromId[BatchViewV1Strict],
    covariant=True,
    default=BatchViewV1Strict | LazyFromId[BatchViewV1Strict],
)
OptionalMC = MoneyConfigViewStrict | None
MC = TypeVar(
    'MC',
    bound=MoneyConfigViewStrict | None | LazyFromView[OptionalMC],
    covariant=True,
    default=MoneyConfigViewStrict | None | LazyFromView[OptionalMC],
)
OptionalGT = GroundTruthConfigViewV0Strict | None
GT = TypeVar(
    'GT',
    bound=GroundTruthConfigViewV0Strict | None | LazyFromView[OptionalGT],
    covariant=True,
    default=GroundTruthConfigViewV0Strict | None | LazyFromView[OptionalGT],
)
OptionalQM = QualityConfigViewV0Strict | None
QM = TypeVar(
    'QM',
    bound=QualityConfigViewV0Strict | None | LazyFromView[OptionalQM],
    covariant=True,
    default=QualityConfigViewV0Strict | None | LazyFromView[OptionalQM],
)
OptionalQRM = QuorumConfigView | None
QRM = TypeVar(
    'QRM',
    bound=QuorumConfigView | None | LazyFromView[OptionalQRM],
    covariant=True,
    default=QuorumConfigView | None | LazyFromView[OptionalQRM],
)
OptionalSW = StatusWorkflowConfigViewStrict | None
SW = TypeVar(
    'SW', bound=OptionalSW | LazyFromView[OptionalSW], covariant=True, default=OptionalSW | LazyFromView[OptionalSW]
)
BatchAnyEager: TypeAlias = 'Batch[BatchViewV1Strict, OptionalMC, OptionalGT, OptionalQM, OptionalQRM, OptionalSW]'
BatchAnyLazy: TypeAlias = """Batch[
    LazyFromId[BatchViewV1Strict],
    LazyFromView[OptionalMC],
    LazyFromView[OptionalGT],
    LazyFromView[OptionalQM],
    LazyFromView[OptionalQRM],
    LazyFromView[OptionalSW]
]"""
BatchWithMoneyConfig: TypeAlias = 'Batch[BatchView, MoneyConfigViewStrict, GT, QM, QRM, SW]'
BatchWithGroundTruth: TypeAlias = 'Batch[BatchView, MC, GroundTruthConfigViewV0Strict, QM, QRM, SW]'
BatchWithQualityManagement: TypeAlias = 'Batch[BatchView, MC, GT, QualityConfigViewV0Strict, QRM, SW]'
BatchWithQuorum: TypeAlias = 'Batch[BatchView, MC, GT, QM, QuorumConfigView, SW]'
BatchWithoutQuorum: TypeAlias = 'Batch[BatchView, MC, GT, QM, None, SW]'
BatchWithStatusWorkflow: TypeAlias = 'Batch[BatchView, MC, GT, QM, QRM, StatusWorkflowConfigViewStrict]'
BatchWithoutStatusWorkflow: TypeAlias = 'Batch[BatchView, MC, GT, QM, QRM, None]'
