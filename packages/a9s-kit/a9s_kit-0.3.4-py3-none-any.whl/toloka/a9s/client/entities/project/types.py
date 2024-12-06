from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from typing_extensions import TypeVar

from toloka.a9s.client.models.annotation_process.status_workflow import StatusWorkflowConfigViewStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.view import (
    QuorumConfigView,
)

if TYPE_CHECKING:
    from toloka.a9s.client.entities.project import Project

from toloka.a9s.client.entities.base import LazyValue
from toloka.a9s.client.models.ground_truth import GroundTruthConfigViewV0Strict
from toloka.a9s.client.models.money_config import MoneyConfigViewStrict
from toloka.a9s.client.models.project import ProjectViewV1Strict
from toloka.a9s.client.models.quality_management.config import QualityConfigViewV0Strict
from toloka.a9s.client.models.types import ProjectId

LazyType = TypeVar('LazyType')
LazyFromId = LazyValue[[ProjectId], LazyType]
LazyFromView = LazyValue[[ProjectViewV1Strict], LazyType]
ProjectView = TypeVar(
    'ProjectView',
    bound=ProjectViewV1Strict | LazyFromId[ProjectViewV1Strict],
    covariant=True,
    default=ProjectViewV1Strict | LazyFromId[ProjectViewV1Strict],
)
OptionalMC = MoneyConfigViewStrict | None
MC = TypeVar(
    'MC',
    bound=OptionalMC | LazyFromView[OptionalMC],
    covariant=True,
    default=OptionalMC | LazyFromView[OptionalMC],
)
OptionalGT = GroundTruthConfigViewV0Strict | None
GT = TypeVar(
    'GT',
    bound=OptionalGT | LazyFromView[OptionalGT],
    covariant=True,
    default=OptionalGT | LazyFromView[OptionalGT],
)
OptionalQM = QualityConfigViewV0Strict | None
QM = TypeVar(
    'QM',
    bound=OptionalQM | LazyFromView[OptionalQM],
    covariant=True,
    default=OptionalQM | LazyFromView[OptionalQM],
)
OptionalQRM = QuorumConfigView | None
QRM = TypeVar(
    'QRM',
    bound=OptionalQRM | LazyFromId[OptionalQRM],
    covariant=True,
    default=OptionalQRM | LazyFromId[OptionalQRM],
)
OptionalSW = StatusWorkflowConfigViewStrict | None
SW = TypeVar(
    'SW',
    bound=OptionalSW | LazyFromId[OptionalSW],
    covariant=True,
    default=OptionalSW | LazyFromId[OptionalSW],
)

ProjectAnyEager: TypeAlias = """
Project[
    ProjectViewV1Strict,
    OptionalMC,
    OptionalGT,
    OptionalQM,
    OptionalQRM,
    OptionalSW
]
"""
ProjectAnyLazy: TypeAlias = """
Project[
    LazyFromId[ProjectViewV1Strict],
    LazyFromView[OptionalMC],
    LazyFromView[OptionalGT],
    LazyFromView[OptionalQM],
    LazyFromId[OptionalQRM],
    LazyFromId[OptionalSW]
]
"""
ProjectWithMoneyConfig: TypeAlias = 'Project[ProjectView, MoneyConfigViewStrict, GT, QM, QRM, SW]'
ProjectWithGroundTruth: TypeAlias = 'Project[ProjectView, MC, GroundTruthConfigViewV0Strict, QM, QRM, SW]'
ProjectWithQualityManagement: TypeAlias = 'Project[ProjectView, MC, GT, QualityConfigViewV0Strict, QRM, SW]'
