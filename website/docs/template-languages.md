---
slug: template-languages
title: Template Languages
---

Curlylint attempts to support all “curly braces” template languages, which tend to have very similar syntax:

```twig
<!-- Double curly braces for variables interpolation -->
{{ pretty_cool_variable }}
<!-- Curly braces with percent signs for special blocks or tags -->
{% my_special_tag %}
<!-- Pipes for filters -->
{{ pretty_cool_list|length }}
```

## [Jinja](https://jinja.palletsprojects.com/)

Curlylint works well as a Jinja linter – its parser has originally been built for Jinja, and the AST uses Jinja nomenclature. Jinja support issues are high-priority bugs.

## [Nunjucks](https://mozilla.github.io/nunjucks/)

Nunjucks is identical to Jinja for all intents and purposes regarding linting, but any Nunjucks-specific issues are worth raising.

## [Django templates](https://docs.djangoproject.com/en/dev/topics/templates/)

Nearly identical to Jinja but with less features – can be used as a linter for Django Templates, and support issues are high-priority bugs.

## [Twig](https://twig.symfony.com/)

Can be used as a Twig linter, since the syntax is very similar. All HTML checks should work as expected. Template syntax checks may be problematic. Curlylint isn’t as well tested on Twig, but bug reports are definitely appreciated and we would love to have good support for Twig.

## [Liquid](https://shopify.github.io/liquid/)

Can be used as a Liquid linter, since the syntax is very similar. All HTML checks should work as expected. Template syntax checks may be problematic. Curlylint isn’t as well tested on Liquid, but bug reports are definitely appreciated and we would love to have good support for Twig.

## HTML

It’s of course also possible to use curlylint as an HTML linter! Most of the linter’s rules only apply to HTML. Any issues parsing specific HTML5, SVG 1.1 / 2.0, or MathML, are treated as high-priority bugs.
