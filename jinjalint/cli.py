"""jinjalint

Usage:
  jinjalint [options] [INPUT ...]

Options:
  -h --help     Show this help message and exit.
  -v --verbose  Verbose mode.
"""
from docopt import docopt

from .lint import lint, resolve_file_paths


def print_issues(issues):
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

    paths = list(resolve_file_paths(input_names, extensions=['.html']))

    if verbose:
        print('Files being analyzed:')
        print('\n'.join(str(p) for p in paths))
        print()

    issues = lint(paths)
    print_issues(issues)
