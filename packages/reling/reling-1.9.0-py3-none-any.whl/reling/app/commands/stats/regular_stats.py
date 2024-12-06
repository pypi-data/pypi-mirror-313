from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, cast

from rich.text import Text

from reling.db import single_session
from reling.db.models import DialogueExam, Language, TextExam
from reling.utils.time import format_time_delta
from reling.utils.tables import build_table, GROUPING_COLUMN, print_table
from .checkpoints import colorize, since
from .filter import get_filter
from .modalities import Modality
from .progress import progress

__all__ = [
    'display_stats',
]

NA = 'N/A'

METRIC = 'Metric'
TEXTS = 'Texts'
DIALOGUES = 'Dialogues'
OVERALL = 'Overall'

TIME_SPENT = 'Total exam time'
EXAMS_TAKEN = 'Exams taken'
SENTENCES_EVALUATED = 'Sentences evaluated'
FIRST_TIME_EXAMS_TAKEN = 'First-time exams'
FIRST_TIME_SENTENCES_EVALUATED = 'Sents in first-time exams'
AVG_FTE_TIME_PER_SENTENCE = 'Avg. time/sent, first-time'
AVG_FTS_SCORE = 'Avg. score/sent, first-time'


@dataclass
class Stats:
    time_spent: timedelta = timedelta(0)
    exams_taken: int = 0
    sentences_evaluated: int = 0
    first_time_exams_taken: int = 0
    first_time_sentences_evaluated: int = 0
    fte_time_spent: timedelta = timedelta(0)
    fts_scores_total: float = 0.0

    def format_time_spent(self) -> str:
        return format_time_delta(self.time_spent)

    def format_exams_taken(self) -> str:
        return str(self.exams_taken)

    def format_sentences_evaluated(self) -> str:
        return str(self.sentences_evaluated)

    def format_first_time_exams_taken(self) -> str:
        return str(self.first_time_exams_taken)

    def format_first_time_sentences_evaluated(self) -> str:
        return str(self.first_time_sentences_evaluated)

    def format_avg_fte_time_per_sentence(self) -> str:
        return (format_time_delta(self.fte_time_spent / self.first_time_sentences_evaluated)
                if self.first_time_sentences_evaluated > 0 else NA)

    def format_avg_fts_score(self) -> str:
        return (f'{self.fts_scores_total / self.first_time_sentences_evaluated:.2f}'
                if self.first_time_sentences_evaluated > 0 else NA)


@dataclass
class TypeStats:
    text: Stats = field(default_factory=Stats)
    dialogue: Stats = field(default_factory=Stats)
    overall: Stats = field(default_factory=Stats)


@dataclass
class Checkpoint:
    start_time: datetime
    stats: TypeStats


@dataclass
class PeriodStats:
    all_time: TypeStats
    checkpoints: list[Checkpoint]


def get_relevant_periods(stats: PeriodStats, exam: TextExam | DialogueExam) -> list[TypeStats]:
    """Return the relevant statistics periods for the given exam."""
    return [
        stats.all_time,
        *(checkpoint.stats for checkpoint in stats.checkpoints if checkpoint.start_time <= exam.started_at),
    ]


def get_relevant_types(stats: TypeStats, exam: TextExam | DialogueExam) -> list[Stats]:
    """Return the relevant types for the given exam."""
    return [
        stats.overall,
        stats.text if isinstance(exam, TextExam) else stats.dialogue,
    ]


def update_single_stats(stats: Stats, exam: TextExam | DialogueExam, is_first_exam: bool) -> None:
    """Update the statistics with the given exam."""
    sentences_evaluated = len(cast(list, exam.results))
    scores_total = sum(result.score for result in exam.results)

    stats.time_spent += exam.duration
    stats.exams_taken += 1
    stats.sentences_evaluated += sentences_evaluated
    if is_first_exam:
        stats.first_time_exams_taken += 1
        stats.first_time_sentences_evaluated += sentences_evaluated
        stats.fte_time_spent += exam.duration
        stats.fts_scores_total += scores_total


def update_stats(stats: PeriodStats, exam: TextExam | DialogueExam, is_first_exam: bool) -> None:
    """Update the statistics with the given exam."""
    for period_stats in get_relevant_periods(stats, exam):
        for type_stats in get_relevant_types(period_stats, exam):
            update_single_stats(type_stats, exam, is_first_exam)


def compute_stats(
        language: Language,
        paired: list[Language] | None,
        modality: Modality,
        checkpoints: list[datetime],
) -> PeriodStats:
    """Compute regular statistics for the given language(s) and modality."""
    with single_session() as session:
        stats = PeriodStats(
            all_time=TypeStats(),
            checkpoints=[Checkpoint(start_time=checkpoint, stats=TypeStats()) for checkpoint in checkpoints],
        )
        for model in [TextExam, DialogueExam]:
            seen_item_ids: set[str] = set()
            condition = get_filter(language, paired, modality, model)
            for exam in progress(
                session.query(model).filter(condition).order_by(model.started_at),
                total=session.query(model).filter(condition).count(),
                modality=modality,
                model=model,
            ):
                update_stats(stats, exam, is_first_exam=exam.item_id not in seen_item_ids)
                seen_item_ids.add(exam.item_id)
        return stats


def build_stats_section(
        stats: PeriodStats,
        title: str,
        formatter: Callable[[Stats], str],
) -> list[dict[str, str | Text]]:
    """Build a section of statistics for the given title and formatter."""
    return [{
        GROUPING_COLUMN: title,
        METRIC: title,
        TEXTS: formatter(stats.all_time.text),
        DIALOGUES: formatter(stats.all_time.dialogue),
        OVERALL: formatter(stats.all_time.overall),
    }, *[{
        GROUPING_COLUMN: title,
        METRIC: colorize(since(checkpoint.start_time)),
        TEXTS: colorize(formatter(checkpoint.stats.text)),
        DIALOGUES: colorize(formatter(checkpoint.stats.dialogue)),
        OVERALL: colorize(formatter(checkpoint.stats.overall)),
    } for checkpoint in stats.checkpoints]]


def print_stats(stats: PeriodStats, modality: Modality) -> None:
    """Print the provided statistics."""
    print_table(build_table(
        title=modality.to_table_title(),
        headers=[
            METRIC,
            TEXTS,
            DIALOGUES,
            OVERALL,
        ],
        justify={
            METRIC: 'left',
            TEXTS: 'right',
            DIALOGUES: 'right',
            OVERALL: 'right',
        },
        data=[
            row
            for title, formatter in [
                (TIME_SPENT, Stats.format_time_spent),
                (EXAMS_TAKEN, Stats.format_exams_taken),
                (SENTENCES_EVALUATED, Stats.format_sentences_evaluated),
                (FIRST_TIME_EXAMS_TAKEN, Stats.format_first_time_exams_taken),
                (FIRST_TIME_SENTENCES_EVALUATED, Stats.format_first_time_sentences_evaluated),
                (AVG_FTE_TIME_PER_SENTENCE, Stats.format_avg_fte_time_per_sentence),
                (AVG_FTS_SCORE, Stats.format_avg_fts_score),
            ]
            for row in build_stats_section(stats, title, formatter)
        ],
        group_by=[GROUPING_COLUMN],
    ))


def display_stats(
        language: Language,
        paired: list[Language] | None,
        modality: Modality,
        checkpoints: list[datetime],
) -> None:
    """Display regular statistics for the given language(s) and modality."""
    stats = compute_stats(language, paired, modality, checkpoints)
    print_stats(stats, modality)
