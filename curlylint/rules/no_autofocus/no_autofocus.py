from curlylint import ast
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue

NO_AUTOFOCUS = "no_autofocus"

RULE = {
    "id": "no_autofocus",
    "type": "accessibility",
    "docs": {
        "description": "Enforce autofocus is not used on inputs.  Autofocusing elements can cause usability issues for sighted and non-sighted users.",
        "url": "https://www.curlylint.org/docs/rules/no_autofocus",
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
                "title": "The `autofocus` attribute must not be used.",
                "examples": [True],
            },
        ],
    },
}


def find_valid(node, file, target_alt):
    name = getattr(node.value, "name", None)
    is_input = (
        isinstance(node.value, ast.Element) and name and name.lower() == "input"
    )

    if is_input:
        attributes = []
        if getattr(node.value, "opening_tag", None):
            attributes = {}
            for n in node.value.opening_tag.attributes.nodes:
                attributes[str(n.name)] = str(n.value).strip("\"'")

        if "autofocus" in attributes:
            return [
                Issue.from_node(
                    file,
                    node,
                    "Do not use the `autofocus` attribute, which causes issues for screen reader users",
                    "no_autofocus",
                )
            ]

    if not node.children:
        return []

    return sum(
        (find_valid(child, file, target_alt) for child in node.children), []
    )


def no_autofocus(file, target_alt):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    if r"autofocus" in src:
        return find_valid(root, file, target_alt)

    return []
