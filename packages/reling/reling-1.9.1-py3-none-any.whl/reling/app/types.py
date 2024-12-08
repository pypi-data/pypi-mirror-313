from datetime import datetime
import re
from typing import Annotated

import typer

from reling.db.enums import ContentCategory, Gender, Level
from reling.db.helpers.content import find_content
from reling.db.helpers.ids import find_ids_by_prefix
from reling.db.helpers.languages import find_language, find_languages_by_prefix
from reling.db.models import Dialogue, Language, Text
from reling.helpers.typer import (
    TyperExtraOption,
    typer_enum_autocompletion,
    typer_enum_options,
    typer_enum_parser,
    typer_func_parser,
    typer_regex_parser,
)
from reling.types import WordWithSense
from reling.utils.time import DATE_FORMAT, TIME_FORMAT

__all__ = [
    'API_KEY',
    'ARCHIVE_OPT',
    'ASR_MODEL',
    'CHECKPOINT_OPT',
    'COMPREHENSION_OPT',
    'CONTENT_ARG',
    'CONTENT_CATEGORY_OPT',
    'FORCE_OPT',
    'GRAMMAR_OPT',
    'HIDE_PROMPTS_OPT',
    'IDS_ONLY_OPT',
    'INCLUDE_OPT',
    'LANGUAGE_ARG',
    'LANGUAGE_OPT',
    'LANGUAGE_OPT_ARG',
    'LANGUAGE_OPT_FROM',
    'LEVEL_OPT',
    'LISTEN_OPT',
    'MODEL',
    'NEW_ID_ARG',
    'OFFLINE_SCORING_OPT',
    'PAIR_LANGUAGE_OPT',
    'PRODUCTION_OPT',
    'READ_LANGUAGE_OPT',
    'READ_OPT',
    'REGEX_CONTENT_OPT',
    'SCAN_OPT',
    'SIZE_DIALOGUE_OPT',
    'SIZE_TEXT_OPT',
    'SPEAKER_GENDER_OPT',
    'SPEAKER_OPT',
    'STYLE_OPT',
    'TOPIC_OPT',
    'TTS_MODEL',
    'USER_GENDER',
]

ENV_PREFIX = 'RELING_'

LAST_CONTENT_MARKER = '.'

API_KEY = Annotated[TyperExtraOption, typer.Option(
    envvar=f'{ENV_PREFIX}API_KEY',
    parser=TyperExtraOption.parser,
    help='your OpenAI API key',
    default_factory=TyperExtraOption.default_factory(
        prompt='Enter your OpenAI API key',
    ),
)]

MODEL = Annotated[TyperExtraOption, typer.Option(
    envvar=f'{ENV_PREFIX}MODEL',
    parser=TyperExtraOption.parser,
    help='identifier for the GPT model to be used',
    default_factory=TyperExtraOption.default_factory(
        prompt='Enter the GPT model identifier',
    ),
)]

TTS_MODEL = Annotated[TyperExtraOption, typer.Option(
    envvar=f'{ENV_PREFIX}TTS_MODEL',
    parser=TyperExtraOption.parser,
    help='identifier for the TTS model to be used',
    default_factory=TyperExtraOption.default_factory(
        prompt='Enter the TTS model identifier',
    ),
)]

ASR_MODEL = Annotated[TyperExtraOption, typer.Option(
    envvar=f'{ENV_PREFIX}ASR_MODEL',
    parser=TyperExtraOption.parser,
    help='identifier for the ASR model to be used',
    default_factory=TyperExtraOption.default_factory(
        prompt='Enter the ASR model identifier',
    ),
)]

USER_GENDER = Annotated[Gender, typer.Option(
    envvar=f'{ENV_PREFIX}USER_GENDER',
    parser=typer_enum_parser(Gender),
    help=f'user\'s gender, one of: {typer_enum_options(Gender)} (to customize the generated content)',
    prompt=f'Enter your gender ({typer_enum_options(Gender)})',
    autocompletion=typer_enum_autocompletion(Gender),
)]

type TextOrDialogue = Text | Dialogue  # Typer does not yet support union types (except for Optional)

CONTENT_ARG = Annotated[TextOrDialogue, typer.Argument(
    parser=typer_func_parser(lambda content_id: find_content(content_id, LAST_CONTENT_MARKER)),
    help=f'ID of the text or dialogue ("{LAST_CONTENT_MARKER}" for the last used content)',
    autocompletion=find_ids_by_prefix,
)]

