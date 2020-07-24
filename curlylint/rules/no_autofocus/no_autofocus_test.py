import unittest

from curlylint.lint import parse_source
from curlylint.rules.rule_test_case import RulesTestMeta

from .no_autofocus import no_autofocus


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = no_autofocus

    def test_skips(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(no_autofocus(file, True), [])
