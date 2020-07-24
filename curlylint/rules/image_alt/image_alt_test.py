import unittest

from curlylint.lint import parse_source
from curlylint.rules.rule_test_case import RulesTestMeta

from .image_alt import image_alt


class TestRule(unittest.TestCase, metaclass=RulesTestMeta):
    fixtures = __file__.replace(".py", ".json")
    rule = image_alt

    def test_skips_no_img(self):
        errors, file = parse_source("test.html", {}, "<p>Test</p>")
        self.assertEqual(image_alt(file, True), [])
