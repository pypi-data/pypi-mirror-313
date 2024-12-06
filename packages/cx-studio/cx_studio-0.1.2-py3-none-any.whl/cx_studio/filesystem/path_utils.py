import os
from pathlib import Path
from typing import Iterable


def normalize_path(path: Path, anchor=Path(".")) -> Path:
    path = Path(path)
    anchor = Path(anchor)
    if path.is_absolute():
        return path.absolute()

    t = str(path)
    if t.startswith("~"):
        return Path(t.replace("~", str(Path.home()))).absolute()

    return (anchor / path).resolve(strict=False)


def normalize_suffix(suffix: str, with_dot=True) -> str:
    """检查扩展名是否带点"""
    s = str(suffix).strip().strip(".").lower()
    return "." + s if with_dot else s


def force_suffix(source: Path, suffix: str, ignore_dir=True):
    if not source:
        return None
    source = Path(source)
    if source.is_dir() and ignore_dir:
        return source
    suffix = normalize_suffix(suffix)
    return source if source.suffix == suffix else source.with_suffix(suffix)


def ensure_folder(source: Path):
    source = normalize_path(source)
    if source.is_file():
        source = source.parent
    return source


def quote_path(path, quote_char='"') -> str:
    path = str(path)
    return f"{quote_char}{path}{quote_char}" if " " in path else path


def is_file_in_dir(file, folder) -> bool:
    f = str(Path(file).resolve().absolute())
    d = str(Path(folder).resolve().absolute())
    return f in d


def is_executable(cmd: Path) -> bool:
    cmd = Path(cmd)
    return cmd.exists() and os.access(cmd, os.X_OK)


def ensure_paths(sources: Iterable) -> list[Path]:
    if not sources:
        sources = []
    for x in sources:
        if isinstance(x, Iterable):
            yield from ensure_paths(x)
        elif isinstance(x, Path):
            yield x
        else:
            yield Path(str(x))

