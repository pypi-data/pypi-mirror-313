from typing import Any, AsyncGenerator, Awaitable, Callable, Protocol, Sequence, TypeVar

T = TypeVar('T', covariant=True)


class Page(Protocol[T]):
    @property
    def has_more(self) -> bool: ...

    @property
    def data(self) -> Sequence[T]: ...


PageType = TypeVar('PageType', bound=Page[Any])


async def async_paginate(
    get_next_page: Callable[[PageType | None], Awaitable[PageType]],
) -> AsyncGenerator[T, None]:
    current_page = await get_next_page(None)
    while current_page is not None and current_page.has_more:
        for item in current_page.data:
            yield item
        current_page = await get_next_page(current_page)
    for item in current_page.data:
        yield item
