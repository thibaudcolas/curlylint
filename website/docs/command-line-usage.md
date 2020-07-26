---
id: command-line-usage
title: Command Line Usage
---

Curlylint is a CLI tool first and foremost, all of its functionality can be configured via command line flags.

## Flags

### `--version`

Show the version and exit.

```bash
curlylint --version
```

### `--verbose`

Turns on verbose mode. This makes it easier to troubleshoot what configuration is used, and what files are being linted.

```bash
curlylint --verbose template-directory/
```

### `--quiet`

Don’t emit non-error messages to stderr. Errors are still emitted; silence those with `2>/dev/null`.

```bash
curlylint --quiet template-directory/
# To silence even errors,
curlylint --quiet template-directory/ 2>/dev/null
```

### `--parse-only`

Don’t lint, check for syntax errors and exit.

```bash
curlylint --parse-only template-directory/
```

### `--print-config`

Print the configuration for the given file, and exit.

```bash
curlylint --print-config some-file.html
```

### `--format`

Use a specific output format. [default: stylish, options: compact|json|stylish]

```bash
curlylint --format json some-file.html
```

### `--include`

A regular expression that matches files and directories that should be included on recursive searches. An empty value means all files are included regardless of the name. Use forward slashes for directories on all platforms (Windows, too). Exclusions are calculated first, inclusions later. [default: \.(html|jinja|twig)$]

```bash
curlylint --parse-only --include .njk nunjucks-templates/
```

### `--exclude`

A regular expression that matches files and directories that should be excluded on recursive searches. An empty value means no paths are excluded. Use forward slashes for directories on all platforms (Windows, too). Exclusions are calculated first, inclusions later. [default: /(\.eggs|\.git|\.hg|\.mypy _cache|\.nox|\.tox|\.venv|venv|myvenv|\.svn| _build|buck-out|build|dist|coverage_html_report|node_modules)/]

### `--rule`

Specify rules, with the syntax `--rule 'code: {"json": "value"}'`. Can be provided multiple times to configure multiple rules.

🚧 **Note the rules’ values are formatted as JSON.** Numbers can be specified as-is, booleans as true/false. Strings must be wrapped in double quotes. Arrays or objects use JSON syntax.

```bash
curlylint --rule 'indent: 2' --rule 'html_has_lang: true' template-directory/
curlylint --rule 'html_has_lang: "en"' template-directory/
curlylint --rule 'html_has_lang: ["en", "en-US"]' template-directory/
```

### `--config`

Read configuration from the provided file.

```bash
curlylint--config test_pyproject.toml template-directory/
```

## Reading from standard input

Pipe the template to curlylint and use a path of `-` so curlylint reads from stdin:

```bash
cat some-file.html | curlylint -
```

The `--stdin-filepath` flag can be used to provide a fake path corresponding to the piped template for linting and reporting:

```bash
cat some-file.html | curlylint - --stdin-filepath some-file.html
```
