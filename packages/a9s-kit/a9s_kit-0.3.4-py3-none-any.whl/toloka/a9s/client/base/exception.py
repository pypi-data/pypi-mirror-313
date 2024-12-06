import json
from functools import wraps
from json import JSONDecodeError
from typing import Any, Awaitable, Callable, TypeVar, cast

from httpx import HTTPStatusError
from pydantic import ConfigDict, TypeAdapter, ValidationError
from pydantic.dataclasses import dataclass

F = TypeVar('F', bound=Callable[..., Awaitable[Any]])


@dataclass(config=ConfigDict(extra='allow'))
class AnnotationStudioError(Exception):
    type: str
    title: str
    status: int
    detail: str
    instance: str
    request_id: str
    timestamp: str

    def __str__(self) -> str:
        # TypeAdapter does not preserve extra fields
        # https://github.com/pydantic/pydantic/issues/9645
        return json.dumps(self.__dict__, indent=2)


A9S_ERROR_TYPE_ADAPTER = TypeAdapter(AnnotationStudioError)


class UnexpectedAnnotationStudioError(Exception):
    pass


def wrap_async_http_status_exception(f: F) -> F:
    @wraps(f)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await f(*args, **kwargs)
        except HTTPStatusError as e:
            try:
                raise A9S_ERROR_TYPE_ADAPTER.validate_json(e.response.text)
            except ValidationError:
                try:
                    response_text = json.dumps(e.response.json(), indent=2)
                except JSONDecodeError:
                    response_text = e.response.text
                raise UnexpectedAnnotationStudioError(response_text)

    return cast(F, wrapper)
