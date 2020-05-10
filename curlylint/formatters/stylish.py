from itertools import groupby
from typing import List

import click

from curlylint.issue import Issue


def format_stylish(issues: List[Issue]):
    sorted_issues = sorted(
        issues,
        key=lambda i: (
            i.location.file_path,
            i.location.line,
            i.location.column,
        ),
    )

    for file_path, group in groupby(
        sorted_issues, lambda i: i.location.file_path
    ):
        print(click.style(str(file_path), underline=True))
        for issue in group:
            loc = click.style(
                f"{issue.location.line}:{issue.location.column}", dim=True
            )
            print(f"{loc}\t{issue.message}\t{issue.code}")
        print("")
