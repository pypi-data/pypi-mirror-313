from typing import Generator

from openai import OpenAI

from reling.helpers.openai import openai_handler
from reling.types import Image
from reling.utils.feeders import Feeder, LineFeeder
from reling.utils.transformers import normalize, Transformer

__all__ = [
    'GPTClient',
]

CREATIVE_TEMPERATURE = 1.0


class GPTClient:
    _client: OpenAI
    _model: str

    def __init__(self, *, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def ask(
            self,
            prompt: str,
            image: Image | None = None,
            creative: bool = True,
            feeder_type: type[Feeder] = LineFeeder,
            transformers: list[Transformer] | None = None,
            auto_normalize: bool = True,
    ) -> Generator[str, None, None]:
        """
        Ask the model a question and yield sections of the response as they become available, applying transformers.
        """
        feeder = feeder_type()

        with openai_handler():
            stream = self._client.chat.completions.create(
                model=self._model,
                stream=True,
                messages=[{'role': 'user', 'content': [
                    {'type': 'text', 'text': prompt},
                    *([{'type': 'image_url', 'image_url': {'url': image.get_url()}}] if image else []),
                ]}],
                temperature=CREATIVE_TEMPERATURE if creative else 0.0,
            )

        section_index = 0

        def flush() -> Generator[str, None, None]:
            nonlocal section_index
            while (section := feeder.get()) is not None:
                for transformer in (transformers or []) + ([normalize] if auto_normalize else []):
                    section = transformer(section, section_index)
                    if section is None:
                        break
                else:
                    yield section
                    section_index += 1

        for chunk in stream:
            feeder.put(chunk.choices[0].delta.content or '')
            yield from flush()

        feeder.end()
        yield from flush()
