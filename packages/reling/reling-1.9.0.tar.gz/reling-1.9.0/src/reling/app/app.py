try:
    import readline  # noqa: F401 (https://stackoverflow.com/a/14796424/430083)
except ImportError:
    pass  # Windows

import typer

__all__ = [
    'app',
]

app = typer.Typer(pretty_exceptions_enable=False)
