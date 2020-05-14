import re
from functools import partial
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Pattern, Set, Tuple, Union

import click  # lgtm [py/import-and-import-from]

from curlylint.rule_param import RULE

from . import __version__
from .config import (
    find_project_root,
    gen_template_files_in_dir,
    get_gitignore,
    read_pyproject_toml,
)
from .lint import lint, lint_one
from .report import Report

out = partial(click.secho, bold=True, err=True)
err = partial(click.secho, fg="red", err=True)

DEFAULT_EXCLUDES = r"/(\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|venv|myvenv|\.svn|_build|buck-out|build|dist|coverage_html_report|node_modules)/"
DEFAULT_INCLUDES = r"\.(html|jinja|twig)$"


def re_compile_maybe_verbose(regex: str) -> Pattern[str]:
    """Compile a regular expression string in `regex`.
    If it contains newlines, use verbose mode.
    """
    if "\n" in regex:
        regex = "(?x)" + regex
    compiled: Pattern[str] = re.compile(regex)
    return compiled


def path_empty(
    src: Tuple[str, ...], quiet: bool, verbose: bool, ctx: click.Context
) -> None:
    """
    Exit if there is no `src` provided for formatting
    """
    if not src:
        if verbose or not quiet:
            out("No Path provided. Nothing to do 😴")
            ctx.exit(0)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version=__version__)
@click.option("-v", "--verbose", is_flag=True, help="Verbose mode.")
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help=(
        "Don’t emit non-error messages to stderr. Errors are still emitted; "
        "silence those with 2>/dev/null."
    ),
)
@click.option(
    "--parse-only",
    is_flag=True,
    help="Don’t lint, check for syntax errors and exit.",
)
@click.option(
    "--print-config",
    is_flag=True,
    help="Print the configuration for the given file.",
    is_eager=True,
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(("compact", "json", "stylish")),
    default="stylish",
    help=("Use a specific output format"),
    show_default=True,
)
@click.option(
    "--stdin-filepath",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=False,
        allow_dash=False,
    ),
    help=("Path to the file to pretend that stdin comes from."),
)
@click.option(
    "--include",
    type=str,
    default=DEFAULT_INCLUDES,
    help=(
        "A regular expression that matches files and directories that should be "
        "included on recursive searches. An empty value means all files are "
        "included regardless of the name. Use forward slashes for directories on "
        "all platforms (Windows, too).  Exclusions are calculated first, inclusions "
        "later."
    ),
    show_default=True,
)
@click.option(
    "--exclude",
    type=str,
    default=DEFAULT_EXCLUDES,
    help=(
        "A regular expression that matches files and directories that should be "
        "excluded on recursive searches. An empty value means no paths are excluded. "
        "Use forward slashes for directories on all platforms (Windows, too).  "
        "Exclusions are calculated first, inclusions later."
    ),
    show_default=True,
)
@click.option(
    "--rule",
    type=RULE,
    help=(
        'Specify rules, with the syntax --rule \'code: {"json": "value"}\'. '
        "Can be provided multiple times to configure multiple rules."
    ),
    multiple=True,
)
@click.argument(
    "src",
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        allow_dash=True,
    ),
    is_eager=True,
)
@click.option(
    "-c",
    "--config",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=True,
        allow_dash=False,
    ),
    is_eager=True,
    help="Read configuration from FILE.",
    callback=read_pyproject_toml,
)
@click.pass_context
def main(
    ctx: click.Context,
    verbose: bool,
    quiet: bool,
    parse_only: bool,
    print_config: bool,
    config: Optional[str],
    format: str,
    stdin_filepath: str,
    include: str,
    exclude: str,
    rule: Union[Mapping[str, Any], Tuple[Mapping[str, Any], ...]],
    src: Tuple[str, ...],
) -> None:
    """Prototype linter for Jinja and Django templates, forked from jinjalint"""

    if config and verbose:
        out(f"Using configuration from: {config}", bold=False, fg="blue")

    try:
        include_regex = re_compile_maybe_verbose(include)
    except re.error:
        err(f"Invalid regular expression for include given: {include!r}")
        ctx.exit(2)
    try:
        exclude_regex = re_compile_maybe_verbose(exclude)
    except re.error:
        err(f"Invalid regular expression for exclude given: {exclude!r}")
        ctx.exit(2)

    report = Report(quiet=quiet, verbose=verbose, format=format)
    root = find_project_root(src)

    if verbose:
        out(f"Identified project root as: {root}", bold=False, fg="blue")

    path_empty(src, quiet, verbose, ctx)

    sources: Set[Path] = set()
    for s in src:
        p = Path(s)
        if p.is_dir():
            sources.update(
                gen_template_files_in_dir(
                    p,
                    root,
                    include_regex,
                    exclude_regex,
                    report,
                    get_gitignore(root),
                )
            )
        elif p.is_file() or s == "-":
            if verbose:
                out("Analyzing file content from stdin")

            sources.add(p)
        else:
            err(f"invalid path: {s}")

    if len(sources) == 0:
        if verbose or not quiet:
            out(
                "No template files are present to be formatted. Nothing to do 😴"
            )
        ctx.exit(0)

    if verbose:
        out("Files being analyzed:")
        out("\n".join(str(s) for s in sources), bold=False, fg="blue")

    configuration = {}  # type: Dict[str, Any]
    if ctx.default_map:
        configuration.update(ctx.default_map)

    rules = configuration.get("rules", {})

    if rule:
        if isinstance(rule, tuple):
            for r in rule:
                rules.update(r)
        else:
            rules.update(rule)

    configuration["rules"] = rules
    configuration["verbose"] = verbose
    configuration["parse_only"] = parse_only

    if stdin_filepath:
        configuration["stdin_filepath"] = Path(stdin_filepath)

    if len(sources) == 1:
        issues = lint_one(sources.pop(), configuration)
    else:
        issues = lint(sources, configuration)

    report.print_issues(issues)

    if verbose or not quiet:
        out("Oh no! 💥 💔 💥" if report.return_code == 1 else "All done! ✨ 🍰 ✨")
        click.secho(str(report), err=True)
    ctx.exit(report.return_code)


def patch_click() -> None:
    """Borrowed from black.
    https://github.com/psf/black/blob/959848c17639bfc646128f6b582c5858164a5001/black.py
    Make Click not crash.
    On certain misconfigured environments, Python 3 selects the ASCII encoding as the
    default which restricts paths that it can access during the lifetime of the
    application.  Click refuses to work in this scenario by raising a RuntimeError.
    In case of Black the likelihood that non-ASCII characters are going to be used in
    file paths is minimal since it's Python source code.  Moreover, this crash was
    spurious on Python 3.7 thanks to PEP 538 and PEP 540.
    """
    try:
        from click import core
        from click import _unicodefun  # type: ignore
    except ModuleNotFoundError:
        return

    for module in (core, _unicodefun):
        if hasattr(module, "_verify_python3_env"):
            module._verify_python3_env = lambda: None


def patched_main() -> None:
    patch_click()
    main()


if __name__ == "__main__":
    patched_main()
