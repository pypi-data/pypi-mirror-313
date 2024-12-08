from __future__ import annotations

from .table_str_enum import TableStrEnum

__all__ = [
    'Pos',
]


class Pos(TableStrEnum):
    NOUNS = 'nouns'
    VERBS = 'verbs'
    ADJECTIVES = 'adjectives'
    ADVERBS = 'adverbs'
    INTERJECTIONS = 'interjections'
    NUMERALS = 'numerals'
    PRONOUNS = 'pronouns'
    ADPOSITIONS = 'adpositions'
    CONJUNCTIONS = 'conjunctions'
    PARTICLES = 'particles'
    DETERMINERS = 'determiners'
    AUXILIARIES = 'auxiliaries'

    @staticmethod
    def from_upos(upos: str) -> Pos | None:
        match upos:
            case 'NOUN':
                return Pos.NOUNS
            case 'PROPN':
                return Pos.NOUNS
            case 'VERB':
                return Pos.VERBS
            case 'ADJ':
                return Pos.ADJECTIVES
            case 'ADV':
                return Pos.ADVERBS
            case 'INTJ':
                return Pos.INTERJECTIONS
            case 'NUM':
                return Pos.NUMERALS
            case 'PRON':
                return Pos.PRONOUNS
            case 'ADP':
                return Pos.ADPOSITIONS
            case 'CCONJ':
                return Pos.CONJUNCTIONS
            case 'SCONJ':
                return Pos.CONJUNCTIONS
            case 'PART':
                return Pos.PARTICLES
            case 'DET':
                return Pos.DETERMINERS
            case 'AUX':
                return Pos.AUXILIARIES
            case _:
                return None
