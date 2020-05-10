from dataclasses import dataclass  # NOQA
from functools import partial
from pathlib import Path
from typing import List

import click

from curlylint.formatters.compact import format_compact
from curlylint.formatters.json import format_json
from curlylint.formatters.stylish import format_stylish
from curlylint.issue import Issue

out = partial(click.secho, bold=True, err=True)
err = partial(click.secho, fg="red", err=True)

formatters = {
    "compact": format_compact,
    "json": format_json,
    "stylish": format_stylish,
}


@dataclass
class Report:
    """Taken from black:
    https://github.com/psf/black/blob/959848c17639bfc646128f6b582c5858164a5001/black.py#L3640
    Provides a reformatting counter. Can be rendered with `str(report)`."""

    quiet: bool = False
    verbose: bool = False
    failure_count: int = 0
    format: str = "compact"

    def path_ignored(self, path: Path, message: str) -> None:
        if self.verbose:
            out(f"{path} ignored: {message}", bold=False)

    def print_issues(self, issues: List[Issue]):
        self.failure_count += len(issues)
        formatter = formatters[self.format]

        formatter(issues)

    @property
    def return_code(self) -> int:
        """Return the exit code that the app should use."""
        if self.failure_count:
            return 1

        return 0

    def __str__(self) -> str:
        """Render a color report of the current state.
        Use `click.unstyle` to remove colors.
        """
        report = []

        if self.failure_count:
            s = "s" if self.failure_count > 1 else ""
            report.append(
                click.style(f"{self.failure_count} error{s} reported", fg="red")
            )

        return ", ".join(report)
