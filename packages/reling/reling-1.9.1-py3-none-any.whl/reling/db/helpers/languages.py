from pathlib import Path

from sqlalchemy.sql import exists, func

from reling.db import single_session
from reling.db.models import Language
from reling.utils.csv import read_csv
from reling.utils.strings import replace_prefix_casing

__all__ = [
    'find_language',
    'find_languages_by_prefix',
    'populate_languages',
]


def populate_languages(data: Path) -> None:
    """Populate the languages table with data from the CSV file, if the table is empty."""
    with single_session() as session:
        if not session.query(exists().where(Language.id.is_not(None))).scalar():
            for language in read_csv(
                data,
                ['id', 'short_code', 'name', 'extra_name_a', 'extra_name_b'],
                empty_as_none=True,
            ):
                session.add(Language(**language))
        session.commit()


def find_language(language: str) -> Language | None:
    """Find a language, either by its ID, short code, or name (case-insensitive), applying filters sequentially."""
    lower = func.lower(language)
    conditions = [
        Language.id == language,
        Language.short_code == language,
        func.lower(Language.name) == lower,
        func.lower(Language.extra_name_a) == lower,
        func.lower(Language.extra_name_b) == lower,
    ]

    with single_session() as session:
        for condition in conditions:
            if result := session.query(Language).where(condition).first():
                return result

    return None


def find_languages_by_prefix(prefix: str) -> list[str]:
    """Find language IDs, short codes, and names that start with the given prefix."""
    lower = func.lower(prefix)
    with single_session() as session:
        return sorted([
            language.id
            for language in session.query(Language).where(Language.id.startswith(prefix)).all()
        ] + [
            language.short_code
            for language in session.query(Language).where(Language.short_code.startswith(prefix)).all()
        ] + [
            replace_prefix_casing(language.name, prefix)
            for language in session.query(Language).where(func.lower(Language.name).startswith(lower)).all()
        ] + [
            replace_prefix_casing(language.extra_name_a, prefix)
            for language in session.query(Language).where(func.lower(Language.extra_name_a).startswith(lower)).all()
        ] + [
            replace_prefix_casing(language.extra_name_b, prefix)
            for language in session.query(Language).where(func.lower(Language.extra_name_b).startswith(lower)).all()
        ])
