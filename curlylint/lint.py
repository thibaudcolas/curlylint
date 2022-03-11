import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Set

import parsy

from .check import check_file
from .file import File
from .issue import Issue, IssueLocation
from .parse import make_parser

PARSER = None


def _make_parser(config):
    """
    Process initializer
    """
    global PARSER
    PARSER = make_parser(config)


def get_parsy_error_location(error, file_path):
    line, column = parsy.line_info_at(error.stream, error.index)
    return IssueLocation(line=line, column=column, file_path=file_path)


def parse_file(path):
    """
    Returns a tuple ([Issue], File | None).
    """
    with path.open("r") as f:
        source = f.read()

    return parse_source(path, source)


def parse_source(path: Path, source: str):
    try:
        file = File(
            path=path,
            source=source,
            lines=source.split("\n"),
            tree=PARSER["content"].parse(source),
        )
        return [], file
    except parsy.ParseError as error:
        location = get_parsy_error_location(error, path)
        issue = Issue(location, "Parse error: " + str(error), "parse_error")
        return [issue], None


def lint(paths: Set[Path], config):
    issues = []

    parse_only = config.get("parse_only", False)
    rules = config.get("rules")

    with ProcessPoolExecutor(
        initializer=_make_parser, initargs=(config,)
    ) as executor:
        futures = [executor.submit(parse_file, path) for path in paths]
        for future in as_completed(futures):
            parse_issues, file = future.result()
            issues.extend(parse_issues)
            if file is not None and not parse_only:
                issues.extend(check_file(file, rules))

    return issues


def lint_one(path: Path, config):
    _make_parser(config)

    if not path.is_file() and str(path) == "-":
        source = sys.stdin.read()
        parse_issues, file = parse_source(
            config.get("stdin_filepath", path), source
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
