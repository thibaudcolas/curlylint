import re

from curlylint import ast
from curlylint.issue import Issue, IssueLocation

WHITESPACE_INDENT_RE = re.compile(r"^\s*")
INDENT_RE = re.compile("^ *")

INDENT = "indent"

RULE = {
    "id": "indent",
    "type": "layout",
    "docs": {
        "description": "Enforce consistent indentation",
        "recommended": False,
        "url": "",
        "examples": {"Use the given number of spaces": 4, "Use tabs": "tab"},
    },
    "schema": [
        {"oneOf": [{"enum": ["tab"]}, {"type": "integer", "minimum": 0}]}
    ],
}


def get_line_beginning(source, node):
    source = source[: node.begin.index]
    return source.split("\n")[-1]


def get_indent_level(source, node):
    """
    Returns the number of whitespace characters before the given node,
    in the first line of node.
    Returns `None` if some characters before the given node in this
    line aren’t whitespace.

    For example, if the source file contains `   <br /> ` on a line,
    `get_indent_level` will return 3 if called with the `<br />` tag
    as `node`.
    """
    beginning = get_line_beginning(source, node)
    if beginning and not beginning.isspace():
        return None
    return len(beginning)


def contains_exclusively(string, char):
    return string.replace(char, "") == ""


def truncate(s, length=16):
    return s[:length] + (s[length:] and "…")


