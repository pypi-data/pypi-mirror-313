from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Union

from ..cx_subtitle import StaticSubtitle


class SubtitleSaver(ABC):
    def __init__(self, filename: Union[str | PathLike], encoding=None):
        self._filename = Path(filename)
        self._encoding = encoding

    @property
    def encoding(self):
        if self._encoding and self._encoding != 'auto':
            return self._encoding
        return None

    @abstractmethod
    def open(self):
        return True

    @abstractmethod
    def close(self):
        return True

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    @abstractmethod
    def write_subtitle(self, subtitle: StaticSubtitle):
        pass
