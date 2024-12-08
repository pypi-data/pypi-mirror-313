from rich.text import Text

__all__ = [
    'default',
    'fade',
    'green',
    'red',
]

FADE = 'grey50'
RED = 'red'
GREEN = 'green'
DEFAULT = 'default'


def fade(text: str) -> Text:
    """Return the text in a faded color."""
    return Text(text, style=FADE)


def red(text: str) -> Text:
    """Return the text in red."""
    return Text(text, style=RED)


def green(text: str) -> Text:
    """Return the text in green."""
    return Text(text, style=GREEN)


def default(text: str) -> Text:
    """Return the text in the default color."""
    return Text(text, style=DEFAULT)
