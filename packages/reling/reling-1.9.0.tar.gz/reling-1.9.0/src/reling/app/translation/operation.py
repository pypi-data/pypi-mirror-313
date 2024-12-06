from typing import cast

from sqlalchemy import ColumnElement, exists
from tqdm import tqdm

from reling.app.exceptions import AlgorithmException
from reling.db import single_session
from reling.db.models import Dialogue, DialogueExchangeTranslation, Language, Text, TextSentenceTranslation
from reling.gpt import GPTClient
from reling.types import DialogueExchangeData, Promise
from .exceptions import TranslationExistsException
from .storage import save_dialogue_translation, save_text_translation
from .translation import translate_dialogue_exchanges, translate_text_sentences

__all__ = [
    'translate_dialogue',
    'translate_text',
]


def is_text_translated(text: Text, language: Language) -> bool:
    """Check if a text has already been translated into a target language."""
    with single_session() as session:
        return session.query(exists().where(
            cast(ColumnElement[bool], TextSentenceTranslation.text_id == text.id),
            cast(ColumnElement[bool], TextSentenceTranslation.language_id == language.id),
        )).scalar()


def is_dialogue_translated(dialogue: Dialogue, language: Language) -> bool:
    """Check if a dialogue has already been translated into a target language."""
    with single_session() as session:
        return session.query(exists().where(
            cast(ColumnElement[bool], DialogueExchangeTranslation.dialogue_id == dialogue.id),
            cast(ColumnElement[bool], DialogueExchangeTranslation.language_id == language.id),
        )).scalar()


def translate_text(gpt: Promise[GPTClient], text: Text, language: Language) -> None:
    """
    Translate a text into another language.

    :raises ValueError: If the text is already in the target language.
    :raises TranslationExistsException: If the text has already been translated into the target language.
    :raises AlgorithmException: If there is an issue with the translation algorithm.
    """
    if language.id == text.language_id:
        raise ValueError(f'The text is already in {language.name}.')
    if is_text_translated(text, language):
        raise TranslationExistsException
    sentences = list(tqdm(
        translate_text_sentences(
            gpt=gpt(),
            sentences=[cast(str, sentence.sentence) for sentence in text.sentences],
            source_language=text.language,
            target_language=language,
        ),
        desc=f'Translating text into {language.name}',
        total=len(text.sentences),
        leave=False,
    ))
    if len(sentences) != len(text.sentences):
        raise AlgorithmException(
            'The number of translated sentences does not match the number of original sentences. You can try again.',
        )
    save_text_translation(text, language, sentences)


def translate_dialogue(gpt: Promise[GPTClient], dialogue: Dialogue, language: Language) -> None:
    """
    Translate a dialogue into another language.

    :raises ValueError: If the dialogue is already in the target language.
    :raises TranslationExistsException: If the dialogue has already been translated into the target language.
    :raises AlgorithmException: If there is an issue with the translation algorithm.
    """
    if language.id == dialogue.language_id:
        raise ValueError(f'The dialogue is already in {language.name}.')
    if is_dialogue_translated(dialogue, language):
        raise TranslationExistsException
    exchanges = list(tqdm(
        translate_dialogue_exchanges(
            gpt=gpt(),
            exchanges=[
                DialogueExchangeData(
                    speaker=exchange.speaker,
                    user=exchange.user,
                )
                for exchange in dialogue.exchanges
            ],
            speaker_gender=dialogue.speaker_gender,
            user_gender=dialogue.user_gender,
            source_language=dialogue.language,
            target_language=language,
        ),
        desc=f'Translating dialogue into {language.name}',
        total=len(dialogue.exchanges),
        leave=False,
    ))
    if len(exchanges) != len(dialogue.exchanges):
        AlgorithmException(
            'The number of translated exchanges does not match the number of original exchanges. You can try again.',
        )
    save_dialogue_translation(dialogue, language, exchanges)
