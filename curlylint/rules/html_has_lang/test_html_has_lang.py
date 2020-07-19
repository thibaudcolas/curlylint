import json
import os
import unittest

from curlylint.issue import Issue
from curlylint.lint import parse_source

from .html_has_lang import html_has_lang

fixtures_path = os.path.join(
    os.path.dirname(__file__), "test_html_has_lang.json"
)
fixtures = json.loads(open(fixtures_path, "r").read())


class TestRule(unittest.TestCase):
    def test_works(self):
        self.maxDiff = 2000

        for item in fixtures:
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
                % item["template"],
            )
            output = list(map(Issue.from_dict, item["output"]))
            self.assertEqual(
                html_has_lang(file, item["config"]), output, item["label"],
            )

    def test_skips_no_html(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(html_has_lang(file, True), [])
