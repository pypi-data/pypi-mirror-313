from typing import Awaitable, Callable, Generic, TypeVar

from typing_extensions import ParamSpec, TypedDict, Unpack

from toloka.a9s.client.client import AsyncKit


class EntityApiBaseParams(TypedDict):
    kit: AsyncKit


class EntityApiBase:
    kit: AsyncKit

    def __init__(self, **kwargs: Unpack[EntityApiBaseParams]) -> None:
        self.kit = kwargs['kit']


P = ParamSpec('P')
ValueType = TypeVar('ValueType')


class LazyValue(Generic[P, ValueType]):
    def __init__(self, callback: Callable[P, Awaitable[ValueType]]) -> None:
        self.callback = callback

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> ValueType:
        return await self.callback(*args, **kwargs)
