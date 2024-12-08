from reling.app.default_content import get_default_content_id
from reling.db import single_session
from reling.db.models import Dialogue, Text
from reling.helpers.typer import typer_raise

__all__ = [
    'find_content',
]


def find_content(content_id: str, last_content_marker: str) -> Text | Dialogue | None:
    """Find a text or dialogue by its ID."""
    if content_id == last_content_marker:
        content_id = get_default_content_id()
        if content_id is None:
            typer_raise('No content has been interacted with yet')
    with single_session() as session:
        return session.get(Text, content_id) or session.get(Dialogue, content_id)
