# -*- coding: utf-8 -*-

import codecs
import datetime

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
        with codecs.open(f"docs/rules/{rule['id']}.md", "w", "utf-8") as file:
            file.write(
                f"""---
# This file is auto-generated, please do not update manually.
# Timestamp: {datetime.datetime.now()}
id: {rule['id']}
title: {rule['id']}
custom_edit_url: https://github.com/thibaudcolas/curlylint/edit/master/curlylint/rules/{rule['id']}/{rule['id']}.py
---

> {rule['docs']['description']}
"""
            )

    rules_list = "\n".join(
        [f"- [{rule['id']}]({rule['id']}.md)" for rule in rules]
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
custom_edit_url: https://github.com/thibaudcolas/curlylint/edit/master/website/build_rules.py
---

{rules_list}
"""
        )
