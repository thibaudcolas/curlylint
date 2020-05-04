import parsy as P

from . import ast
from .ast import Location
from .parse import (
    comment,
    jinja_comment,
    make_attribute_parser,
    make_attribute_value_parser,
    make_attributes_parser,
    make_closing_tag_parser,
    make_opening_tag_parser,
    make_parser,
    tag_name,
    tag_name_char,
)

parser = make_parser()
element = parser["element"]
jinja = parser["jinja"]
content = parser["content"]
attribute_value = make_attribute_value_parser(jinja=jinja)
attribute = make_attribute_parser(jinja=jinja)
opening_tag = make_opening_tag_parser({}, jinja=jinja)


class DummyLocation:
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
        return self.__class__.__name__ + "()"


def with_dummy_locations(node_class):
    def create_node(*args, **kwargs):
        kwargs = kwargs.copy()
        kwargs["begin"] = DummyLocation()
        kwargs["end"] = DummyLocation()

        try:
            return node_class(*args, **kwargs)
        except Exception as error:
            print(node_class)
            raise error

    return create_node


Attribute = with_dummy_locations(ast.Attribute)
Element = with_dummy_locations(ast.Element)
ClosingTag = with_dummy_locations(ast.ClosingTag)
Comment = with_dummy_locations(ast.Comment)
JinjaComment = with_dummy_locations(ast.JinjaComment)
Integer = with_dummy_locations(ast.Integer)
Interp = with_dummy_locations(ast.Interpolated)
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

    assert not dummy != real  # lgtm [py/redundant-comparison]
    assert not real != dummy  # lgtm [py/redundant-comparison]


def test_tag_name():
    assert tag_name_char.parse("a") == "a"
    assert tag_name.parse("bcd-ef9") == "bcd-ef9"


def test_attribute_value():
    assert attribute_value.parse("hello-world") == String(
        value=Interp("hello-world"), quote=None
    )

    assert attribute_value.parse("hello{{a}}world") == String(
        value=Interp(["hello", JinjaVariable(content="a"), "world"]), quote=None
    )

    assert attribute_value.parse("123") == Integer(value=123, has_percent=False)

    assert attribute_value.parse('"hello"') == String(
        value=Interp("hello"), quote='"'
    )

    assert attribute_value.parse("'hello'") == String(
        value=Interp("hello"), quote="'"
    )

    assert attribute_value.parse("''") == String(value=Interp([]), quote="'")

    assert attribute_value.parse("'hello{{b}}world'") == String(
        value=Interp(["hello", JinjaVariable(content="b"), "world"]), quote="'"
    )


def test_attribute():
    assert attribute.parse("hello=world") == Attribute(
        name=Interp("hello"),
        value=Interp(String(value=Interp("world"), quote=None)),
    )

    assert attribute.parse('a= "b"') == Attribute(
        name=Interp("a"), value=Interp(String(value=Interp("b"), quote='"'))
    )

    assert attribute.parse('A="b"') == Attribute(
        name=Interp("A"), value=Interp(String(value=Interp("b"), quote='"'))
    )

    assert attribute.parse('viewBox="b"') == Attribute(
        name=Interp("viewBox"),
        value=Interp(String(value=Interp("b"), quote='"')),
    )

    assert attribute.parse("a =b_c23") == Attribute(
        name=Interp("a"),
        value=Interp(String(value=Interp("b_c23"), quote=None)),
    )

    assert attribute.parse("valueless-attribute") == Attribute(
        name=Interp("valueless-attribute"), value=None
    )


def test_comment():
    assert comment.parse("<!--hello--world-->") == Comment(text="hello--world")


def test_jinja_comment():
    assert jinja_comment.parse("{# hello world #}") == JinjaComment(
        text="hello world"
    )


def test_opening_tag():
    assert opening_tag.parse("<div>") == OpeningTag(
        name="div", attributes=Interp([])
    )

    assert opening_tag.parse("<div\n >") == OpeningTag(
        name="div", attributes=Interp([])
    )

    assert opening_tag.parse('<div class="red" style="" >') == OpeningTag(
        name="div",
        attributes=Interp(
            [
                Attribute(
                    name=Interp("class"),
                    value=Interp(String(value=Interp("red"), quote='"')),
                ),
                Attribute(
                    name=Interp("style"),
                    value=Interp(String(value=Interp([]), quote='"')),
                ),
            ]
        ),
    )


def test_closing_tag():
    closing_tag = make_closing_tag_parser(P.string("div"))
    assert closing_tag.parse("</div>") == ClosingTag(name="div")


def test_raw_text_elements():
    assert element.parse("<style a=b> <wont-be-parsed> </style>") == Element(
        content=" <wont-be-parsed> ",
        opening_tag=OpeningTag(
            name="style",
            attributes=Interp(
                [
                    Attribute(
                        name=Interp("a"),
                        value=Interp(String(value=Interp("b"), quote=None)),
                    )
                ]
            ),
        ),
        closing_tag=ClosingTag(name="style"),
    )


