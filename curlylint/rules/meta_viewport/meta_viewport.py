from curlylint import ast
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue

META_VIEWPORT = "meta_viewport"

RULE = {
    "id": "meta_viewport",
    "type": "accessibility",
    "docs": {
        "description": "The `viewport` meta tag should not use `user-scalable=no`, and `maximum-scale` should be 2 or above, so end users can zoom",
        "url": "https://www.curlylint.org/docs/rules/meta_viewport",
        "impact": "Critical",
        "tags": ["cat.language", "wcag2aa", "wcag144"],
        "resources": [
            "[Understanding WCAG SC 1.4.4 Resize Text](http://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-scale.html)",
            "[axe-core, meta-viewport](https://dequeuniversity.com/rules/axe/3.5/meta-viewport)",
        ],
    },
    "schema": {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "oneOf": [
            {
                "const": True,
                "title": "`user-scalable=no` must not be used, and `maximum-scale` should be 2 or above.",
                "examples": [True],
            },
        ],
    },
}


def find_valid(node, file):
    name = getattr(node.value, "name", None)
    is_meta = (
        isinstance(node.value, ast.Element) and name and name.lower() == "meta"
    )

    if is_meta:
        attributes = []
        if getattr(node.value, "opening_tag", None):
            attributes = {}
            for n in node.value.opening_tag.attributes.nodes:
                attributes[str(n.name)] = str(n.value).strip("\"'")

        if "name" in attributes and attributes["name"] == "viewport":
            if "user-scalable=no" in attributes["content"]:
                return [
                    Issue.from_node(
                        file,
                        node,
                        "Remove `user-scalable=no` from the viewport meta so users can zoom",
                        "meta_viewport",
                    )
                ]

            if (
                "maximum-scale=1" in attributes["content"]
                or "maximum-scale=0" in attributes["content"]
            ):
                return [
                    Issue.from_node(
                        file,
                        node,
                        "`maximum-scale` should not be less than 2",
                        "meta_viewport",
                    )
                ]

    if not node.children:
        return []

    return sum((find_valid(child, file) for child in node.children), [])


def meta_viewport(file, config):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    if r"user-scalable" in src or r"maximum-scale" in src:
        return find_valid(root, file)

    return []
