import re

from cx_studio.core import Time
from .cx_subtitle_loader import SubtitleLoader
from ..cx_subtitle import StaticSubtitle


class TxtLoader(SubtitleLoader):
    DURATION_PER_CHAR = 120
    MIN_DURATION_PER_LINE = 2000
    GAP_BETWEEN_ITEMS = 0
    TS_PATTERN = r'\s*\d{2}:\d{2}:\d{2}.\d{3}\s*'

    def __init__(self, filename, encoding=None,
                 duration_per_char: int = None,
                 min_duration_per_line: int = None,
                 gap_between_items: int = None):
        super().__init__(filename, encoding)
        self._file = None
        self._encoding = encoding
        self.duration_per_char = duration_per_char or self.DURATION_PER_CHAR
        self.gap_between_items = gap_between_items or self.GAP_BETWEEN_ITEMS
        self.min_duration_per_line = (
                min_duration_per_line or self.MIN_DURATION_PER_LINE)
        self._prev_time = Time()

    def open(self):
        self._file = open(self._filename, 'r', encoding=self.encoding)
        return True

    def close(self):
        if self._file:
            self._file.close()
        return True

    def subtitles(self):
        for line in self._file:
            content = re.sub(self.TS_PATTERN, '', line)
            duration = max(len(content) * self.duration_per_char,
                           self.min_duration_per_line)
            yield StaticSubtitle(
                start=self._prev_time,
                end=self._prev_time + Time(duration),
                content=content
            )
            self._prev_time += duration + self.gap_between_items
