from curlylint import ast
from curlylint.ast import JinjaElement
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue

IMAGE_ALT = "image_alt"

RULE = {
    "id": "image_alt",
    "type": "accessibility",
    "docs": {
        "description": "`<img>` elements must have a `alt` attribute, either with meaningful text, or an empty string for decorative images",
        "url": "https://www.curlylint.org/docs/rules/image_alt",
        "impact": "Serious",
        "tags": ["cat.language", "wcag2a", "wcag111"],
        "resources": [
            "[WCAG2.1 SC 1.1.1: Non-text Content (Level A)](https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html)",
            "[axe-core, image-alt](https://dequeuniversity.com/rules/axe/3.5/image-alt)",
            "[eslint-plugin-jsx-a11y, alt-text](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/alt-text.md)",
        ],
    },
    "schema": {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "oneOf": [
            {
                "const": True,
                "title": "The `alt` attribute must be present.",
                "examples": [True],
            },
        ],
    },
}


def find_valid(node, file, target_alt):
    name = getattr(node.value, "name", None)
    is_img = (
        isinstance(node.value, ast.Element) and name and name.lower() == "img"
    )

    if is_img:
        attributes = []
        if getattr(node.value, "opening_tag", None):
            attributes = {}
            for n in node.value.opening_tag.attributes.nodes:
                if not isinstance(n, JinjaElement):
                    attributes[str(n.name)] = str(n.value).strip("\"'")

        if len(attributes) == 0 or "alt" not in attributes:
            return [
                Issue.from_node(
                    file,
                    node,
                    "The `<img>` tag must have a `alt` attribute, either with meaningful text, or an empty string for decorative images",
                    "image_alt",
                )
            ]

    if not node.children:
        return []

    return sum(
        (find_valid(child, file, target_alt) for child in node.children), []
    )


def image_alt(file, target_alt):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    if r"<img" in src:
        return find_valid(root, file, target_alt)

    return []
