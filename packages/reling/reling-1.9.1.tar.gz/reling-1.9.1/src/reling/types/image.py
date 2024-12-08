__all__ = [
    'Image',
]


class Image:
    _url: str

    def __init__(self, url: str) -> None:
        self._url = url

    def get_url(self) -> str:
        return self._url
