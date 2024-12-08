from math import floor
from statistics import mean

from lcs2 import diff, lcs_length

from reling.app.config import MAX_SCORE
from reling.utils.strings import tokenize

__all__ = [
    'calculate_diff_score',
    'format_average_score',
]


def format_average_score(scores: list[int]) -> str:
    return f'{mean(scores):.1f}'


def calculate_char_diff_score(a: str, b: str) -> int:
    """Return the score based on the longest common subsequence of two strings."""
    if a == b:  # Avoid division by zero
        return MAX_SCORE
    return floor(lcs_length(a, b) / max(len(a), len(b)) * MAX_SCORE)


def calculate_mistake_score(mistakes: int) -> int:
    """Return the score based on the number of mistakes."""
    return floor(MAX_SCORE * ((1 - 1 / MAX_SCORE) ** mistakes))


def calculate_word_diff_score(a: str, b: str) -> int:
    """Return the score based on the diff between two strings tokenized into lowercase words."""
    a_words, b_words = ([word.lower() for word in tokenize(sentence, words_only=True)] for sentence in (a, b))
    a_diff: list[str] = []
    b_diff: list[str] = []
    mistakes = 0
    for a_tokens, b_tokens in diff(a_words, b_words):
        mistakes += max(len(a_tokens), len(b_tokens))
        a_diff.extend(a_tokens)
        b_diff.extend(b_tokens)
    mistakes -= lcs_length(a_diff, b_diff)
    return calculate_mistake_score(mistakes)


def calculate_diff_score(a: str, b: str) -> int:
    """Return the score based on the diff between two strings."""
    return min(
        calculate_char_diff_score(a, b),
        calculate_word_diff_score(a, b),
    )
