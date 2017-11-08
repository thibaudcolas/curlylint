from pathlib import Path
import re

import attr

from . import ast
from .util import flatten
from .issue import Issue, IssueLocation


def visit(n, on_enter, on_exit):
    on_enter(n)

    get_children = {
        ast.OpeningTag: lambda: [n.name, n.attributes, n.slash],
        ast.ClosingTag: lambda: [n.name],
        ast.Element: lambda: [n.opening_tag, n.content, n.closing_tag],
        ast.String: lambda: [n.value],
        ast.Integer: lambda: [n.value],
        ast.Attribute: lambda: [n.name, n.value],
        ast.Comment: lambda: [n.text],
        ast.JinjaVariable: lambda: [n.content],
        ast.JinjaComment: lambda: [n.text],
        ast.JinjaTag: lambda: [n.name, n.content],
        ast.JinjaElement: lambda: n.parts + [n.closing_tag],
        ast.JinjaElementPart: lambda: [n.tag, n.content],
        ast.Interpolated: lambda: n.nodes,
    }.get(type(n), lambda: [])

    children = get_children()

    for child in children:
        if isinstance(child, ast.Node):
            visit(child, on_enter, on_exit)

    on_exit(n)


def get_line_beginning(source, index):
    source = source[:index]
    return source.split('\n')[-1]


def get_indent_level(source, node):
    beginning = get_line_beginning(source, node.begin.index)
    if beginning and not beginning.isspace():
        return None
    return len(beginning)


def contains_exclusively(string, char):
    return string.replace(char, '') == ''


def check_attributes_indentation(file):
    level = None
    issues = []

    def on_enter(node):
        nonlocal level
        if (isinstance(node, ast.OpeningTag) and
                node.begin.line != node.end.line and
                len(node.attributes) > 0):
            attr = node.attributes[0]
            beginning = get_line_beginning(file.source, attr.begin.index)
            level = len(beginning)
            return
        if isinstance(node, ast.Attribute) and level is not None:
            node_level = get_indent_level(file.source, node)
            if node_level is not None and node_level != level:
                msg = 'Bad indentation, expected {}, got {}'.format(
                    level, node_level,
                )
                issues.append(Issue.from_ast(file, node.begin, msg))

    def on_exit(node):
        nonlocal level
        if isinstance(node, ast.OpeningTag):
            level = None

    visit(file.tree, on_enter, on_exit)
    assert level is None
    return issues


def check_indentation(file):
    level = 0
    indentor_classes = (ast.Element, ast.JinjaElementPart)
    indented_classes = indentor_classes + (
        ast.JinjaVariable, ast.JinjaComment, ast.Comment)
    issues = []

    def on_enter(node):
        nonlocal level

        node_level = get_indent_level(file.source, node)
        if node_level is None:
            return

        if (isinstance(node, indented_classes) and node_level != level):
            msg = 'Bad indentation, expected {}, got {}'.format(
                level, node_level,
            )
            issues.append(Issue.from_ast(file, node.begin, msg))

        if (isinstance(node, indentor_classes) and
                node.begin.line != node.end.line):
            level += 4

    def on_exit(node):
        nonlocal level

        node_level = get_indent_level(file.source, node)
        if node_level is None:
            return

        if (isinstance(node, indentor_classes) and
                node.begin.line != node.end.line):
            level -= 4
            assert level >= 0

    visit(file.tree, on_enter, on_exit)
    assert level == 0
    return issues


def check_no_tabs(file):
    issues = []
    match_indent = re.compile('^\s*')
    for i, line in enumerate(file.lines):
        indent = match_indent.match(line).group(0)
        if not contains_exclusively(indent, ' '):
            loc = IssueLocation(
                file_path=file.path,
                line=i,
                column=0,
            )
            issue = Issue(loc, 'Should be indented with spaces')
            issues.append(issue)
    return issues


checks = [
    check_no_tabs,
    check_indentation,
    check_attributes_indentation,
]


def check_file(file):
    return flatten(check(file) for check in checks)


def check_files(files):
    return flatten(check_file(file) for file in files)
