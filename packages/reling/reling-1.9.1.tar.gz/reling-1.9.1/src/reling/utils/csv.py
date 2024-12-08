from pathlib import Path
from typing import Generator

__all__ = [
    'read_csv',
]

DELIMITER = ','


def read_csv(
        path: Path,
        columns: list[str],
        *,
        empty_as_none: bool = False,
) -> Generator[dict[str, str | None], None, None]:
    """Read a CSV file and yield dictionaries with column names as keys."""
    with path.open('r') as file:
        for line in file:
            yield {
                column: value if value != '' or not empty_as_none else None
                for column, value in zip(columns, line.strip().split(DELIMITER))
            }
