from functools import lru_cache, partial
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Pattern, Union

import click
import toml
from pathspec import PathSpec

from . import __version__
from .report import Report

out = partial(click.secho, bold=True, err=True)


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


def dump_toml_config(ctx: click.Context, config: Dict[str, Any] = None):
    """Prints the provided config object as TOML, if present."""
    if not config:
        out(
            "Oops! Something went wrong! :( curlylint couldn’t find a configuration file.\n"
            f"curlylint: v{__version__}.\n\n"
        )
        ctx.exit(2)

    print(toml.dumps({"tool": {"curlylint": config}}))
    ctx.exit(0)


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
    print_config = ctx.params.get("print_config", False)

    if not value:
        value = find_pyproject_toml(ctx.params.get("src", ()))
        if value is None:
            if print_config:
                dump_toml_config(ctx)
            return None

    try:
        config = parse_pyproject_toml(value)
    except (toml.TomlDecodeError, OSError) as e:
        raise click.FileError(
            filename=value, hint=f"Error reading configuration file: {e}"
        )

    if not config:
        if print_config:
            dump_toml_config(ctx)
        return None

    if print_config:
        dump_toml_config(ctx, config)

    if ctx.default_map is None:
        ctx.default_map = {}
    ctx.default_map.update(config)  # type: ignore  # bad types in .pyi
    return value


@lru_cache()
def get_gitignore(root: Path) -> PathSpec:
    """ Return a PathSpec matching gitignore content if present."""
    gitignore = root / ".gitignore"
    lines: List[str] = []
    if gitignore.is_file():
        with gitignore.open() as gf:
            lines = gf.readlines()
    return PathSpec.from_lines("gitwildmatch", lines)


def gen_template_files_in_dir(
    path: Path,
    root: Path,
    include: Pattern[str],
    exclude: Pattern[str],
    report: "Report",
    gitignore: PathSpec,
) -> Iterator[Path]:
    """Generate all files under `path` whose paths are not excluded by the
    `exclude` regex, but are included by the `include` regex.
    Symbolic links pointing outside of the `root` directory are ignored.
    `report` is where output about exclusions goes.
    """
    assert (
        root.is_absolute()
    ), f"INTERNAL ERROR: `root` must be absolute but is {root}"
    for child in path.iterdir():
        # First ignore files matching .gitignore
        if gitignore.match_file(child.as_posix()):
            report.path_ignored(child, f"matches the .gitignore file content")
            continue

        # Then ignore with `exclude` option.
        try:
            normalized_path = "/" + child.resolve().relative_to(root).as_posix()
        except OSError as e:
            report.path_ignored(child, f"cannot be read because {e}")
            continue

        except ValueError:
            if child.is_symlink():
                report.path_ignored(
                    child, f"is a symbolic link that points outside {root}"
                )
                continue

            raise

        if child.is_dir():
            normalized_path += "/"

        exclude_match = exclude.search(normalized_path)
        if exclude_match and exclude_match.group(0):
            report.path_ignored(
                child, f"matches the --exclude regular expression"
            )
            continue

        if child.is_dir():
            yield from gen_template_files_in_dir(
                child, root, include, exclude, report, gitignore
            )

        elif child.is_file():
            include_match = include.search(normalized_path)
            if include_match:
                yield child
