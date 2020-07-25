from curlylint import ast
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue

HTML_HAS_LANG = "html_has_lang"

RULE = {
    "id": "html_has_lang",
    "type": "accessibility",
    "docs": {
        "description": "`<html>` elements must have a `lang` attribute, using a [BCP 47](https://www.ietf.org/rfc/bcp/bcp47.txt) language tag.",
        "url": "https://www.curlylint.org/docs/rules/html_has_lang",
        "impact": "Serious",
        "tags": ["cat.language", "wcag2a", "wcag311"],
        "resources": [
            "[WCAG2.1 SC 3.1.1: Language of Page (Level A)](https://www.w3.org/WAI/WCAG21/Understanding/language-of-page)",
            "[axe-core, html-has-lang](https://dequeuniversity.com/rules/axe/3.5/html-has-lang)",
            "[axe-core, html-lang-valid](https://dequeuniversity.com/rules/axe/3.5/html-lang-valid)",
            "[eslint-plugin-jsx-a11y, html-has-lang](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/html-has-lang.md)",
        ],
    },
    "schema": {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "oneOf": [
            {
                "const": True,
                "title": "The `lang` attribute must be present.",
                "examples": [True],
            },
            {
                "type": "string",
                "title": "The `lang` attribute must match the configured language tag.",
                "examples": ["en-US"],
            },
            {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True,
                "title": "The `lang` attribute must match one of the configured language tags.",
                "examples": [["en", "en-US"]],
            },
        ],
    },
}


def find_valid(node, file, target_lang):
    name = getattr(node.value, "name", None)
    is_html = (
        isinstance(node.value, ast.Element) and name and name.lower() == "html"
    )

    if is_html:
        attributes = []
        if getattr(node.value, "opening_tag", None):
            attributes = {}
            for n in node.value.opening_tag.attributes.nodes:
                attributes[str(getattr(n, "name", ""))] = str(
                    getattr(n, "value", "")
                ).strip("\"'")
        if len(attributes) == 0 or "lang" not in attributes:
            return [
                Issue.from_node(
                    file,
                    node,
                    "The `<html>` tag should have a `lang` attribute with a valid value, describing the main language of the page",
                    "html_has_lang",
                )
            ]

        if target_lang[0] is True or attributes["lang"] in target_lang:
            return []
        else:
            return [
                Issue.from_node(
                    file,
                    node,
                    f"The `<html>` tag should have a `lang` attribute with a valid value, describing the main language of the page. Allowed values: {', '.join(target_lang)}",
                    "html_has_lang",
                )
            ]

    if not node.children:
        return []

    return sum(
        (find_valid(child, file, target_lang) for child in node.children), []
    )


def html_has_lang(file, target_lang):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    target = (
        target_lang
        if isinstance(target_lang, (tuple, list))
        else (target_lang,)
    )

    if r"<html" in src:
        return find_valid(root, file, target)

    return []
