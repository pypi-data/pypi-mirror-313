from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from tempfile import mkstemp
from typing import Callable

from reling.db.models import Language
from reling.scanner import Scanner
from reling.types import Input, Transcriber
from reling.utils.console import clear_previous, input_and_erase, interruptible_input, print_and_erase
from reling.utils.prompts import ENTER, format_shortcut, Prompt
from .wave import FILE_EXTENSION, play, record

__all__ = [
    'get_input',
    'ScannerParams',
    'TranscriberParams',
]


class AudioAction(StrEnum):
    RE_RECORD = 're-record'
    LISTEN = 'listen'
    MANUAL_INPUT = 'manual input'


class ImageAction(StrEnum):
    RETAKE = 'retake'
    MANUAL_INPUT = 'manual input'


ENTER_TO_START_RECORDING = f'({ENTER} to start recording)'
RECORDING_REDO_SHORTCUT = AudioAction.RE_RECORD.value[0]
RECORDING_UNTIL_ENTER = f'(recording... {ENTER} to stop, {format_shortcut(RECORDING_REDO_SHORTCUT)} to redo)'
TRANSCRIBING = '(transcribing...)'

ENTER_TO_CAPTURE_IMAGE = f'({ENTER} to capture image)'
CAPTURING = '(capturing...)'
PROCESSING = '(processing...)'

PAUSED = f'PAUSED ({ENTER} to resume)'


@dataclass
class TranscriberParams:
    transcribe: Transcriber
    storage: Path


@dataclass
class ScannerParams:
    scanner: Scanner
    language: Language


def get_manual_input(prompt: str) -> Input:
    """Prompt the user for manual input."""
    return Input(interruptible_input(prompt))


def get_temp_file(storage: Path) -> Path:
    """Generate a temporary file in the given storage directory."""
    return Path(mkstemp(dir=storage, suffix=FILE_EXTENSION)[1])


def do_record(prompt: str, file: Path) -> bool:
    """Record audio and return whether the user is satisfied with the recording."""
    with record(file):
        return input_and_erase(prompt + RECORDING_UNTIL_ENTER).strip().lower() != RECORDING_REDO_SHORTCUT.lower()


def do_transcribe(prompt: str, transcribe: Transcriber, file: Path) -> str:
    """Transcribe the audio file and return the transcription."""
    with print_and_erase(prompt + TRANSCRIBING):
        try:
            return transcribe(file)
        except KeyboardInterrupt:
            return ''


def get_audio_input(prompt: str, params: TranscriberParams) -> Input | None:
    """
    Get input from the user via audio recording, with options for re-recording, listening, and manual input.
    :return: The user's input, or None if the user has chosen to manually input the text.
    """
    input_and_erase(prompt + ENTER_TO_START_RECORDING)
    file = get_temp_file(params.storage)
    while True:
        if not do_record(prompt, file):
            continue
        transcription = do_transcribe(prompt, params.transcribe, file)
        print(prompt + transcription)
        try:
            while True:
                match Prompt.from_enum(AudioAction).prompt():
                    case AudioAction.RE_RECORD:
                        clear_previous()
                        break
                    case AudioAction.LISTEN:
                        try:
                            play(file)
                        except KeyboardInterrupt:
                            pass
                    case AudioAction.MANUAL_INPUT:
                        clear_previous()
                        return None
                    case None:
                        return Input(transcription, audio=file)
                    case _:
                        assert False
        except KeyboardInterrupt:
            clear_previous()
            raise


def do_scan(prompt: str, scanner: Scanner, language: Language) -> str:
    """Capture an image and return the extracted text."""
    with print_and_erase(prompt + CAPTURING):
        try:
            image = scanner.capture()
        except KeyboardInterrupt:
            return ''
    with print_and_erase(prompt + PROCESSING):
        try:
            return scanner.process(image, language)
        except KeyboardInterrupt:
            return ''


def get_image_input(prompt: str, params: ScannerParams) -> Input | None:
    """
    Get input from the user via image capture, with options for retaking or manual input.
    :return: The user's input, or None if the user has chosen to manually input the text.
    """
    input_and_erase(prompt + ENTER_TO_CAPTURE_IMAGE)
    while True:
        text = do_scan(prompt, params.scanner, params.language)
        print(prompt + text)
        try:
            while True:
                match Prompt.from_enum(ImageAction).prompt():
                    case ImageAction.RETAKE:
                        clear_previous()
                        break
                    case ImageAction.MANUAL_INPUT:
                        clear_previous()
                        return None
                    case None:
                        return Input(text)
                    case _:
                        assert False
        except KeyboardInterrupt:
            clear_previous()
            raise


def get_input(
        on_pause: Callable[[], None],
        on_resume: Callable[[], None],
        prompt: str = '',
        transcriber_params: TranscriberParams | None = None,
        scanner_params: ScannerParams | None = None,
) -> Input:
    """Get user input, optionally via audio recording or image capture."""
    if transcriber_params and scanner_params:
        raise ValueError('Cannot use both transcriber and scanner')

    while True:
        try:
            return (
                (transcriber_params and get_audio_input(prompt, transcriber_params)) or
                (scanner_params and get_image_input(prompt, scanner_params)) or
                get_manual_input(prompt)
            )
        except KeyboardInterrupt:
            on_pause()
            input_and_erase(PAUSED)
            on_resume()
