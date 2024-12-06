from typing import Literal, Mapping

from typing_extensions import assert_never

SortValue = Literal['asc', 'desc'] | None


def _direction_to_prefix(direction: Literal['asc', 'desc']) -> str:
    match direction:
        case 'asc':
            return ''
        case 'desc':
            return '-'
        case _:
            assert_never(direction)


def to_sort_string(sort_values: Mapping[str, SortValue]) -> str:
    return ','.join(
        _direction_to_prefix(sv_value) + sv_key for sv_key, sv_value in sort_values.items() if sv_value is not None
    )


def from_sort_string(sort_string: str) -> dict[str, SortValue]:
    result: dict[str, SortValue] = {}
    for item in sort_string.split(','):
        if item.startswith('-'):
            result[item[1:]] = 'desc'
        else:
            result[item] = 'asc'
    return result
