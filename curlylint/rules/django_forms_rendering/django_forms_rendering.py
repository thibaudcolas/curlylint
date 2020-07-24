from curlylint import ast
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue

DJANGO_FORMS_RENDERING = "django_forms_rendering"

RULE = {
    "id": "django_forms_rendering",
    "type": "accessibility",
    "docs": {
        "description": "Disallows using Django’s convenience form rendering helpers, for which the markup isn’t screen-reader-friendly",
        "url": "https://www.curlylint.org/docs/rules/django_forms_rendering",
        "impact": "Serious",
        "tags": ["wcag2a", "wcag131"],
        "resources": [
            "[WCAG2.1 SC 1.3.1: Info and Relationships (Level A)](https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships.html)",
        ],
    },
    "schema": {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "oneOf": [
            {
                "const": True,
                "title": "Forms cannot be rendered with as_table, as_ul, or as_p",
                "examples": [True],
            },
            {"const": "as_p", "title": "Allows as_p", "examples": ["as_p"]},
        ],
    },
}


def find_valid(node, file, disallowed_variants):
    if isinstance(node.value, ast.JinjaVariable):
        matches = [v for v in disallowed_variants if v in node.value.content]
        if matches:
            return [
                Issue.from_node(
                    file,
                    node,
                    f"Avoid using `{matches[0]}` to render Django forms",
                    DJANGO_FORMS_RENDERING,
                )
            ]

    if not node.children:
        return []

    return sum(
        (
            find_valid(child, file, disallowed_variants)
            for child in node.children
        ),
        [],
    )


def django_forms_rendering(file, target):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    if r".as_table" in src or ".as_ul" in src or ".as_p" in src:
        disallowed_variants = (
            ["as_table", "as_ul"]
            if target == "as_p"
            else ["as_table", "as_ul", "as_p"]
        )

        return find_valid(root, file, disallowed_variants)

    return []
