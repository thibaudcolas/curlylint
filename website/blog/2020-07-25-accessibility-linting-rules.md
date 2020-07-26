---
id: accessibility-linting-rules
title: Accessibility linting rules
author: Thibaud Colas
author_url: https://github.com/thibaudcolas
author_image_url: https://avatars1.githubusercontent.com/u/877585?s=460&v=4
tags: [accessibility, rules]
---

Curlylint now comes with 7 accessibility-related rules, ready to use in HTML templates. See [All rules](/docs/rules/all) for details about the individual rules.

<!-- truncate -->

This is an important milestone for the linter – essentially demonstrating its usefulness once and for all, if that was still needed.

## HTML best practices

Most of the rules Curlylint currently ships with are very simple "HTML linting" rules for accessibility, based on established best practice:

- [`aria_role`](/docs/rules/aria_role) just checks that `role` attributes are valid.
- Same for [`html_has_lang`](/docs/rules/html_has_lang), for the `html` `lang` attribute.
- Same for [`image_alt`](/docs/rules/image_alt), [`meta_viewport`](/docs/rules/meta_viewport), [`no_autofocus`](/docs/rules/no_autofocus), [`tabindex_no_positive`](/docs/rules/tabindex_no_positive)!

See a pattern? All of these are variations on the same theme of “HTML attributes should only contain a limited range of values based on established best practices”. This is great news for this project – it means there can be quite a lot of results achieved with minimal complexity when it comes to creating individual rules.

In the future, this could easily be taken further to cover:

- Security best practices, for example `rel="noopener"`, or disallowing `javascript:` URLs in `href`.
- HTML maintainability best practices, for example disallowing duplicate class attributes.
- And of course, more accessibility and ARIA best practices.

Obligatory mention of [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y), which has been a huge source of inspiration. Generally, modern React tooling has this figured out, with extensive static analysis available. For me, this isn’t just a nice-to-have – it’s hard to always keel all of those best practices in mind, and linting is there to automate this for you. Note this isn’t just React – Vue has its [eslint-plugin-vue-a11y](https://github.com/maranran/eslint-plugin-vue-a11y) too!

## Templates best practices

This doesn’t have to stop at HTML. Curlylint already supports parsing template syntax, attempting to be usable as a linter for Jinja, Twig, Liquid, [and the likes](/docs/template-languages). We can also have rules to enforce best practices for this template syntax.

The first example of such a rule is [`django_forms_rendering`](/docs/rules/django_forms_rendering), which restricts how forms can be rendered in Django projects, for accessibility reasons. I’m very excited about opportunities like this to codify and share best practices in a way that scales well.

- Hopefully there will be more [linting rules for Django](https://github.com/django/deps/pull/69) coming in the future.
- And more linting rules [for Wagtail](https://github.com/wagtail/wagtail/issues/6090) as well.
