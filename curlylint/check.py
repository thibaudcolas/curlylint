from .util import flatten

from curlylint.rules.indent.indent import indent

checks = [indent]


def check_file(file, config):
    return set(flatten(check(file, config) for check in checks))


def check_files(files, config):
    return flatten(check_file(file, config) for file in files)
