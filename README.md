# jinjalint

A prototype linter which checks the indentation and the correctness of
[Jinja][jinja]-like/HTML templates. Can [fix issues][django-commit].

It works with [Django’s templates][djangotemplates] too, it should
work with [Twig](https://twig.symfony.com/) and similar template languages.
It should work fine with any kind of HTML 4 and 5, however XHTML is not
supported.

This linter parses both HTML and Jinja tags and will report mismatched
tags and indentation errors:

```html+jinja
<div>
    {% if something %}
    </div>
{% endif %}
```

```html+jinja
<div>
    <span>
    </div>
</span>
```

```html+jinja
  {% if something %}
 <div> not indented properly
      </div>
   {% endif %}
```

```html+jinja
{% if something %}<a href="somewhere">{% endif %}
    <p>something</p>
{% if not something %}</a>{% endif %}
```

## Usage

You need Python 3. Jinjalint doesn’t work with Python 2. Install it with
`pip install jinjalint` (or `pip3 install jinjalint` depending on how `pip` is
called on your system), then run it with:

```sh
$ jinjalint template-directory/
```

…or:

```sh
$ jinjalint some-file.html some-other-file.html
```

This is a work in progress. Feel free to contribute :upside_down_face:

### Configuration

Jinjalint supports defining a config file with the flag `--config`. Here is an [example config](./example_config.py) file with the available options:

```python
# Specify additional Jinja elements which can wrap HTML here. You
# don't neet to specify simple elements which can't wrap anything like
# {% extends %} or {% include %}.
# Default: [].
jinja_custom_elements_names = [
    ('cache', 'endcache'),
    ('captureas', 'endcaptureas'),
    # ('for', 'else', 'empty', 'endfor'),
]

# How many spaces to use when checking indentation.
# Default: 4
indent_size = 4
```

This config file can then be used with:

```sh
$ jinjalint --config example_config.py template-directory/
```

## Usage with [pre-commit](https://pre-commit.com) git hooks framework

Add to your `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/motet-a/jinjalint
    rev: ''  # select a tag / sha to point at
    hooks:
    -   id: jinjalint
```

Make sure to fill in the `rev` with a valid revision.

_Note_: by default this configuration will only match `.jinja` and `.jinja2`
files.  To match by regex pattern instead, override `types` and `files` as
follows:

```yaml
    -   id: jinjalint
        types: [file]  # restore the default `types` matching
        files: \.(html|sls)$
```

## Hacking

Jinjalint is powered by [Parsy][parsy]. Parsy is an extremely powerful
library and Jinjalint’s parser relies heavily on it. You have to read
Parsy’s documentation in order to understand what’s going on in
`parse.py`.

[jinja]: http://jinja.pocoo.org/docs/2.9/
[django-commit]: https://github.com/django/djangoproject.com/commit/14a964d626196c857809d9b3b492ff4cfa4b3f40
[djangotemplates]: https://docs.djangoproject.com/en/1.11/ref/templates/language/
[parsy]: https://github.com/python-parsy/parsy
