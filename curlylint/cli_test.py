import unittest

from curlylint.tests.utils import BlackRunner

from curlylint.cli import main


class TestParser(unittest.TestCase):
    def test_flag_help(self):
        runner = BlackRunner()
        result = runner.invoke(main, ["--help"])
        self.assertIn(
            "Prototype linter for Jinja and Django templates",
            runner.stdout_bytes.decode(),
        )
        self.assertEqual(runner.stderr_bytes.decode(), "")
        self.assertEqual(result.exit_code, 0)
