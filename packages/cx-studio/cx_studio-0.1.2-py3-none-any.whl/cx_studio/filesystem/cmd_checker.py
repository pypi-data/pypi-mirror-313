import itertools
import os
from pathlib import Path
from cx_studio.core import MemberCaches
from .path_utils import ensure_paths, is_executable


class CommandChecker:
    def __init__(
        self,
        executable: str,
        include_pwd=True,
        extra_paths: list[Path] = None,
        extra_suffixes: list[str] = None,
    ):
        self._source = str(executable)
        self._include_pwd = include_pwd
        self._extra_paths = [x for x in ensure_paths(extra_paths)]
        self._extra_suffixes = extra_suffixes if extra_suffixes else []

    def _possible_sources(self):
        possible_suffixes = [".exe", ".com"]
        yield self._source
        for suffix in possible_suffixes:
            yield self._source + suffix
        for x in self._extra_suffixes:
            suffix = str(x)
            if not suffix.startswith("."):
                suffix = "." + suffix
            yield self._source + suffix

    @staticmethod
    def os_paths():
        for p in os.environ["PATH"].split(os.pathsep):
            yield Path(p)

    def additional_paths(self):
        for p in self._extra_paths:
            if p.is_dir():
                yield p
        if self._include_pwd:
            yield Path.cwd()

    def search_paths(self):
        yield from self.os_paths()
        yield from self.additional_paths()

    def executable(self) -> str:
        if os.path.isabs(self._source) and is_executable(Path(self._source)):
            return self._source

        for folder, file in itertools.product(
            self.os_paths(), self._possible_sources()
        ):
            cmd = Path(folder) / file
            if is_executable(cmd):
                return self._source

        for folder, file in itertools.product(
            self.additional_paths(), self._possible_sources()
        ):
            cmd = Path(folder) / file
            if is_executable(cmd):
                return cmd.resolve()

        return ""

    def absolute(self) -> str:
        result = self.executable()
        if result:
            return str(Path(result).resolve())
        return ""
