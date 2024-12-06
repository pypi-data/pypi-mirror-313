from typing import Iterable, Optional, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")


def common_prefix_length(list1: list, list2: list):
    i = 0
    while i < len(list1) and i < len(list2) and list1[i] == list2[i]:
        i += 1
    return i


def or_false(value: Optional[bool]) -> bool:
    return or_default(value, False)


def or_true(value: Optional[bool]) -> bool:
    return or_default(value, True)


def or_default(value: Optional[T], default_value: T) -> T:
    return value if value is not None else default_value
