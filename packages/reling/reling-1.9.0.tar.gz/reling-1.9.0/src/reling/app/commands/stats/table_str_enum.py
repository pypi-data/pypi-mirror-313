from enum import StrEnum

__all__ = [
    'TableStrEnum',
]


class TableStrEnum(StrEnum):
    def to_table_title(self) -> str:
        return self.value.capitalize()
