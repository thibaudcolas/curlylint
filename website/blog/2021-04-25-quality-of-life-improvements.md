---
slug: quality-of-life-improvements
title: Quality-of-life improvements
author: Thibaud Colas
author_url: https://github.com/thibaudcolas
author_image_url: https://avatars1.githubusercontent.com/u/877585?s=460&v=4
tags: [roadmap, inspirations]
---

Curlylint v0.13.0 is out. It’s a relatively minor release, but comes with a few nice-to-haves for users, and a lot of behind-the-scenes project changes.

<!-- truncate -->

## Modern Python support

Curlylint now officially supports Python 3.9, and (tentatively) Python 3.10, based on the 6th alpha release. From now on, you can expect support for all Python versions [actively supported by CPython maintainers](https://devguide.python.org/#status-of-python-branches). In the future, this will also mean actively removing support for Python versions that reach their scheduled end-of-life.

## Removed extras for development dependencies

Python packaging is very messy. I’ve recently started using the [Poetry](https://python-poetry.org/) package manager at work, primarily for the benefit of having lockfiles to pin transitive dependencies on application-style projects (a must, in my opinion). Here is an excerpt of what installing curlylint looks like in a `poetry.lock`:

```ini
[[package]]
name = "curlylint"
version = "0.12.2"
description = "{{ 🎀}} Experimental HTML templates linting for Jinja, Nunjucks, Django templates, Twig, Liquid"
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
attrs = ">=17.2.0"
click = ">=6.5"
dataclasses = {version = ">=0.6", markers = "python_version < \"3.7\""}
parsy = "1.1.0"
pathspec = ">=0.6,<1"
toml = ">=0.9.4"

[package.extras]
dev = ["black (==19.10b0)", "flake8 (==3.8.4)", "mypy (==0.812)", "pytest (==6.2.2)", "coverage (==5.4)"]
```

I find this last line very puzzling – there really should be no need for dependencies intended only for development to be visible in the published package. I don’t want curlylint’s development dependencies changing from release to release to cause noise in upgrade diffs, hence why the `dev` extra has been removed.

It’s worth saying Poetry has otherwise been a pleasure to work with, with only a few minor inconveniences like this one. I would happily recommend it to people wanting more out of their Python package management.

## New `--template-tags` CLI flag

As the [`--template-tags` documentation](https://www.curlylint.org/docs/command-line-usage#--template-tags) now states, this makes Curlylint aware of custom tags used in templates, so the parser can understand they contain HTML content to go through.

This option was previously only available via a TOML configuration file, via the (now deprecated) `jinja-custom-elements-names` / `jinja_custom_elements_names` setting. The new setting works the same, but can also be set via CLI flags.

## Behind-the-scenes changes

There really is only one I want to highlight – improvements to Curlylint’s test suite, which have resulted in a [14% increase in test coverage](https://coveralls.io/github/thibaudcolas/curlylint?branch=main). While test coverage percentages generally don’t mean much, in this case this means:

- The command line interface now has unit tests. While relatively basic in the current iteration, they should be very easy to add to.
- The parser has more unit tests, and they are now in line with the rest of the test suite.

[![Screen capture of the Coveralls coverage score over time as an area chart, from 59% in early March to 74% now](/img/blog/2021-04-25-quality-of-life-improvements/coverage-over-time.png)](https://coveralls.io/github/thibaudcolas/curlylint)

> [Coveralls](https://coveralls.io/) shows coverage increasing from 59.39% in early March to 74% in late April.

Having comprehensive unit tests really matters to me as a maintainer, and from now on it should be much more realistic to expect all changes to the project to come with corresponding unit tests.

## Up next

There are a lot of [parser bugs](https://github.com/thibaudcolas/curlylint/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3Aparser) I will now feel much more comfortable approaching, due to having a way to easily write tests for them.

Short-term, I want to make sure to get to all of the open pull request, hopefully fully clearing the backlog. I can see people are responding very well to Curlylint despite its experimental nature, and are eager to help making it more useful:

- [#53 Optional HTML container parsing for if-else-endif type code](https://github.com/thibaudcolas/curlylint/pull/53)
- [#75 Add test for unresolved missing alt attribute inside django block (#72)](https://github.com/thibaudcolas/curlylint/pull/75)
- [#76 Use types_or directive for hook instead of files](https://github.com/thibaudcolas/curlylint/pull/76)

For me, the most immediate next step will be presenting Curlylint at [PyCon US 2021](https://us.pycon.org/2021/)! I hope to get critical feedback on the tool, and am also working on an “online playground” version to try lint templates without installing anything, we should make it simpler for people to try out the linter.
