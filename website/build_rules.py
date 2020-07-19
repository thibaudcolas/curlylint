# -*- coding: utf-8 -*-

import codecs
import datetime
import json

import toml

from curlylint.rules.aria_role import aria_role
from curlylint.rules.html_has_lang import html_has_lang
from curlylint.rules.indent import indent

rules = [
    html_has_lang.RULE,
    aria_role.RULE,
    indent.RULE,
]

if __name__ == "__main__":
    for rule in rules:
        description = rule["docs"]["description"]  # type: ignore
        impact = rule["docs"]["impact"]  # type: ignore

        config_toml = []
        config_cli = []
        one_off_schema = rule["schema"].get("oneOf", [])  # type: ignore
        for item in one_off_schema:
            title = f"# {item['title']}"
            example = item["examples"][0]

            config_toml.append(title)
            config_cli.append(title)
            config_toml.append(
                toml.dumps({rule["id"]: example}).replace("\n", "")  # type: ignore
            )
            config_cli.append(
                f"curlylint --rule '{rule['id']}: {json.dumps(example)}' template.html"
            )

        config_toml_str = "\\n".join(config_toml).replace("`", "\\`")
        config_cli_str = "\\n".join(config_cli).replace("`", "\\`")

        config_section = ""
        if config_toml_str:
            config_section = f"""This rule supports the following configuration:

<Tabs
  groupId="config-language"
  defaultValue="toml"
  values={{[
    {{ label: "TOML", value: "toml" }},
    {{ label: "Command line", value: "shell" }},
  ]}}
>
  <TabItem value="toml">
    <CodeSnippet
      snippet={{`{config_toml_str}`}}
      annotations={{[]}}
      lang="toml"
    />
  </TabItem>
  <TabItem value="shell">
    <CodeSnippet
      snippet={{`{config_cli_str}`}}
      annotations={{[]}}
      lang="shell"
    />
  </TabItem>
</Tabs>"""

        resources_section = ""

        if rule["docs"]["resources"]:  # type: ignore
            resources = "\n".join([f"- {r}" for r in rule["docs"]["resources"]])  # type: ignore

            resources_section = f"""## Resources\n\n{resources}"""

        with codecs.open(f"docs/rules/{rule['id']}.mdx", "w", "utf-8") as file:
            file.write(
                f"""---
# This file is auto-generated, please do not update manually.
# Timestamp: {datetime.datetime.now()}
id: {rule['id']}
title: {rule['id']}
custom_edit_url: https://github.com/thibaudcolas/curlylint/edit/main/curlylint/rules/{rule['id']}/{rule['id']}.py
---

import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";
import CodeSnippet from "@theme/CodeSnippet";

> {description}
>
> User impact: **{impact}**

{config_section}

{resources_section}"""
            )

    rules_list = "\n".join(
        [f"- [{rule['id']}]({rule['id']}.mdx)" for rule in rules]
    )
    rules_id = ",\n  ".join([f"\"rules/{rule['id']}\"" for rule in rules])

    with codecs.open(f"rules-sidebar.js", "w", "utf-8") as file:
        file.write(
            f"""module.exports = [
    {rules_id}
];
        """
        )

    with codecs.open(f"docs/rules/all.md", "w", "utf-8") as file:
        file.write(
            f"""---
# This file is auto-generated, please do not update manually.
# Timestamp: {datetime.datetime.now()}
id: all
title: All rules
custom_edit_url: https://github.com/thibaudcolas/curlylint/edit/main/website/build_rules.py
---

{rules_list}
"""
        )
