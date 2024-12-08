from reling.db.models import Dialogue, Text
from reling.shelf import get_value, set_value

__all__ = [
    'get_default_content_id',
    'set_default_content',
]

VAR_NAME = 'DEFAULT_CONTENT'


def get_default_content_id() -> str | None:
    """Get the default content ID."""
    return get_value(VAR_NAME)


def set_default_content(content: Text | Dialogue | None) -> None:
    """Set the default content for the commands."""
    set_value(VAR_NAME, content.id if content is not None else None)
