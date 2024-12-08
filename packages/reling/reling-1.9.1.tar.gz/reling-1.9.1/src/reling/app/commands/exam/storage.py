from datetime import datetime, timedelta

from reling.db import single_session
from reling.db.models import Dialogue, DialogueExam, DialogueExamResult, Language, Text, TextExam, TextExamResult
from reling.utils.ids import generate_id
from .types import ExchangeWithTranslation, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'save_dialogue_exam',
    'save_text_exam',
]


def save_text_exam(
        text: Text,
        source_language: Language,
        target_language: Language,
        read_source: bool,
        read_target: bool,
        listened: bool,
        scanned: bool,
        started_at: datetime,
        finished_at: datetime,
        total_pause_time: timedelta,
        sentences: list[SentenceWithTranslation],
        results: list[ScoreWithSuggestion],
) -> TextExam:
    """Save the results of a text exam."""
    with single_session() as session:
        exam = TextExam(
            id=generate_id(),
            text_id=text.id,
            source_language_id=source_language.id,
            target_language_id=target_language.id,
            read_source=read_source,
            read_target=read_target,
            listened=listened,
            scanned=scanned,
            started_at=started_at,
            finished_at=finished_at,
            total_pause_time=total_pause_time,
        )
        session.add(exam)
        for index, (sentence, result) in enumerate(zip(sentences, results)):
            session.add(TextExamResult(
                text_exam_id=exam.id,
                text_sentence_index=index,
                answer=sentence.translation.text,
                suggested_answer=result.suggestion,
                score=result.score,
            ))
        session.commit()
        return exam


def save_dialogue_exam(
        dialogue: Dialogue,
        source_language: Language,
        target_language: Language,
        read_source: bool,
        read_target: bool,
        listened: bool,
        scanned: bool,
        started_at: datetime,
        finished_at: datetime,
        total_pause_time: timedelta,
        exchanges: list[ExchangeWithTranslation],
        results: list[ScoreWithSuggestion],
) -> DialogueExam:
    """Save the results of a dialogue exam."""
    with single_session() as session:
        exam = DialogueExam(
            id=generate_id(),
            dialogue_id=dialogue.id,
            source_language_id=source_language.id,
            target_language_id=target_language.id,
            read_source=read_source,
            read_target=read_target,
            listened=listened,
            scanned=scanned,
            started_at=started_at,
            finished_at=finished_at,
            total_pause_time=total_pause_time,
        )
        session.add(exam)
        for index, (exchange, result) in enumerate(zip(exchanges, results)):
            session.add(DialogueExamResult(
                dialogue_exam_id=exam.id,
                dialogue_exchange_index=index,
                answer=exchange.user_translation.text,
                suggested_answer=result.suggestion,
                score=result.score,
            ))
        session.commit()
        return exam
