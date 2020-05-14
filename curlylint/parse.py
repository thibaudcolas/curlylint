import re

# TODO: Move it elsewhere
import sys

import parsy as P

from .ast import (
    Attribute,
    ClosingTag,
    Comment,
    Element,
    Integer,
    Interpolated,
    Jinja,
    JinjaComment,
    JinjaElement,
    JinjaElementPart,
    JinjaOptionalContainer,
    JinjaTag,
    JinjaVariable,
    Location,
    OpeningTag,
    String,
)
from .util import flatten

sys.setrecursionlimit(10000)

# https://html.spec.whatwg.org/multipage/syntax.html#elements-2
# https://github.com/html5lib/html5lib-python/blob/0cae52b2073e3f2220db93a7650901f2200f2a13/html5lib/constants.py#L560
VOID_ELEMENTS = (
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
)

# https://www.w3.org/TR/SVG2/eltindex.html
# https://developer.mozilla.org/en-US/docs/Web/SVG/Element
# Technically it’s valid for any SVG element to be written as a self-closing tag,
# for the parser this is equivalent to the element not having any content.
# In practice there are a lot of elements which wouldn’t be of much use if they didn’t
# have any content. This list omits those elements.
# This list also omits elements that have (next to) no browser implementation.
# Elements are only commented out so it’s easy to understand what isn’t there, and why.
SVG_SELF_CLOSING_ELEMENTS = (
    # "a",
    "animate",
    "animateMotion",
    "animateTransform",
    # "audio",
    # "canvas",
    "circle",
    # "clipPath",
    # "defs",
    # "desc",
    # "discard",
    "ellipse",
    "feBlend",
    "feColorMatrix",
    # "feComponentTransfer",
    "feComposite",
    "feConvolveMatrix",
    # "feDiffuseLighting",
    "feDisplacementMap",
    "feDistantLight",
    "feDropShadow",
    "feFlood",
    "feFuncA",
    "feFuncB",
    "feFuncG",
    "feFuncR",
    "feGaussianBlur",
    "feImage",
    # "feMerge",
    "feMergeNode",
    "feMorphology",
    "feOffset",
    "fePointLight",
    # "feSpecularLighting",
    "feSpotLight",
    "feTile",
    "feTurbulence",
    # "filter",
    # "foreignObject",
    # "g",
    # "hatchpath",
    # "iframe",
    "image",
    "line",
    # "linearGradient",
    # "marker",
    # "mask",
    # "metadata",
    "mpath",
    "path",
    # "pattern",
    "polygon",
    "polyline",
    # "radialGradient",
    "rect",
    # "script",
    "set",
    "stop",
    # "style",
    # "svg",
    # "switch",
    # "symbol",
    # "text",
    # "textPath",
    # "title",
    # "tspan",
    # "unknown",
    "use",
    # "video",
    # "view",
)

DEFAULT_JINJA_STRUCTURED_ELEMENTS_NAMES = [
    ("autoescape", "endautoescape"),
    ("block", "endblock"),
    ("blocktrans", "plural", "endblocktrans"),
    ("comment", "endcomment"),
    ("filter", "endfilter"),
    ("for", "else", "empty", "endfor"),
    ("if", "elif", "else", "endif"),
    ("ifchanged", "else", "endifchanged"),
    ("ifequal", "endifequal"),
    ("ifnotequal", "endifnotequal"),
    ("spaceless", "endspaceless"),
    ("verbatim", "endverbatim"),
    ("with", "endwith"),
]


# `\s` in an `str` pattern does match Unicode fancy spaces (especially the
# non-breaking ones). We’ll warn against some of these fancy spaces in the
# check phase.
# XXX: It could be better and simpler to only allow ASCII whitespaces here.
whitespace = P.regex(r"\s*")
mandatory_whitespace = P.regex(r"\s+")


def until(parser):
    return parser.should_fail(repr(parser)).then(P.any_char).many()


