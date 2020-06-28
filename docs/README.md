# Documentation

## Inspiration

Here are tools that this linter could learn from. Suggestions welcome.

### Linting rules

- [x] https://github.com/yannickcr/eslint-plugin-react, last reviewed 2020-04-16
- [x] https://github.com/vuejs/eslint-plugin-vue, last reviewed 2020-04-16
- [x] https://github.com/htmlhint/HTMLHint, last reviewed 2020-04-16

#### Accessibility checks

- [x] https://github.com/evcohen/eslint-plugin-jsx-a11y, last reviewed 2020-04-16
- [ ] https://github.com/squizlabs/HTML_CodeSniffer
- [ ] https://github.com/dequelabs/axe-core
- [ ] https://github.com/GoogleChrome/accessibility-developer-tools

#### HTML validation

- [ ] Nu "vnu.jar" HTML5 validator https://github.com/validator/validator
- [ ] https://github.com/html5lib/html5lib-python
- [ ] https://github.com/html5lib/html5lib-tests

## Developer tools

- [x] https://github.com/prettier/prettier, last reviewed 2020-05-06
- [x] https://github.com/eslint/eslint, last reviewed 2020-05-06
- [ ] https://github.com/stylelint/stylelint

## Research

- [ ] https://www.w3.org/WAI/RD/2011/metrics/paper3/
- [ ] https://dl.acm.org/doi/10.1145/2461121.2461124

### Python developer tools

Most of curlylint’s CLI is already based on that of black: include/excludes, config file, error, success, verbose output. It would be nice to learn from flake8’s plugin system, eventually.

- [ ] https://pypi.org/project/flake8/
- [ ] https://github.com/tommilligan/flake8-fixme
- [ ] https://github.com/PyCQA/flake8-bugbear
- [x] https://github.com/psf/black, last reviewed 2020-05-06

## CLI ideas

- Support configuration from `setup.cfg`.
- Support configuration from `.editorconfig`.
- Support using a file with ignore paths.
- Disable colored output.
- Cache results / only check changed files.

## Linting ideas

- Support disabling rules via code comments.

## Rules ideas

### Wishlist

#### Code smells

- `<input type="submit">` is banned. Use `<button type="submit">` instead.
- `<input type="button">` is banned. Use `<button type="button">` instead.
- `<button>` elements must have a `type` attribute.
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/button-has-type.md
- Duplicate attributes on the same element are disallowed.
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-duplicate-props.md
  - https://eslint.vuejs.org/rules/no-duplicate-attributes.html
  - https://github.com/htmlhint/HTMLHint/wiki/attr-no-duplication
- `id` must be unique.
  - https://github.com/htmlhint/HTMLHint/wiki/id-unique
- Forbid specified attributes on specified elements.
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-component-props.md
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-dom-props.md
  - https://eslint.vuejs.org/rules/no-static-inline-styles.html
- Forbid speicified elements.
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-elements.md
- Disallow common typos (e.g. `tab-index` instead of `tabindex`).
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-typos.md
- Disallow unescaped HTML entities
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-unescaped-entities.md
  - https://github.com/htmlhint/HTMLHint/wiki/spec-char-escape

#### HTML5

- `type="text/javascript"` is banned on `<script>` elements.
- Deprecated attributes on an element are disallowed.
- Deprecated elements are disallowed.
- Elements can only have the attributes that are valid for them.
- Void elements have a consistent self-closing tag style.
  - https://github.com/htmlhint/HTMLHint/wiki/empty-tag-not-self-closed

#### Accessibility

- `<img>` tags must have an `alt` attribute.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/alt-text.md
  - https://github.com/htmlhint/HTMLHint/wiki/alt-require
- `<a>` tags must have textual content.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/anchor-has-content.md
- `<a>` tags cannot have content such as "Read more".
- `<a>` tags are only used for links.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/anchor-is-valid.md
- Alt text doesn’t start or end with "picture", "image", or "icon". Doesn’t end with a file extension.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/img-redundant-alt.md
- `<table>` elements must have a `<caption>`.
- Multiple heading elements cannot have the same content.
- Heading elements must have content.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/heading-has-content.md
- `autocomplete` attribute must use valid values.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/autocomplete-valid.md
- `<html>` element has a `lang` attribute.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/html-has-lang.md
- Enforce lang attribute has a valid value.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/lang.md
- Enforce iframe elements have a title attribute.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/iframe-has-title.md
- Enforce `autofocus` attribute is not used.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-autofocus.md
- `tabindex` should only be declared on interactive elements.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-noninteractive-tabindex.md
- Enforce `tabindex` value is not greater than zero.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/tabindex-no-positive.md

##### ARIA

- All ARIA roles must be valid.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-role.md
- All ARIA attributes must be valid.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-props.md
- Forbidden ARIA roles: menu, menubar, menuitem.
- Non-interactive elements should not be assigned interactive roles.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-noninteractive-element-to-interactive-role.md
- Enforce explicit `role` is not the same as implicit/default role property on element.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-redundant-roles.md
- Enforce that elements with ARIA roles must have all required attributes for that role.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/role-has-required-aria-props.md
- Enforce that elements with explicit or implicit roles defined contain only aria-\* properties supported by that role.
  - https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/role-supports-aria-props.md

#### Security

- Enforce usage of `rel="noopener noreferrer"` for `target="\_blank"` `<a>` tags
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-target-blank.md
- Enforce methods always having an explicit `method` to avoid unintentional data leaks in logs.
- Forbid the use of `javascript:` URLs
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-script-url.md
  - https://github.com/htmlhint/HTMLHint/wiki/inline-script-disabled
- Forbid the use of inline script tags without CSP-compatible fingerprints.
- Forbid the use of inline styles without CSP-compatible fingerprints.
- Forbid loading scripts / styles from third-party resources, even with integrity attributes.
- Forbid the use of `http:` URLs
- Forbid the use of protocol-relative URLs `//`

#### Template languages

- Forbid specified template language syntax.

##### Django

- `{% if foo %}{{ foo }}{% else %}bar{% endif %}` => `{{ foo|default:"bar" }}`
- `{% with foo as bar %}` ... [ not using `{{ bar }}` ] ... `{% endwith %}`
- `{% endblock %}` vs. `{% endblock blockname %}`
- Forbid marking variables as "safe"

#### Code style

- Enforce ordering of HTML attributes
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-sort-props.md
  - https://eslint.vuejs.org/rules/attributes-order.html
- Enforce compliance with `.editorconfig`

### Rejected ideas

#### Formatting

See <https://github.com/prettier/prettier/issues/5944#issuecomment-549805364>. I’m much more interested in having automated formatting with a Prettier plugin, than adding formatting rules to a linter.
