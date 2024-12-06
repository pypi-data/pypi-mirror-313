from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Iterable

from reling.db import init_db as do_init_db, migrate

__all__ = [
    'DatabaseVersion',
    'get_db_path',
    'init_db',
]

DB_PATH: Path | None = None


@dataclass
class DatabaseVersion:
    version: str
    path: Path


def try_migrate(versions: Iterable[DatabaseVersion]) -> DatabaseVersion:
    """
    Attempt to migrate the database to the latest version by iterating through the provided database versions
    to find an existing database file. If found, perform step-by-step migration to the latest version.

    :param versions: An iterable of `DatabaseVersion` objects, ordered from latest to oldest.
    :return: The `DatabaseVersion` object representing the latest version, even if no database file was found.
    """
    iter_versions = iter(versions)
    latest_version = next(iter_versions)
    if not latest_version.path.exists():
        versions_to_upgrade: list[DatabaseVersion] = []
        while True:
            if not (version := next(iter_versions, None)):
                break
            versions_to_upgrade.append(version)
            if version.path.exists():
                for from_version, to_version in zip(
                        reversed(versions_to_upgrade),
                        reversed([latest_version] + versions_to_upgrade[:-1]),
                ):
                    migrate(from_version.path, from_version.version)
                    from_version.path.rename(to_version.path)
                    print(f'Migrated database from version {from_version.version} to {to_version.version}',
                          file=sys.stderr)
    return latest_version


def init_db(versions: Iterable[DatabaseVersion]) -> None:
    """
    Initialize the database by finding or creating the latest version.

    This function first checks whether the database has already been initialized. If not, it attempts to
    migrate an existing database file to the latest version by calling `try_migrate`. If no existing
    database file is found, it initializes a new database at the latest version.

    :param versions: An iterable of `DatabaseVersion` objects, ordered from latest to oldest.
    :raises RuntimeError: If the database has already been initialized.
    """
    global DB_PATH
    if DB_PATH is not None:
        raise RuntimeError('Database is already initialized')
    DB_PATH = try_migrate(versions).path
    do_init_db(f'sqlite:///{DB_PATH}')


def get_db_path() -> Path:
    if DB_PATH is None:
        raise RuntimeError('Database is not initialized')
    return DB_PATH