LANGUAGE_ARG = Annotated[Language, typer.Argument(
    parser=typer_func_parser(find_language),
    help='language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT_ARG = Annotated[Language | None, typer.Argument(
    parser=typer_func_parser(find_language),
    help='language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT = Annotated[Language | None, typer.Option(
    parser=typer_func_parser(find_language),
    help='language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT_FROM = Annotated[Language | None, typer.Option(
    '--from',  # `from` is a reserved keyword
    parser=typer_func_parser(find_language),
    help='language code or name',
    autocompletion=find_languages_by_prefix,
)]

CONTENT_CATEGORY_OPT = Annotated[ContentCategory | None, typer.Option(
    parser=typer_enum_parser(ContentCategory),
    help=f'content category, one of: {typer_enum_options(ContentCategory)}',
    autocompletion=typer_enum_autocompletion(ContentCategory),
)]

LEVEL_OPT = Annotated[Level | None, typer.Option(
    parser=typer_enum_parser(Level),
    help=f'level, one of: {typer_enum_options(Level)}',
    autocompletion=typer_enum_autocompletion(Level),
)]

TOPIC_OPT = Annotated[str | None, typer.Option(
    help='topic of the content, e.g., "food" or "zoology"',
)]

STYLE_OPT = Annotated[str | None, typer.Option(
    help='style of the text, e.g., "mystery" or "news article"',
)]

SPEAKER_OPT = Annotated[str | None, typer.Option(
    help='interlocutor in the dialogue, e.g., "waiter" or "friend"',
)]

SPEAKER_GENDER_OPT = Annotated[Gender | None, typer.Option(
    parser=typer_enum_parser(Gender),
    help=f'interlocutor\'s gender, one of: {typer_enum_options(Gender)}',
    autocompletion=typer_enum_autocompletion(Gender),
)]

SIZE_TEXT_OPT = Annotated[int, typer.Option(
    min=1,
    help='number of sentences in the text',
)]

SIZE_DIALOGUE_OPT = Annotated[int, typer.Option(
    min=1,
    help='number of exchanges in the dialogue',
)]

INCLUDE_OPT = Annotated[list[str] | None, typer.Option(
    help=f'word(s) or phrase(s) to be included in the content '
         f'(e.g., "bank" or "bank{WordWithSense.DELIMITER_WITH_WHITE_SPACE}financial institution" for disambiguation)',
)]

NEW_ID_ARG = Annotated[str, typer.Argument(
    help='new ID for the text or dialogue',
)]

REGEX_CONTENT_OPT = Annotated[re.Pattern | None, typer.Option(
    parser=typer_regex_parser,
    help='regular expression to filter results by ID, content, topic, style, or speaker',
)]

CHECKPOINT_OPT = Annotated[list[datetime] | None, typer.Option(
    help='starting date(s) or time(s) to add statistics checkpoints',
    formats=[DATE_FORMAT, TIME_FORMAT],
)]

READ_LANGUAGE_OPT = Annotated[list[Language] | None, typer.Option(
    parser=typer_func_parser(find_language),
    help='language(s) to read the content out loud in',
    autocompletion=find_languages_by_prefix,
)]

READ_OPT = Annotated[bool | None, typer.Option(
    help='Read the content out loud.',
)]

LISTEN_OPT = Annotated[bool | None, typer.Option(
    help='Record the response as audio and transcribe it into text.',
)]

SCAN_OPT = Annotated[int | None, typer.Option(
    min=0,
    help='Capture the response using the specified camera index.',
)]

HIDE_PROMPTS_OPT = Annotated[bool | None, typer.Option(
    help='Hide the original language text and interlocutor\'s turn.',
)]

OFFLINE_SCORING_OPT = Annotated[bool | None, typer.Option(
    help='Score answers using an offline algorithm.',
)]

PAIR_LANGUAGE_OPT = Annotated[list[Language] | None, typer.Option(
    parser=typer_func_parser(find_language),
    help='language(s) to restrict statistics to translations between the main language and these languages',
    autocompletion=find_languages_by_prefix,
)]

GRAMMAR_OPT = Annotated[bool | None, typer.Option(
    help='Include statistics on learned words.',
)]

COMPREHENSION_OPT = Annotated[bool | None, typer.Option(
    help='Compute only comprehension-related statistics.',
)]

PRODUCTION_OPT = Annotated[bool | None, typer.Option(
    help='Compute only production-related statistics.',
)]

ARCHIVE_OPT = Annotated[bool | None, typer.Option(
    help='Search within archived items.',
)]

IDS_ONLY_OPT = Annotated[bool | None, typer.Option(
    help='Display only the IDs of the items.',
)]

FORCE_OPT = Annotated[bool | None, typer.Option(
    help='Force execution of the operation.',
)]
