from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .path_utils import normalize_path


class PathExpander:
    @dataclass
    class Settings:
        anchor_dir: Path = Path.cwd()
        search_subdir: bool = True
        resolve_symlinks: bool = True
        existed_only: bool = True
        accept_file: bool = True
        accept_dir: bool = True
        accept_other: bool = False
        global_validator: Callable[[Path], bool] = None
        file_validator: Callable[[Path], bool] = None
        dir_validator: Callable[[Path], bool] = None
        skip_duplicated: bool = True
        skip_unknown_type: bool = True

    @staticmethod
    def _prepare_path_list(source) -> list[Path]:
        if not isinstance(source, Iterable):
            return [Path(str(source))]
        return sorted([Path(str(x)) for x in source], key=lambda a: a.absolute())

    def __init__(
            self,
            sources: Any,
            settings: Settings = None,
            anchor_dir: Path = None,
            search_subdir: bool = None,
            resolve_symlinks: bool = None,
            existed_only: bool = None,
            accept_file: bool = None,
            accept_dir: bool = None,
            accept_other: bool = None,
            global_validator: Callable[[Path], bool] = None,
            file_validator: Callable[[Path], bool] = None,
            dir_validator: Callable[[Path], bool] = None,
            skip_duplicated: bool = None,
            **kwargs
    ):
        self._sources = PathExpander._prepare_path_list(sources)

        self.settings = settings or PathExpander.Settings()
        if anchor_dir is not None:
            self.settings.anchor_dir = Path(anchor_dir)
        if search_subdir is not None:
            self.settings.search_subdir = search_subdir
        if resolve_symlinks is not None:
            self.settings.resolve_symlinks = resolve_symlinks
        if existed_only is not None:
            self.settings.existed_only = existed_only
        if accept_file is not None:
            self.settings.accept_file = accept_file
        if accept_dir is not None:
            self.settings.accept_dir = accept_dir
        if accept_other is not None:
            self.settings.accept_other = accept_other
        if global_validator is not None:
            self.settings.global_validator = global_validator
        if file_validator is not None:
            self.settings.file_validator = file_validator
        if dir_validator is not None:
            self.settings.dir_validator = dir_validator
        if skip_duplicated is not None:
            self.settings.skip_duplicated = skip_duplicated

        if kwargs:
            self.__dict__.update(kwargs)

        self.__entry_cache = set() if self.settings.skip_duplicated else None

    def _prepare_path(self, s):
        path = normalize_path(s, self.settings.anchor_dir)
        if path.is_symlink() and self.settings.resolve_symlinks:
            path = path.resolve(strict=False)
        return path

    def _cache_entry(self, entry: Path):
        if self.__entry_cache:
            self.__entry_cache.add(entry)

    def _is_cached(self, entry: Path):
        return self.__entry_cache and (entry in self.__entry_cache)

    def clear_cache(self):
        if self.__entry_cache:
            self.__entry_cache.clear()

    def _is_acceptable_file(self, entry: Path) -> bool:
        """
        根据设置判断entry是否是一个可接受的文件。
        如果它不是文件或设置了不接受文件，则会返回 False。
        :param entry:
        :return:
        """
        if not entry.is_file():
            return False
        if not self.settings.accept_file:
            return False
        if (not entry.exists()) and self.settings.existed_only:
            return False
        if self.settings.file_validator:
            return self.settings.file_validator(entry)
        return True

    def _is_acceptable_dir(self, entry: Path) -> bool:
        """
        判断是否是一个可以接受的目录
        accept_dir 属性指定是否提出目录，并决定是否迭代它，所以此方法中不包含该判定。
        :param entry:
        :return:
        """
        if not entry.is_dir():
            return False
        if (not entry.exists()) and self.settings.existed_only:
            return False
        if self.settings.dir_validator:
            return self.settings.dir_validator(entry)
        return True

    def _expand(self, *entries):
        for entry in entries:
            entry = self._prepare_path(entry)
            if self._is_cached(entry):
                continue
            if self.settings.global_validator and not self.settings.global_validator(entry):
                continue
            if self._is_acceptable_file(entry):
                self._cache_entry(entry)
                yield entry
            elif self._is_acceptable_dir(entry):
                if self.settings.accept_dir:
                    # 如果接受目录的话，将会迭代出目录的路径
                    yield entry
                if self.settings.search_subdir:
                    for sub_entry in entry.iterdir():
                        yield from self._expand(entry / sub_entry)
            elif self.settings.accept_other:
                self._cache_entry(entry)
                yield entry

    def __iter__(self):
        return self._expand(*self._sources)


class SuffixValidator:
    """
    简单的扩展名判断器，
    通过输入的扩展名判断路径是否合法。
    可以方便地插入到 PathExpander 中。
    """

    def __init__(self, acceptable_suffixes: Iterable):
        self._suffixes = {
            x if x.startswith(".") else "." + x
            for x in [str(a).strip().lower() for a in acceptable_suffixes]
        }

    def __call__(self, entry: Path):
        entry = Path(entry)
        return entry.suffix.lower() in self._suffixes


class BlackListValidator:
    """
    指定黑名单并进行验证，
    可以用于 global_validator
    """

    def __init__(self, blacklist):
        self._excluded_entries = None
        if not blacklist:
            return

        if isinstance(blacklist, Iterable):
            self._excluded_entries = (Path(str(x)).absolute() for x in blacklist)
        else:
            self._excluded_entries = Path(str(blacklist))

    def __call__(self, entry: Path):
        if not self._excluded_entries:
            return True
        return entry.absolute() in self._excluded_entries


class MultiValidator:
    """融合多个 validator"""

    def __init__(self, *validators):
        self._validators = set()
        for val in validators:
            self.add(val)

    def add(self, validator: Callable[[Path], bool]):
        if isinstance(validator, MultiValidator):
            self._validators = self._validators.union(validator._validators)
        else:
            self._validators.add(validator)
        return self

    def __call__(self, entry: Path) -> bool:
        if not self._validators:
            return True
        for val in self._validators:
            if not val(entry):
                return False
        return True
