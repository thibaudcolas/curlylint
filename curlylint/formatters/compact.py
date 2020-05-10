from typing import List

from curlylint.issue import Issue


def format_compact(issues: List[Issue]):
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
