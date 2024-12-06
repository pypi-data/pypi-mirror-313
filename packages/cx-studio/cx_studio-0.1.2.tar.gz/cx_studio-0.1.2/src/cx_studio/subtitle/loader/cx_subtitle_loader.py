from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Union

from cx_studio.utils import detect_encoding


class SubtitleLoader(ABC):
    def __init__(self, filename: Union[str | PathLike], encoding=None):
        self._filename = Path(filename)
        self._encoding = str(encoding)

    @property
    def encoding(self):
        if self._encoding and self._encoding != 'auto':
            return self._encoding
        return detect_encoding(self._filename)

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
    def subtitles(self):
        pass
