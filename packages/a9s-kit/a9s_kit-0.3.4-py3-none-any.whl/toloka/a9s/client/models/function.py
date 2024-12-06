# pyright: reportGeneralTypeIssues=false


from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.functions.web.v0 import FunctionForm, FunctionViewV0


class FunctionFormStrict(FunctionForm):
    signature: Literal['SIMILARITY', 'AGGREGATION']


class FunctionViewV0Strict(FunctionViewV0):
    id: str
    created_at: str
    created_by: str
    name: str
    code: str
    signature: Literal['SIMILARITY', 'AGGREGATION']
