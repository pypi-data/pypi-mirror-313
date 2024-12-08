from __future__ import annotations
from abc import ABC, abstractmethod

from reling.types import Reader, Speed
from .voices import Voice

__all__ = [
    'TTSClient',
    'TTSVoiceClient',
]


class TTSClient(ABC):
    @abstractmethod
    def read(self, text: str, voice: Voice, speed: Speed) -> None:
        """Read the text in real time using the specified voice."""
        pass

    def with_voice(self, voice: Voice) -> TTSVoiceClient:
        return TTSVoiceClient(self, voice)


class TTSVoiceClient:
    """A wrapper around TTSClient with a specific voice."""
    _tts: TTSClient
    _voice: Voice

    def __init__(self, tts: TTSClient, voice: Voice) -> None:
        self._tts = tts
        self._voice = voice

    def get_reader(self, text: str) -> Reader:
        def read(speed: Speed) -> None:
            self._tts.read(text, self._voice, speed)
        return read
