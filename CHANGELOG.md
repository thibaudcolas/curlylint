# Changelog

> All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased

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
