from dataclasses import dataclass
from typing import Literal, NewType, get_args

from typing_extensions import TypeIs

AnnotationStudioProductionEnvironment = Literal[
    'bat',
    'bee',
    'cat',
    'demo',
    'duck',
    'frog',
    'indri',
    'jerboa',
    'ladybug',
    'lion',
    'lynx',
    'reindeer',
    'sole',
    'swan',
    'toad',
    'toucan',
    'unicorn',
]
AnnotationStudioTestEnvironment = Literal[
    'staging',
    'prestable',
    'regress-release',
]

AnnotationStudioEnvironment = Literal[
    AnnotationStudioProductionEnvironment,
    AnnotationStudioTestEnvironment,
]
ExpertsPortalEnvironment = Literal['production', 'prestable', 'regress-release']
FunctionsEnvironment = Literal['production', 'prestable', 'regress-release']


def is_production_preset_a9s_environment(
    environment: AnnotationStudioEnvironment,
) -> TypeIs[AnnotationStudioProductionEnvironment]:
    return environment in get_args(AnnotationStudioProductionEnvironment)


@dataclass
class EnvironmentSpec:
    annotation_studio: AnnotationStudioEnvironment
    experts_portal: ExpertsPortalEnvironment
    functions_environment: FunctionsEnvironment


GlobalEnvironment = Literal[
    'bat',
    'bee',
    'cat',
    'demo',
    'duck',
    'frog',
    'indri',
    'jerboa',
    'ladybug',
    'lion',
    'lynx',
    'reindeer',
    'sole',
    'swan',
    'toad',
    'toucan',
    'unicorn',
    # test environments
    'staging',
    'prestable',
    'regress-release',
]

BaseUrl = NewType('BaseUrl', str)


@dataclass
class CustomEnvironment:
    a9s_base_url: BaseUrl
    experts_portal_base_url: BaseUrl
    functions_base_url: BaseUrl

    @classmethod
    def default(cls, a9s_base_url: str) -> 'CustomEnvironment':
        return cls(
            a9s_base_url=BaseUrl(a9s_base_url),
            experts_portal_base_url=BaseUrl('https://experts-portal.toloka.ai'),
            functions_base_url=BaseUrl('https://functions.a9s.toloka.ai'),
        )
