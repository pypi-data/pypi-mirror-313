from dataclasses import dataclass

from reling.types import DialogueExchangeData, Input

__all__ = [
    'ExchangeWithTranslation',
    'PreScoreWithSuggestion',
    'ScoreWithSuggestion',
    'SentenceWithTranslation',
]


@dataclass
class SentenceWithTranslation:
    sentence: str
    translation: Input


@dataclass
class ExchangeWithTranslation:
    exchange: DialogueExchangeData
    user_translation: Input


@dataclass
class PreScoreWithSuggestion:
    score: int
    suggestion: str | None


@dataclass
class ScoreWithSuggestion:
    score: int
    suggestion: str | None