def test_element():
    assert element.parse("<div> hey </div>") == Element(
        opening_tag=OpeningTag(name="div", attributes=Interp([])),
        content=Interp([" hey "]),
        closing_tag=ClosingTag(name="div"),
    )

    attributes = [
        Attribute(
            name=Interp("onclick"),
            value=Interp(String(value=Interp([]), quote='"')),
        ),
        JinjaVariable(content="var"),
        Attribute(
            name=Interp("class"),
            value=Interp(String(value=Interp("red"), quote='"')),
        ),
    ]

    assert element.parse('<br onclick="" {{var}} class="red">') == Element(
        opening_tag=OpeningTag(name="br", attributes=Interp(attributes)),
        closing_tag=None,
        content=None,
    )

    src = "<{% if a %}bcd{% endif %}></{% if a %}bcd{% endif %}>"
    assert src == str(element.parse(src))

    src = '<div{{ "ider" }}></div>'
    assert '<div {{ "ider" }}></div>' == str(element.parse(src))

    src = '<div{% if a %}foo="bar"{% endif %}></div>'
    assert '<div {% if a %}foo="bar"{% endif %}></div>' == str(
        element.parse(src)
    )

    src = '<div{% if a %} foo="bar"  a=2 {% endif %}></div>'
    assert '<div {% if a %}foo="bar"a=2{% endif %}></div>' == str(
        element.parse(src)
    )

    src = "<colgroup></colgroup>"
    assert src == str(element.parse(src))


def test_self_closing_elements():
    assert element.parse("<br>") == Element(
        opening_tag=OpeningTag(name="br", attributes=Interp([])),
        content=None,
        closing_tag=None,
    )

    src = "<br />"
    assert src == str(element.parse(src))


def test_jinja_blocks():
    assert jinja.parse("{% name something == 123 %}") == JinjaElement(
        parts=[
            JinjaElementPart(
                tag=JinjaTag(name="name", content="something == 123"),
                content=None,
            )
        ],
        closing_tag=None,
    )

    assert jinja.parse("{% if a %}b{% else %}c{% endif %}") == JinjaElement(
        parts=[
            JinjaElementPart(
                tag=JinjaTag(name="if", content="a"), content=Interp(["b"])
            ),
            JinjaElementPart(
                tag=JinjaTag(name="else", content=""), content=Interp(["c"])
            ),
        ],
        closing_tag=JinjaTag(name="endif", content=""),
    )

    src = "{% if a %}b{% elif %}c{% elif %}d{% else %}e{% endif %}"
    assert src == str(jinja.parse(src))


def test_jinja_whitespace_controls():
    assert jinja.parse("{%- foo -%}") == JinjaElement(
        parts=[
            JinjaElementPart(
                tag=JinjaTag(
                    name="foo", content="", left_minus=True, right_minus=True
                ),
                content=None,
            )
        ],
        closing_tag=None,
    )

    assert str(jinja.parse("{%- foo -%}")) == "{%- foo -%}"
    assert str(jinja.parse("{%- foo %}")) == "{%- foo %}"
    assert str(jinja.parse("{{- bar -}}")) == "{{- bar -}}"
    assert str(jinja.parse("{{ bar -}}")) == "{{ bar -}}"
    assert str(jinja.parse("{%+ foo %}")) == "{%+ foo %}"
    assert str(jinja.parse("{{+ bar }}")) == "{{+ bar }}"


def test_doctype():
    assert content.parse("<!DOCTYPE html>") == Interp("<!DOCTYPE html>")


def test_attrs():
    attrs = make_attributes_parser({}, jinja)
    parse = attrs.parse

    assert str(parse("{% if %}{% endif %}")) == "{% if %}{% endif %}"
    assert str(parse("{% if %}  {% endif %}")) == "{% if %}{% endif %}"
    assert str(parse("{% if %}a=b{% endif %}")) == "{% if %}a=b{% endif %}"
    assert str(parse("{% if %} a=b {% endif %}")) == "{% if %}a=b{% endif %}"


def test_optional_container():
    src = '{% if a %}<a href="b">{% endif %}c<b>d</b>{% if a %}</a>{% endif %}'
    assert src == str(content.parse(src))

    src = """
    {% if a %} <a href="b"> {% endif %}
        c <b> d </b>
    {% if a %} </a> {% endif %}
    """
    content.parse(src)


def test_whole_document():
    src = '<html lang="fr"><body>Hello<br></body></html>'
    assert src == str(element.parse(src))


def test():
    test_dummy_location()
    test_tag_name()
    test_attribute_value()
    test_attribute()
    test_comment()
    test_jinja_comment()
    test_opening_tag()
    test_closing_tag()
    test_raw_text_elements()
    test_element()
    test_self_closing_elements()
    test_jinja_blocks()
    test_jinja_whitespace_controls()
    test_doctype()
    test_attrs()
    test_optional_container()
