from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model import (
    MetricProviderAnnotationProcessView,
)


class MetricProviderAnnotationProcessViewDataStrict(MetricProviderAnnotationProcessView):
    type: Literal['metric-provider'] = 'metric-provider'
