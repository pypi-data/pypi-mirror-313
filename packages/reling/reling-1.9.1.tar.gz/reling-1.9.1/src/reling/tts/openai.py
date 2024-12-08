from openai import OpenAI

from reling.helpers.openai import openai_handler
from reling.helpers.pyaudio import get_audio, get_stream
from reling.types import Speed
from .tts_client import TTSClient
from .voices import Voice

__all__ = [
    'OpenAITTSClient',
]

CHANNELS = 1
RATE = 24000
CHUNK_SIZE = 1024
RESPONSE_FORMAT = 'pcm'


class OpenAITTSClient(TTSClient):
    _client: OpenAI
    _model: str

    def __init__(self, *, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def read(self, text: str, voice: Voice, speed: Speed) -> None:
        with (
            get_audio() as pyaudio,
            get_stream(
                pyaudio=pyaudio,
                format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                output=True,
            ) as stream,
            openai_handler(),
            self._client.audio.speech.with_streaming_response.create(
                model=self._model,
                voice=voice.value,
                response_format=RESPONSE_FORMAT,
                input=text,
                speed=speed.value,
            ) as response,
        ):
            for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                stream.write(chunk)
