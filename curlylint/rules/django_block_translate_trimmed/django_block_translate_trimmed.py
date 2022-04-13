from curlylint import ast
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue

DJANGO_FORMS_RENDERING = "django_block_translate_trimmed"

RULE = {
    "id": "django_block_translate_trimmed",
    "type": "internationalisation",
    "docs": {
        "description": "Enforces the use of Django’s `trimmed` option when using `blocktranslate`/`blocktrans` so that translations do not contain leading or trailing whitespace.",
        "url": "https://www.curlylint.org/docs/rules/django_block_translate_trimmed",
        "impact": "Serious",
        "tags": ["cat:language"],
        "resources": [
            "[Django translations](https://docs.djangoproject.com/en/stable/topics/i18n/translation/)",
        ],
    },
    "schema": {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "oneOf": [
            {
                "const": True,
                "title": "Template tags of blocktranslate or blocktrans must use the trimmed option",
                "examples": [True],
            }
        ],
    },
}

BLOCK_NAMES = ["blocktranslate", "blocktrans"]


def find_valid(node, file):

    if isinstance(node.value, ast.JinjaElement):
        for part in node.value.parts:

            tag = part.tag

            if tag.name in BLOCK_NAMES:
                if "trimmed" not in tag.content.split(" "):
                    return [
                        Issue.from_node(
                            file,
                            node,
                            f"`{tag}` must use the `trimmed` option",
                            DJANGO_FORMS_RENDERING,
                        )
                    ]

    if not node.children:
        return []

    return sum(
        (find_valid(child, file) for child in node.children),
        [],
    )


def django_block_translate_trimmed(file, target):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    if "blocktrans" in src or "blocktranslate" in src:
        return find_valid(root, file)

    return []