def combine_locations(begin_index, begin, result, end_index, end):
    begin_loc = Location(line=begin[0], column=begin[1], index=begin_index)
    end_loc = Location(line=end[0], column=end[1], index=end_index)
    locations = {"begin": begin_loc, "end": end_loc}

    return (locations, result)


def locate(parser):

    return P.seq(P.index, P.line_info, parser, P.index, P.line_info).combine(
        combine_locations
    )


def _combine_jinja_tag(locations, props):
    return JinjaTag(
        name=props["name"],
        content=props["extra_content"],
        left_plus=props["left_plus"],
        left_minus=props["left_minus"],
        right_minus=props["right_minus"],
        **locations,
    )


def _combine_jinja_variable(locations, props):
    return JinjaVariable(
        content=props["extra_content"],
        left_plus=props["left_plus"],
        left_minus=props["left_minus"],
        right_minus=props["right_minus"],
        **locations,
    )


def _combine_jinja_comment(locations, text):
    return JinjaComment(text=text, **locations)


def _combine_jinja_tag_like(locations, props):
    return (
        locations,
        {
            "left_plus": props[0] is not None,
            "left_minus": props[1] is not None,
            "name": props[2],
            "extra_content": props[3],
            "right_minus": props[4] is not None,
        },
    )


def make_jinja_tag_like_parser(name, ml="{", mr="}"):
    """
    Create parsers for Jinja variables and regular Jinja tags.

    `name` should be a parser to parse the tag name.
    """
    end = whitespace.then(P.string("-").optional()).skip(P.string(mr + "}"))
    return locate(
        P.seq(
            P.string("{" + ml).then(P.string("+").optional()),
            P.string("-").optional().skip(whitespace),
            name.skip(whitespace),
            until(end).concat(),
            end,
        )
    ).combine(_combine_jinja_tag_like)


jinja_variable = make_jinja_tag_like_parser(P.success(None), "{", "}").combine(
    _combine_jinja_variable
)


jinja_comment = locate(
    P.string("{#")
    .skip(whitespace)
    .then(until(whitespace + P.string("#}")).concat())
    .skip(whitespace + P.string("#}"))
).combine(_combine_jinja_comment)


def make_jinja_tag_parser(name_parser):
    return make_jinja_tag_like_parser(name_parser, "%", "%").combine(
        _combine_jinja_tag
    )


def _combine_jinja_element(locations, content):
    parts = list(flatten(content[0]))
    closing_tag = content[1] if len(content) == 2 else None

    e = JinjaElement(parts=parts, closing_tag=closing_tag, **locations)
    return e


def _combine_jinja_element_part(locations, props):
    tag, content = props
    return JinjaElementPart(tag=tag, content=content, **locations)


def make_jinja_element_part_parser(name_parser, content):
    return locate(P.seq(make_jinja_tag_parser(name_parser), content)).combine(
        _combine_jinja_element_part
    )


def make_jinja_element_parser(name_parsers, content):
    """
    `name_parsers` must be a list of tag name parsers. For example,
    `name_parsers` can be defined as follow in order to parse `if` statements:

        name_parsers = [P.string(n) for n in ['if', 'elif', 'else', 'endif']]
    """

    if len(name_parsers) == 1:
        tag = make_jinja_tag_parser(name_parsers[0])
        part = locate(P.seq(tag, P.success(None))).combine(
            _combine_jinja_element_part
        )
        parts = [part]
        end_tag_parser = None
    else:
        part_names = name_parsers[:-1]
        first_part = make_jinja_element_part_parser(
            part_names[0], content=content
        )
        next_parts = [
            make_jinja_element_part_parser(name, content=content).many()
            for name in part_names[1:]
        ]
        parts = [first_part] + next_parts
        end_tag_parser = make_jinja_tag_parser(name_parsers[-1])

    content = [P.seq(*parts)]
    if end_tag_parser:
        content.append(end_tag_parser)

    return locate(P.seq(*content)).combine(_combine_jinja_element)


