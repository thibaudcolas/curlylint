---
id: integrations
title: Integrations
---

## Editor integration

We would love to have Curlylint directly integrate with IDEs – but it’s not there yet.

## Usage with [pre-commit](https://pre-commit.com) git hooks framework

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/thibaudcolas/curlylint
  rev: "" # select a tag / sha to point at
  hooks:
    - id: curlylint
```

Make sure to fill in the `rev` with a valid revision.

_Note_: by default this configuration will match `.html`, `.jinja`, and `.twig` files.
If you want to override this, you will need to use the `files` setting. For example:

```yaml
- id: curlylint
  files: \.(html|sls)$
```
