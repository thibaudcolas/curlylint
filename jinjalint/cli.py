"""jinjalint

Usage:
  jinjalint [options] [INPUT ...]

Options:
  -h --help          Show this help message and exit.
  -v --verbose       Verbose mode.
  -c --config FILE   Specify the configuration file.

The configuration file must be a valid Python file.
"""
from docopt import docopt

from .lint import lint, resolve_file_paths
from .config import parse_config


def print_issues(issues, config):
    sorted_issues = sorted(
        issues,
        key=lambda i: (i.location.file_path, i.location.line),
    )

    for issue in sorted_issues:
        print(str(issue))


def main():
    arguments = docopt(__doc__)

    input_names = arguments['INPUT'] or ['.']
    verbose = arguments['--verbose']

    if arguments['--config']:
        if verbose:
            print('Using configuration file {}'.format(arguments['--config']))
        config = parse_config(arguments['--config'])
    else:
        config = {}

    config['verbose'] = verbose

    paths = list(resolve_file_paths(input_names, extensions=['.html']))

    if verbose:
        print('Files being analyzed:')
        print('\n'.join(str(p) for p in paths))
        print()

    issues = lint(paths, config)
    print_issues(issues, config)


if __name__ == '__main__':
    main()
