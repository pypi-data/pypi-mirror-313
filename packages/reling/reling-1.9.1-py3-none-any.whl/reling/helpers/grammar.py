from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from typing import cast, TYPE_CHECKING

if TYPE_CHECKING:
    from stanza import Pipeline

from reling.db import Session, single_session
from reling.db.models import GrammarCacheSentence, GrammarCacheWord, Language
from reling.utils.ids import generate_id
from .typer import typer_raise, typer_raise_import

__all__ = [
    'Analyzer',
    'WordInfo',
]

PROCESSORS = 'tokenize,pos,lemma'

EXCLUDED_UPOS = {'PUNCT', 'SYM', 'X'}


@dataclass
class WordInfo:
    text: str
    lemma: str
    upos: str


@dataclass
class Analyzer:
    _nlp: Pipeline
    language: Language

    @staticmethod
    @lru_cache
    def get(language: Language) -> Analyzer:
        """Get a Stanza pipeline for the specified language."""
        try:
            import stanza
            from stanza.resources.common import UnknownLanguageError
        except ImportError:
            raise typer_raise_import('Stanza')
        import logging
        stanza_logger = logging.getLogger('stanza')
        stanza_logger.setLevel(logging.ERROR)
        try:
            stanza.download(language.short_code)
        except UnknownLanguageError:
            raise typer_raise(f'{language.name} is not supported by Stanza.')
        return Analyzer(
            _nlp=stanza.Pipeline(language.short_code, processors=PROCESSORS),
            language=language,
        )

    def _get_analysis_from_cache(self, session: Session, sentence: str) -> list[WordInfo] | None:
        """Get the analysis of a sentence from the cache."""
        return [
            WordInfo(
                text=cast(str, word.text),
                lemma=cast(str, word.lemma),
                upos=cast(str, word.upos),
            )
            for word in (session.query(GrammarCacheWord)
                         .filter_by(sentence_id=cached_sentence.id)
                         .order_by(GrammarCacheWord.index).all())
        ] if (cached_sentence := session.query(GrammarCacheSentence).filter_by(
            language_id=self.language.id,
            sentence=sentence,
        ).first()) else None

    def _put_analysis_to_cache(self, session: Session, sentence: str, words: list[WordInfo]) -> None:
        """Put the analysis of a sentence to the cache."""
        sentence_id = generate_id()
        cached_sentence = GrammarCacheSentence(
            id=sentence_id,
            language_id=self.language.id,
            sentence=sentence,
        )
        session.add(cached_sentence)
        for index, word in enumerate(words):
            session.add(GrammarCacheWord(
                sentence_id=sentence_id,
                index=index,
                text=word.text,
                lemma=word.lemma,
                upos=word.upos,
            ))
        session.commit()

    def _do_analyze(self, sentence: str) -> list[WordInfo]:
        """Analyze a sentence."""
        for section in self._nlp(sentence).sentences:
            return [
                WordInfo(
                    text=word.text,
                    lemma=word.lemma,
                    upos=word.upos,
                )
                for word in section.words
                if word.upos not in EXCLUDED_UPOS
            ]

    def analyze(self, sentence: str) -> list[WordInfo]:
        """Analyze a sentence and cache the result."""
        with single_session() as session:
            if (words := self._get_analysis_from_cache(session, sentence)) is not None:
                return words
            else:
                words = self._do_analyze(sentence)
                self._put_analysis_to_cache(session, sentence, words)
                return words
