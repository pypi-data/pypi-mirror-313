from pathlib import Path
import shelve

__all__ = [
    'get_value',
    'init_shelf',
    'set_value',
]

FILENAME: Path | None = None


def init_shelf(filename: Path) -> None:
    global FILENAME
    FILENAME = filename


def get_filename() -> str:
    if FILENAME is None:
        raise RuntimeError('Shelf is not initialized')
    return str(FILENAME.absolute())


def get_value(key: str) -> str | None:
    with shelve.open(get_filename()) as db:
        return db.get(key)


def set_value(key: str, value: str | None) -> None:
    with shelve.open(get_filename()) as db:
        db[key] = value
