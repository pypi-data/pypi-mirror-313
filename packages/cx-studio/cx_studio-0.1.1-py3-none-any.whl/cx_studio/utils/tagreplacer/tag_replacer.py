import re


class TagReplacer:
    TAG_PATTERN = re.compile(r"\${([^:{}]+)(?::([^:{}]+))?}")

    def __init__(self, keep_unknown_tags=True, default_data=""):
        self._data_sources = {}
        self._keep_unknown_tags = keep_unknown_tags
        self._default_data = default_data

    def install_data_source(self, tag: str, source):
        if callable(source):
            self._data_sources[tag] = source
        else:
            self._data_sources[tag] = str(source)
        return self

    def tags(self):
        return self._data_sources.keys()

    def __lookup_match(self, match: re.Match):
        tag = match.group(1)
        param = match.group(2) or None
        if tag in self._data_sources:
            source = self._data_sources[tag]
            if callable(source):
                return source(param)
            elif isinstance(source, str):
                return source
            else:
                return tag

        if self._keep_unknown_tags:
            return match.group(0)
        return self._default_data

    def lookup(self, tag: str):
        match = self.TAG_PATTERN.match(tag)
        if match:
            return self.__lookup_match(match)
        return tag if self._keep_unknown_tags else self._default_data

    def replace_tags(self, text: str):
        return self.TAG_PATTERN.sub(self.__lookup_match, text)

    def __call__(self, text: str):
        t = str(text or "")
        result = self.replace_tags(t)
        return result
