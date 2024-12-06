from random import shuffle
from typing import cast

from reling.db.enums import Gender
from reling.tts import Voice

__all__ = [
    'pick_voice',
    'pick_voices',
]


def pick_voices(*positions: Gender | None) -> tuple[Voice, ...]:
    """
    Pick random non-repeating voices of the specified genders
    (`None` denoting no gender preference for the given position).

    :raises ValueError: If there are not enough voices to satisfy the requirements.
    """
    pools: dict[Gender | None, list[Voice]] = {None: []}

    for gender in Gender:
        gender_voices = [cast(Voice, voice) for voice in Voice if cast(Voice, voice).gender == gender]

        required_count = positions.count(gender)
        if len(gender_voices) < required_count:
            raise ValueError(f'Not enough voices of {gender}')

        shuffle(gender_voices)
        pools[cast(Gender, gender)] = gender_voices[:required_count]
        pools[None].extend(gender_voices[required_count:])

    if len(pools[None]) < positions.count(None):
        raise ValueError('Not enough voices')

    shuffle(pools[None])
    return tuple(pools[position].pop() for position in positions)


def pick_voice(gender: Gender | None = None) -> Voice:
    """Pick a random voice of the specified gender (`None` denoting no gender preference)."""
    return pick_voices(gender)[0]
