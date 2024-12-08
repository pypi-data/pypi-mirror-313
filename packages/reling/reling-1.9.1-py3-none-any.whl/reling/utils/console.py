from contextlib import contextmanager
from typing import Generator

from .strings import universal_normalize

__all__ = [
    'clear_current_line',
    'clear_previous',
    'erase_previous',
    'input_and_erase',
    'interruptible_input',
    'print_and_erase',
]


def clear_current_line() -> None:
    print('\033[2K', end='\r')


def clear_previous(lines: int = 1) -> None:
    print('\033[F\033[K' * lines, end='\r')


def erase_previous(text: str, include_extra_line: bool = True) -> None:
    clear_current_line()
    clear_previous(text.count('\n') + (1 if include_extra_line else 0))


def interruptible_input(prompt: str) -> str:
    try:
        return universal_normalize(input(prompt))
    except KeyboardInterrupt:
        erase_previous(prompt, include_extra_line=False)
        raise


def input_and_erase(prompt: str) -> str:
    data = interruptible_input(prompt)
    erase_previous(prompt)
    return data


@contextmanager
def print_and_erase(text: str) -> Generator[None, None, None]:
    print(text)
    yield
    erase_previous(text)
