from sqlalchemy.exc import IntegrityError

from reling.db import single_session
from reling.db.models import Dialogue, DialogueExchangeTranslation, Language, Text, TextSentenceTranslation
from reling.types import DialogueExchangeData
from .exceptions import TranslationExistsException


__all__ = [
    'save_dialogue_translation',
    'save_text_translation',
]


def save_text_translation(
        source_text: Text,
        target_language: Language,
        translated_sentences: list[str],
) -> None:
    """
    Save the translation of a text.
    :raises TranslationExistsError: If the text has already been translated into the target language.
    """
    try:
        with single_session() as session:
            session.add_all([
                TextSentenceTranslation(
                    text_id=source_text.id,
                    language_id=target_language.id,
                    text_sentence_index=index,
                    sentence=sentence,
                )
                for index, sentence in enumerate(translated_sentences)
            ])
            session.commit()
    except IntegrityError:
        raise TranslationExistsException


def save_dialogue_translation(
        source_dialogue: Dialogue,
        target_language: Language,
        translated_exchanges: list[DialogueExchangeData],
) -> None:
    """
    Save the translation of a dialogue.
    :raises TranslationExistsError: If the dialogue has already been translated into the target language.
    """
    try:
        with single_session() as session:
            session.add_all([
                DialogueExchangeTranslation(
                    dialogue_id=source_dialogue.id,
                    language_id=target_language.id,
                    dialogue_exchange_index=index,
                    speaker=exchange.speaker,
                    user=exchange.user,
                )
                for index, exchange in enumerate(translated_exchanges)
            ])
            session.commit()
    except IntegrityError:
        raise TranslationExistsException
