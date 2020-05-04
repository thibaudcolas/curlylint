from curlylint.rules.indent.indent import INDENT, indent
from curlylint.util import flatten

checks = {INDENT: indent}


def check_rule(file, code: str, options):
    check = checks.get(code, None)
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
