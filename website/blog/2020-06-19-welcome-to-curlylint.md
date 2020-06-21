---
id: welcome-to-curlylint
title: Welcome to curlylint.org!
author: Thibaud Colas
author_url: https://github.com/thibaudcolas
author_image_url: https://avatars1.githubusercontent.com/u/877585?s=460&v=4
tags: [project, roadmap]
---

Curlylint now has a website! 🎉

<!-- truncate -->

While the linter itself is still very experimental, and subject to major changes, I believe that having great documentation is a much more important step than any single feature or linting rule of the linter. Particularly:

- Documenting the rules, with their respective configuration options, with lots of examples.
- Documenting CLI options, and (hopefully) future editor integrations.

With a standalone site (as opposed to Markdown files in GitHub), I can create clean URLs for each of the rules, that can then be used directly in the CLI’s output. This is all inspired by [ESLint](https://eslint.org/), which is years ahead of any other static analysis tool I’ve ever used.

![Screen capture of ESLint in VS Code, with link to a rule’s documentation, and options to automatically disable the rule](/img/blog/2020-06-19-welcome-to-curlylint/eslint-awesome.gif)

> ESLint’s VS Code integration, with link straight to the rule’s documentation, and options to auto-disable the violation.

## The website

The website itself is built with [Docusaurus v2](https://v2.docusaurus.io/). I don’t think this matters too much – the main features I was after were:

- A focus on documentation websites – with versioning, code highlighting.
- Being able to write docs in Markdown without having to worry about creating a theme, or manually writing HTML / CSS.
- Having a blog section and blogging features directly on the same docs website.

The fact that it’s built with React is a plus that will come in handy should I want to build more bespoke pages. MDX is a plus too.

## Up next

Once the website is up and running, there are two things I’d really like to make:

- An editor integration with VS Code. I’ve had some exposure to this with [vscode-stylelint](https://github.com/stylelint/vscode-stylelint), but still don’t have the clearest understanding of how best to do this for a Python CLI.
- An online playground similar to that of [Prettier](https://prettier.io/). I think it’s the best demonstrator of a tool’s capabilities, and it simplifies bug reports / quick tests greatly.

Onwards!
