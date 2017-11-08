from collections import namedtuple
from functools import lru_cache
import re

import parsy as P

from .ast import (
    Attribute, ClosingTag, Comment, Element, Integer, Interpolated,
    Jinja, JinjaComment, JinjaElement, JinjaElementPart, JinjaTag,
    JinjaVariable, Location, Node, OpeningTag, String,
)
from .util import flatten


# TODO: Move it elsewhere
import sys
sys.setrecursionlimit(10000)


# Also called “void elements”
SELF_CLOSING_ELEMENTS = """
area base br col command embed hr img input keygen link meta param source
track wbr
""".split()

DEPRECATED_ELEMENTS = """
acronym applet basefont big center dir font frame frameset noframes isindex
strike tt
""".split()

DEFAULT_JINJA_STRUCTURED_ELEMENTS_NAMES = [
    ('autoescape', 'endautoescape'),
    ('block', 'endblock'),
    ('blocktrans', 'endblocktrans'),
    ('comment', 'endcomment'),
    ('filter', 'endfilter'),
    ('for', 'else', 'empty', 'endfor'),
    ('if', 'elif', 'else', 'endif'),
    ('ifchanged', 'endifchanged'),
    ('ifequal', 'endifequal'),
    ('ifnotequal', 'endifnotequal'),
    ('spaceless', 'endspaceless'),
    ('verbatim', 'endverbatim'),
    ('with', 'endwith'),
]


whitespace = P.regex(r'\s*')


def until(parser):
    return parser.should_fail(repr(parser)).then(P.any_char).many()


def combine_locations(begin_index, begin, result, end_index, end):
    begin_loc = Location(line=begin[0], column=begin[1], index=begin_index)
    end_loc = Location(line=end[0], column=end[1], index=end_index)
    locations = {
        'begin': begin_loc,
        'end': end_loc,
    }

    return (
        locations,
        result,
    )


def locate(parser):

    return (
        P.seq(
            P.index,
            P.line_info,
            parser,
            P.index,
            P.line_info,
        )
        .combine(combine_locations)
    )


def _combine_jinja_tag(locations, props):
    head, name, content, tail = props
    return JinjaTag(
        name=name,
        content=content,
        **locations,
    )


def _combine_jinja_variable(locations, content):
    return JinjaVariable(
        content=content,
        **locations,
    )


def _combine_jinja_comment(locations, text):
    return JinjaComment(
        text=text,
        **locations,
    )


jinja_variable = (
    locate(
        P.string('{{')
        .skip(whitespace)
        .then(until(whitespace + P.string('}}')).concat())
        .skip(whitespace + P.string('}}'))
    )
    .combine(_combine_jinja_variable)
)

jinja_comment = (
    locate(
        P.string('{#')
        .skip(whitespace)
        .then(until(whitespace + P.string('#}')).concat())
        .skip(whitespace + P.string('#}'))
    )
    .combine(_combine_jinja_comment)
)


def make_jinja_tag_parser(name_parser):
    return (
        locate(
            P.seq(
                P.string('{%') + whitespace,
                name_parser.skip(whitespace),
                until(whitespace + P.string('%}')).concat(),
                whitespace + P.string('%}'),
            )
        )
        .combine(_combine_jinja_tag)
    )


def _combine_jinja_element(locations, content):
    parts = list(flatten(content[0]))
    closing_tag = content[1] if len(content) == 2 else None

    e = JinjaElement(
        parts=parts,
        closing_tag=closing_tag,
        **locations,
    )
    return e


def _combine_jinja_element_part(locations, props):
    tag, content = props
    return JinjaElementPart(
        tag=tag,
        content=content,
        **locations,
    )


def make_jinja_element_part_parser(name_parser, content):
    return locate(P.seq(
        make_jinja_tag_parser(name_parser),
        content,
    )).combine(_combine_jinja_element_part)


