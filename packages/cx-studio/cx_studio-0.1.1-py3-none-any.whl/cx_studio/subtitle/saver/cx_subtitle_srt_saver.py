from cx_studio.core import TimeCode
from .cx_subtitle_saver import SubtitleSaver
from ..cx_subtitle import StaticSubtitle


class SrtSaver(SubtitleSaver):
    SUBTITLE_PATTERN = '{number}\n{start} --> {end}\n{content}\n\n'

    def __init__(self, filename, encoding=None, newline='\n'):
        super().__init__(filename, encoding)
        self._newline = newline or ''
        self._file = None
        self._number = 1

    def open(self):
        self._file = open(self._filename, 'wt', encoding=self.encoding)
        return True

    def close(self):
        if self._file:
            self._file.flush()
            self._file.close()
        return True

    def _compile_content(self, number: int, subtitle: StaticSubtitle):
        start = TimeCode(subtitle.start)
        end = TimeCode(subtitle.end)
        contents = subtitle.content.splitlines()
        return self.SUBTITLE_PATTERN.format(
            number=number,
            start=start, end=end,
            content=self._newline.join(contents)
        )

    def write_subtitle(self, subtitle: StaticSubtitle):
        compiled_subtitle = self._compile_content(self._number, subtitle)
        self._file.write(compiled_subtitle)
        self._number += 1
