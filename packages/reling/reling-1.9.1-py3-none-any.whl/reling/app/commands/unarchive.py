from reling.app.app import app
from reling.app.default_content import set_default_content
from reling.app.types import CONTENT_ARG
from reling.db import single_session
from reling.helpers.typer import typer_raise

__all__ = [
    'unarchive',
]


@app.command()
def unarchive(content: CONTENT_ARG) -> None:
    """Unarchive a text or dialogue."""
    set_default_content(content)

    if content.archived_at is None:
        typer_raise('The content is not archived.')

    with single_session() as session:
        content.archived_at = None
        session.commit()
    print(f'Unarchived "{content.id}".')