def make_jinja_element_parser(name_parsers, content):
    if len(name_parsers) == 1:
        tag = make_jinja_tag_parser(name_parsers[0])
        part = locate(P.seq(
            tag, P.success(None),
        )).combine(_combine_jinja_element_part)
        parts = [part]
        end_tag_parser = None
    else:
        part_names = name_parsers[:-1]
        first_part = make_jinja_element_part_parser(
            part_names[0], content=content)
        next_parts = [
            make_jinja_element_part_parser(name, content=content).many()
            for name in part_names[1:]
        ]
        parts = [first_part] + next_parts
        end_tag_parser = make_jinja_tag_parser(name_parsers[-1])

    content = [P.seq(*parts)]
    if end_tag_parser:
        content.append(end_tag_parser)

    return (
        locate(P.seq(*content))
        .combine(_combine_jinja_element)
    )


jinja_name = P.letter + (
    P.letter | P.decimal_digit | P.string('_')
).many().concat()


def interpolated(parser):
    def combine_interpolated(locations, result):
        return Interpolated(
            nodes=result,
            **locations,
        )

    return (
        locate(parser)
        .combine(combine_interpolated)
    )

tag_name_start_char = P.regex(r'[:a-z]')
tag_name_char = tag_name_start_char | P.regex(r'[0-9-_.]')
tag_name = tag_name_start_char + tag_name_char.many().concat()

dtd = P.regex(r'<![^>]*>')

string_attribute_char = P.char_from('-_./+,?=:;#') | P.regex(r'[0-9a-zA-Z]')


def make_quoted_string_attribute_parser(quote, jinja):
    """
    quote: A single or a double quote
    """
    def combine(locations, value):
        return String(
            value=value,
            quote=quote,
            **locations,
        )

    value_char = P.regex(r'[^<]', flags=re.DOTALL)
    value = interpolated(
        P.string(quote).should_fail('no ' + quote)
        .then(jinja | value_char)
        .many()
    )

    return locate(
        P.string(quote)
        .then(value)
        .skip(P.string(quote))
    ).combine(combine)


def _combine_string_attribute_value(locations, value):
    return String(
        value=value,
        quote=None,
        **locations,
    )


def _combine_int_attribute_value(locations, value):
    return Integer(
        value=value,
        has_percent=False,
        **locations,
    )


int_attribute_value = locate(
    P.regex(r'[0-9]+')
    .map(int)
).combine(_combine_int_attribute_value)


def _combine_attribute(locations, props):
    name, equal_and_value = props
    value = None if equal_and_value is None else equal_and_value['value']
    return Attribute(
        name=name,
        value=value,
        **locations,
    )


def make_attribute_value_parser(jinja):
    string_attribute_value = locate(
        interpolated(
            (jinja | string_attribute_char)
            .at_least(1)
        )
    ).combine(_combine_string_attribute_value)

    return (
        make_quoted_string_attribute_parser('"', jinja) |
        make_quoted_string_attribute_parser("'", jinja) |
        int_attribute_value |
        string_attribute_value
    ).desc('attribute value')


def make_attribute_parser(jinja):
    attribute_value = make_attribute_value_parser(jinja)
    return (
        locate(
            P.seq(
                interpolated(tag_name).skip(whitespace),
                P.seq(
                    P.string('=').skip(whitespace).tag('equal'),
                    interpolated(attribute_value).tag('value'),
                ).map(dict).optional(),
            )
        )
        .combine(_combine_attribute)
        .desc('attribute')
    )


@lru_cache(maxsize=8)
def make_attributes_parser(jinja):
    attribute = make_attribute_parser(jinja)
    return interpolated((jinja | attribute).sep_by(whitespace))


def _combine_comment(locations, text):
    return Comment(
        text=text,
        **locations,
    )

comment = locate(
    P.string('<!--')
    .then(P.regex(r'.*?(?=-->)', flags=re.DOTALL))
    .skip(P.string('-->'))
).combine(_combine_comment)


def _combine_opening_tag(locations, props):
    _lt, tag_name, attributes, slash, _gt = props
    return OpeningTag(
        name=tag_name,
        attributes=attributes,
        slash=slash,
        **locations,
    )


def _combine_closing_tag(locations, name):
    return ClosingTag(
        name=name,
        **locations
    )


def make_closing_tag_parser(tag_name_parser):
    return locate(
        P.string('</')
        .then(tag_name_parser)
        .skip(P.string('>'))
    ).combine(_combine_closing_tag)


