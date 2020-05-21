import unittest

from curlylint.issue import Issue, IssueLocation
from curlylint.lint import parse_source

from .aria_role import aria_role

cases = {
    "double quotes": ('role="search"', True, []),
    "single quotes": ("role='search'", True, []),
    "no quotes": ("role=search", True, []),
    "multiple attributes": ('class="potato" role="search"', True, []),
    "invalid": (
        'role="potato"',
        True,
        [
            Issue(
                location=IssueLocation(
                    file_path="test.html", column=21, line=7
                ),
                message="The `role` attribute needs to have a valid value",
                code="aria_role",
            )
        ],
    ),
}


class TestRule(unittest.TestCase):
    def test_works(self):
        for label, (input_, config, output) in cases.items():
            errors, file = parse_source(
                "test.html",
                {},
                """<!doctype HTML>
                <html>
                <head>
                    <title>Log in</title>
                </head>
                <body>
                    <h1 %s>Log in</h1>
                </body>
                </html>
                """
                % input_,
            )
            self.assertEqual(aria_role(file, config), output, label)

    def test_skips_no_role(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(aria_role(file, True), [])
