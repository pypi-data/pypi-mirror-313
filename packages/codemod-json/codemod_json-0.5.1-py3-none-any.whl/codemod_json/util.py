from typing import Iterable, TypeVar

T = TypeVar("T")


def marklast(it: Iterable[T]) -> Iterable[tuple[T, bool]]:
    lst = list(it)
    for i, x in enumerate(lst):
        if i == (len(lst) - 1):
            yield x, True
        else:
            yield x, False
