import unittest

from curlylint.rules.rule_test_case import RulesTestMeta

from .django_block_translate_trimmed import django_block_translate_trimmed


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = django_block_translate_trimmed
