from pathlib import Path
import parsy

from .parse import make_parser
from .util import flatten
from .check import check_files
from .issue import Issue, IssueLocation
from .file import File


def get_parsy_error_location(error, file_path):
    line, column = parsy.line_info_at(error.stream, error.index)
    return IssueLocation(
        line=line,
        column=column,
        file_path=file_path,
    )


def resolve_file_paths_(input_name, extensions):
    path = Path(input_name)
    if not path.exists():
        raise Exception('{} does not exist'.format(path))

    if path.is_dir():
        return flatten(
            resolve_file_paths_(child, extensions) for child in path.iterdir()
        )

    if not path.is_file():
        raise Exception('{} is not a regular file'.format(path))

    return [path] if path.suffix in extensions else []


def resolve_file_paths(input_names, extensions):
    path_lists = (resolve_file_paths_(i, extensions) for i in input_names)
    return flatten(path_lists)


def parse_file(path_and_config):
    """
    Returns a tuple ([Issue], File | None).
    """
    path, config = path_and_config

    with path.open('r') as f:
        source = f.read()

    parser = make_parser(config)

    try:
        file = File(
            path=path,
            source=source,
            lines=source.split('\n'),
            tree=parser['content'].parse(source),
        )
        return [], file
    except parsy.ParseError as error:
        location = get_parsy_error_location(error, path)
        issue = Issue(location, 'Parse error: ' + str(error))
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

    issues += check_files(files)
    return issues
