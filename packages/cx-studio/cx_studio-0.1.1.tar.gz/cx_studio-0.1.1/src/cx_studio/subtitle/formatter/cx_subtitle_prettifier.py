import dataclasses
import re

from .cx_subtitle_processor import SubtitleProcessor
from ..cx_subtitle import StaticSubtitle


class SubtitlePrettifier(SubtitleProcessor):
    def __init__(self, **kwargs):
        super(SubtitlePrettifier, self).__init__()
        self.replacements = {'\t': ' '}

        self.remove_xml_tags = True

        self.normal_strip = True
        self.quotes_strip = True
        self.extra_strip = ''

        self.remove_empty_lines = True
        self.shrink_long_spaces = True
        self.shrink_long_quotes = True

        self.remove_empty_subtitles = True
        self.remove_zero_duration_subtitles = True

        self.__dict__.update(kwargs)

    def __basic_content_cleaning(self, content: str):
        result = content
        for k, v in self.replacements.items():
            result = re.sub(k, v, result)
        result = re.sub(r'\r\n', r'\n', result)
        return result

    @staticmethod
    def _remove_xml_tags(content: str):
        return re.sub(
            r'<(\w+)>([^<>]*)</\1>',
            r'\2',
            content
        )

    def _strip(self, content: str):
        result = str(content)
        while True:
            current = result
            if self.normal_strip:
                current = current.strip()
            if self.quotes_strip:
                current = current.strip('\'"‘’“”')
            if self.extra_strip:
                current = current.strip(self.extra_strip)
            if current == result:
                break
            result = current
        return result

    @staticmethod
    def _remove_empty_lines(content: str):
        return re.sub(r'\n\s+', r'\n', content)

    @staticmethod
    def _shrink_long_spaces(content: str):
        return re.sub(r' +', r' ', content)

    @staticmethod
    def _shrink_long_quotes(content: str):
        return re.sub(r'([\'\"‘“”’])+', r'\1', content)

    def is_subtitle_legal(self, subtitle: StaticSubtitle) -> bool:
        if self.remove_empty_subtitles and not subtitle.content:
            return False
        if self.remove_zero_duration_subtitles and subtitle.duration() == 0:
            return False
        return True

    def __call__(self, subtitle: StaticSubtitle):
        content = self.__basic_content_cleaning(subtitle.content)
        content = self._strip(content)
        if self.remove_xml_tags:
            content = self._remove_xml_tags(content)
        if self.remove_empty_lines:
            content = self._remove_empty_lines(content)
        if self.shrink_long_spaces:
            content = self._shrink_long_spaces(content)
        if self.shrink_long_quotes:
            content = self._shrink_long_quotes(content)
        result = dataclasses.replace(subtitle, content=content)
        return result if self.is_subtitle_legal(result) else None
