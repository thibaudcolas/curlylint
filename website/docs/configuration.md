---
slug: configuration
title: Configuration
---

Curlylint is able to read project-specific default values for its command line options, or from a [PEP 518](https://www.python.org/dev/peps/pep-0518/) `pyproject.toml` file.

## Command Line flags

See [Command Line Usage](command-line-usage) for all flags.

## `pyproject.toml`

### Where Curlylint looks for the file

By default Curlylint looks for `pyproject.toml` starting from the common base directory of all files and directories passed on the command line. If it's not there, it looks in parent directories. It stops looking when it finds the file, or a `.git` directory, or a `.hg` directory, or the root of the file system, whichever comes first.

You can also explicitly specify the path to a particular file that you want with `--config`.

Use `--verbose` to display whether a file was found and used.

### Configuration format

`pyproject.toml` is a [TOML](https://github.com/toml-lang/toml) file. It contains separate sections for
different tools. Curlylint is using the `[tool.curlylint]` section. The option keys are the same as long names of options on the command line.

Example `pyproject.toml`, note how rules are under `[tool.curlylint.rules]`:

```toml
[tool.curlylint]
include = '\.(html|jinja)$'
exclude = '''
(
  /(
      \.eggs           # exclude a few common directories in the root of the project
    | \.git
    | \.venv
  )/
  | webpack-stats.html # also separately exclude a file named webpack-stats.html in the root of the project
)
'''

[tool.curlylint.rules]
indent = 4
html_has_lang = 'en-GB'
```

### Lookup hierarchy

Command-line options have defaults that you can see in `--help`. A `pyproject.toml` can override those defaults. Finally, options provided by the user on the command line override both.

Curlylint will only ever use one `pyproject.toml` file during an entire run. It doesn't look for multiple files, and doesn't compose configuration from different levels of the file hierarchy.
