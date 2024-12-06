from .typer import typer_raise_import

__all__ = [
    'ensure_audio',
]


def ensure_audio() -> None:
    """Ensure the tool is installed with the necessary audio dependencies."""
    try:
        import pyaudio
    except ImportError:
        typer_raise_import('Audio dependencies')
