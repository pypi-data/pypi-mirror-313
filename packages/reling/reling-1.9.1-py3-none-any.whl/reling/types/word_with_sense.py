from dataclasses import dataclass
from typing import Self

__all__ = [
    'WordWithSense',
]


@dataclass
class WordWithSense:
    word: str
    sense: str | None

    DELIMITER_WITH_WHITE_SPACE = ': '

    @classmethod
    def parse(cls, text: str) -> Self:
        """
        Parse the word and sense from the given string:
        "word: sense" -> WordWithSense("word", "sense")
        "word" -> WordWithSense("word", None)
        """
        delimiter = cls.DELIMITER_WITH_WHITE_SPACE.strip()
        if delimiter in text:
            word, sense = text.split(delimiter, 1)
            return cls(word.strip(), sense.strip())
        else:
            return cls(text.strip(), None)

    def format(self) -> str:
        return f'"{self.word}"' + (f' ({self.sense})' if self.sense else '')
