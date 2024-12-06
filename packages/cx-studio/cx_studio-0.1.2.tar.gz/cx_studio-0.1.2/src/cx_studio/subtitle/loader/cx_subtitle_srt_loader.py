import re
from enum import StrEnum

from cx_studio.core import TCMode, Time, TimeCode
from .cx_subtitle_loader import SubtitleLoader
from ..cx_subtitle import StaticSubtitle


class SrtLoader(SubtitleLoader):
    class State(StrEnum):
        ExpectingNumber = "number"
        ExpectingTimecode = "timecode"
        ExpectingContent = "content"

    PATTERN_NUMBER = re.compile(r'^\d+$')
    PATTERN_TIME = re.compile(
        r'^(\d\d:\d\d:\d\d[,.]\d\d\d) --> (\d\d:\d\d:\d\d[,.]\d\d\d)$')

    def __init__(self, filename, encoding=None, newline='\n'):
        super().__init__(filename, encoding)
        self._newline = newline or ''
        self._file = None
        self._state = self.State.ExpectingNumber

    def open(self):
        self._file = open(self._filename, 'rt', self.encoding)
        return True

    def close(self):
        if self._file:
            self._file.close()

    def subtitles(self):
        start, end, content = Time(), Time(), []

        for a in self._file:
            line = str(a).strip()
            match self._state:
                case self.State.ExpectingNumber:
                    if self.PATTERN_NUMBER.fullmatch(line):
                        self._state = self.State.ExpectingTimecode
                case self.State.ExpectingTimecode:
                    match = self.PATTERN_TIME.fullmatch(line)
                    if match:
                        start = TimeCode(match.group(1), TCMode.Stamp).time
                        end = TimeCode(match.group(2), TCMode.Stamp).time
                        self._state = self.State.ExpectingContent
                case self.State.ExpectingContent:
                    if line:
                        content.append(line)
                    else:
                        yield StaticSubtitle(start=start,
                                             end=end,
                                             content=self._newline.join(
                                                 content))
                        self._state = self.State.ExpectingNumber
