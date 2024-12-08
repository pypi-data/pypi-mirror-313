from abc import ABC, abstractmethod
from queue import Queue

__all__ = [
    'Feeder',
    'LineFeeder',
]


class Feeder(ABC):
    """
    Feeder can be fed chunks of text data. It then processes the data and provides it in a different form
    (say, line-by-line).
    """

    @abstractmethod
    def put(self, chunk: str) -> None:
        """Feed a chunk of data."""
        pass

    @abstractmethod
    def end(self) -> None:
        """Signal the end of the data."""
        pass

    @abstractmethod
    def get(self) -> str | None:
        """Get the next piece of data or None if there is no more data ready."""
        pass


class LineFeeder(Feeder):
    """
    Feeder that provides data line-by-line when the lines are ready.
    If the data ends with \n, the last empty line is not included.
    """

    _lines: Queue[str]
    _buffer: list[str]

    def __init__(self) -> None:
        self._lines = Queue()
        self._buffer = []

    def put(self, chunk: str) -> None:
        lines = chunk.split('\n')
        self._buffer.append(lines[0])
        if len(lines) > 1:
            self._lines.put(''.join(self._buffer))
            for line in lines[1:-1]:
                self._lines.put(line)
            self._buffer.clear()
            self._buffer.append(lines[-1])

    def end(self) -> None:
        if line := ''.join(self._buffer):
            self._lines.put(line)
        self._buffer.clear()

    def get(self) -> str | None:
        return self._lines.get() if not self._lines.empty() else None
