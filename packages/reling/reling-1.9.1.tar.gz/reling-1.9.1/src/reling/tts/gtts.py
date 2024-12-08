from io import BytesIO

from reling.db.models import Language
from reling.helpers.typer import typer_raise
from reling.types import Speed
from .tts_client import TTSClient
from .voices import Voice

__all__ = [
    'GTTSClient',
]

FORMAT = 'mp3'


class GTTSClient(TTSClient):
    _language_code: str

    def __init__(self, language: Language) -> None:
        self._language_code = language.short_code

    def read(self, text: str, _voice: Voice, speed: Speed) -> None:
        if not text.strip():
            return

        # Only import the modules if audio is used
        from gtts import gTTS, gTTSError
        from pydub import AudioSegment
        from pydub.playback import play

        try:
            tts = gTTS(
                text=text,
                lang=self._language_code,
                slow=speed == Speed.SLOW,
            )
        except (AssertionError, RuntimeError, ValueError) as e:
            typer_raise(f'Failed to generate audio: {e}')
        audio_data = BytesIO()
        try:
            tts.write_to_fp(audio_data)
            audio_data.seek(0)
            audio_segment = AudioSegment.from_file(audio_data, format=FORMAT)
            play(audio_segment)
        except gTTSError as e:
            typer_raise(f'Failed to generate audio: {e}')
        finally:
            audio_data.close()
