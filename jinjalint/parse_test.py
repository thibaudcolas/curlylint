import parsy as P

from .parse import (
    tag_name, tag_name_char, comment,
    make_attribute_value_parser, make_attribute_parser,
    make_closing_tag_parser, make_opening_tag_parser, make_parser,
)

from . import ast
from .ast import Location


parser = make_parser()
element = parser['element']
jinja = parser['jinja']
content = parser['content']
attribute_value = make_attribute_value_parser(jinja=jinja)
attribute = make_attribute_parser(jinja=jinja)
opening_tag = make_opening_tag_parser(jinja=jinja)


class DummyLocation():
    """
    Any instance of this class is equal to any Location.
    """
    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + '()'


def with_dummy_locations(node_class):
    def create_node(*args, **kwargs):
        kwargs = kwargs.copy()
        kwargs['begin'] = DummyLocation()
        kwargs['end'] = DummyLocation()

        return node_class(
            *args,
            **kwargs,
        )

    return create_node


Attribute = with_dummy_locations(ast.Attribute)
Element = with_dummy_locations(ast.Element)
ClosingTag = with_dummy_locations(ast.ClosingTag)
Comment = with_dummy_locations(ast.Comment)
Integer = with_dummy_locations(ast.Integer)
Interpolated = with_dummy_locations(ast.Interpolated)
I = Interpolated
JinjaComment = with_dummy_locations(ast.JinjaComment)
JinjaElement = with_dummy_locations(ast.JinjaElement)
JinjaElementPart = with_dummy_locations(ast.JinjaElementPart)
JinjaTag = with_dummy_locations(ast.JinjaTag)
JinjaVariable = with_dummy_locations(ast.JinjaVariable)
OpeningTag = with_dummy_locations(ast.OpeningTag)
String = with_dummy_locations(ast.String)


def test_dummy_location():
    dummy = DummyLocation()
    real = Location(0, 0, 0)
    assert dummy == real
    assert real == dummy

    assert not dummy != real
    assert not real != dummy


def test_tag_name():
    assert tag_name_char.parse('a') == 'a'
    assert tag_name.parse('bcd-ef9') == 'bcd-ef9'


def test_attribute_value():
    assert attribute_value.parse('hello-world') == String(
        value=I('hello-world'),
        quote=None,
    )

    assert attribute_value.parse('hello{{a}}world') == String(
        value=I([
            'hello',
            JinjaVariable(content='a'),
            'world',
        ]),
        quote=None,
    )

    assert attribute_value.parse('123') == Integer(
        value=123,
        has_percent=False,
    )

    assert attribute_value.parse('"hello"') == String(
        value=I('hello'),
        quote='"',
    )

    assert attribute_value.parse("'hello'") == String(
        value=I('hello'),
        quote="'",
    )

    assert attribute_value.parse("''") == String(
        value=I([]),
        quote="'",
    )

    assert attribute_value.parse("'hello{{b}}world'") == String(
        value=I([
            'hello',
            JinjaVariable(content='b'),
            'world',
        ]),
        quote="'",
    )


def test_attribute():
    assert attribute.parse('hello=world') == Attribute(
        name=I('hello'),
        value=I(
            String(
                value=I('world'),
                quote=None,
            ),
        ),
    )

    assert attribute.parse('a= "b"') == Attribute(
        name=I('a'),
        value=I(
            String(
                value=I('b'),
                quote='"',
            ),
        ),
    )

    assert attribute.parse('a =b_c23') == Attribute(
        name=I('a'),
        value=I(
            String(
                value=I('b_c23'),
                quote=None,
            ),
        ),
    )

    assert attribute.parse('valueless-attribute') == Attribute(
        name=I('valueless-attribute'),
        value=None,
    )


def test_comment():
    assert comment.parse('<!--hello--world-->') == Comment(
        text='hello--world',
    )


