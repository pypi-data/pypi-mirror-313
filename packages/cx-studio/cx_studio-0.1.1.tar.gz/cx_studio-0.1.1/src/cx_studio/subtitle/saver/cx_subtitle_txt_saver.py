from cx_studio.core import TimeCode
from .cx_subtitle_saver import SubtitleSaver
from ..cx_subtitle import StaticSubtitle


class TxtSaver(SubtitleSaver):
    def __init__(self, filename, encoding=None, newline=None,
                 time_pattern=None):
        super().__init__(filename, encoding)
        self._newline = newline or ''
        self._time_pattern = time_pattern
        self._file = None

    def _compile_content(self, subtitle: StaticSubtitle):
        _time = ''
        if self._time_pattern:
            start_tc = TimeCode(subtitle.start)
            end_tc = TimeCode(subtitle.end)
            duration_tc = TimeCode(subtitle.duration())
            _time = str(self._time_pattern).format(start=start_tc, end=end_tc,
                                                   duration=duration_tc)
        _contents = subtitle.content.splitlines()
        return f'{_time}{self._newline.join(_contents)}\n'

    def open(self):
        self._file = open(self._filename, 'wt', encoding=self.encoding)
        return True

    def close(self):
        if self._file:
            self._file.flush()
            self._file.close()
        return True

    def write_subtitle(self, subtitle: StaticSubtitle):
        line = self._compile_content(subtitle)
        self._file.write(line)
