from .table_str_enum import TableStrEnum

__all__ = [
    'Modality',
]


class Modality(TableStrEnum):
    COMPREHENSION = 'comprehension'
    PRODUCTION = 'production'
