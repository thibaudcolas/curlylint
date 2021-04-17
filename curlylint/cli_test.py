import unittest

from io import BytesIO

from curlylint.tests.utils import BlackRunner

from curlylint.cli import main


class TestParser(unittest.TestCase):
    def test_no_flag(self):
        runner = BlackRunner()
        result = runner.invoke(main, [])
        self.assertEqual(runner.stdout_bytes.decode(), "")
        self.assertEqual(
            runner.stderr_bytes.decode(), "No Path provided. Nothing to do 😴\n"
        )
        self.assertEqual(result.exit_code, 0)

    def test_stdin(self):
        runner = BlackRunner()
        result = runner.invoke(
            main, ["-"], input=BytesIO("<p>Hello, World!</p>".encode("utf8")),
        )
        self.assertEqual(runner.stdout_bytes.decode(), "")
        self.assertEqual(runner.stderr_bytes.decode(), "All done! ✨ 🍰 ✨\n\n")
        self.assertEqual(result.exit_code, 0)

    def test_stdin_verbose(self):
        runner = BlackRunner()
        result = runner.invoke(
            main,
            ["--verbose", "-"],
            input=BytesIO("<p>Hello, World!</p>".encode("utf8")),
        )
        self.assertEqual(runner.stdout_bytes.decode(), "")
        self.assertIn(
            "Identified project root as:", runner.stderr_bytes.decode()
        )
        self.assertIn(
            """Analyzing file content from stdin
Files being analyzed:
-
All done! ✨ 🍰 ✨
""",
            runner.stderr_bytes.decode(),
        )
        self.assertEqual(result.exit_code, 0)

    def test_flag_help(self):
        runner = BlackRunner()
        result = runner.invoke(main, ["--help"])
        self.assertIn(
            "Prototype linter for Jinja and Django templates",
            runner.stdout_bytes.decode(),
        )
        self.assertEqual(runner.stderr_bytes.decode(), "")
        self.assertEqual(result.exit_code, 0)
