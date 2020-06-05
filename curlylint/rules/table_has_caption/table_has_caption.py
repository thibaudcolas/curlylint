from curlylint import ast
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue, IssueLocation

HTML_HAS_LANG = "html_has_lang"

RULE = {
    "docs": {
        "description": "<table> elements must contain a <caption>",
        "url": "",
    },
    "schema": [],
}

def is_caption(node):
    name = getattr(node.value, "name", None)
    return isinstance(node.value, ast.Element) and name and name.lower() == "caption"


def find_valid(node, file):
    name = getattr(node.value, "name", None)
    is_table = (
        isinstance(node.value, ast.Element) and name and name.lower() == "table"
    )

    if is_table:
        children = [for child in node.children]
        return [
            Issue(
                IssueLocation(
                    file_path=file.path,
                    line=node.value.begin.line + 1,
                    column=node.value.begin.column + 1,
                ),
                "The `<html>` tag should have a `lang` attribute with a valid value, describing the main language of the page",
                "html_has_lang",
            )
        ]

    if not node.children:
        return []

    return sum((find_valid(child, file) for child in node.children), [])


def table_has_caption(file, is_enabled):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    if is_enabled and r"<table" in src:
        return find_valid(root, file)

    return []
