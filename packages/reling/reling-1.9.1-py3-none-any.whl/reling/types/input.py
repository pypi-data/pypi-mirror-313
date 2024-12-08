from dataclasses import dataclass
from pathlib import Path

__all__ = [
    'Input',
]


@dataclass
class Input:
    text: str
    audio: Path | None = None

    def __init__(self, text: str, audio: Path | None = None) -> None:
        self.text = text.strip()
        self.audio = audio
