import logging

from typing_extensions import Self, Unpack

from toloka.a9s.client.base.client import AsyncBaseQMSClient
from toloka.a9s.client.base.types import AnnotationStudioEnvironment, BaseUrl
from toloka.a9s.client.client.experimental.quality_management.async_config import AsyncQmsAsyncQualityConfigClient
from toloka.a9s.client.client.experimental.quality_management.config import AsyncQmsQualityConfigClient
from toloka.a9s.client.client.experimental.quality_management.restriction import AsyncQmsRestrictionClient
from toloka.common.http.args import BaseHttpClientNotRequiredArgs
from toloka.common.http.client import AsyncHttpClient

logger = logging.getLogger(__name__)


class AsyncQmsClient(AsyncBaseQMSClient):
    restriction: AsyncQmsRestrictionClient
    quality_config: AsyncQmsQualityConfigClient
    async_quality_config: AsyncQmsAsyncQualityConfigClient

    def __init__(self, transport: AsyncHttpClient):
        super().__init__(transport)
        self.restriction = AsyncQmsRestrictionClient(transport)
        self.quality_config = AsyncQmsQualityConfigClient(transport)
        self.async_quality_config = AsyncQmsAsyncQualityConfigClient(transport)

    @classmethod
    def from_credentials(
        cls,
        environment: AnnotationStudioEnvironment | BaseUrl,
        api_key: str,
        **kwargs: Unpack[BaseHttpClientNotRequiredArgs],
    ) -> Self:
        if cls.is_preset(environment):
            base_url = AsyncBaseQMSClient.environment_to_url(environment=environment)
        else:
            base_url = environment
        return cls(
            transport=AsyncHttpClient.from_api_key(
                base_url=base_url,
                api_key=api_key,
                **kwargs,
            )
        )
