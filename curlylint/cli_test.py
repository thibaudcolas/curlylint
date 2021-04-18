import unittest

from io import BytesIO
from typing import List

from curlylint.tests.utils import BlackRunner

from curlylint.cli import main


class TestCLI(unittest.TestCase):
    """
    Heavily inspired by Black’s CLI tests.
    See https://github.com/psf/black/blob/master/tests/test_black.py.
    """

    def invoke_curlylint(
        self, exit_code: int, args: List[str], input: str = None
    ):
        runner = BlackRunner()
        result = runner.invoke(
            main, args, input=BytesIO(input.encode("utf8")) if input else None
        )
        self.assertEqual(
            result.exit_code,
            exit_code,
            msg=(
                f"Failed with args: {args}\n"
                f"stdout: {runner.stdout_bytes.decode()!r}\n"
                f"stderr: {runner.stderr_bytes.decode()!r}\n"
                f"exception: {result.exception}"
            ),
        )
        return runner

    def test_no_flag(self):
        runner = self.invoke_curlylint(0, [])
        self.assertEqual(runner.stdout_bytes.decode(), "")
        self.assertEqual(
            runner.stderr_bytes.decode(), "No Path provided. Nothing to do 😴\n"
        )

    def test_stdin(self):
        runner = self.invoke_curlylint(0, ["-"], input="<p>Hello, World!</p>")
        self.assertEqual(runner.stdout_bytes.decode(), "")
        self.assertEqual(runner.stderr_bytes.decode(), "All done! ✨ 🍰 ✨\n\n")

    def test_stdin_verbose(self):
        runner = self.invoke_curlylint(
            0, ["--verbose", "-"], input="<p>Hello, World!</p>"
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

    def test_flag_help(self):
        runner = self.invoke_curlylint(0, ["--help"])
        self.assertIn(
            "Prototype linter for Jinja and Django templates",
            runner.stdout_bytes.decode(),
        )
        self.assertEqual(runner.stderr_bytes.decode(), "")

    def test_template_tags_validation_fail_no_nesting(self):
        runner = self.invoke_curlylint(
            2,
            ["--template-tags", '["cache", "endcache"]', "-"],
            input="<p>Hello, World!</p>",
        )
        self.assertIn(
            "Error: Invalid value for '--template-tags': expected a list of lists of tags as JSON, got '[\"cache\", \"endcache\"]'",
            runner.stderr_bytes.decode(),
        )

    def test_template_tags_cli_configured(self):
        self.invoke_curlylint(
            0,
            ["--template-tags", '[["of", "elseof", "endof"]]', "-"],
            input="<p>{% of a %}c{% elseof %}test{% endof %}</p>",
        )

    def test_template_tags_cli_unconfigured_fails(self):
        runner = self.invoke_curlylint(
            1,
            ["--template-tags", "[]", "-"],
            input="<p>{% of a %}c{% elseof %}test{% endof %}</p>",
        )
        self.assertIn(
            "Parse error: expected one of 'autoescape', 'block', 'blocktrans', 'comment', 'filter', 'for', 'if', 'ifchanged', 'ifequal', 'ifnotequal', 'not an intermediate Jinja tag name', 'spaceless', 'verbatim', 'with' at 0:17\tparse_error",
            runner.stdout_bytes.decode(),
        )
