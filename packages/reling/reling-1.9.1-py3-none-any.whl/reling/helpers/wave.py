from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import Generator, Mapping
import wave

from reling.types import Speed
from .pyaudio import get_audio, get_stream

__all__ = [
    'FILE_EXTENSION',
    'play',
    'record',
]

FILE_EXTENSION = '.wav'

CHUNK_SIZE = 1024

RECORD_CHANNELS = 1
RECORD_RATE = 16000
RECORD_BITS_PER_SAMPLE = 16


@contextmanager
def write(
        file: Path,
        channels: int,
        sample_width: int,
        rate: float,
) -> Generator[wave.Wave_write, None, None]:
    """Initialize a WAV file for writing, yield it, and close it afterward."""
    wav = wave.open(str(file.absolute()), 'wb')
    try:
        wav.setnchannels(channels)
        wav.setsampwidth(sample_width)
        wav.setframerate(rate)
        yield wav
    finally:
        wav.close()


def play(file: Path, speed: Speed = Speed.NORMAL) -> None:
    """Play a WAV file."""
    with (
        wave.open(str(file.absolute()), 'rb') as wav,
        get_audio() as pyaudio,
        get_stream(
            pyaudio=pyaudio,
            format=pyaudio.audio.get_format_from_width(wav.getsampwidth()),
            channels=wav.getnchannels(),
            rate=int(wav.getframerate() * speed.value),
            output=True,
        ) as stream,
    ):
        data = wav.readframes(CHUNK_SIZE)
        while data:
            stream.write(data)
            data = wav.readframes(CHUNK_SIZE)


def record_on_data(
        wav: wave.Wave_write,
        flag_to_return: int,
        data: bytes,
        _frame_count: int,
        _time_info: Mapping[str, float],
        _status_flags: int,
) -> tuple[None, int]:
    """Implement the stream callback for recording audio."""
    wav.writeframes(data)
    return None, flag_to_return


@contextmanager
def record(file: Path) -> Generator[None, None, None]:
    """Record audio in real time and save it to a file."""
    with (
        write(
            file,
            channels=RECORD_CHANNELS,
            sample_width=RECORD_BITS_PER_SAMPLE // 8,
            rate=RECORD_RATE,
        ) as wav,
        get_audio() as pyaudio,
        get_stream(
            pyaudio=pyaudio,
            format=pyaudio.paInt16,
            channels=RECORD_CHANNELS,
            rate=RECORD_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
            stream_callback=partial(record_on_data, wav, pyaudio.paContinue),
        ),
    ):
        yield
