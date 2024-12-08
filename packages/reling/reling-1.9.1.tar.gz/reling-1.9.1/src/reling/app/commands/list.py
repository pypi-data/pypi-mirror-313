from datetime import datetime
import re
from typing import cast, Generator

from sqlalchemy import ColumnElement

from reling.app.app import app
from reling.app.types import (
    ARCHIVE_OPT,
    CONTENT_CATEGORY_OPT,
    IDS_ONLY_OPT,
    LANGUAGE_OPT,
    LEVEL_OPT,
    REGEX_CONTENT_OPT,
)
from reling.db import Session, single_session
from reling.db.enums import ContentCategory, Level
from reling.db.models import Dialogue, Language, Text
from reling.utils.time import format_time
from reling.utils.tables import build_table, print_table

__all__ = [
    'list_',
]

ID = 'ID'
LANGUAGE = 'Language'
LEVEL = 'Level'
TOPIC = 'Topic'
STYLE = 'Style'
SPEAKER = 'Speaker'
SIZE = 'Size'
CREATED_AT = 'Created at'
ARCHIVED_AT = 'Archived at'

NO_TOPIC = 'N/A'


def get_text(item: Text | Dialogue) -> list[str]:
    """Return the text content of a text or dialogue, including the speaker, topic, style, and sentences."""
    if isinstance(item, Text):
        return [
            item.topic,
            item.style,
            *(sentence.sentence for sentence in item.sentences),
        ]
    else:
        return [
            item.speaker,
            *([item.topic] if item.topic is not None else []),
            *(turn for exchange in item.exchanges for turn in [exchange.speaker, exchange.user]),
        ]


def match(item: Text | Dialogue, level: Level | None, language: Language | None, search: re.Pattern | None) -> bool:
    return (
        (level is None or item.level == level)
        and (language is None or cast(Language, item.language).id == language.id)
        and (search is None
             or search.search(cast(str, item.id)) is not None
             or any(search.search(text) is not None for text in get_text(item)))
    )


def find_items[T: type[Text | Dialogue]](
        session: Session,
        model: type[T],
        archive: bool,
        level: Level | None,
        language: Language | None,
        search: re.Pattern | None,
) -> Generator[T, None, None]:
    archived_at = cast(ColumnElement[datetime | None], model.archived_at)
    created_at = cast(ColumnElement[datetime], model.created_at)

    for item in session.query(model).filter(
        archived_at.is_not(None) if archive else archived_at.is_(None),
    ).order_by(
        archived_at.desc(), created_at.desc(),
    ):
        if match(item, level, language, search):
            yield item


@app.command(name='list')
def list_(
        category: CONTENT_CATEGORY_OPT = None,
        level: LEVEL_OPT = None,
        language: LANGUAGE_OPT = None,
        search: REGEX_CONTENT_OPT = None,
        archive: ARCHIVE_OPT = False,
        ids_only: IDS_ONLY_OPT = False,
) -> None:
    """List texts and/or dialogues, optionally filtered by ID or other criteria."""
    with single_session() as session:
        for model in [
            *([Text] if category != ContentCategory.DIALOGUE else []),
            *([Dialogue] if category != ContentCategory.TEXT else []),
        ]:
            items = find_items(session, model, archive, level, language, search)
            if ids_only:
                for item in items:
                    print(item.id)
            else:
                table = build_table(
                    title=('Texts' if model is Text else 'Dialogues') + (' (archived)' if archive else ''),
                    headers=[
                        ID,
                        LANGUAGE,
                        LEVEL,
                        *([SPEAKER] if model is Dialogue else []),
                        TOPIC,
                        *([STYLE] if model is Text else []),
                        SIZE,
                        CREATED_AT,
                        *([ARCHIVED_AT] if archive else []),
                    ],
                    justify={
                        SIZE: 'right',
                    },
                    data=({
                        ID: item.id,
                        LANGUAGE: item.language.name,
                        LEVEL: item.level.value,
                        **({SPEAKER: item.speaker} if model is Dialogue else {}),
                        TOPIC: item.topic or NO_TOPIC,
                        **({STYLE: item.style} if model is Text else {}),
                        SIZE: str(len(item.sentences if model is Text else item.exchanges)),
                        CREATED_AT: format_time(item.created_at),
                        **({ARCHIVED_AT: format_time(item.archived_at)} if archive else {}),
                    } for item in items),
                )
                print()
                print_table(table)
