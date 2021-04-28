from curlylint import ast
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue

TABINDEX_NO_POSITIVE = "tabindex_no_positive"

RULE = {
    "id": "tabindex_no_positive",
    "type": "accessibility",
    "docs": {
        "description": "Prevents using positive `tabindex` values, which are very easy to misuse with problematic consequences for keyboard users.",
        "url": "https://www.curlylint.org/docs/rules/tabindex_no_positive",
        "impact": "Serious",
        "tags": ["cat.language", "wcag2a"],
        "resources": [
            "[WHATWG HTML Standard, The autofocus attribute](https://html.spec.whatwg.org/multipage/interaction.html#attr-fe-autofocus)",
            "[The accessibility of HTML 5 autofocus](https://www.brucelawson.co.uk/2009/the-accessibility-of-html-5-autofocus/)",
            "[MDN: input `autofocus` attribute usage considerations](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefautofocus)",
        ],
    },
    "schema": {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "oneOf": [
            {
                "const": True,
                "title": "Avoid positive `tabindex` values, change the order of elements on the page instead.",
                "examples": [True],
            }
        ],
    },
}


def find_valid(node, file):
    is_elt = isinstance(node.value, ast.Element)

    if is_elt:
        attributes = []
        if getattr(node.value, "opening_tag", None):
            attributes = {}
            for n in node.value.opening_tag.attributes.nodes:
                attributes[str(n.name)] = str(n.value).strip("\"'")

        if "tabindex" in attributes and int(attributes["tabindex"]) > 0:
            return [
                Issue.from_node(
                    file,
                    node,
                    "Avoid positive `tabindex` values, change the order of elements on the page instead",
                    "tabindex_no_positive",
                )
            ]

    if not node.children:
        return []

    return sum((find_valid(child, file) for child in node.children), [])


def tabindex_no_positive(file, config):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    if r"tabindex" in src:
        return find_valid(root, file)

    return []
