# Documentation

## Inspiration

Here are tools that this linter could learn from. Suggestions welcome.

### Linting rules

- https://github.com/yannickcr/eslint-plugin-react
- https://github.com/vuejs/eslint-plugin-vue
- https://github.com/htmlhint/HTMLHint
- https://github.com/DavidAnson/markdownlint
- https://github.com/textlint/textlint

#### Accessibility checks

- https://github.com/evcohen/eslint-plugin-jsx-a11y
- https://github.com/squizlabs/HTML_CodeSniffer
- https://github.com/dequelabs/axe-core

#### HTML validation

- Nu "vnu.jar" HTML5 validator https://github.com/validator/validator
- https://github.com/html5lib/html5lib-python
- https://github.com/html5lib/html5lib-tests

## Developer tools

- https://github.com/prettier/prettier
- https://github.com/eslint/eslint

### Python developer tools

Most of curlylint’s CLI is already based on that of black: include/excludes, config file, error, success, verbose output. It would be nice to learn from flake8’s plugin system, eventually.

- https://pypi.org/project/flake8/
- https://github.com/tommilligan/flake8-fixme
- https://github.com/PyCQA/flake8-bugbear
- https://github.com/psf/black

## Linting rules ideas

### Wishlist

#### Code smells

- `<input type="submit">` is banned. Use `<button type="submit">` instead.
- `<input type="button">` is banned. Use `<button type="button">` instead.
- `<button>` elements must have a `type` attribute.
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/button-has-type.md
- Duplicate attributes on the same element are disallowed.
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-duplicate-props.md
- Forbid specified attributes on specified elements.
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-component-props.md
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-dom-props.md
- Forbid speicified elements.
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-elements.md
- Disallow common typos (e.g. `tab-index` instead of `tabindex`).
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-typos.md
- Disallow unescaped HTML entities
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-unescaped-entities.md

#### HTML5

- `type="text/javascript"` is banned on `<script>` elements.
- Deprecated attributes on an element are disallowed.
- Deprecated elements are disallowed.
- Elements can only have the attributes that are valid for them.
- Void elements have a consistent self-closing tag style.

#### Accessibility

- `<img>` tags must have an `alt` attribute.
- Alt text doesn’t start or end with "image" or "icon". Doesn’t end with a file extension.
- All ARIA roles must be valid.
- Forbidden ARIA roles: menu, menubar, menuitem.
- `<table>` elements must have a `<caption>`.
- Multiple heading elements cannot have the same content.

#### Security

- Enforce usage of `rel="noopener noreferrer"` for `target="\_blank"` `<a>` tags
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-target-blank.md
- Enforce methods always having an explicit `method` to avoid unintentional data leaks in logs.
- Forbid the use of `javascript:` URLs
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-script-url.md
- Forbid the use of `http:` URLs
- Forbid the use of protocol-relative URLs `//`

#### Template languages

- Forbid specified template language syntax.

##### Django

- `{% if foo %}{{ foo }}{% else %}bar{% endif %}` => `{{ foo|default:"bar" }}`
- `{% with foo as bar %}` ... [ not using `{{ bar }}` ] ... `{% endwith %}`
- `{% endblock %}` vs. `{% endblock blockname %}`

#### Code style

- Enforce ordering of HTML attributes
  - https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-sort-props.md

### Rejected ideas

#### Formatting

See <https://github.com/prettier/prettier/issues/5944#issuecomment-549805364>. I’m much more interested in having automated formatting with a Prettier plugin, than adding formatting rules to a linter.
