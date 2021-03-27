# Changelog

> All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Changed

- Add more descriptive error message for missing whitespace between HTML attributes ([#23 (comment)](https://github.com/thibaudcolas/curlylint/issues/23#issuecomment-700622837), [#68](https://github.com/thibaudcolas/curlylint/pull/68)).
- Move development dependencies from extras to separate `requirements.txt` ([#68](https://github.com/thibaudcolas/curlylint/pull/68)).
- Declare support for Python 3.9.
- Tentatively declare support for Python 3.10 (tested with `Python 3.10.0a6+`).

### Fixed

- Fix Python 3.10 deprecation warning by importing Iterable from collections.abc ([#68](https://github.com/thibaudcolas/curlylint/pull/68)).

## [v0.12.2](https://github.com/thibaudcolas/curlylint/releases/tag/v0.12.2) 2021-03-06

### Fixed

- The `image_alt` rule no longer crashes when encountering template conditionals in img attributes ([#57](https://github.com/thibaudcolas/curlylint/pull/57)). Thanks to [@adrien-delhorme](https://github.com/adrien-delhorme).

## [v0.12.1](https://github.com/thibaudcolas/curlylint/releases/tag/v0.12.1) 2021-03-06

### Fixed

- The project’s sdist now includes all needed files to run the test suite ([#49](https://github.com/thibaudcolas/curlylint/issues/49), [#50](https://github.com/thibaudcolas/curlylint/pull/50)). Thanks to [@jayvdb](https://github.com/jayvdb).

## [v0.12.0](https://github.com/thibaudcolas/curlylint/releases/tag/v0.12.0) 2020-07-26

Release notes from the blog: [Accessibility linting rules](https://www.curlylint.org/blog/accessibility-linting-rules)

### Added

- Add experimental `django_forms_rendering` rule.
- Add experimental `image_alt` rule.
- Add experimental `no_autofocus` rule.
- Add experimental `tabindex_no_positive` rule.
- Add experimental `meta_viewport` rule.

### Changed

- Support parsing HTML elements with UPPERCASE or camelCase tag names, for example `clipPath`.

## [v0.11.0](https://github.com/thibaudcolas/curlylint/releases/tag/v0.11.0) 2020-05-21

### Added

- Add helpful error message when curlylint can’t find any configuration with `--print-config`.

### Changed

- Fix `--print-config` flag running linting when no config is found for the given file.
- Clarify error message for invalid `--rule` declarations.
- Publish package with Python wheels as well as egg.

### Fixed

- Fix `html_has_lang` not raising an error when the HTML element has no `lang` but has other attributes.

## [v0.10.0](https://github.com/thibaudcolas/curlylint/releases/tag/v0.10.0) 2020-05-21

### Added

- Add `--print-config` CLI flag to print the configuration for the given file.
- Add experimental `html_has_lang` rule.
- Add experimental `aria_role` rule.

### Changed

- Show a warning when attempting to use a rule that does not exist.
- Rename `parse-error` errors to `parse_error`.

### Fixed

- Fix parsing failing for self-closing SVG elements, e.g. `<path />`.

## [v0.9.0](https://github.com/thibaudcolas/curlylint/releases/tag/v0.9.0) 2020-05-14

### Added

- Add support for configuring and disabling individual rules via configuration file, under `[tool.curlylint.rules]`.
- Add support for tabs as indentation, with `indent = 'tab'`.
- Add a way to configure rules via CLI parameters, with `--rule`: `curlylint --rule 'indent: 2' template-directory/`.
- Support piping template contents from stdin with "-" as the file path.
- Publish curlylint as typed with a `py.typed` file and `Typing :: Typed` classifier.
- Add `--stdin-filepath` CLI flag to provide a pretend path when linting standard input.

### Changed

- Indentation is now enforced via the rules configuration, e.g. `indent = 4` underneath `[tool.curlylint.rules]`, instead of a top-level `indent-size` configuration.

## [v0.8.0](https://github.com/thibaudcolas/curlylint/releases/tag/v0.8.0) 2020-05-04

### Added

- Add support for configurable formatters with `--format` CLI parameter / `format` config attribute.
- Add support for JSON formatting with `--format json --quiet`.
- Add new `stylish` reporter and make it the default. `compact` is still available via `--format compact`.
- Add codes for rules – `indent` and `parse-error` for the two existing checks.

## [v0.7.0](https://github.com/thibaudcolas/curlylint/releases/tag/v0.7.0) 2020-04-16

Generally reworked the CLI to match the experience of black.

### Added

- Improve command line output, matching experience provided by black.
- Add dependencies on `toml`, `pathspec`, `dataclasses`.
- Automatically look for the configuration based on provided source paths.
- Add support for excluding files from linting with the `--exclude` / `exclude` config.
- Add support for including files for linting with the `--include` / `include` config.
- Add automatic reading of `.gitignore` and exclusion of all files ignored there.
- Add excludes for more common build tool folders: `venv`, `myvenv`, `coverage_html_report`, `node_modules`.

### Changed

- Add a `python_requires` to enforce support of Python 3.6+ only.
- Switch from docopt to click, like black, with an open-end version range.
- Change curlylint to abort if no input is provided.
- Add `-q` / `--quiet` CLI flag.
- Switch from Python config files to `pyproject.toml`

### Removed

- Remove support for `--extension` flag. Use `--include` (or `include` in the config file) instead.

## [v0.6.0](https://github.com/thibaudcolas/curlylint/releases/tag/v0.6.0) 2020-03-30

### Changed

- Open `attrs` dependency from `attrs==17.2.0` to `attrs>=17.2.0`.
- Support parsing attributes with uppercase letters (e.g. `viewBox`).

## [v0.5.0](https://github.com/thibaudcolas/curlylint/releases/tag/v0.5.0) 2020-03-24

First usable release as `curlylint`! This release is functionally equivalent to [jinjalint 0.5](https://pypi.org/project/jinjalint/0.5/), with different metadata, and a different package & executable name.

### Migration guide from jinjalint

1. Uninstall jinjalint from your project.
2. If needed, make sure to also uninstall its dependencies: `parsy==1.1.0`, `attrs==17.2.0`, `docopt==0.6.2`.
3. Install curlylint from PyPI.
4. Replace the `jinjalint` executable with `curlylint` wherever necessary.

---

## [v0.5.0-jinjalint](https://github.com/thibaudcolas/curlylint/releases/tag/v0.5.0-jinjalint) 2018-11-10

- c60bea7: Fix a few edge cases with attribute parsing.
- 402130a: Fix parser bug with some tags like <colgroup>, tags beginning with col or br were parsed incorrectly.

## [v0.4.0-jinjalint](https://github.com/thibaudcolas/curlylint/releases/tag/v0.4.0-jinjalint) 2018-11-04

## [v0.3.0-jinjalint](https://github.com/thibaudcolas/curlylint/releases/tag/v0.3.0-jinjalint) 2018-11-04

- 0abd2c2: Optional Jinja containers support:

```html
{% if something %}<a href="somewhere"
  >{% endif %}
  <p>something</p>
  {% if something %}</a
>{% endif %}
```

This pattern is pretty common in real-world projects. I finally found a way to parse it.

- fa60351, [#11](https://github.com/motet-a/jinjalint/issues/11): Jinja whitespace control syntax support:

```html
{%- foo -%} {%- foo %} {{- bar -}} {{ bar -}} {%+ foo %} {{+ bar }}
```

There is no such thing in the Django flavor.

## [v0.2.0-jinjalint](https://github.com/thibaudcolas/curlylint/releases/tag/v0.2.0-jinjalint) 2018-11-04

## [v0.1.0-jinjalint](https://github.com/thibaudcolas/curlylint/releases/tag/v0.1.0-jinjalint) 2017-11-10

---

## [vx.y.z](https://github.com/thibaudcolas/curlylint/releases/tag/x.y.z) (Template: https://keepachangelog.com/en/1.0.0/)

### Added

- Something was added to the API / a new feature was introduced.

### Changed

### Fixed

### Removed

### How to upgrade
