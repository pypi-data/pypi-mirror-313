from reling.app.app import app
from reling.app.default_content import set_default_content
from reling.app.types import CONTENT_ARG
from reling.db import single_session
from reling.helpers.typer import typer_raise
from reling.utils.time import now

__all__ = [
    'archive',
]


@app.command()
def archive(content: CONTENT_ARG) -> None:
    """Archive a text or dialogue."""
    set_default_content(content)

    if content.archived_at is not None:
        typer_raise('The content is already archived.')

    with single_session() as session:
        content.archived_at = now()
        session.commit()
    print(f'Archived "{content.id}".')
