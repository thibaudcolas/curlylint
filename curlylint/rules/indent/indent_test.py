import unittest

from curlylint.rules.rule_test_case import RulesTestMeta

from .indent import indent


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = indent
