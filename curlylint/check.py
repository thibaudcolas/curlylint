from functools import partial

import click

from curlylint.rules.html_has_lang.html_has_lang import (
    HTML_HAS_LANG,
    html_has_lang,
)
from curlylint.rules.aria_role.aria_role import (
    ARIA_ROLE,
    aria_role,
)
from curlylint.rules.indent.indent import INDENT, indent
from curlylint.util import flatten

err = partial(click.secho, fg="red", err=True)

checks = {HTML_HAS_LANG: html_has_lang, ARIA_ROLE: aria_role, INDENT: indent}


def check_rule(file, code: str, options):
    check = checks.get(code, None)

    if not check:
        err("Warning: rule `{}` does not exist.".format(code))
        return []

    return check(file, options)


def check_file(file, rules):
    return set(
        flatten(
            check_rule(file, code, options)
            for code, options in rules.items()
            if options != "off"
        )
    )


def check_files(files, rules):
    return flatten(check_file(file, rules) for file in files)
