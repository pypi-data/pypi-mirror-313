import os
from pathlib import Path
import sys

__all__ = [
    'get_app_data_parent',
]


def get_app_data_parent() -> Path:
    """Get the parent directory for the app's data directory."""
    home = Path.home()
    if os.name == 'nt':  # Windows
        return home / 'AppData' / 'Local'
    elif os.name == 'posix':
        if sys.platform == 'darwin':  # MacOS
            return home / 'Library' / 'Application Support'
        else:  # Linux
            return Path(os.getenv('XDG_DATA_HOME', home / '.local' / 'share'))
    else:
        return home