jinja_name = (
    P.letter
    + (P.letter | P.decimal_digit | P.string("_"))  # type: ignore
    .many()
    .concat()
)


def interpolated(parser):
    def combine_interpolated(locations, result):
        return Interpolated(nodes=result, **locations)

    return locate(parser).combine(combine_interpolated)


tag_name_start_char = P.regex(r"[:a-z]")
tag_name_char = tag_name_start_char | P.regex(r"[0-9-_.]")
tag_name = tag_name_start_char + tag_name_char.many().concat()

dtd = P.regex(r"<![^>]*>")

# TODO This is overly restrictive on what can be inside attributes, it’s unclear why. Fails on e.g. `data-test=">"`.
string_attribute_char = P.char_from("-_./+,?=:;#") | P.regex(r"[0-9a-zA-Z]")


def make_quoted_string_attribute_parser(quote, jinja):
    """
    quote: A single or a double quote
    """

    def combine(locations, value):
        return String(value=value, quote=quote, **locations)

    value_char = P.regex(r"[^<]", flags=re.DOTALL)
    value = interpolated(
        P.string(quote)
        .should_fail("no " + quote)
        .then(jinja | value_char)
        .many()
    )

    return locate(P.string(quote).then(value).skip(P.string(quote))).combine(
        combine
    )


def _combine_string_attribute_value(locations, value):
    return String(value=value, quote=None, **locations)


def _combine_int_attribute_value(locations, value):
    return Integer(value=value, has_percent=False, **locations)


int_attribute_value = locate(P.regex(r"[0-9]+").map(int)).combine(
    _combine_int_attribute_value
)


def _combine_attribute(locations, props):
    name, equal_and_value = props
    value = None if equal_and_value is None else equal_and_value["value"]
    return Attribute(name=name, value=value, **locations)


def make_attribute_value_parser(jinja):
    string_attribute_value = locate(
        interpolated((jinja | string_attribute_char).at_least(1))
    ).combine(_combine_string_attribute_value)

    return (
        make_quoted_string_attribute_parser('"', jinja)
        | make_quoted_string_attribute_parser("'", jinja)
        | int_attribute_value
        | string_attribute_value
    ).desc("attribute value")


attr_name_start_char = P.regex(r"[:a-zA-Z]")
attr_name_char = attr_name_start_char | P.regex(r"[0-9A-Z-_.]")
attr_name = attr_name_start_char + attr_name_char.many().concat()


def make_attribute_parser(jinja):
    attribute_value = make_attribute_value_parser(jinja)
    return (
        locate(
            P.seq(
                interpolated(attr_name),
                whitespace.then(
                    P.seq(
                        P.string("=").skip(whitespace).tag("equal"),
                        interpolated(attribute_value).tag("value"),
                    ).map(dict)
                ).optional(),
            )
        )
        .combine(_combine_attribute)
        .desc("attribute")
    )


def make_attributes_parser(config, jinja):
    attribute = make_attribute_parser(jinja)

    jinja_attr = make_jinja_parser(
        config,
        interpolated(
            whitespace.then((attribute | jinja).sep_by(whitespace)).skip(
                whitespace
            )
        ),
    )

    attrs = interpolated(
        (
            whitespace.then(jinja_attr) | mandatory_whitespace.then(attribute)
        ).many()
    )

    return attrs


def _combine_comment(locations, text):
    return Comment(text=text, **locations)


comment = locate(
    P.string("<!--")
    .then(P.regex(r".*?(?=-->)", flags=re.DOTALL))
    .skip(P.string("-->"))
).combine(_combine_comment)


def _combine_opening_tag(locations, props):
    _lt, tag_name, attributes, slash, _gt = props
    return OpeningTag(
        name=tag_name, attributes=attributes, slash=slash, **locations
    )