def _combine_slash(locations, _):
    return locations['begin']


def make_opening_tag_parser(jinja,
                            tag_name_parser=None,
                            allow_slash=False):
    attributes = make_attributes_parser(jinja)

    if not tag_name_parser:
        tag_name_parser = tag_name | jinja

    if allow_slash:
        slash = (
            locate(
                P.string('/')
                .skip(whitespace)
            )
            .combine(_combine_slash)
            .optional()
        )
    else:
        slash = P.success(None)

    return (
        locate(P.seq(
            P.string('<'),
            tag_name_parser.skip(whitespace),
            attributes.skip(whitespace),
            slash,
            P.string('>'),
        ))
        .combine(_combine_opening_tag)
    )


def _combine_element(locations, props):
    opening_tag, content, closing_tag = props
    return Element(
        opening_tag=opening_tag,
        closing_tag=closing_tag,
        content=content,
        **locations,
    )


def make_raw_text_element_parser(tag_name, jinja):
    """
    Used for <style> and <script>.
    """
    opening_tag = make_opening_tag_parser(
        tag_name_parser=P.string(tag_name),
        jinja=jinja,
    )

    body = P.regex(r'.*?(?=</' + tag_name + '>)', flags=re.DOTALL)

    closing_tag = make_closing_tag_parser(P.string(tag_name))

    return (
        locate(P.seq(
            opening_tag,
            body,
            closing_tag,
        ))
        .combine(_combine_element)
    )


slow_text_char = (
    (P.string('<') | P.string('{%') | P.string('{#') | P.string('{{'))
    .should_fail('text')
    .then(P.any_char)
)

# Not as precise as slow_text_char but must faster
quick_text = P.regex(r'[^{<]+', flags=re.DOTALL)


def make_jinja_parser(config, content):
    jinja_structured_elements_names = (
        DEFAULT_JINJA_STRUCTURED_ELEMENTS_NAMES +
        config.get('jinja_custom_elements_names', [])
    )

    jinja_structured_element = P.alt(*[
        make_jinja_element_parser(
            [P.string(name) for name in names],
            content=content,
        )
        for names in jinja_structured_elements_names
    ])

    # These tag names can't begin a Jinja element
    jinja_intermediate_tag_names = [
        n
        for _, *sublist in jinja_structured_elements_names
        for n in sublist
    ]

    jinja_intermediate_tag_name = P.alt(*(
        P.string(n) for n in jinja_intermediate_tag_names
    ))

    jinja_element_single = make_jinja_element_parser(
        [jinja_intermediate_tag_name
         .should_fail('not an intermediate Jinja tag name')
         .then(jinja_name)],
        content=content,
    )

    jinja_element = jinja_structured_element | jinja_element_single

    return jinja_variable | jinja_comment | jinja_element


def make_container_element_parser(content, jinja):
    opening_tag = make_opening_tag_parser(jinja=jinja)

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

    return (
        locate(container_element_impl)
        .combine(_combine_element)
    )


def make_element_parser(content, jinja):
    container_element = make_container_element_parser(
        content=content,
        jinja=jinja,
    )

    self_closing_element_opening_tag = make_opening_tag_parser(
        tag_name_parser=P.string_from(*SELF_CLOSING_ELEMENTS),
        allow_slash=True,
        jinja=jinja,
    )

    self_closing_element = (
        locate(P.seq(
            self_closing_element_opening_tag.skip(whitespace),
            P.success(None),  # No content
            P.success(None),  # No closing tag
        ))
        .combine(_combine_element)
    )

    style = make_raw_text_element_parser('style', jinja=jinja)
    script = make_raw_text_element_parser('script', jinja=jinja)

    return style | script | self_closing_element | container_element


def make_parser(config=None):
    if config is None:
        config = {}

    content_ = None

    @P.generate
    def content():
        c = yield content_
        return c

    jinja = make_jinja_parser(config, content)

    element = make_element_parser(content, jinja)

    content_ = interpolated(
        (quick_text | comment | dtd | element | jinja | slow_text_char).many()
    )

    return {
        'content': content,
        'jinja': jinja,
        'element': element,
    }