def test_opening_tag():
    assert opening_tag.parse('<div>') == OpeningTag(
        name='div',
        attributes=I([]),
    )

    assert opening_tag.parse('<div\n >') == OpeningTag(
        name='div',
        attributes=I([]),
    )

    assert opening_tag.parse('<div class="red" style="" >') == OpeningTag(
        name='div',
        attributes=I([
            Attribute(
                name=I('class'),
                value=I(
                    String(
                        value=I('red'),
                        quote='"',
                    ),
                ),
            ),

            Attribute(
                name=I('style'),
                value=I(
                    String(
                        value=I([]),
                        quote='"',
                    ),
                ),
            ),
        ]),
    )


def test_closing_tag():
    closing_tag = make_closing_tag_parser(P.string('div'))
    assert closing_tag.parse('</div>') == ClosingTag(
        name='div',
    )


def test_raw_text_elements():
    assert element.parse('<style a=b> <wont-be-parsed> </style>') == Element(
        content=' <wont-be-parsed> ',

        opening_tag=OpeningTag(
            name='style',
            attributes=I([

                Attribute(
                    name=I('a'),
                    value=I(
                        String(
                            value=I('b'),
                            quote=None,
                        ),
                    ),
                ),

            ]),
        ),

        closing_tag=ClosingTag(
            name='style',
        ),
    )


def test_element():
    assert element.parse('<div> hey </div>') == Element(
        opening_tag=OpeningTag(
            name='div',
            attributes=I([]),
        ),
        content=I([' hey ']),
        closing_tag=ClosingTag(
            name='div',
        ),
    )

    attributes = [
        Attribute(
            name=I('onclick'),
            value=I(
                String(
                    value=I([]),
                    quote='"',
                ),
            ),
        ),

        JinjaVariable(content='var'),

        Attribute(
            name=I('class'),
            value=I(
                String(
                    value=I('red'),
                    quote='"',
                ),
            ),
        ),
    ]

    assert element.parse('<br onclick="" {{var}} class="red">') == Element(
        opening_tag=OpeningTag(
            name='br',
            attributes=I(attributes),
        ),
        closing_tag=None,
        content=None,
    )

    src = '<{% if a %}bcd{% endif %}></{% if a %}bcd{% endif %}>'
    assert src == str(element.parse(src))


def test_self_closing_elements():
    assert element.parse('<br>') == Element(
        opening_tag=OpeningTag(
            name='br',
            attributes=I([]),
        ),
        content=None,
        closing_tag=None,
    )


def test_jinja_blocks():
    assert jinja.parse('{% name something == 123 %}') == JinjaElement(
        parts=[
            JinjaElementPart(
                tag=JinjaTag(
                    name='name',
                    content='something == 123',
                ),
                content=None,
            ),
        ],
        closing_tag=None,
    )

    assert jinja.parse('{% if a %}b{% else %}c{% endif %}') == JinjaElement(
        parts=[
            JinjaElementPart(
                tag=JinjaTag(
                    name='if',
                    content='a',
                ),
                content=I(['b']),
            ),
            JinjaElementPart(
                tag=JinjaTag(
                    name='else',
                    content='',
                ),
                content=I(['c']),
            ),
        ],
        closing_tag=JinjaTag(
            name='endif',
            content='',
        ),
    )

    src = '{% if a %}b{% elif %}c{% elif %}d{% else %}e{% endif %}'
    assert src == str(jinja.parse(src))


def test_doctype():
    assert content.parse('<!DOCTYPE html>') == I('<!DOCTYPE html>')


def test():
    test_dummy_location()
    test_tag_name()
    test_attribute_value()
    test_attribute()
    test_comment()
    test_opening_tag()
    test_closing_tag()
    test_raw_text_elements()
    test_element()
    test_self_closing_elements()
    test_jinja_blocks()
    test_doctype()

    src = '<html lang="fr"><body>Hello<br></body></html>'
    assert src == str(element.parse(src))

    src = '<br />'
    assert src == str(element.parse(src))
