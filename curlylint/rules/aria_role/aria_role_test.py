import unittest

from curlylint.lint import parse_source
from curlylint.rules.rule_test_case import RulesTestMeta

from .aria_role import aria_role


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = aria_role

    def test_skips(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(aria_role(file, True), [])
