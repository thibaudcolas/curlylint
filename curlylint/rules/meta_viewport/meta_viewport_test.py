import unittest

from curlylint.lint import parse_source
from curlylint.rules.rule_test_case import RulesTestMeta

from .meta_viewport import meta_viewport


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = meta_viewport

    def test_skips(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(meta_viewport(file, True), [])