def _combine_closing_tag(locations, name):
    return ClosingTag(name=name, **locations)


def make_closing_tag_parser(tag_name_parser):
    return locate(
        P.string("</").then(tag_name_parser).skip(P.string(">"))
    ).combine(_combine_closing_tag)


def _combine_slash(locations, _):
    return locations["begin"]


def make_opening_tag_parser(
    config, jinja, tag_name_parser=None, allow_slash=False, mandate_slash=False
):
    attributes = make_attributes_parser(config, jinja)

    if not tag_name_parser:
        tag_name_parser = tag_name | jinja

    if allow_slash:
        slash = (
            locate(P.string("/").skip(whitespace))
            .combine(_combine_slash)
            .optional()
        )
    elif mandate_slash:
        slash = locate(P.string("/").skip(whitespace)).combine(_combine_slash)
    else:
        slash = P.success(None)

    return locate(
        P.seq(
            P.string("<"),
            tag_name_parser,
            attributes.skip(whitespace),
            slash,
            P.string(">"),
        )
    ).combine(_combine_opening_tag)


def _combine_element(locations, props):
    opening_tag, content, closing_tag = props
    return Element(
        opening_tag=opening_tag,
        closing_tag=closing_tag,
        content=content,
        **locations,
    )


def make_raw_text_element_parser(config, tag_name, jinja):
    """
    Used for <style> and <script>.
    """
    opening_tag = make_opening_tag_parser(
        config, tag_name_parser=P.string(tag_name), jinja=jinja
    )

    body = P.regex(r".*?(?=</" + tag_name + ">)", flags=re.DOTALL)

    closing_tag = make_closing_tag_parser(P.string(tag_name))

    return locate(P.seq(opening_tag, body, closing_tag)).combine(
        _combine_element
    )


slow_text_char = (
    (P.string("<") | P.string("{%") | P.string("{#") | P.string("{{"))
    .should_fail("text")
    .then(P.any_char)
)

# Not as precise as slow_text_char but must faster
quick_text = P.regex(r"[^{<]+", flags=re.DOTALL)


def _combine_optional_container(locations, nodes):
    return JinjaOptionalContainer(
        first_opening_if=nodes[0],
        opening_tag=nodes[1],
        first_closing_if=nodes[2],
        content=nodes[3],
        second_opening_if=nodes[4],
        closing_tag=nodes[5],
        second_closing_if=nodes[6],
        **locations,
    )


# Awkward hack to handle optional HTML containers, for example:
#
#   {% if a %}
#     <div>
#   {% endif %}
#   foo
#   {% if a %}
#     </div>
#   {% endif %}
#
# Currently, this only works with `if` statements and the two conditions
# must be exactly the same.
def make_jinja_optional_container_parser(config, content, jinja):
    jinja_if = make_jinja_tag_parser(P.string("if"))
    jinja_endif = make_jinja_tag_parser(P.string("endif"))
    opening_tag = make_opening_tag_parser(config, jinja, allow_slash=False)

    @P.generate
    def opt_container_impl():
        o_first_if_node = yield jinja_if.skip(whitespace)
        o_tag_node = yield opening_tag.skip(whitespace)
        c_first_if_node = yield jinja_endif

        content_nodes = yield content

        o_second_if_node = yield jinja_if.skip(whitespace)
        if o_second_if_node.content != o_first_if_node.content:
            yield P.fail("expected `{% if " + content + " %}`")
            return
        html_tag_name = o_tag_node.name
        if isinstance(html_tag_name, str):
            closing_tag = make_closing_tag_parser(P.string(html_tag_name))
        else:
            assert isinstance(html_tag_name, Jinja)
            closing_tag = make_closing_tag_parser(jinja)
        c_tag_node = yield closing_tag.skip(whitespace)
        c_second_if_node = yield jinja_endif

        return [
            o_first_if_node,
            o_tag_node,
            c_first_if_node,
            content_nodes,
            o_second_if_node,
            c_tag_node,
            c_second_if_node,
        ]

    return locate(opt_container_impl).combine(_combine_optional_container)


