from pydantic import BaseModel

from toloka.a9s.client.models.project import ProjectViewV1Strict
from toloka.a9s.client.models.quality_management.async_config import AsyncQualityConfigViewV0Strict
from toloka.a9s.client.models.quality_management.config import QualityConfigViewV0Strict


class AddFastResponsesBanForProjectResult(BaseModel):
    project: ProjectViewV1Strict
    quality_config: QualityConfigViewV0Strict
    async_quality_config: AsyncQualityConfigViewV0Strict
