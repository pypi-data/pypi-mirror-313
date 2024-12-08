from sqlalchemy.exc import IntegrityError, NoResultFound

from reling.app.app import app
from reling.app.default_content import set_default_content
from reling.app.types import CONTENT_ARG, NEW_ID_ARG
from reling.db import single_session
from reling.db.models import IdIndex
from reling.helpers.typer import typer_raise

__all__ = [
    'rename',
]


@app.command()
def rename(content: CONTENT_ARG, new_id: NEW_ID_ARG) -> None:
    """Rename a text or dialogue."""
    set_default_content(content)
    old_id = content.id
    with single_session() as session:
        try:
            id_index_item = session.query(IdIndex).filter_by(id=content.id).one()
        except NoResultFound:
            typer_raise(f'There is no content with the ID "{content.id}".')  # Should never happen
        id_index_item.id = new_id
        content.id = new_id
        try:
            session.commit()
            set_default_content(content)
            print(f'Renamed "{old_id}" to "{new_id}".')
        except IntegrityError:
            typer_raise(f'The ID "{new_id}" is already in use.')
