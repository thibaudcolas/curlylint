---
title: Getting Started
slug: /
---

Start by installing curlylint with pip:

```bash
pip install curlylint
```

We support [all active Python releases](https://devguide.python.org/#status-of-python-branches).

Make sure curlylint is correctly installed by running:

```bash
curlylint --version
curlylint --help
```

You can start linting!

```bash
curlylint template-directory/
# Or,
curlylint some-file.html some-other-file.html
```

Without any configuration, curlylint will only parse the templates and not run any linting rules. Have a look at our other documentation pages to make the most of it.
