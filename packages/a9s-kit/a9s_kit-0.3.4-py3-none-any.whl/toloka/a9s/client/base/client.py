from abc import abstractmethod
from copy import copy
from typing import ClassVar, Generic, TypeVar

from typing_extensions import LiteralString, Self, TypeIs, Unpack, assert_never

from toloka.a9s.client.base.converter import (
    is_preset_a9s_environment,
    is_preset_experts_portal_environment,
    is_preset_functions_environment,
)
from toloka.a9s.client.base.exception import wrap_async_http_status_exception
from toloka.a9s.client.base.types import (
    AnnotationStudioEnvironment,
    BaseUrl,
    ExpertsPortalEnvironment,
    FunctionsEnvironment,
    is_production_preset_a9s_environment,
)
from toloka.common.http.args import BaseHttpClientNotRequiredArgs
from toloka.common.http.client import AsyncHttpClient

EnvironmentType = TypeVar('EnvironmentType', bound=LiteralString)


class AsyncBaseClient(Generic[EnvironmentType]):
    V1_PREFIX: ClassVar[str] = '/api/v1'
    V0_PREFIX: ClassVar[str] = '/api/v0'
    UI_API_PREFIX: ClassVar[str] = '/api'

    @classmethod
    def from_credentials(
        cls,
        environment: BaseUrl | EnvironmentType,
        api_key: str,
        **kwargs: Unpack[BaseHttpClientNotRequiredArgs],
    ) -> Self:
        if cls.is_preset(environment):
            base_url = cls.environment_to_url(environment)
        return cls(
            transport=AsyncHttpClient.from_api_key(
                base_url=base_url,
                api_key=api_key,
                **kwargs,
            ),
        )

    def __init__(self, transport: AsyncHttpClient) -> None:
        self.client = copy(transport)  # as we are going to patch some methods
        self.client.make_request = wrap_async_http_status_exception(self.client.make_request)  # type: ignore[method-assign]  # noqa: E501
        self.client.make_retriable_request = wrap_async_http_status_exception(self.client.make_retriable_request)  # type: ignore[method-assign]  # noqa: E501

    @staticmethod
    @abstractmethod
    def is_preset(environment: EnvironmentType | BaseUrl) -> TypeIs[EnvironmentType]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def environment_to_url(environment: EnvironmentType) -> BaseUrl:
        raise NotImplementedError


class AsyncBaseAnnotationStudioClient(AsyncBaseClient[AnnotationStudioEnvironment]):
    @staticmethod
    def is_preset(environment: AnnotationStudioEnvironment | BaseUrl) -> TypeIs[AnnotationStudioEnvironment]:
        return is_preset_a9s_environment(environment)

    @staticmethod
    def environment_to_url(environment: AnnotationStudioEnvironment) -> BaseUrl:
        if is_production_preset_a9s_environment(environment):
            return BaseUrl(f'https://{environment}.a9s.toloka.ai')
        elif environment == 'regress-release' or environment == 'prestable' or environment == 'staging':
            return BaseUrl(f'https://{environment}.a9s.toloka-test.ai')
        else:
            assert_never(environment)


class AsyncBaseQMSClient(AsyncBaseClient[AnnotationStudioEnvironment]):
    @staticmethod
    def is_preset(environment: AnnotationStudioEnvironment | BaseUrl) -> TypeIs[AnnotationStudioEnvironment]:
        return is_preset_a9s_environment(environment)

    @staticmethod
    def environment_to_url(environment: AnnotationStudioEnvironment) -> BaseUrl:
        if is_production_preset_a9s_environment(environment):
            return BaseUrl('https://qms.a9s.toloka.ai')
        elif environment == 'regress-release' or environment == 'prestable' or environment == 'staging':
            return BaseUrl(f'https://{environment}.a9s.toloka-test.ai')
        else:
            assert_never(environment)


class AsyncBaseExpertsPortalClient(AsyncBaseClient[ExpertsPortalEnvironment]):
    @staticmethod
    def is_preset(environment: ExpertsPortalEnvironment | BaseUrl) -> TypeIs[ExpertsPortalEnvironment]:
        return is_preset_experts_portal_environment(environment)

    @staticmethod
    def environment_to_url(environment: ExpertsPortalEnvironment) -> BaseUrl:
        match environment:
            case 'production':
                return BaseUrl('https://experts-portal.toloka.ai')
            case 'prestable' | 'regress-release':
                return BaseUrl(f'https://{environment}.experts-portal.toloka-test.ai')
            case _:
                assert_never(environment)


class AsyncBaseFunctionsClient(AsyncBaseClient[FunctionsEnvironment]):
    @staticmethod
    def is_preset(environment: FunctionsEnvironment | BaseUrl) -> TypeIs[FunctionsEnvironment]:
        return is_preset_functions_environment(environment)

    @staticmethod
    def environment_to_url(environment: FunctionsEnvironment) -> BaseUrl:
        match environment:
            case 'production':
                return BaseUrl('https://functions.a9s.toloka.ai')
            case 'regress-release' | 'prestable':
                return BaseUrl(f'https://{environment}.a9s.toloka-test.ai')
            case _:
                assert_never(environment)
