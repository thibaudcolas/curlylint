import json
from typing import Callable

from curlylint.issue import Issue
from curlylint.lint import parse_source


class RulesTestMeta(type):
    """
    Generates test cases dynamically.
    See http://stackoverflow.com/a/20870875/1798491
    """

    def __new__(mcs, name, bases, tests):
        def gen_test(item) -> Callable[[None], None]:
            def test(self):
                errors, file = parse_source("test.html", {}, item["template"])
                output = list(map(Issue.from_dict, item["output"]))
                self.assertEqual(tests["rule"](file, item["config"]), output)

            return test

        fixtures = json.loads(open(tests["fixtures"], "r").read())

        for item in fixtures:
            test_label = item["label"].lower().replace(" ", "_")
            test_name = f"test_{test_label}"
            tests[test_name] = gen_test(item)

        return type.__new__(mcs, name, bases, tests)