def check_indentation(file, options):
    indent_size = options

    issues = []

    def add_issue(location, msg):
        issues.append(Issue.from_ast(file, location, msg, INDENT))

    def check_indent(expected_level, node, inline=False, allow_same_line=False):
        node_level = get_indent_level(file.source, node)
        if node_level is None:
            if not inline and not allow_same_line:
                node_s = repr(truncate(str(node)))
                add_issue(node.begin, node_s + " should be on the next line")
            return

        if node_level != expected_level:
            msg = "Bad indentation, expected {}, got {}".format(
                expected_level, node_level
            )
            add_issue(node.begin, msg)

    def check_attribute(expected_level, attr, inline=False, **_):
        if not attr.value:
            return

        if attr.begin.line != attr.value.begin.line:
            add_issue(
                attr.begin,
                "The value must begin on line {}".format(attr.begin.line),
            )
        check_content(
            expected_level,
            attr.value,
            inline=attr.value.begin.line == attr.value.end.line,
            allow_same_line=True,
        )

    def check_opening_tag(expected_level, tag, inline=False, **_):
        if len(tag.attributes) and tag.begin.line != tag.end.line:
            first = tag.attributes[0]
            check_node(
                expected_level + indent_size,
                first,
                inline=isinstance(first, ast.Attribute),
            )
            attr_level = len(get_line_beginning(file.source, first))
            for attr in tag.attributes[1:]:
                # attr may be a JinjaElement
                check_node(
                    expected_level if inline else attr_level,
                    attr,
                    inline=isinstance(attr, ast.Attribute),
                )

    def check_comment(expected_level, tag, **_):
        pass

    def check_jinja_comment(expected_level, tag, **_):
        pass

    def check_jinja_tag(expected_level, tag, **_):
        pass

    def check_string(
        expected_level, string, inline=False, allow_same_line=False
    ):
        if string.value.begin.line != string.value.end.line:
            inline = False
        check_content(
            string.value.begin.column,
            string.value,
            inline=inline,
            allow_same_line=allow_same_line,
        )

    def check_integer(expected_level, integer, **_):
        pass

    def get_first_child_node(parent):
        for c in parent:
            if isinstance(c, ast.Node):
                return c
        return None

    def check_jinja_element_part(
        expected_level, part, inline=False, allow_same_line=False
    ):
        check_node(
            expected_level,
            part.tag,
            inline=inline,
            allow_same_line=allow_same_line,
        )
        if part.begin.line != part.end.line:
            inline = False
        shift = 0 if inline else indent_size
        content_level = expected_level + shift
        if part.content is not None:
            check_content(content_level, part.content, inline=inline)

    def check_jinja_optional_container_if(
        expected_level, o_if, html_tag, c_if, inline=False
    ):
        check_indent(expected_level, o_if, inline=inline)
        shift = 0 if inline else indent_size
        if isinstance(html_tag, ast.OpeningTag):
            check_opening_tag(expected_level + shift, html_tag, inline=inline)
        elif isinstance(html_tag, ast.ClosingTag):
            check_indent(expected_level + shift, html_tag, inline=inline)
        else:
            raise AssertionError("invalid tag")
        check_indent(expected_level, c_if, inline=inline)
        return inline

    def check_jinja_optional_container(
        expected_level, element, inline=False, **_
    ):
        if (
            element.first_opening_if.begin.line
            == element.second_opening_if.end.line
        ):
            inline = True

        inline = check_jinja_optional_container_if(
            expected_level,
            element.first_opening_if,
            element.opening_tag,
            element.first_closing_if,
            inline=inline,
        )

        check_content(expected_level, element.content, inline=inline)

        check_jinja_optional_container_if(
            expected_level,
            element.second_opening_if,
            element.closing_tag,
            element.second_closing_if,
            inline=inline,
        )

    def check_jinja_element(
        expected_level, element, inline=False, allow_same_line=False
    ):
        if element.begin.line == element.end.line:
            inline = True
        for part in element.parts:
            check_node(
                expected_level,
                part,
                inline=inline,
                allow_same_line=allow_same_line,
            )
        if element.closing_tag is not None:
            check_indent(expected_level, element.closing_tag, inline=inline)

    def check_jinja_variable(expected_level, var, **_):
        pass

    def check_element(expected_level, element, inline=False, **_):
        opening_tag = element.opening_tag
        closing_tag = element.closing_tag
        check_opening_tag(expected_level, opening_tag, inline=inline)
        if not closing_tag:
            return
        if inline or opening_tag.end.line == closing_tag.begin.line:
            check_content(expected_level, element.content, inline=True)
        else:
            check_content(expected_level + indent_size, element.content)
            check_indent(expected_level, closing_tag)

    def check_node(
        expected_level, node, inline=False, allow_same_line=False, **_
    ):
        check_indent(
            expected_level, node, inline=inline, allow_same_line=allow_same_line
        )

        types_to_functions = {
            ast.Attribute: check_attribute,
            ast.Comment: check_comment,
            ast.Element: check_element,
            ast.Integer: check_integer,
            ast.JinjaComment: check_jinja_comment,
            ast.JinjaElement: check_jinja_element,
            ast.JinjaElementPart: check_jinja_element_part,
            ast.JinjaOptionalContainer: check_jinja_optional_container,
            ast.JinjaTag: check_jinja_tag,
            ast.JinjaVariable: check_jinja_variable,
            ast.String: check_string,
        }

        func = types_to_functions.get(type(node))
        if func is None:
            raise Exception(
                "Unexpected {!r} node at {}".format(type(node), node.begin)
            )

        func(
            expected_level, node, inline=inline, allow_same_line=allow_same_line
        )

    def check_content_str(expected_level, string, parent_node):
        lines = string.split("\n")
        expected_indent = expected_level * " "

        indent = INDENT_RE.match(lines[0]).group(0)

        if len(indent) > 1:
            msg = (
                "Expected at most one space at the beginning of the text "
                "node, got {} spaces"
            ).format(len(indent))
            add_issue(parent_node.begin, msg)

        # skip the first line since there is certainly an HTML tag before
        for line in lines[1:]:
            if line.strip() == "":
                continue
            indent = INDENT_RE.match(line).group(0)
            if indent != expected_indent:
                msg = "Bad text indentation, expected {}, got {}".format(
                    expected_level, len(indent)
                )
                add_issue(parent_node.begin, msg)

    def check_content(
        expected_level, parent_node, inline=False, allow_same_line=False
    ):
        inline_parent = inline
        for i, child in enumerate(parent_node):
            next_child = get_first_child_node(parent_node[i + 1 :])

            if isinstance(child, str):
                check_content_str(expected_level, child, parent_node)
                if not child.strip(" "):
                    inline = True
                elif child.strip() and child.count("\n") <= 1:
                    inline = True
                elif (
                    next_child
                    and child.strip()
                    and not child.replace(" ", "").endswith("\n")
                ):
                    inline = True
                elif child.replace(" ", "").endswith("\n\n"):
                    inline = False
                if inline_parent and not inline:
                    msg = (
                        "An inline parent element must only contain "
                        "inline children"
                    )
                    add_issue(parent_node.begin, msg)
                continue

            if isinstance(child, ast.Node):
                if next_child and child.begin.line == next_child.end.line:
                    inline = True
                check_node(
                    expected_level,
                    child,
                    inline=inline,
                    allow_same_line=allow_same_line,
                )
                continue

            raise Exception()

    check_content(0, file.tree)

    return issues


def check_space_only_indent(file):
    issues = []
    for i, line in enumerate(file.lines):
        indent = WHITESPACE_INDENT_RE.match(line).group(0)
        if not contains_exclusively(indent, " "):
            loc = IssueLocation(file_path=file.path, line=i, column=0)
            issue = Issue(loc, "Should be indented with spaces", INDENT)
            issues.append(issue)
    return issues


def check_tab_only_indent(file):
    issues = []
    for i, line in enumerate(file.lines):
        indent = WHITESPACE_INDENT_RE.match(line).group(0)
        if not contains_exclusively(indent, "\t"):
            loc = IssueLocation(file_path=file.path, line=i, column=0)
            issue = Issue(loc, "Should be indented with tabs", INDENT)
            issues.append(issue)
    return issues


def indent(file, options):
    if options == "tab":
        return check_tab_only_indent(file)

    return check_space_only_indent(file) + check_indentation(file, options)
