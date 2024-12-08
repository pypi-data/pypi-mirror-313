from __future__ import annotations
import base64
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import cv2

from reling.db.models import Language
from reling.gpt import GPTClient
from reling.helpers.typer import typer_raise, typer_raise_import
from reling.types import Image
from reling.utils.transformers import strip

__all__ = [
    'Scanner',
    'ScannerManager',
    'ScannerParams',
]

IMAGE_EXTENSION = '.jpg'
IMAGE_URL_FORMAT = 'data:image/jpeg;base64,{image}'


@dataclass
class ScannerParams:
    camera_index: int
    gpt: GPTClient


class Scanner:
    _camera: cv2.VideoCapture
    _gpt: GPTClient

    def __init__(self, params: ScannerParams) -> None:
        try:
            import cv2
        except ImportError:
            typer_raise_import('OpenCV')
        self._camera = cv2.VideoCapture(params.camera_index)
        if not self._camera.isOpened():
            typer_raise(f'Camera with index {params.camera_index} is not available.')
        self._gpt = params.gpt

    def release(self) -> None:
        self._camera.release()

    def capture(self) -> Image:
        """Capture an image from the camera."""
        success, frame = self._camera.read()
        if not success:
            typer_raise('Failed to capture an image.')
        import cv2
        success, buffer = cv2.imencode(IMAGE_EXTENSION, frame)
        if not success:
            typer_raise('Failed to encode the image.')
        return Image(IMAGE_URL_FORMAT.format(image=base64.b64encode(buffer).decode('utf-8')))

    def process(self, image: Image, language: Language) -> str:
        """Process the image and extract text in the specified language."""
        return list(self._gpt.ask(
            '\n'.join([
                f'What is written in the following image? The text is in {language.name}.',
                f'It might be written across several lines, but it forms a single sentence or paragraph.',
                f'Please provide your answer in a single line. Say nothing else.',
                f'If no text in {language.name} is detected, write three dots.',
            ]),
            image=image,
            creative=False,
            transformers=[strip],
        ))[0]


class ScannerManager:
    _params: ScannerParams | None

    def __init__(self, params: ScannerParams | None) -> None:
        self._params = params

    @contextmanager
    def get_scanner(self) -> Scanner | None:
        if self._params is None:
            yield None
        else:
            scanner = Scanner(self._params)
            try:
                yield scanner
            finally:
                scanner.release()
