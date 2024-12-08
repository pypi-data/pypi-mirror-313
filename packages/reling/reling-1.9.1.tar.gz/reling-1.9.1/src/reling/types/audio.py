from enum import Enum
from pathlib import Path
from typing import Callable

__all__ = [
    'Reader',
    'Speed',
    'Transcriber',
]


class Speed(Enum):
    SLOW = 0.5
    NORMAL = 1.0


type Reader = Callable[[Speed], None]
type Transcriber = Callable[[Path], str]
