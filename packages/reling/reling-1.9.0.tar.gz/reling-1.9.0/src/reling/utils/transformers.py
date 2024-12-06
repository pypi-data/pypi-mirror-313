import re
from typing import Callable, Iterable, Generator

from .strings import universal_normalize

__all__ = [
    'add_numbering',
    'apply',
    'get_numbering_prefix',
    'normalize',
    'omit_empty',
    'remove_numbering',
    'slugify',
    'strip',
    'Transformer',
]

type Transformer = Callable[[str, int], str | None]
# The second argument is the index of the item in the list.


def apply(transformer: Transformer, items: Iterable[str]) -> Generator[str, None, None]:
    for index, item in enumerate(items):
        yield transformer(item, index)


def get_numbering_prefix(index: int) -> str:
    return f'{index + 1}. '


def add_numbering(text: str, index: int) -> str:
    return f'{get_numbering_prefix(index)}{text}'


def remove_numbering(text: str, _: int) -> str:
    return re.sub(r'^\s*\d+[.)]\s+', '', text)


def strip(text: str, _: int) -> str:
    return text.strip()


def omit_empty(text: str, _: int) -> str | None:
    return text or None


def slugify(text: str, _: int) -> str:
    return re.sub(r'[^\w-]', '', re.sub(r'\s+', '-', text.lower().strip()))


def normalize(text: str, _: int) -> str:
    return universal_normalize(text)
