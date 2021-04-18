import json

import click


class TemplateTagsParamType(click.ParamType):
    """
    Validates and converts CLI-provided template tags configuration.
    Expects: --template-tags '[["cache", "endcache"]]'
    """

    name = "template tags"

    def convert(self, value, param, ctx):
        try:
            if isinstance(value, str):
                template_tags = json.loads(value)
            else:
                template_tags = value
            # Validate the expected list of lists.
            if not isinstance(template_tags, (list, tuple)):
                raise ValueError
            for tags in template_tags:
                if not isinstance(tags, (list, tuple)):
                    raise ValueError
            return template_tags
        except ValueError:
            self.fail(
                f"expected a list of lists of tags as JSON, got {value!r}",
                param,
                ctx,
            )


TEMPLATE_TAGS = TemplateTagsParamType()
