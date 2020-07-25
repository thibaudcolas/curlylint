import unittest

from curlylint.lint import parse_source
from curlylint.rules.rule_test_case import RulesTestMeta

from .tabindex_no_positive import tabindex_no_positive


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = tabindex_no_positive

    def test_skips(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(tabindex_no_positive(file, True), [])
