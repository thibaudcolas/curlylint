"""jinjalint

Usage:
  jinjalint [options] [INPUT ...]

Options:
  -h --help          Show this help message and exit.
  --version          Show version information and exit.
  -v --verbose       Verbose mode.
  -c --config FILE   Specify the configuration file.
  --parse-only       Don’t lint, check for syntax errors and exit.

The configuration file must be a valid Python file.
"""
from docopt import docopt

from .lint import lint, resolve_file_paths
from .config import parse_config
from ._version import get_versions


def print_issues(issues, config):
    sorted_issues = sorted(
        issues,
        key=lambda i: (
            i.location.file_path,
            i.location.line,
            i.location.column
        ),
    )

    for issue in sorted_issues:
        print(str(issue))


def main():
    arguments = docopt(__doc__)

    input_names = arguments['INPUT'] or ['.']
    verbose = arguments['--verbose']

    if arguments['--version']:
        print(get_versions()['version'])
        return

    if arguments['--config']:
        if verbose:
            print('Using configuration file {}'.format(arguments['--config']))
        config = parse_config(arguments['--config'])
    else:
        config = {}

    config['verbose'] = verbose
    config['parse_only'] = arguments['--parse-only']

    paths = list(resolve_file_paths(input_names, extensions=['.html']))

    if verbose:
        print('Files being analyzed:')
        print('\n'.join(str(p) for p in paths))
        print()

    issues = lint(paths, config)
    print_issues(issues, config)

    if any(issues):
        exit(1)


if __name__ == '__main__':
    main()
