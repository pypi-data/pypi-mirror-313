from datetime import datetime

from rich.text import Text

from reling.helpers.colors import fade
from reling.utils.time import format_time

__all__ = [
    'colorize',
    'since',
]

SINCE_TEXT = 'since {checkpoint}'
TODAY_TEXT = 'today'


def since(checkpoint: datetime) -> str:
    """Return a string indicating the time period since the given checkpoint."""
    return SINCE_TEXT.format(checkpoint=format_time(checkpoint, omit_zero_time=True))


def colorize(text: str) -> Text:
    """Colorize the given checkpoint text for display."""
    return fade(text)
