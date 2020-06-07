import unittest

from curlylint.issue import Issue, IssueLocation
from curlylint.lint import parse_source

from .html_has_lang import html_has_lang

cases = {
    "double quotes": ('<html lang="en">', True, []),
    "single quotes": ("<html lang='en'>", True, []),
    "no quotes": ("<html lang=en>", True, []),
    "multiple attributes": ('<html class="no-js" lang="en">', True, []),
    "missing": (
        "<html>",
        True,
        [
            Issue(
                location=IssueLocation(
                    file_path="test.html", column=17, line=2
                ),
                message="The `<html>` tag should have a `lang` attribute with a valid value, describing the main language of the page",
                code="html_has_lang",
            )
        ],
    ),
    "multiple attributes, missing": (
        '<html class="no-js">',
        True,
        [
            Issue(
                location=IssueLocation(
                    file_path="test.html", column=17, line=2
                ),
                message="The `<html>` tag should have a `lang` attribute with a valid value, describing the main language of the page",
                code="html_has_lang",
            )
        ],
    ),
    "correct language": ("<html lang='en'>", "en", [],),
    "correct language, multiple options": (
        "<html lang='en'>",
        ("en", "en-GB"),
        [],
    ),
    "wrong language": (
        "<html lang='fr'>",
        "en",
        [
            Issue(
                location=IssueLocation(
                    file_path="test.html", column=17, line=2
                ),
                message="The `<html>` tag should have a `lang` attribute with a valid value, describing the main language of the page. Allowed values: en",
                code="html_has_lang",
            )
        ],
    ),
    "wrong language, multiple options": (
        "<html lang='fr'>",
        ("en", "en-GB"),
        [
            Issue(
                location=IssueLocation(
                    file_path="test.html", column=17, line=2
                ),
                message="The `<html>` tag should have a `lang` attribute with a valid value, describing the main language of the page. Allowed values: en, en-GB",
                code="html_has_lang",
            )
        ],
    ),
}


class TestRule(unittest.TestCase):
    def test_works(self):
        self.maxDiff = 2000

        for label, (input_, config, output) in cases.items():
            errors, file = parse_source(
                "test.html",
                {},
                """<!doctype HTML>
                %s
                <head>
                    <title>Log in</title>
                </head>
                <body>
                    <h1>Log in</h1>
                </body>
                </html>
                """
                % input_,
            )
            self.assertEqual(html_has_lang(file, config), output, label)

    def test_skips_no_html(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(html_has_lang(file, True), [])
