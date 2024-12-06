from reling.db.models import Language
from reling.types import Promise
from .gtts import GTTSClient
from .openai import OpenAITTSClient
from .tts_client import TTSClient, TTSVoiceClient
from .voices import Voice

__all__ = [
    'get_tts_client',
    'TTSClient',
    'TTSVoiceClient',
    'Voice',
]

GTTS_MODEL = '_gtts'


def get_tts_client(model: str, api_key: Promise[str], language: Language) -> TTSClient:
    if model == GTTS_MODEL:
        return GTTSClient(language)
    else:
        return OpenAITTSClient(api_key=api_key(), model=model)
