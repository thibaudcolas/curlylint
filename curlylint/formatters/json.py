import json
from typing import List

from curlylint.issue import Issue


def format_json(issues: List[Issue]):
    sorted_issues = sorted(
        issues,
        key=lambda i: (
            i.location.file_path,
            i.location.line,
            i.location.column,
        ),
    )

    output = []

    for issue in sorted_issues:
        output.append(
            {
                "file_path": str(issue.location.file_path),
                "line": issue.location.line,
                "column": issue.location.column,
                "message": issue.message,
                "code": issue.code,
            }
        )

    print(json.dumps(output))
