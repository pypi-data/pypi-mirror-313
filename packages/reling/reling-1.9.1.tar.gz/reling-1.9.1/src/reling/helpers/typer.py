from __future__ import annotations
from enum import Enum
import re
from typing import Callable, Never

import typer

from reling.types import Promise
from reling.utils.functions import named_function
from reling.utils.strings import replace_prefix_casing

__all__ = [
    'TyperExtraOption',
    'typer_enum_autocompletion',
    'typer_enum_options',
    'typer_enum_parser',
    'typer_func_parser',
    'typer_raise',
    'typer_raise_import',
    'typer_regex_parser',
]


def typer_raise(message: str) -> Never:
    typer.echo(message, err=True)
    raise typer.Exit(code=1)


def typer_raise_import(library: str) -> Never:
    typer_raise(f'{library} could not be imported. See Readme for installation instructions.')


def typer_func_parser[R](func: Callable[[str], R | None]) -> Callable[[str], R]:
    """Create a Typer argument parser from a function that returns a value or None."""

    @named_function('')
    def wrapper(arg: str) -> R:
        result = func(arg)
        if result is None:
            raise typer.BadParameter(arg)
        return result

    return wrapper


def typer_enum_options(enum: type[Enum]) -> str:
    """Return a string of the enum options for use in Typer help messages."""
    return ', '.join(f'"{member.lower()}"' for member in enum.__members__)


def typer_enum_parser(enum: type[Enum]) -> Callable[[str | Enum], Enum]:
    """Create a Typer argument parser from an Enum type."""

    @named_function('enum')
    def wrapper(arg: str | Enum) -> Enum:
        if isinstance(arg, Enum):  # Due to https://github.com/tiangolo/typer/discussions/720
            return arg
        for member in enum:
            if member.name.lower().startswith(arg.lower()):
                return member
        raise typer.BadParameter(
            f'{arg} (expected one of {typer_enum_options(enum)})',
        )

    return wrapper


@named_function('regex')
def typer_regex_parser(arg: str) -> re.Pattern:
    """Parse a regular expression string and return a compiled pattern or raise a Typer error."""
    try:
        return re.compile(arg)
    except re.error as e:
        raise typer.BadParameter(str(e))


def typer_enum_autocompletion(enum: type[Enum]) -> Callable[[str], list[str]]:
    """Create a Typer autocompletion function from an Enum type."""

    def wrapper(prefix: str) -> list[str]:
        lower = prefix.lower()
        return [
            replace_prefix_casing(member.lower(), prefix)
            for member in enum.__members__ if member.lower().startswith(lower)
        ]

    return wrapper


class TyperExtraOption:
    """A class for defining Typer options which are required in some cases but optional in others."""
    _prompt: str | None
    _data: str | None

    def __init__(self, *, prompt: str | None = None, data: str | None = None) -> None:
        self._prompt = prompt
        self._data = data

    @staticmethod
    @named_function('text')
    def parser(arg: str | TyperExtraOption) -> TyperExtraOption:
        # See https://github.com/tiangolo/typer/discussions/720
        return arg if isinstance(arg, TyperExtraOption) else TyperExtraOption(data=arg)

    @staticmethod
    def default_factory(prompt: str) -> Callable[[], TyperExtraOption]:
        return lambda: TyperExtraOption(prompt=prompt)

    def get(self) -> str:
        if self._data is None:
            self._data = typer.prompt(self._prompt)
        return self._data

    def promise(self) -> Promise[str]:
        return lambda: self.get()
