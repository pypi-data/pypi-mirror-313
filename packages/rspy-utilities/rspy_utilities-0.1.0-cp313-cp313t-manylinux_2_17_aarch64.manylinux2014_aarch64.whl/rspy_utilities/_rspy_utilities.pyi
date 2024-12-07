from typing import Any, Callable, Generator, Iterable, Optional, TypeVar

T = TypeVar("T")

def distinct(
    iterable: Iterable[T],
    key: Optional[Callable[[T], Any]] = None,
) -> Generator[T, None, None]: ...
