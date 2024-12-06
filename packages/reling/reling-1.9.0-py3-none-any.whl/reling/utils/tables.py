from typing import Iterable

from rich.console import Console, JustifyMethod
from rich.table import Table
from rich.text import Text

__all__ = [
    'build_table',
    'DEFAULT_JUSTIFY_METHOD',
    'GROUPING_COLUMN',
    'JustifyMethod',
    'Table',
    'print_table',
]

GROUPING_COLUMN = '__grouping_column__'

DEFAULT_JUSTIFY_METHOD: JustifyMethod = 'left'
HEADER_JUSTIFY_METHOD: JustifyMethod = 'center'


def build_table(
        *,
        title: str | None = None,
        headers: list[str],
        data: Iterable[dict[str, str | Text]],
        justify: dict[str, JustifyMethod] | None = None,
        widths: dict[str, int | None] | None = None,
        group_by: list[str] | None = None,
) -> Table:
    """
    Build a Rich Table from headers and data.

    :param title: Table title.
    :param headers: List of column headers.
    :param data: Iterable of dictionaries with data. Keys, except for GROUPING_COLUMN, must match headers.
    :param justify: Dictionary of column justifications. Keys must be in headers. Default is DEFAULT_JUSTIFY_METHOD.
    :param widths: Dictionary of column widths. Keys must be in headers. Default is None (auto-size).
    :param group_by: List of columns to group by: rows with the same values in these columns will be grouped together.
                     Only the first row of each group will have the group values displayed.
    :return: Rich Table.
    """
    justify = justify or {}
    if any(col not in headers for col in justify.keys()):
        raise ValueError('Justify columns must be in headers.')

    widths = widths or {}
    if any(col not in headers for col in widths.keys()):
        raise ValueError('Width columns must be in headers.')

    table = Table(title=title)
    for header in headers:
        table.add_column(
            Text(header, justify=HEADER_JUSTIFY_METHOD),
            justify=justify.get(header, DEFAULT_JUSTIFY_METHOD),
            width=widths.get(header),
        )

    group_by = group_by or []
    if any(col not in headers for col in group_by if col != GROUPING_COLUMN):
        raise ValueError('Group by columns must be in headers.')
    last_group: tuple[str, ...] | None = None

    for row in data:
        if sorted(set(row.keys()) - {GROUPING_COLUMN}) != sorted(headers):
            raise ValueError('Data keys must match headers.')
        if GROUPING_COLUMN in group_by and GROUPING_COLUMN not in row:
            raise ValueError(f'{GROUPING_COLUMN} must be in data if {GROUPING_COLUMN} is in group_by.')
        group = tuple(row[col] for col in group_by)
        if new_section := group != last_group:
            last_group = group
            table.add_section()
        table.add_row(*[row[col]
                        if new_section or col not in group_by
                        else ''
                        for col in headers])

    return table


def print_table(table: Table) -> None:
    Console().print(table)
