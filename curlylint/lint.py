import parsy

from .check import check_files
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
        issue = Issue(location, "Parse error: " + str(error))
        return [issue], None


def lint(paths, config):
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

    if not config.get("parse_only", False):
        issues += check_files(files, config)

    return issues
