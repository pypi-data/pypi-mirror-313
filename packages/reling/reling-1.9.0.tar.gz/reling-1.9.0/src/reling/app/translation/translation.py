from itertools import starmap
from typing import Generator

from reling.db.enums import Gender
from reling.db.models import Language
from reling.gpt import GPTClient
from reling.types import DialogueExchangeData
from reling.utils.iterables import pair_items
from reling.utils.transformers import add_numbering, apply, omit_empty, remove_numbering, strip

__all__ = [
    'translate_dialogue_exchanges',
    'translate_text_sentences',
]


def translate_text_sentences(
        gpt: GPTClient,
        sentences: list[str],
        source_language: Language,
        target_language: Language,
) -> Generator[str, None, None]:
    return gpt.ask(
        '\n'.join([
            f'Translate the following text from {source_language.name} into {target_language.name}.',
            f'Generate only the specified translations without any additional text.',
            f'Number each translated sentence and place each on a new line.',
            f'---',
            *apply(add_numbering, sentences),
        ]),
        transformers=[strip, omit_empty, remove_numbering],
    )


def translate_dialogue_exchanges(
        gpt: GPTClient,
        exchanges: list[DialogueExchangeData],
        speaker_gender: Gender,
        user_gender: Gender,
        source_language: Language,
        target_language: Language,
) -> Generator[DialogueExchangeData, None, None]:
    DialogueExchangeData.assert_speaker_comes_first()
    return iter(starmap(DialogueExchangeData, pair_items(gpt.ask(
        '\n'.join([
            f'Translate the following dialogue between {speaker_gender.describe()} and {user_gender.describe()} '
            f'from {source_language.name} into {target_language.name}'
            f'{f' ({speaker_gender.describe()} speaks in the odd-numbered sentences,'
               f' and {user_gender.describe()} responds in the even-numbered sentences)'
               if speaker_gender != user_gender
               else ''}'
            f'.',

            f'Generate only the specified translations without any additional text.',
            f'Number each translated sentence and place each on a new line.',
            f'---',
            *apply(add_numbering, [turn for exchange in exchanges for turn in exchange.all()]),
        ]),
        transformers=[strip, omit_empty, remove_numbering],
    ))))
