# jinjalint

A prototype linter which checks the indentation and the correctness of
[Jinja][jinja]-like/HTML templates. It works with
[Django’s templates][djangotemplates] too, it should work with
[Twig](https://twig.symfony.com/) and similar template languages.

This linter parses both HTML and Jinja tags and will report mismatched
tags and indentation errors:

```
<div>
    {% if something %}
    </div>
{% endif %}
```

```
<div>
    <span>
    </div>
</span>
```

```
  {% if something %}
 <div> not indented properly
      </div>
   {% endif %}
```

```
{% if something %}<a href="somewhere">{% endif %}
    <p>something</p>
{% if not something %}</a>{% endif %}
```

This is a work in progress. Feel free to contribute :upside_down_face:

[jinja]: http://jinja.pocoo.org/docs/2.9/
[djangotemplates]: https://docs.djangoproject.com/en/1.11/ref/templates/language/
