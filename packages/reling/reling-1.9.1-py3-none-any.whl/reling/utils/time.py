from datetime import datetime, timedelta, UTC

import pytz

__all__ = [
    'DATE_FORMAT',
    'format_time',
    'format_time_delta',
    'local_to_utc',
    'now',
    'TIME_FORMAT',
]

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = f'{DATE_FORMAT}, %H:%M'


def now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def local_to_utc(time: datetime) -> datetime:
    return time.astimezone(UTC).replace(tzinfo=None)


def format_time(time: datetime, omit_zero_time: bool = False) -> str:
    localized = pytz.utc.localize(time).astimezone()
    return localized.strftime(
        DATE_FORMAT if omit_zero_time and localized.time() == datetime.min.time() else TIME_FORMAT,
    )


def format_time_delta(delta: timedelta) -> str:
    """Format timedelta as follows: '[[H:]MM:]SS'."""
    total_seconds = int(delta.total_seconds())

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f'{hours}:{minutes:02}:{seconds:02}'
    else:
        return f'{minutes}:{seconds:02}'
