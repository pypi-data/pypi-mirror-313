from reling.app.app import app
from reling.app.types import (
    CHECKPOINT_OPT,
    COMPREHENSION_OPT,
    GRAMMAR_OPT,
    LANGUAGE_ARG,
    PAIR_LANGUAGE_OPT,
    PRODUCTION_OPT,
)
from reling.utils.time import local_to_utc
from .grammar_stats import display_stats as display_grammar_stats
from .modalities import Modality
from .regular_stats import display_stats as display_regular_stats

__all__ = [
    'stats',
]


@app.command()
def stats(
        language: LANGUAGE_ARG,
        pair: PAIR_LANGUAGE_OPT = None,
        grammar: GRAMMAR_OPT = False,
        comprehension: COMPREHENSION_OPT = False,
        production: PRODUCTION_OPT = False,
        checkpoint: CHECKPOINT_OPT = None,
) -> None:
    """Show learning statistics for a specific language."""
    comprehension, production = comprehension or not production, production or not comprehension
    display_stats = display_grammar_stats if grammar else display_regular_stats
    checkpoint_dates = list(map(local_to_utc, checkpoint or []))
    for (modality, should_display) in [
        (Modality.COMPREHENSION, comprehension),
        (Modality.PRODUCTION, production),
    ]:
        if should_display:
            print()
            display_stats(language, pair, modality, checkpoint_dates)
