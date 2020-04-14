from dataclasses import dataclass  # NOQA
from functools import partial
from pathlib import Path
from typing import List

import click

out = partial(click.secho, bold=True, err=True)
err = partial(click.secho, fg="red", err=True)


@dataclass
class Report:
    """Taken from black:
    https://github.com/psf/black/blob/959848c17639bfc646128f6b582c5858164a5001/black.py#L3640
    Provides a reformatting counter. Can be rendered with `str(report)`."""

    quiet: bool = False
    verbose: bool = False
    failure_count: int = 0

    def path_ignored(self, path: Path, message: str) -> None:
        if self.verbose:
            out(f"{path} ignored: {message}", bold=False)

    def print_issues(self, issues: List["Issue"]):
        sorted_issues = sorted(
            issues,
            key=lambda i: (
                i.location.file_path,
                i.location.line,
                i.location.column,
            ),
        )

        for issue in sorted_issues:
            self.failure_count += 1
            print(str(issue))

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

        return ", ".join(report) + "."
