import unittest

from curlylint.rules.rule_test_case import RulesTestMeta

from .django_forms_rendering import django_forms_rendering


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = django_forms_rendering
