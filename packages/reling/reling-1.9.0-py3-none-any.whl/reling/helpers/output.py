from __future__ import annotations
from dataclasses import dataclass
from typing import cast

from rich.console import Console
from rich.text import Text

from reling.tts import TTSVoiceClient
from reling.types import Reader, Speed
from reling.utils.console import clear_current_line
from reling.utils.prompts import enter_to_continue, Prompt, PromptOption
from reling.utils.values import coalesce, ensure_not_none
from .colors import fade

__all__ = [
    'output',
    'SentenceData',
]

NA = fade('N/A')

PROMPT_TITLE = 'Play'
NORMAL_SPEED = 'normal speed'
SLOWLY = 'slowly'
REPLAY = 'replay'


@dataclass
class SentenceData:
    print_text: str | Text | None = None
    print_prefix: str | Text | None = None
    reader: Reader | None = None
    reader_id: str | None = None

    @staticmethod
    def from_tts(
            text: str | None,
            client: TTSVoiceClient | None,
            *,
            print_text: str | Text | None = None,
            print_prefix: str | Text | None = None,
            reader_id: str | None = None,
    ) -> SentenceData:
        return SentenceData(
            print_text=coalesce(print_text, text),
            print_prefix=print_prefix,
            reader=client.get_reader(text) if client and (text is not None) else None,
            reader_id=reader_id,
        )


@dataclass
class ReaderWithSpeed:
    reader: Reader
    speed: Speed


@dataclass
class ReaderWithId:
    reader: Reader
    id: str


def add_single_sentence_options(prompt: Prompt[ReaderWithSpeed], reader: Reader) -> None:
    """Attach the options for a single sentence to the prompt: '[n]ormal speed | [s]lowly'."""
    prompt.add_option(PromptOption(
        description=NORMAL_SPEED,
        action=ReaderWithSpeed(reader, Speed.NORMAL),
    ))
    prompt.add_option(PromptOption(
        description=SLOWLY,
        action=ReaderWithSpeed(reader, Speed.SLOW),
    ))


def add_multi_sentence_options(prompt: Prompt[ReaderWithSpeed], readers: list[ReaderWithId]) -> None:
    """Attach the options for multiple sentences to the prompt: '[i]mproved | [is] | [o]riginal | [os]'."""
    for reader in readers:
        prompt.add_option(PromptOption(
            description=reader.id,
            action=ReaderWithSpeed(reader.reader, Speed.NORMAL),
            modifiers={
                SLOWLY: ReaderWithSpeed(reader.reader, Speed.SLOW),
            },
        ))


def construct_prompt(
        sentences_with_readers: list[SentenceData],
        current: ReaderWithSpeed | None,
        multi_sentence: bool,
) -> Prompt:
    """
    Construct a prompt for the user to choose the next sentence to read and the speed of the reading.
    :raises ValueError: If reader_id is not provided for a sentence with a reader in a multi-sentence output.
    """
    prompt = Prompt(PROMPT_TITLE)
    if multi_sentence:
        add_multi_sentence_options(prompt, [
            ReaderWithId(
                reader=ensure_not_none(sentence.reader),
                id=ensure_not_none(sentence.reader_id),
            )
            for sentence in sentences_with_readers
        ])
    else:
        add_single_sentence_options(prompt, sentences_with_readers[0].reader)
    if current:
        prompt.add_option(PromptOption(
            description=REPLAY,
            action=current,
        ))
    return prompt


def output(*sentences: SentenceData) -> None:
    """
    Output the sentences, reading them if a reader is provided.
    If multiple readers are provided, the user can choose which sentence to read next.
    The user can also choose the speed of the reading.

    :raises ValueError: If reader_id is not provided for a sentence with a reader in a multi-sentence output.
    """
    console = Console(highlight=False)
    for sentence in sentences:
        console.print(sentence.print_prefix or '', end='')
        console.print(coalesce(sentence.print_text, cast(str | Text, NA)))
    multi_sentence = len(sentences) > 1
    if sentences_with_readers := [sentence for sentence in sentences if sentence.reader]:
        current = ReaderWithSpeed(sentences_with_readers[0].reader, Speed.NORMAL) if len(sentences) == 1 else None
        while True:
            if current:
                try:
                    current.reader(current.speed)
                except KeyboardInterrupt:
                    pass
                clear_current_line()  # Otherwise the input made during the reading will get displayed twice
            current = construct_prompt(sentences_with_readers, current, multi_sentence).prompt()
            if not current:
                break
    elif multi_sentence:
        enter_to_continue()
