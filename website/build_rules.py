# -*- coding: utf-8 -*-
# type: ignore

import codecs
import datetime
import json
import os

import toml

from curlylint.rules.aria_role import aria_role
from curlylint.rules.django_forms_rendering import django_forms_rendering
from curlylint.rules.html_has_lang import html_has_lang
from curlylint.rules.image_alt import image_alt
from curlylint.rules.indent import indent
from curlylint.rules.meta_viewport import meta_viewport
from curlylint.rules.no_autofocus import no_autofocus
from curlylint.rules.tabindex_no_positive import tabindex_no_positive

rules = [
    aria_role.RULE,
    django_forms_rendering.RULE,
    html_has_lang.RULE,
    image_alt.RULE,
    indent.RULE,
    meta_viewport.RULE,
    no_autofocus.RULE,
    tabindex_no_positive.RULE,
]

if __name__ == "__main__":
    for rule in rules:
        test_cases_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "curlylint",
            "rules",
            rule["id"],
            f"{rule['id']}_test.json",
        )
        test_cases = json.loads(open(test_cases_path, "r").read())

        description = rule["docs"]["description"]
        impact = rule["docs"]["impact"]

        config_toml = []
        config_cli = []
        one_off_schema = rule["schema"].get("oneOf", [])

        for item in one_off_schema:
            title = f"# {item['title']}"
            example = item["examples"][0]

            config_toml.append(title)
            config_cli.append(title)
            config_toml.append(
                toml.dumps({rule["id"]: example}).replace("\n", "")
            )
            config_cli.append(
                f"curlylint --rule '{rule['id']}: {json.dumps(example)}' ."
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
    {{ label: "Shell", value: "shell" }},
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

        success_section = ""
        fail_section = ""

        if test_cases:
            success_cases = filter(
                lambda c: c.get("example") and len(c["output"]) == 0, test_cases
            )
            success_toml = []
            success_cli = []
            for c in success_cases:
                toml_config = toml.dumps({rule["id"]: c["config"]}).replace(
                    "\n", ""
                )
                success_toml.append(f"<!-- Good: {c['label']} -->")
                success_toml.append(f"<!-- {toml_config} -->")
                success_toml.append(c["template"])
                success_cli.append(f"<!-- Good: {c['label']} -->")
                success_cli.append(
                    f"<!-- curlylint --rule '{rule['id']}: {json.dumps(c['config'])}' . -->"
                )
                success_cli.append(c["template"])

            success_toml_str = "\\n".join(success_toml).replace("`", "\\`")
            success_cli_str = "\\n".join(success_cli).replace("`", "\\`")

            if success_cases:
                success_section = f"""## Success

<Tabs
  groupId="config-language"
  defaultValue="toml"
  values={{[
    {{ label: "TOML", value: "toml" }},
    {{ label: "Shell", value: "shell" }},
  ]}}
>
  <TabItem value="toml">
    <CodeSnippet
      snippet={{`{success_toml_str}`}}
      annotations={{[]}}
      lang="html"
    />
  </TabItem>
  <TabItem value="shell">
    <CodeSnippet
      snippet={{`{success_cli_str}`}}
      annotations={{[]}}
      lang="html"
    />
  </TabItem>
</Tabs>
"""
            fail_cases = filter(
                lambda c: c.get("example") and len(c["output"]) > 0, test_cases
            )
            fail_annotations = []
            fail_toml = []
            fail_cli = []
            for c in fail_cases:
                toml_config = toml.dumps({rule["id"]: c["config"]}).replace(
                    "\n", ""
                )
                fail_toml.append(f"<!-- Bad: {c['label']} -->")
                fail_toml.append(f"<!-- {toml_config} -->")
                fail_toml.append(c["template"])
                fail_cli.append(f"<!-- Bad: {c['label']} -->")
                fail_cli.append(
                    f"<!-- curlylint --rule '{rule['id']}: {json.dumps(c['config'])}' . -->"
                )
                fail_cli.append(c["template"])

                fail_annotations = fail_annotations + [
                    {
                        "file": o["file"],
                        "column": o["column"],
                        "line": o["line"] + 2 + (len(fail_annotations)) * 3,
                        "code": o["code"],
                        "message": o["message"],
                    }
                    for o in c["output"]
                ]

            fail_toml_str = "\\n".join(fail_toml).replace("`", "\\`")
            fail_cli_str = "\\n".join(fail_cli).replace("`", "\\`")

            if fail_cases:
                fail_section = f"""## Fail

<Tabs
  groupId="config-language"
  defaultValue="toml"
  values={{[
    {{ label: "TOML", value: "toml" }},
    {{ label: "Shell", value: "shell" }},
  ]}}
>
  <TabItem value="toml">
    <CodeSnippet
      snippet={{`{fail_toml_str}\\n\\n`}}
      annotations={{{json.dumps(fail_annotations)}}}
      lang="html"
    />
  </TabItem>
  <TabItem value="shell">
    <CodeSnippet
      snippet={{`{fail_cli_str}\\n\\n`}}
      annotations={{{json.dumps(fail_annotations)}}}
      lang="html"
    />
  </TabItem>
</Tabs>
"""

        resources_section = ""

        if rule["docs"]["resources"]:
            resources = "\n".join([f"- {r}" for r in rule["docs"]["resources"]])

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

{success_section}

{fail_section}

{resources_section}"""
            )

    rules_list = "\n".join(
        [
            f"- [{rule['id']}]({rule['id']}): {rule['docs']['description']}"
            for rule in rules
        ]
    )
    rules_id = ",\n  ".join([f"\"rules/{rule['id']}\"" for rule in rules])

    with codecs.open(f"rules-sidebar.js", "w", "utf-8") as file:
        file.write(
            f"""module.exports = [
    {rules_id}
];
        """
        )

    all_config_toml = []
    all_config_cli = []

    for rule in rules:
        one_off_schema = rule["schema"].get("oneOf", [])
        first_config = one_off_schema[0]
        title = f"# {first_config['title']}"
        example = first_config["examples"][0]

        all_config_toml.append(title)
        all_config_toml.append(f"# See {rule['docs']['url']}.")
        all_config_toml.append(
            toml.dumps({rule["id"]: example}).replace("\n", "")
        )
        all_config_cli.append(f"--rule '{rule['id']}: {json.dumps(example)}'")

    all_config_toml_str = "\\n".join(all_config_toml).replace("`", "\\`")
    all_config_cli_str = " ".join(all_config_cli)

    with codecs.open(f"docs/rules/all.mdx", "w", "utf-8") as file:
        file.write(
            f"""---
# This file is auto-generated, please do not update manually.
# Timestamp: {datetime.datetime.now()}
id: all
title: All rules
custom_edit_url: https://github.com/thibaudcolas/curlylint/edit/main/website/build_rules.py
---

import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";
import CodeSnippet from "@theme/CodeSnippet";

{rules_list}

## Try them all

Here is a sample configuration with all of Curlylint’s rules enabled. Note **this isn’t a recommended configuration**, just a convenient way to try it all at once:

<Tabs
  groupId="config-language"
  defaultValue="toml"
  values={{[
    {{ label: "TOML", value: "toml" }},
    {{ label: "Shell", value: "shell" }},
  ]}}
>
  <TabItem value="toml">
    <CodeSnippet
      snippet={{`[tool.curlylint.rules]\\n{all_config_toml_str}`}}
      annotations={{[]}}
      lang="toml"
    />
  </TabItem>
  <TabItem value="shell">
    <CodeSnippet
      snippet={{`curlylint {all_config_cli_str} .`}}
      annotations={{[]}}
      lang="shell"
    />
  </TabItem>
</Tabs>
"""
        )
