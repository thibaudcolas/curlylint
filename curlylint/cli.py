"""curlylint

Usage:
  curlylint [-v | --verbose] [--config CONFIG] [--parse-only]
            [--extension EXT | -e EXT]... [INPUT ...]
  curlylint (-h | --help)
  curlylint --version

Options:
  -h --help             Show this help message and exit.
  --version             Show version information and exit.
  -v --verbose          Verbose mode.
  -c --config CONFIG    Specify the configuration file.
  --parse-only          Don’t lint, check for syntax errors and exit.
  -e --extension EXT    Extension of the files to analyze (used if INPUT
                        contains directories to crawl).
                        [default: html jinja twig]

The configuration file must be a valid Python file.
"""
from docopt import docopt

from .lint import lint, resolve_file_paths
from .config import parse_config


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
    extensions = ['.' + e for e in arguments['--extension']]
    verbose = arguments['--verbose']

    if arguments['--version']:
        print('0.5.0')
        return

    if arguments['--config']:
        if verbose:
            print('Using configuration file {}'.format(arguments['--config']))
        config = parse_config(arguments['--config'])
    else:
        config = {}

    config['verbose'] = verbose
    config['parse_only'] = arguments['--parse-only']

    paths = list(resolve_file_paths(input_names, extensions=extensions))

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
