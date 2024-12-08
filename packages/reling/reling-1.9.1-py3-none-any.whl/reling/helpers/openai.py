from contextlib import contextmanager
from typing import Generator

from openai import APIError

from .typer import typer_raise

__all__ = [
    'openai_handler',
]


@contextmanager
def openai_handler() -> Generator[None, None, None]:
    try:
        yield
    except APIError as e:
        typer_raise(f'OpenAI API error:\n{e}')
