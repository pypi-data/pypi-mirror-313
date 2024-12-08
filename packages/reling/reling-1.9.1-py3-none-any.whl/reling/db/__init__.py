from contextlib import contextmanager
from sqlite3 import Connection
from typing import Any, Generator

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import Session

from . import models  # Register models with SQLAlchemy
from .base import Base
from .migrations import migrate

__all__ = [
    'init_db',
    'migrate',
    'Session',
    'single_session',
]

SESSION: Session | None = None


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection: Connection, _connection_record: Any) -> None:
    """
    Enable foreign key support for SQLite.
    See https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
    """
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


def init_db(url: str) -> None:
    global SESSION
    if SESSION is None:
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        SESSION = Session(engine)


@contextmanager
def single_session() -> Generator[Session, None, None]:
    if SESSION is None:
        raise RuntimeError('Database is not initialized')
    try:
        yield SESSION
    except Exception:
        SESSION.rollback()
        raise
