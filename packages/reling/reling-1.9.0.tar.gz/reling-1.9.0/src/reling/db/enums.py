from enum import StrEnum

__all__ = [
    'ContentCategory',
    'Gender',
    'Level',
]


class ContentCategory(StrEnum):
    TEXT = 'text'
    DIALOGUE = 'dialogue'


class Level(StrEnum):
    BASIC = 'basic'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'


class Gender(StrEnum):
    MALE = 'male'
    FEMALE = 'female'
    NONBINARY = 'nonbinary'

    def describe(self) -> str:
        match self:
            case Gender.MALE:
                return 'a male'
            case Gender.FEMALE:
                return 'a female'
            case Gender.NONBINARY:
                return 'a nonbinary person'
