import json

import click


class RuleParamType(click.ParamType):
    name = "rule"

    def convert(self, value, param, ctx):
        try:
            rule_parts = value.split(":")
            code = rule_parts[0]
            options = json.loads(":".join(rule_parts[1:]))

            return {code: options}
        except TypeError:
            self.fail(
                "expected string rule, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        except ValueError:
            self.fail(
                f"{value!r} is not a valid rule configuration", param, ctx
            )


RULE = RuleParamType()
