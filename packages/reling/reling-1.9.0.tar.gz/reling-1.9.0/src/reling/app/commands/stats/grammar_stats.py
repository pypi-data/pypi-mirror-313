from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from heapq import merge
from typing import cast

from rich.text import Text

from reling.app.config import MAX_SCORE
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.db import single_session
from reling.db.models import DialogueExam, Language, TextExam
from reling.helpers.grammar import Analyzer, WordInfo
from reling.utils.console import print_and_erase
from reling.utils.tables import build_table, print_table
from .checkpoints import colorize, since
from .filter import get_filter
from .modalities import Modality
from .pos import Pos
from .progress import progress
from .table_str_enum import TableStrEnum

__all__ = [
    'display_stats',
]

PREPARING = 'Preparing...'

TITLE = '{modality}\n(only perfect answers are included; entry = unique text or dialogue)'

POS = 'Part of\nspeech'
TYPE = 'Word\ntype'
ONCE = '≥ 1\nentry'
OCCURRENCES = '≥ {occurrences}\nentries'

TOTAL = 'Total'

STATS_TYPE_DIVIDER = '---'

type Threshold = int

REPETITION_THRESHOLDS: list[Threshold] = [1, 3, 10, 25, 100]


class StatsType(TableStrEnum):
    FORMS = 'forms'
    LEMMAS = 'lemmas'


type Stats = defaultdict[tuple[Pos, StatsType, Threshold], int]

type NormalizedForm = tuple[str, str]


@dataclass
class Checkpoint:
    start_time: datetime
    stats: Stats


@dataclass
class PeriodStats:
    all_time: Stats
    checkpoints: list[Checkpoint]


def get_pos_stats(stats: Stats, pos: Pos | None, stats_type: StatsType, threshold: Threshold) -> int:
    """Get the statistics for the given pos, type, and threshold; or, if pos is None, sum over all parts of speech."""
    return (stats[pos, stats_type, threshold]
            if pos else
            sum(stats[cast(Pos, pos_), stats_type, threshold] for pos_ in Pos))


def get_normalized_form(word: WordInfo) -> NormalizedForm:
    return word.lemma, word.text.lower().replace('’', "'")


def get_relevant_periods(stats: PeriodStats, exam: TextExam | DialogueExam) -> list[Stats]:
    """Return the relevant statistics periods for the given exam."""
    return [
        stats.all_time,
        *(checkpoint.stats for checkpoint in stats.checkpoints if checkpoint.start_time <= exam.started_at),
    ]


def update_stats(stats: Stats, pos: Pos, stats_type: StatsType, occurrences: int) -> None:
    """Update the statistics with the given word."""
    for threshold in REPETITION_THRESHOLDS:
        if occurrences == threshold:
            stats[pos, stats_type, threshold] += 1


def get_relevant_sentences(exam: TextExam | DialogueExam, language: Language, modality: Modality) -> list[str]:
    """Return the relevant sentences to analyze."""
    if modality == Modality.PRODUCTION:
        return [result.answer for result in exam.results]
    elif isinstance(exam, TextExam):
        return get_text_sentences(exam.text, language)
    else:
        return [exchange.user for exchange in get_dialogue_exchanges(cast(DialogueExam, exam).dialogue, language)]


class StatsHandler:
    stats: PeriodStats
    analyzer: Analyzer
    lemma_item_ids: defaultdict[str, set[str]]
    form_item_ids: defaultdict[NormalizedForm, set[str]]

    def __init__(self, language: Language, checkpoints: list[datetime]) -> None:
        self.stats = PeriodStats(
            all_time=defaultdict(int),
            checkpoints=[Checkpoint(start_time=checkpoint, stats=defaultdict(int)) for checkpoint in checkpoints],
        )
        with print_and_erase(PREPARING):
            self.analyzer = Analyzer.get(language)
        self.lemma_item_ids = defaultdict(set)
        self.form_item_ids = defaultdict(set)

    def update(self, exam: TextExam | DialogueExam, sentence: str) -> None:
        """Update the statistics with the given exam and sentence."""
        for word in self.analyzer.analyze(sentence):
            for stats_type, item_ids in [
                (StatsType.LEMMAS, self.lemma_item_ids[word.lemma]),
                (StatsType.FORMS, self.form_item_ids[get_normalized_form(word)]),
            ]:
                if exam.item_id not in item_ids:
                    item_ids.add(exam.item_id)
                    for period in get_relevant_periods(self.stats, exam):
                        update_stats(period, Pos.from_upos(word.upos), stats_type, len(item_ids))


