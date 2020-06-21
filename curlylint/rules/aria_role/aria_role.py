from curlylint.check_node import CheckNode, build_tree
from curlylint.issue import Issue, IssueLocation

ARIA_ROLE = "aria_role"

RULE = {
    "id": "aria_role",
    "type": "accessibility",
    "docs": {"description": "role attributes must be valid", "url": ""},
    "schema": [],
}

VALID_ROLES = (
    # Abstract roles, which shouldn’t ever be used in web pages – included here for reference.
    # "command",
    # "composite",
    # "input",
    # "landmark",
    # "range",
    # "roletype",
    # "section",
    # "sectionhead",
    # "select",
    # "structure",
    # "widget",
    # "window",
    "alert",
    "alertdialog",
    "application",
    "article",
    "banner",
    "button",
    "cell",
    "checkbox",
    "columnheader",
    "combobox",
    "complementary",
    "contentinfo",
    "definition",
    "dialog",
    "directory",
    "document",
    "feed",
    "figure",
    "form",
    "grid",
    "gridcell",
    "group",
    "heading",
    "img",
    "link",
    "list",
    "listbox",
    "listitem",
    "log",
    "main",
    "marquee",
    "math",
    "menu",
    "menubar",
    "menuitem",
    "menuitemcheckbox",
    "menuitemradio",
    "navigation",
    "none",
    "note",
    "option",
    "presentation",
    "progressbar",
    "radio",
    "radiogroup",
    "region",
    "row",
    "rowgroup",
    "rowheader",
    "scrollbar",
    "search",
    "searchbox",
    "separator",
    "slider",
    "spinbutton",
    "status",
    "switch",
    "tab",
    "table",
    "tablist",
    "tabpanel",
    "term",
    "textbox",
    "timer",
    "toolbar",
    "tooltip",
    "tree",
    "treegrid",
    "treeitem",
    "doc-abstract",
    "doc-acknowledgments",
    "doc-afterword",
    "doc-appendix",
    "doc-backlink",
    "doc-biblioentry",
    "doc-bibliography",
    "doc-biblioref",
    "doc-chapter",
    "doc-colophon",
    "doc-conclusion",
    "doc-cover",
    "doc-credit",
    "doc-credits",
    "doc-dedication",
    "doc-endnote",
    "doc-endnotes",
    "doc-epigraph",
    "doc-epilogue",
    "doc-errata",
    "doc-example",
    "doc-footnote",
    "doc-foreword",
    "doc-glossary",
    "doc-glossref",
    "doc-index",
    "doc-introduction",
    "doc-noteref",
    "doc-notice",
    "doc-pagebreak",
    "doc-pagelist",
    "doc-part",
    "doc-preface",
    "doc-prologue",
    "doc-pullquote",
    "doc-qna",
    "doc-subtitle",
    "doc-tip",
    "doc-toc",
)


def find_role_errors(node, file, target_roles):
    attributes = []
    if getattr(node.value, "opening_tag", None):
        attributes = {}
        for n in node.value.opening_tag.attributes.nodes:
            attributes[str(n.name)] = str(n.value).strip("\"'")

    target = VALID_ROLES if target_roles is True else target_roles

    if "role" in attributes:
        return (
            []
            if attributes["role"] in target
            else [
                Issue(
                    IssueLocation(
                        file_path=file.path,
                        line=node.value.begin.line + 1,
                        column=node.value.begin.column + 1,
                    ),
                    "The `role` attribute needs to have a valid value",
                    "aria_role",
                )
            ]
        )

    if not node.children:
        return []

    return sum(
        (
            find_role_errors(child, file, target_roles)
            for child in node.children
        ),
        [],
    )


def aria_role(file, target_roles):
    root = CheckNode(None)
    build_tree(root, file.tree)
    src = file.source.lower()

    if r" role" in src:
        return find_role_errors(root, file, target_roles)

    return []
