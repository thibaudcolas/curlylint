import unittest

from curlylint.lint import parse_source
from curlylint.rules.rule_test_case import RulesTestMeta

from .html_has_lang import html_has_lang


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = html_has_lang

    def test_skips(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(html_has_lang(file, True), [])
