import unittest

from .issue import Issue, IssueLocation


class TestIssue(unittest.TestCase):
    def test_from_ast(self):
        self.assertEqual(
            Issue.from_ast(
                file="test.html",
                line=4,
                column=23,
                code="test_code",
                message="Test message",
            ),
            Issue(
                IssueLocation(file_path="test.html", line=4, column=23),
                "Test message",
                "test_code",
            ),
        )

    def test_from_dict(self):
        self.assertEqual(
            Issue.from_dict(
                {
                    "file": "test.html",
                    "line": 4,
                    "column": 23,
                    "code": "test_code",
                    "message": "Test message",
                }
            ),
            Issue.from_ast(
                file="test.html",
                line=4,
                column=23,
                code="test_code",
                message="Test message",
            ),
        )
