from functools import lru_cache
from pathlib import Path

import toml
import click

from typing import Any, Dict, Iterable, Optional, Union


@lru_cache()
def find_project_root(srcs: Iterable[str]) -> Path:
    """Taken from black:
    https://github.com/psf/black/blob/959848c17639bfc646128f6b582c5858164a5001/black.py#L237
    Return a directory containing .git, .hg, or pyproject.toml.
    That directory can be one of the directories passed in `srcs` or their
    common parent.
    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.
    """
    if not srcs:
        return Path("/").resolve()

    common_base = min(Path(src).resolve() for src in srcs)
    if common_base.is_dir():
        # Append a fake file so `parents` below returns `common_base_dir`, too.
        common_base /= "fake-file"
    for directory in common_base.parents:
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

    return directory


def find_pyproject_toml(path_search_start: str) -> Optional[str]:
    """Find the absolute filepath to a pyproject.toml if it exists"""
    path_project_root = find_project_root(path_search_start)
    path_pyproject_toml = path_project_root / "pyproject.toml"
    return str(path_pyproject_toml) if path_pyproject_toml.is_file() else None


def parse_pyproject_toml(path_config: str) -> Dict[str, Any]:
    """Parse a pyproject toml file, pulling out relevant parts for the linter
    If parsing fails, will raise a toml.TomlDecodeError
    """
    pyproject_toml = toml.load(path_config)
    config = pyproject_toml.get("tool", {}).get("curlylint", {})
    return {k.replace("--", "").replace("-", "_"): v for k, v in config.items()}


def read_pyproject_toml(
    ctx: click.Context,
    param: click.Parameter,
    value: Union[str, int, bool, None],
) -> Optional[str]:
    """Inject configuration from "pyproject.toml" into defaults in `ctx`.
    Returns the path to a successfully found and read configuration file, None
    otherwise.
    """
    assert not isinstance(value, (int, bool)), "Invalid parameter type passed"
    if not value:
        value = find_pyproject_toml(ctx.params.get("src", ()))
        if value is None:
            return None

    try:
        config = parse_pyproject_toml(value)
    except (toml.TomlDecodeError, OSError) as e:
        raise click.FileError(
            filename=value, hint=f"Error reading configuration file: {e}"
        )

    if not config:
        return None

    if ctx.default_map is None:
        ctx.default_map = {}
    ctx.default_map.update(config)  # type: ignore  # bad types in .pyi
    return value
