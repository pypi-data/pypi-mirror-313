from __future__ import annotations
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reling.db.base import Base
from reling.db.enums import Gender, Level
from .languages import Language

__all__ = [
    'Dialogue',
    'DialogueExam',
    'DialogueExamResult',
    'DialogueExchange',
    'DialogueExchangeTranslation',
]


class Dialogue(Base):
    __tablename__ = 'dialogues'

    id: Mapped[str] = mapped_column(primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    language: Mapped[Language] = relationship(Language)
    level: Mapped[Level]
    speaker: Mapped[str]
    topic: Mapped[str | None]
    speaker_gender: Mapped[Gender]
    user_gender: Mapped[Gender]
    created_at: Mapped[datetime]
    archived_at: Mapped[datetime | None]
    exchanges: Mapped[list[DialogueExchange]] = relationship(
        'DialogueExchange',
        order_by='DialogueExchange.index',
        passive_deletes=True,
    )
    exchange_translations: Mapped[list[DialogueExchangeTranslation]] = relationship(
        'DialogueExchangeTranslation',
        passive_deletes=True,
    )
    exams: Mapped[list[DialogueExam]] = relationship('DialogueExam', passive_deletes=True)

    __table_args__ = (
        Index('dialogue_chronological', 'archived_at', 'created_at'),
    )


class DialogueExchange(Base):
    __tablename__ = 'dialogue_exchanges'

    dialogue_id: Mapped[str] = mapped_column(
        ForeignKey(Dialogue.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    index: Mapped[int] = mapped_column(primary_key=True)
    speaker: Mapped[str]
    user: Mapped[str]


class DialogueExchangeTranslation(Base):
    __tablename__ = 'dialogue_exchange_translations'

    dialogue_id: Mapped[str] = mapped_column(
        ForeignKey(Dialogue.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id), primary_key=True)
    dialogue_exchange_index: Mapped[int] = mapped_column(primary_key=True)
    speaker: Mapped[str]
    user: Mapped[str]


class DialogueExam(Base):
    __tablename__ = 'dialogue_exams'

    id: Mapped[str] = mapped_column(primary_key=True)
    dialogue_id: Mapped[str] = mapped_column(ForeignKey(Dialogue.id, onupdate='CASCADE', ondelete='CASCADE'))
    dialogue: Mapped[Dialogue] = relationship(Dialogue, viewonly=True)
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
    results: Mapped[list[DialogueExamResult]] = relationship(
        'DialogueExamResult',
        order_by='DialogueExamResult.dialogue_exchange_index',
        passive_deletes=True,
    )

    __table_args__ = (
        Index('dialogue_exam_source_language', 'source_language_id', 'started_at'),
        Index('dialogue_exam_target_language', 'target_language_id', 'started_at'),
    )

    @property
    def item_id(self) -> str:
        return self.dialogue_id

    @property
    def duration(self) -> timedelta:
        return self.finished_at - self.started_at - self.total_pause_time


class DialogueExamResult(Base):
    __tablename__ = 'dialogue_exam_results'

    dialogue_exam_id: Mapped[str] = mapped_column(
        ForeignKey(DialogueExam.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    dialogue_exchange_index: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str]
    suggested_answer: Mapped[str | None]
    score: Mapped[int]
