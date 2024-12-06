from reling.data import LANGUAGES_PATH, SPEAKERS_PATH, STYLES_PATH, TOPICS_PATH
from reling.db.helpers.languages import populate_languages
from reling.db.helpers.modifiers import populate_modifiers
from reling.db.models import Speaker, Style, Topic
from reling.helpers.paths import get_app_data_parent
from reling.shelf import init_shelf
from reling.utils.strings import char_range
from . import commands  # Register commands with Typer
from .app import app
from .db import DatabaseVersion, init_db

__all__ = [
    'app',
]

APP_NAME = 'ReLing'

LATEST_DB_VERSION = 'c'
OLDEST_DB_VERSION = 'a'
DB_NAME = 'reling-{version}.db'

SHELF_NAME = 'shelf'

# This code must run both during app execution and on auto-completion.
# Therefore, it should be placed at the top level of the module.
DATA_PATH = get_app_data_parent() / APP_NAME
DATA_PATH.mkdir(parents=True, exist_ok=True)
init_shelf(DATA_PATH / SHELF_NAME)
init_db(DatabaseVersion(version, DATA_PATH / DB_NAME.format(version=version))
        for version in char_range(LATEST_DB_VERSION, OLDEST_DB_VERSION))
populate_languages(LANGUAGES_PATH)
populate_modifiers(Topic, TOPICS_PATH)
populate_modifiers(Style, STYLES_PATH)
populate_modifiers(Speaker, SPEAKERS_PATH)
