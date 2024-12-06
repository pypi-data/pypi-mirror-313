from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from reling.db.base import Base
from .languages import Language

__all__ = [
    'GrammarCacheSentence',
    'GrammarCacheWord',
]


class GrammarCacheSentence(Base):
    __tablename__ = 'grammar_cache_sentences'

    id: Mapped[str] = mapped_column(primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    sentence: Mapped[str]

    __table_args__ = (
        Index('grammar_cache_sentence_language_sentence', 'language_id', 'sentence', unique=True),
    )


class GrammarCacheWord(Base):
    __tablename__ = 'grammar_cache_words'

    sentence_id: Mapped[str] = mapped_column(
        ForeignKey(GrammarCacheSentence.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    index: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    lemma: Mapped[str]
    upos: Mapped[str]
