from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model import (
    PostAcceptanceAnnotationProcessView,
)


class PostAcceptanceAnnotationProcessViewDataStrict(PostAcceptanceAnnotationProcessView):
    type: Literal['post-acceptance'] = 'post-acceptance'
