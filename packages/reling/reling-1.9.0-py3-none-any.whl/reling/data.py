from pathlib import Path

__all__ = [
    'LANGUAGES_PATH',
    'SPEAKERS_PATH',
    'STYLES_PATH',
    'TOPICS_PATH',
]

DATA = Path(__file__).parent / 'data'

LANGUAGES_PATH = DATA / 'languages.csv'
SPEAKERS_PATH = DATA / 'speakers.csv'
STYLES_PATH = DATA / 'styles.csv'
TOPICS_PATH = DATA / 'topics.csv'
