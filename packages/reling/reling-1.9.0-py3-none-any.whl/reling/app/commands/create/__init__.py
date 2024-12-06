from random import choice
from tqdm import tqdm
import typer

from reling.app.app import app
from reling.app.default_content import set_default_content
from reling.app.types import (
    API_KEY,
    INCLUDE_OPT,
    LANGUAGE_ARG,
    LEVEL_OPT,
    MODEL,
    SIZE_DIALOGUE_OPT,
    SIZE_TEXT_OPT,
    SPEAKER_GENDER_OPT,
    SPEAKER_OPT,
    STYLE_OPT,
    TOPIC_OPT,
    USER_GENDER,
)
from reling.db.enums import Gender, Level
from reling.db.helpers.modifiers import get_random_modifier
from reling.db.models import Speaker, Style, Topic
from reling.gpt import GPTClient
from reling.helpers.typer import typer_raise
from reling.types import WordWithSense
from .generation import generate_dialogue_exchanges, generate_id, generate_text_sentences
from .storage import save_dialogue, save_text

__all__ = [
    'create',
]

DEFAULT_SIZE_TEXT = 10
DEFAULT_SIZE_DIALOGUE = 10

MIN_SIZE_THRESHOLD = 0.9

create = typer.Typer()
app.add_typer(
    create,
    name='create',
    help='Create a new text or dialogue.',
)


@create.command()
def text(
        api_key: API_KEY,
        model: MODEL,
        language: LANGUAGE_ARG,
        level: LEVEL_OPT = Level.INTERMEDIATE,
        topic: TOPIC_OPT = None,
        style: STYLE_OPT = None,
        size: SIZE_TEXT_OPT = DEFAULT_SIZE_TEXT,
        include: INCLUDE_OPT = None,
) -> None:
    """Create a text and save it to the database."""
    gpt = GPTClient(api_key=api_key.get(), model=model.get())
    topic = topic or get_random_modifier(Topic).name
    style = style or get_random_modifier(Style).name

    sentences = list(tqdm(
        generate_text_sentences(
            gpt=gpt,
            num_sentences=size,
            language=language,
            level=level,
            topic=topic,
            style=style,
            include=list(map(WordWithSense.parse, include or [])),
        ),
        desc=f'Generating text in {language.name}',
        total=size,
        leave=False,
    ))
    if len(sentences) < round(size * MIN_SIZE_THRESHOLD):
        typer_raise('Failed to generate the text.')

    content = save_text(
        suggested_id=generate_id(gpt, sentences),
        sentences=sentences,
        language=language,
        level=level,
        topic=topic,
        style=style,
    )
    set_default_content(content)
    print(f'Generated text with the following ID:\n{content.id}')


@create.command()
def dialogue(
        api_key: API_KEY,
        model: MODEL,
        user_gender: USER_GENDER,
        language: LANGUAGE_ARG,
        level: LEVEL_OPT = Level.INTERMEDIATE,
        speaker: SPEAKER_OPT = None,
        speaker_gender: SPEAKER_GENDER_OPT = None,
        topic: TOPIC_OPT = None,
        size: SIZE_DIALOGUE_OPT = DEFAULT_SIZE_DIALOGUE,
        include: INCLUDE_OPT = None,
) -> None:
    """Create a dialogue and save it to the database."""
    gpt = GPTClient(api_key=api_key.get(), model=model.get())
    speaker = speaker or get_random_modifier(Speaker).name
    speaker_gender = speaker_gender or choice([Gender.MALE, Gender.FEMALE])

    exchanges = list(tqdm(
        generate_dialogue_exchanges(
            gpt=gpt,
            num_exchanges=size,
            language=language,
            level=level,
            user_gender=user_gender,
            speaker=speaker,
            speaker_gender=speaker_gender,
            topic=topic,
            include=list(map(WordWithSense.parse, include or [])),
        ),
        desc=f'Generating dialogue in {language.name}',
        total=size,
        leave=False,
    ))
    if len(exchanges) < round(size * MIN_SIZE_THRESHOLD):
        typer_raise('Failed to generate the dialogue.')

    content = save_dialogue(
        suggested_id=generate_id(gpt, [turn for exchange in exchanges for turn in exchange.all()]),
        exchanges=exchanges,
        language=language,
        level=level,
        speaker=speaker,
        topic=topic,
        speaker_gender=speaker_gender,
        user_gender=user_gender,
    )
    set_default_content(content)
    print(f'Generated dialogue with the following ID:\n{content.id}')