def make_jinja_parser(config, content):
    # Allow to override elements with the configuration
    jinja_structured_elements_names = dict(
        (names[0], names)
        for names in (
            DEFAULT_JINJA_STRUCTURED_ELEMENTS_NAMES
            + config.get("jinja_custom_elements_names", [])
        )
    ).values()

    jinja_structured_element = P.alt(
        *[
            make_jinja_element_parser(
                [P.string(name) for name in names], content=content
            )
            for names in jinja_structured_elements_names
        ]
    )

    # These tag names can't begin a Jinja element
    jinja_intermediate_tag_names = set(
        n for _, *sublist in jinja_structured_elements_names for n in sublist
    )

    jinja_intermediate_tag_name = P.alt(
        *(P.string(n) for n in jinja_intermediate_tag_names)
    )

    jinja_element_single = make_jinja_element_parser(
        [
            P.alt(
                # HACK: If we allow `{% if %}`s without `{% endif %}`s here,
                # `make_jinja_optional_container_parser` doesn’t work. It
                # is probably better to reject any structured tag name here.
                P.string("if"),
                jinja_intermediate_tag_name,
            )
            .should_fail("not an intermediate Jinja tag name")
            .then(jinja_name)
        ],
        content=content,
    )

    jinja_element = jinja_structured_element | jinja_element_single

    return jinja_variable | jinja_comment | jinja_element


def make_container_element_parser(config, content, jinja):
    opening_tag = make_opening_tag_parser(config, jinja=jinja)

    @P.generate
    def container_element_impl():
        o_tag_node = yield opening_tag
        content_nodes = yield content
        tag_name = o_tag_node.name
        if isinstance(tag_name, str):
            closing_tag = make_closing_tag_parser(P.string(tag_name))
        else:
            assert isinstance(tag_name, Jinja)
            closing_tag = make_closing_tag_parser(jinja)
        c_tag_node = yield closing_tag
        return [o_tag_node, content_nodes, c_tag_node]

    return locate(container_element_impl).combine(_combine_element)


def make_element_parser(config, content, jinja):
    container_element = make_container_element_parser(
        config, content=content, jinja=jinja
    )

    void_element_opening_tag = make_opening_tag_parser(
        config,
        tag_name_parser=P.string_from(*VOID_ELEMENTS),
        allow_slash=True,
        jinja=jinja,
    )

    void_element = locate(
        P.seq(
            void_element_opening_tag.skip(whitespace),
            P.success(None),  # No content
            P.success(None),  # No closing tag
        )
    ).combine(_combine_element)

    svg_self_closing_tag = make_opening_tag_parser(
        config,
        tag_name_parser=P.string_from(*SVG_SELF_CLOSING_ELEMENTS),
        mandate_slash=True,
        jinja=jinja,
    )

    svg_self_closing_element = locate(
        P.seq(
            svg_self_closing_tag.skip(whitespace),
            P.success(None),  # No content
            P.success(None),  # No closing tag
        )
    ).combine(_combine_element)

    style = make_raw_text_element_parser(config, "style", jinja=jinja)
    script = make_raw_text_element_parser(config, "script", jinja=jinja)

    return (
        style
        | script
        | void_element
        | svg_self_closing_element
        | container_element
    )


def make_parser(config=None):
    if config is None:
        config = {}

    content_ = None

    @P.generate
    def content():
        c = yield content_
        return c

    jinja = make_jinja_parser(config, content)

    element = make_element_parser(config, content, jinja)

    opt_container = make_jinja_optional_container_parser(config, content, jinja)

    content_ = interpolated(
        (
            quick_text
            | comment
            | dtd
            | element
            | opt_container
            | jinja
            | slow_text_char
        ).many()
    )

    return {"content": content_, "jinja": jinja, "element": element}
