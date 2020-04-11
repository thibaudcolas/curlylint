import click

from . import __version__
from .config import parse_config
from .lint import lint, resolve_file_paths

from typing import List, Optional, Tuple


def print_issues(issues, config):
    sorted_issues = sorted(
        issues,
        key=lambda i: (
            i.location.file_path,
            i.location.line,
            i.location.column,
        ),
    )

    for issue in sorted_issues:
        print(str(issue))


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version=__version__)
@click.option("-v", "--verbose", is_flag=True, help="Verbose mode.")
@click.option(
    "--parse-only",
    is_flag=True,
    help="Don’t lint, check for syntax errors and exit.",
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
)
@click.option(
    "-e",
    "--extension",
    multiple=True,
    default=["html", "jinja", "twig"],
    help="Extension of the files to analyze (used if SRC contains directories to crawl).",
    show_default=True,
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
@click.pass_context
def main(
    ctx: click.Context,
    verbose: bool,
    parse_only: bool,
    config: Optional[str],
    extension: List[str],
    src: Tuple[str, ...],
) -> None:
    """Prototype linter for Jinja and Django templates, forked from jinjalint"""

    input_names = src or (".")

    if config:
        if verbose:
            print("Using configuration file {}".format(config))
        config = parse_config(config)
    else:
        config = {}

    config["verbose"] = verbose
    config["parse_only"] = parse_only

    extensions = ["." + e for e in extension]
    paths = list(resolve_file_paths(input_names, extensions=extensions))

    if verbose:
        print("Files being analyzed:")
        print("\n".join(str(p) for p in paths))
        print()

    issues = lint(paths, config)
    print_issues(issues, config)

    if any(issues):
        exit(1)


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
