from pathlib import Path
from typing import cast

from sqlalchemy import ColumnElement
from sqlalchemy.sql import exists, func

from reling.db import single_session
from reling.db.models import Speaker, Style, Topic
from reling.utils.csv import read_csv

__all__ = [
    'get_random_modifier',
    'populate_modifiers',
]


def populate_modifiers[T: (Speaker, Style, Topic)](entity_class: type[T], data: Path) -> None:
    """Populate the table with data from the CSV file, if the table is empty."""
    with single_session() as session:
        if not session.query(exists().where(cast(ColumnElement[str], entity_class.name).is_not(None))).scalar():
            for entity in read_csv(data, ['name']):
                session.add(entity_class(**entity))
        session.commit()


def get_random_modifier[T: (Speaker, Style, Topic)](entity_class: type[T]) -> T:
    """Get a random entity from the given table."""
    with single_session() as session:
        entity = session.query(entity_class).order_by(func.random()).first()
    if entity is None:
        raise RuntimeError(f'Table "{entity_class.__tablename__}" is empty.')
    return entity
