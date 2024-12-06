from reling.app.app import app
from reling.app.db import get_db_path

__all__ = [
    'db',
]


@app.command()
def db() -> None:
    """Display the file path of the database."""
    print(get_db_path().absolute())
