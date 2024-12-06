from itertools import zip_longest
from pathlib import Path
from typing import Callable, Generator, Iterable

from reling.asr import ASRClient
from reling.db.models import Language
from reling.helpers.input import get_input, ScannerParams, TranscriberParams
from reling.helpers.output import output, SentenceData
from reling.scanner import Scanner
from reling.tts import TTSVoiceClient
from reling.types import DialogueExchangeData
from reling.utils.transformers import get_numbering_prefix
from .types import ExchangeWithTranslation, SentenceWithTranslation

__all__ = [
    'collect_dialogue_translations',
    'collect_text_translations',
]

HIDDEN_TEXT = '(...)'
TRANSLATION_PROMPT = 'Translation: '


def collect_text_translations(
        sentences: Iterable[str],
        target_language: Language,
        source_tts: TTSVoiceClient | None,
        asr: ASRClient | None,
        scanner: Scanner | None,
        hide_prompts: bool,
        storage: Path,
        on_pause: Callable[[], None],
        on_resume: Callable[[], None],
) -> Generator[SentenceWithTranslation, None, None]:
    """Collect the translations of text sentences."""
    collected: list[str] = []
    for index, sentence in enumerate(sentences):
        output(SentenceData.from_tts(
            sentence,
            source_tts,
            print_text=HIDDEN_TEXT if hide_prompts else None,
            print_prefix=get_numbering_prefix(index),
        ))
        translation = get_input(
            on_pause=on_pause,
            on_resume=on_resume,
            prompt=TRANSLATION_PROMPT,
            transcriber_params=TranscriberParams(
                transcribe=asr.get_transcriber(target_language, '\n'.join(collected)),
                storage=storage,
            ) if asr else None,
            scanner_params=ScannerParams(
                scanner=scanner,
                language=target_language,
            ) if scanner else None,
        )
        collected.append(translation.text)
        yield SentenceWithTranslation(sentence, translation)
        print()


def collect_dialogue_translations(
        exchanges: Iterable[DialogueExchangeData],
        original_translations: Iterable[DialogueExchangeData],
        target_language: Language,
        source_user_tts: TTSVoiceClient | None,
        target_speaker_tts: TTSVoiceClient | None,
        asr: ASRClient | None,
        scanner: Scanner | None,
        hide_prompts: bool,
        storage: Path,
        on_pause: Callable[[], None],
        on_resume: Callable[[], None],
) -> Generator[ExchangeWithTranslation, None, None]:
    """Collect the translations of user turns in a dialogue."""
    speaker_translations: list[str] = []
    collected: list[str] = []
    for index, (exchange, original_translation) in enumerate(zip(exchanges, original_translations)):
        output(SentenceData.from_tts(
            original_translation.speaker,
            target_speaker_tts,
            print_text=HIDDEN_TEXT if hide_prompts else None,
        ))
        output(SentenceData.from_tts(
            exchange.user,
            source_user_tts,
            print_text=HIDDEN_TEXT if hide_prompts else None,
            print_prefix=get_numbering_prefix(index),
        ))
        speaker_translations.append(original_translation.speaker)
        translation = get_input(
            on_pause=on_pause,
            on_resume=on_resume,
            prompt=TRANSLATION_PROMPT,
            transcriber_params=TranscriberParams(
                transcribe=asr.get_transcriber(target_language, '\n'.join(
                    turn for exchange in zip_longest(speaker_translations, collected) for turn in exchange if turn
                )),
                storage=storage,
            ) if asr else None,
            scanner_params=ScannerParams(
                scanner=scanner,
                language=target_language,
            ) if scanner else None,
        )
        collected.append(translation.text)
        yield ExchangeWithTranslation(exchange, translation)
        print()
