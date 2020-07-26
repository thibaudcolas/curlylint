# Test templates

| Templates                              | Source                                                                                          | Last updated                                                                                                        | Credit                                                         |
| -------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [`jinja2-nunjucks`](./jinja2-nunjucks) | [springload/rikki-patterns](https://github.com/springload/rikki-patterns)                       | [20170926](https://github.com/springload/rikki-patterns/commit/9906f69f9a29f587911ff66cf997fcf2f4f90452)            | (c) 2016 Springload, MIT license.                              |
| [`nunjucks`](./nunjucks)               | [justrhysism/prettier-plugin-nunjucks](https://github.com/justrhysism/prettier-plugin-nunjucks) | [20191231](https://github.com/justrhysism/prettier-plugin-nunjucks/commit/fda95b13a74624e07442baebfea6bf8d16b6293e) | (c) 2019-current Rhys Lloyd, MIT license.                      |
| [`twig`](./twig)                       | [trivago/prettier-plugin-twig-melody](https://github.com/trivago/prettier-plugin-twig-melody)   | [20200323](https://github.com/trivago/prettier-plugin-twig-melody/commit/bbd983a05896e3dead9c99bc3cc7314a927d5b7e)  | (c) 2019-current Trivago, Apache License 2.0.                  |
| [`liquid`](./liquid)                   | [Shopify/liquid](https://github.com/Shopify/liquid)                                             | [20200121](https://github.com/Shopify/liquid/commit/e9b649b3455c63859f1b865a8684607d6ff5b050)                       | (c) 2005, 2006 Tobias Luetke, MIT.                             |
| [`jinja2`](./jinja2)                   | [cfpb/cfgov-refresh](https://github.com/cfpb/cfgov-refresh)                                     | [20200327](https://github.com/cfpb/cfgov-refresh/commit/92e96ff5e1f11d071b447c7cd4910f329dc3695c)                   | Thanks to CFPB – Public domain, CC0 1.0                        |
| [`django`](./django)                   | [wagtail/wagtail](https://github.com/wagtail/wagtail)                                           | [20200325](https://github.com/wagtail/wagtail/commit/8c1a234f139cdd77dd20cce9ee087ec309709851)                      | (c) 2014-present Torchbox Ltd and individual contributors, BSD |

## Updating the templates

Clone the source repository, then:

```bash
find . ! -name '*.html' -type f -delete
find . -type d -empty -delete
tree .
```