def compute_stats(
        language: Language,
        paired: list[Language] | None,
        modality: Modality,
        checkpoints: list[datetime],
) -> PeriodStats:
    """Compute grammar statistics for the given language(s) and modality."""
    handler = StatsHandler(language, checkpoints)
    with single_session() as session:
        for exam in progress(
            merge(
                *[(item for item in session.query(model).filter(
                    get_filter(language, paired, modality, model),
                ).order_by(model.started_at))
                  for model in [TextExam, DialogueExam]],
                key=lambda item: item.started_at,
            ),
            total=sum(
                session.query(model).filter(get_filter(language, paired, modality, model)).count()
                for model in [TextExam, DialogueExam]
            ),
            modality=modality,
        ):
            for result, sentence in zip(
                    exam.results,
                    get_relevant_sentences(exam, language, modality),
            ):
                if result.score == MAX_SCORE:
                    handler.update(exam, sentence)
    return handler.stats


def format_increment(increment: int) -> str:
    return f'+{increment}' if increment > 0 else '0'


def build_stats_section(
        stats: PeriodStats,
        pos: Pos | None,
        stats_type: StatsType,
        threshold_headers: list[str],
        prepend_divider: bool = False,
) -> list[dict[str, str | Text]]:
    """Build the statistics section for the given part of speech and type."""
    pos_title = pos.to_table_title() if pos else TOTAL
    return [*([{
        POS: pos_title,
        TYPE: STATS_TYPE_DIVIDER,
        **{header: STATS_TYPE_DIVIDER for header in threshold_headers},
    }] if prepend_divider else []), {
        POS: pos_title,
        TYPE: stats_type.to_table_title(),
        **{header: str(get_pos_stats(stats.all_time, pos, stats_type, threshold))
           for header, threshold in zip(threshold_headers, REPETITION_THRESHOLDS)},
    }, *[{
        POS: pos_title,
        TYPE: colorize(since(checkpoint.start_time)),
        **{header: colorize(format_increment(get_pos_stats(checkpoint.stats, pos, stats_type, threshold)))
           for header, threshold in zip(threshold_headers, REPETITION_THRESHOLDS)},
    } for checkpoint in stats.checkpoints]]


def print_stats(stats: PeriodStats, modality: Modality, add_dividers: bool) -> None:
    """Print the provided statistics."""
    threshold_headers = [
        OCCURRENCES.format(occurrences=threshold) if threshold != 1 else ONCE
        for threshold in REPETITION_THRESHOLDS
    ]
    print_table(build_table(
        title=TITLE.format(modality=modality.to_table_title()),
        headers=[
            POS,
            TYPE,
            *threshold_headers,
        ],
        justify={
            POS: 'left',
            TYPE: 'left',
            **{header: 'right' for header in threshold_headers},
        },
        widths={
            header: max(len(line) for header in threshold_headers for line in header.splitlines())
            for header in threshold_headers
        },
        data=[row
              for pos in list(Pos) + [None]
              for stats_type in StatsType
              for row in build_stats_section(
                stats,
                pos,
                cast(StatsType, stats_type),
                threshold_headers,
                prepend_divider=add_dividers and stats_type != next(iter(StatsType)),
              )],
        group_by=[POS],
    ))


def display_stats(
        language: Language,
        paired: list[Language] | None,
        modality: Modality,
        checkpoints: list[datetime],
) -> None:
    """Display grammar statistics for the given language(s) and modality."""
    stats = compute_stats(language, paired, modality, checkpoints)
    print_stats(stats, modality, add_dividers=len(checkpoints) > 0)
