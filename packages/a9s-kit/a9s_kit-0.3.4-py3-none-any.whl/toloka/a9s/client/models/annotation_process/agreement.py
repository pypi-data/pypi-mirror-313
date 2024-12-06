from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model import AgreementAnnotationProcessView


class AgreementAnnotationProcessViewDataStrict(AgreementAnnotationProcessView):
    type: Literal['agreement'] = 'agreement'
