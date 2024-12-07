from typing import Mapping

from jinja2 import DictLoader


class RegisteredLoader(DictLoader):
    """Loader for templates specified by user code."""

    pass


class UrlLoader(DictLoader):
    """Loader for templates loaded by the user from a URL."""

    url: str

    def __init__(self, mapping: Mapping[str, str], url: str) -> None:
        self.url = url
        super().__init__(mapping)
