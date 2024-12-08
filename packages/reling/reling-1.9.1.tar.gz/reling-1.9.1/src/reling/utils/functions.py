from typing import Callable

__all__ = [
    'name_function',
    'named_function',
]


def name_function[T: Callable](function: T, name: str) -> T:
    """Set the name of a function."""
    function.__name__ = name
    return function


def named_function[T: Callable](name: str) -> Callable[[T], T]:
    """Decorator to set the name of a function."""
    return lambda function: name_function(function, name)
