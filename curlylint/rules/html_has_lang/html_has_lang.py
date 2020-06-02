from curlylint import ast
from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue, IssueLocation

HTML_HAS_LANG = "html_has_lang"

RULE = {
    "docs": {
        "description": "<html> elements must have a `lang` attribute",
        "url": "",
    },
    "schema": [],
}


def find_valid(node, file, target_lang):
    name = getattr(node.value, "name", None)
    is_html = (
        isinstance(node.value, ast.Element) and name and name.lower() == "html"
    )
    attributes = []
    if getattr(node.value, "opening_tag", None):
        attributes = {}
        for n in node.value.opening_tag.attributes.nodes:
            attributes[str(n.name)] = str(n.value).strip("\"'")

    if is_html and len(attributes) == 0:
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

    if is_html and "lang" in attributes:
        if target_lang[0] is True:
            return []
        else:
            return (
                []
                if attributes["lang"] in target_lang
                else [
                    Issue(
                        IssueLocation(
                            file_path=file.path,
                            line=node.value.begin.line + 1,
                            column=node.value.begin.column + 1,
                        ),
                        f"The `<html>` tag should have a `lang` attribute with a valid value, describing the main language of the page. Allowed values: {', '.join(target_lang)}",
                        "html_has_lang",
                    )
                ]
            )

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
