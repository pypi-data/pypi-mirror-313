from typing import Callable

__all__ = [
    'Promise',
]

type Promise[T] = Callable[[], T]
