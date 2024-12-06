import re
from functools import lru_cache
from pathlib import Path

from cx_studio.utils.textutils import contains_invisible_char, is_quoted, \
    quote_text


class TagSourcePath:
    SPACE_MODES = ['quote', 'escape', None]

    def __init__(self, path: Path, space_mode=None):
        self._source = Path(path)
        self._space_mode = space_mode

    @property
    @lru_cache
    def _neat_source(self):
        return self._source.resolve()

    @lru_cache
    def _handle(self, argument):
        match argument:
            case 'absolute':
                return self._neat_source.absolute()
            case 'name':
                return self._source.name
            case 'basename':
                name = self._source.name
                index = name.find('.')
                if index != -1:
                    return name[:index]
                else:
                    return name
            case 'suffix':
                return self._source.suffix
            case 'complete_suffix':
                return ''.join(self._source.suffixes)
            case 'suffix_no_dot':
                suffix = self._source.suffix
                if suffix.startswith('.'):
                    return suffix[1:]
                return suffix
            case 'complete_suffix_no_dot':
                suffix = ''.join(self._source.suffixes)
                if suffix.startswith('.'):
                    return suffix[1:]
                return suffix
            case 'complete_basename':
                return self._source.stem
            case 'parent':
                return self._source.parent
            case 'parent_absolute':
                return self._neat_source.parent.absolute()
            case 'parent_name':
                return self._source.parent.name
            case _:
                return self._source

    def __call__(self, argument):
        result = str(self._handle(argument))
        if is_quoted(result) and contains_invisible_char(result):
            if self._space_mode == 'quote':
                result = quote_text(result)
            elif self._space_mode == 'escape':
                result = re.sub(r'\s+', '\\ ', result)
        return result
