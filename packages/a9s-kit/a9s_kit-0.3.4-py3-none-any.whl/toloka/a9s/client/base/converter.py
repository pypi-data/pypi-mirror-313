from typing import get_args

from pydantic import BaseModel, TypeAdapter
from typing_extensions import TypeIs

from toloka.a9s.client.base.types import (
    AnnotationStudioEnvironment,
    ExpertsPortalEnvironment,
    FunctionsEnvironment,
)
from toloka.common.http.client import QueryParam

_QUERY_TYPE_ADAPTER: TypeAdapter[QueryParam] = TypeAdapter(QueryParam)


def model_to_query_params(model: BaseModel) -> QueryParam:
    return _QUERY_TYPE_ADAPTER.validate_python(model.model_dump(mode='json', exclude_none=True))


def is_preset_a9s_environment(
    environment: str,
) -> TypeIs[AnnotationStudioEnvironment]:
    return isinstance(environment, str) and environment in get_args(AnnotationStudioEnvironment)


def is_preset_experts_portal_environment(
    environment: str,
) -> TypeIs[ExpertsPortalEnvironment]:
    return isinstance(environment, str) and environment in get_args(ExpertsPortalEnvironment)


def is_preset_functions_environment(
    environment: str,
) -> TypeIs[FunctionsEnvironment]:
    return isinstance(environment, str) and environment in get_args(FunctionsEnvironment)
