# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Any, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

from toloka.a9s.client.models.extension_id import ExtensionId
from toloka.a9s.client.models.generated.ai.toloka.a9s.project.web.v1.form import ProjectFormV1
from toloka.a9s.client.models.generated.ai.toloka.a9s.project.web.v1.view import ListProjectViewV1, ProjectViewV1
from toloka.a9s.client.models.generated.ai.toloka.a9s.project.web.v1.viewform import (
    ProjectExtensionInstanceConfigViewFormV1,
    ProjectExtensionsViewFormV1,
    SpecificationViewFormV1,
)
from toloka.a9s.client.models.types import ProjectId
from toloka.a9s.client.models.utils import none_default_validator


class ProjectExtensionInstanceConfigViewFormV1Strict(ProjectExtensionInstanceConfigViewFormV1):
    extension_id: ExtensionId
    instance_id: str


class ProjectExtensionsViewFormV1Strict(ProjectExtensionsViewFormV1):
    instances: Annotated[
        Sequence[ProjectExtensionInstanceConfigViewFormV1Strict],
        Field(max_length=100, min_length=0, default_factory=list),
        none_default_validator(default_factory=list),
    ]


class TemplateBuilderConfig(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
    )

    config: Mapping[str, Any]


class TemplateBuilderConfigState(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
    )

    config_state: Annotated[TemplateBuilderConfig, Field(alias='configState')]
    input_example: Annotated[Mapping[str, Any] | None, Field(alias='inputExample')] = None


class SpecificationViewFormV1Strict(SpecificationViewFormV1):
    type: str = 'LEGACY_TEMPLATE_BUILDER'
    view: TemplateBuilderConfigState
    input: Mapping[str, Any] | SerializeAsAny[BaseModel]
    output: Mapping[str, Any] | SerializeAsAny[BaseModel]


class ProjectViewV1Strict(ProjectViewV1):
    id: ProjectId
    name: str
    specification: SpecificationViewFormV1Strict
    extensions: Annotated[
        ProjectExtensionsViewFormV1Strict,
        Field(default_factory=ProjectExtensionsViewFormV1Strict),
        none_default_validator(default_factory=ProjectExtensionsViewFormV1Strict),
    ]
    tags: Annotated[
        Sequence[str],
        none_default_validator(default_factory=list),
    ]


class ListProjectViewV1Strict(ListProjectViewV1):
    data: Sequence[ProjectViewV1Strict]
    has_more: bool


class ProjectFormV1Strict(ProjectFormV1):
    specification: SpecificationViewFormV1Strict
    extensions: Annotated[
        ProjectExtensionsViewFormV1Strict,
        Field(default_factory=ProjectExtensionsViewFormV1Strict),
        none_default_validator(default_factory=ProjectExtensionsViewFormV1Strict),
    ]
    tags: Annotated[
        Sequence[str],
        Field(max_length=100, min_length=0),
        none_default_validator(default_factory=list),
    ]

    @classmethod
    def from_view(cls, view: ProjectViewV1Strict) -> 'ProjectFormV1Strict':
        return cls.model_validate(view, from_attributes=True)

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags = list(self.tags) + [tag]
