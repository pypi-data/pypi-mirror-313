from enum import StrEnum

from reling.db.enums import Gender

__all__ = [
    'Voice',
]


class Voice(StrEnum):
    ALLOY = 'alloy'
    ECHO = 'echo'
    FABLE = 'fable'
    ONYX = 'onyx'
    NOVA = 'nova'
    SHIMMER = 'shimmer'

    @property
    def gender(self) -> Gender:
        match self:
            case Voice.ALLOY:
                return Gender.NONBINARY
            case Voice.ECHO:
                return Gender.MALE
            case Voice.FABLE:
                return Gender.NONBINARY
            case Voice.ONYX:
                return Gender.MALE
            case Voice.NOVA:
                return Gender.FEMALE
            case Voice.SHIMMER:
                return Gender.FEMALE
            case _:
                raise ValueError(f'Unknown voice: {self}')
