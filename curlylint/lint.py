import sys
from pathlib import Path
from typing import Set

import parsy

from .check import check_file, check_files
from .file import File
from .issue import Issue, IssueLocation
from .parse import make_parser


def get_parsy_error_location(error, file_path):
    line, column = parsy.line_info_at(error.stream, error.index)
    return IssueLocation(line=line, column=column, file_path=file_path)


def parse_file(path_and_config):
    """
    Returns a tuple ([Issue], File | None).
    """
    path, config = path_and_config

    with path.open("r") as f:
        source = f.read()

    return parse_source(path, config, source)


def parse_source(path: Path, config, source: str):
    parser = make_parser(config)

    try:
        file = File(
            path=path,
            source=source,
            lines=source.split("\n"),
            tree=parser["content"].parse(source),
        )
        return [], file
    except parsy.ParseError as error:
        location = get_parsy_error_location(error, path)
        issue = Issue(location, "Parse error: " + str(error), "parse_error")
        return [issue], None


def lint(paths: Set[Path], config):
    issues = []
    files = []

    from multiprocessing import Pool

    pool = Pool()

    parse_file_args = ((p, config) for p in paths)
    results = pool.map(parse_file, parse_file_args)
    for result in results:
        parse_issues, file = result
        issues += parse_issues
        if file is not None:
            files.append(file)

    if config.get("parse_only", False):
        return issues

    rules = config.get("rules")

    if rules:
        issues += check_files(files, rules)

    return issues


def lint_one(path: Path, config):
    if not path.is_file() and str(path) == "-":
        source = sys.stdin.read()
        parse_issues, file = parse_source(
            config.get("stdin_filepath", path), config, source
        )
    else:
        parse_issues, file = parse_file((path, config))

    issues = parse_issues

    if config.get("parse_only", False):
        return issues

    rules = config.get("rules")

    if rules and file is not None:
        issues += check_file(file, rules)

    return issues
