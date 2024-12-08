from dataclasses import dataclass

__all__ = [
    'DialogueExchangeData',
]


@dataclass
class DialogueExchangeData:
    speaker: str
    user: str

    @staticmethod
    def assert_speaker_comes_first() -> None:
        pass

    def all(self) -> tuple[str, str]:
        return self.speaker, self.user
