from datetime import datetime, timedelta

from .time import now

__all__ = [
    'TimeTracker',
]


class TimeTracker:
    started_at: datetime
    finished_at: datetime | None
    total_pause_time: timedelta
    _paused_at: datetime | None

    def __init__(self) -> None:
        self.started_at = now()
        self.finished_at = None
        self.total_pause_time = timedelta()
        self._paused_at = None

    def stop(self) -> None:
        self.finished_at = now()

    def pause(self) -> None:
        if self._paused_at is not None:
            raise RuntimeError('Already paused')
        self._paused_at = now()

    def resume(self) -> None:
        if self._paused_at is None:
            raise RuntimeError('Not paused')
        self.total_pause_time += now() - self._paused_at
        self._paused_at = None
