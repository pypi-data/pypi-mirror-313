from __future__ import annotations
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reling.db.base import Base
from reling.db.enums import Level
from .languages import Language

__all__ = [
    'Text',
    'TextExam',
    'TextExamResult',
    'TextSentence',
    'TextSentenceTranslation',
]


class Text(Base):
    __tablename__ = 'texts'

    id: Mapped[str] = mapped_column(primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    language: Mapped[Language] = relationship(Language)
    level: Mapped[Level]
    topic: Mapped[str]
    style: Mapped[str]
    created_at: Mapped[datetime]
    archived_at: Mapped[datetime | None]
    sentences: Mapped[list[TextSentence]] = relationship(
        'TextSentence',
        order_by='TextSentence.index',
        passive_deletes=True,
    )
    sentence_translations: Mapped[list[TextSentenceTranslation]] = relationship(
        'TextSentenceTranslation',
        passive_deletes=True,
    )
    exams: Mapped[list[TextExam]] = relationship('TextExam', passive_deletes=True)

    __table_args__ = (
        Index('text_chronological', 'archived_at', 'created_at'),
    )


class TextSentence(Base):
    __tablename__ = 'text_sentences'

    text_id: Mapped[str] = mapped_column(ForeignKey(Text.id, onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    index: Mapped[int] = mapped_column(primary_key=True)
    sentence: Mapped[str]


class TextSentenceTranslation(Base):
    __tablename__ = 'text_sentence_translations'

    text_id: Mapped[str] = mapped_column(ForeignKey(Text.id, onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id), primary_key=True)
    text_sentence_index: Mapped[int] = mapped_column(primary_key=True)
    sentence: Mapped[str]


class TextExam(Base):
    __tablename__ = 'text_exams'

    id: Mapped[str] = mapped_column(primary_key=True)
    text_id: Mapped[str] = mapped_column(ForeignKey(Text.id, onupdate='CASCADE', ondelete='CASCADE'))
    text: Mapped[Text] = relationship(Text, viewonly=True)
    source_language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    source_language: Mapped[Language] = relationship(Language, foreign_keys=source_language_id)
    target_language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    target_language: Mapped[Language] = relationship(Language, foreign_keys=target_language_id)
    read_source: Mapped[bool]
    read_target: Mapped[bool]
    listened: Mapped[bool]
    scanned: Mapped[bool]
    started_at: Mapped[datetime]
    finished_at: Mapped[datetime]
    total_pause_time: Mapped[timedelta]
    results: Mapped[list[TextExamResult]] = relationship(
        'TextExamResult',
        order_by='TextExamResult.text_sentence_index',
        passive_deletes=True,
    )

    __table_args__ = (
        Index('text_exam_source_language', 'source_language_id', 'started_at'),
        Index('text_exam_target_language', 'target_language_id', 'started_at'),
    )

    @property
    def item_id(self) -> str:
        return self.text_id

    @property
    def duration(self) -> timedelta:
        return self.finished_at - self.started_at - self.total_pause_time


class TextExamResult(Base):
    __tablename__ = 'text_exam_results'

    text_exam_id: Mapped[str] = mapped_column(
        ForeignKey(TextExam.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    text_sentence_index: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str]
    suggested_answer: Mapped[str | None]
    score: Mapped[int]
