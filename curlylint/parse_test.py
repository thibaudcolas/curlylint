import unittest
import pytest

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


class TestUtil(unittest.TestCase):
    def test_dummy_location(self):
        dummy = DummyLocation()
        real = Location(0, 0, 0)
        self.assertEqual(dummy, real)
        self.assertEqual(real, dummy)

        self.assertEqual(dummy != real, False)  # lgtm [py/redundant-comparison]
        self.assertEqual(real != dummy, False)  # lgtm [py/redundant-comparison]


class TestParser(unittest.TestCase):
    def test_tag_name(self):
        self.assertEqual(tag_name_char.parse("a"), "a")
        self.assertEqual(tag_name.parse("bcd-ef9"), "bcd-ef9")
        self.assertEqual(tag_name.parse("clipPath"), "clipPath")
        self.assertEqual(tag_name.parse("HTML"), "HTML")

    def test_attribute_value(self):
        self.assertEqual(
            attribute_value.parse("hello-world"),
            String(value=Interp("hello-world"), quote=None),
        )

        self.assertEqual(
            attribute_value.parse("hello{{a}}world"),
            String(
                value=Interp(["hello", JinjaVariable(content="a"), "world"]),
                quote=None,
            ),
        )

        self.assertEqual(
            attribute_value.parse("123"), Integer(value=123, has_percent=False)
        )

        self.assertEqual(
            attribute_value.parse('"hello"'),
            String(value=Interp("hello"), quote='"'),
        )

        self.assertEqual(
            attribute_value.parse("'hello'"),
            String(value=Interp("hello"), quote="'"),
        )

        self.assertEqual(
            attribute_value.parse("''"), String(value=Interp([]), quote="'")
        )

        self.assertEqual(
            attribute_value.parse("'hello{{b}}world'"),
            String(
                value=Interp(["hello", JinjaVariable(content="b"), "world"]),
                quote="'",
            ),
        )

    def test_attribute(self):
        self.assertEqual(
            attribute.parse("hello=world"),
            Attribute(
                name=Interp("hello"),
                value=Interp(String(value=Interp("world"), quote=None)),
            ),
        )

        self.assertEqual(
            attribute.parse('a= "b"'),
            Attribute(
                name=Interp("a"),
                value=Interp(String(value=Interp("b"), quote='"')),
            ),
        )

        self.assertEqual(
            attribute.parse('A="b"'),
            Attribute(
                name=Interp("A"),
                value=Interp(String(value=Interp("b"), quote='"')),
            ),
        )

        self.assertEqual(
            attribute.parse('viewBox="b"'),
            Attribute(
                name=Interp("viewBox"),
                value=Interp(String(value=Interp("b"), quote='"')),
            ),
        )

        self.assertEqual(
            attribute.parse("a =b_c23"),
            Attribute(
                name=Interp("a"),
                value=Interp(String(value=Interp("b_c23"), quote=None)),
            ),
        )

        self.assertEqual(
            attribute.parse("valueless-attribute"),
            Attribute(name=Interp("valueless-attribute"), value=None),
        )

    def test_comment(self):
        self.assertEqual(
            comment.parse("<!--hello--world-->"), Comment(text="hello--world")
        )

    def test_jinja_comment(self):
        self.assertEqual(
            jinja_comment.parse("{# hello world #}"),
            JinjaComment(text="hello world"),
        )

    def test_opening_tag(self):
        self.assertEqual(
            opening_tag.parse("<div>"),
            OpeningTag(name="div", attributes=Interp([])),
        )

        self.assertEqual(
            opening_tag.parse("<div\n >"),
            OpeningTag(name="div", attributes=Interp([])),
        )

        self.assertEqual(
            opening_tag.parse('<div class="red" style="" >'),
            OpeningTag(
                name="div",
                attributes=Interp(
                    [
                        Attribute(
                            name=Interp("class"),
                            value=Interp(
                                String(value=Interp("red"), quote='"')
                            ),
                        ),
                        Attribute(
                            name=Interp("style"),
                            value=Interp(String(value=Interp([]), quote='"')),
                        ),
                    ]
                ),
            ),
        )

    def test_opening_tag_attributes_no_space(self):
        # See https://html.spec.whatwg.org/multipage/syntax.html#start-tags
        # "Attributes must be separated from each other by one or more ASCII whitespace."
        # See https://github.com/thibaudcolas/curlylint/issues/23#issuecomment-700622837
        with pytest.raises(
            P.ParseError,
            match="space\\(s\\) between attributes",
        ):
            opening_tag.parse(
                '<a class="govuk-button"href="/cookies">Set cookie preferences</a>'
            )

    def test_opening_tag_jinja_block_attributes_whitespace_after(self):
        opening_tag.parse(
            '<form{% if has_file_field %} enctype="multipart/form-data"{% endif %} action="{{ form_url }}">'
        )

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_opening_tag_jinja_block_attributes_whitespace_before_37(self):
        # https://github.com/thibaudcolas/curlylint/issues/37
        opening_tag.parse(
            '<form {% if has_file_field %}enctype="multipart/form-data" {% endif %}action="{{ form_url }}">'
        )

    def test_closing_tag(self):
        closing_tag = make_closing_tag_parser(P.string("div"))
        self.assertEqual(closing_tag.parse("</div>"), ClosingTag(name="div"))

    def test_raw_text_elements(self):
        self.assertEqual(
            element.parse("<style a=b> <wont-be-parsed> </style>"),
            Element(
                content=" <wont-be-parsed> ",
                opening_tag=OpeningTag(
                    name="style",
                    attributes=Interp(
                        [
                            Attribute(
                                name=Interp("a"),
                                value=Interp(
                                    String(value=Interp("b"), quote=None)
                                ),
                            )
                        ]
                    ),
                ),
                closing_tag=ClosingTag(name="style"),
            ),
        )

    def test_element(self):
        self.assertEqual(
            element.parse("<div> hey </div>"),
            Element(
                opening_tag=OpeningTag(name="div", attributes=Interp([])),
                content=Interp([" hey "]),
                closing_tag=ClosingTag(name="div"),
            ),
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

        self.assertEqual(
            element.parse('<br onclick="" {{var}} class="red">'),
            Element(
                opening_tag=OpeningTag(
                    name="br", attributes=Interp(attributes)
                ),
                closing_tag=None,
                content=None,
            ),
        )

        src = "<{% if a %}bcd{% endif %}></{% if a %}bcd{% endif %}>"
        self.assertEqual(src, str(element.parse(src)))

        src = '<div{{ "ider" }}></div>'
        self.assertEqual('<div {{ "ider" }}></div>', str(element.parse(src)))

        src = '<div{% if a %}foo="bar"{% endif %}></div>'
        self.assertEqual(
            '<div {% if a %}foo="bar"{% endif %}></div>',
            str(element.parse(src)),
        )

        src = '<div{% if a %} foo="bar"  a=2 {% endif %}></div>'
        self.assertEqual(
            '<div {% if a %}foo="bar"a=2{% endif %}></div>',
            str(element.parse(src)),
        )

        src = "<colgroup></colgroup>"
        self.assertEqual(src, str(element.parse(src)))

    def test_self_closing_elements(self):
        self.assertEqual(
            element.parse("<br>"),
            Element(
                opening_tag=OpeningTag(name="br", attributes=Interp([])),
                content=None,
                closing_tag=None,
            ),
        )

        src = "<br />"
        self.assertEqual(src, str(element.parse(src)))

    def test_jinja_blocks(self):
        self.assertEqual(
            jinja.parse("{% name something == 123 %}"),
            JinjaElement(
                parts=[
                    JinjaElementPart(
                        tag=JinjaTag(name="name", content="something == 123"),
                        content=None,
                    )
                ],
                closing_tag=None,
            ),
        )

        self.assertEqual(
            jinja.parse("{% if a %}b{% else %}c{% endif %}"),
            JinjaElement(
                parts=[
                    JinjaElementPart(
                        tag=JinjaTag(name="if", content="a"),
                        content=Interp(["b"]),
                    ),
                    JinjaElementPart(
                        tag=JinjaTag(name="else", content=""),
                        content=Interp(["c"]),
                    ),
                ],
                closing_tag=JinjaTag(name="endif", content=""),
            ),
        )

        src = "{% if a %}b{% elif %}c{% elif %}d{% else %}e{% endif %}"
        self.assertEqual(src, str(jinja.parse(src)))

    def test_jinja_custom_tag_self_closing(self):
        self.assertEqual(
            jinja.parse("{% potato %}"),
            JinjaElement(
                parts=[
                    JinjaElementPart(
                        tag=JinjaTag(name="potato", content=""),
                        content=None,
                    )
                ],
                closing_tag=None,
            ),
        )

    def test_jinja_custom_tag_open_close_unconfigured(self):
        with pytest.raises(P.ParseError):
            jinja.parse("{% of a %}c{% endof %}")

    def test_jinja_custom_tag_open_close_configured_deprecated(self):
        # Deprecated, will be removed in a future release.
        parser = make_parser({"jinja_custom_elements_names": [["of", "endof"]]})
        jinja = parser["jinja"]
        self.assertEqual(
            jinja.parse("{% of a %}c{% endof %}"),
            JinjaElement(
                parts=[
                    JinjaElementPart(
                        tag=JinjaTag(name="of", content="a"),
                        content=Interp(["c"]),
                    ),
                ],
                closing_tag=JinjaTag(name="endof", content=""),
            ),
        )

    def test_jinja_custom_tag_open_close_configured(self):
        parser = make_parser({"template_tags": [["of", "endof"]]})
        jinja = parser["jinja"]
        self.assertEqual(
            jinja.parse("{% of a %}c{% endof %}"),
            JinjaElement(
                parts=[
                    JinjaElementPart(
                        tag=JinjaTag(name="of", content="a"),
                        content=Interp(["c"]),
                    ),
                ],
                closing_tag=JinjaTag(name="endof", content=""),
            ),
        )

    def test_jinja_custom_tag_open_middle_close_unconfigured(self):
        with pytest.raises(P.ParseError):
            jinja.parse("{% of a %}b{% elseof %}c{% endof %}")

    def test_jinja_custom_tag_open_middle_close(self):
        parser = make_parser(
            {"jinja_custom_elements_names": [["of", "elseof", "endof"]]}
        )
        jinja = parser["jinja"]
        self.assertEqual(
            jinja.parse("{% of a %}b{% elseof %}c{% endof %}"),
            JinjaElement(
                parts=[
                    JinjaElementPart(
                        tag=JinjaTag(name="of", content="a"),
                        content=Interp(["b"]),
                    ),
                    JinjaElementPart(
                        tag=JinjaTag(name="elseof", content=""),
                        content=Interp(["c"]),
                    ),
                ],
                closing_tag=JinjaTag(name="endof", content=""),
            ),
        )

    def test_jinja_whitespace_controls(self):
        self.assertEqual(
            jinja.parse("{%- foo -%}"),
            JinjaElement(
                parts=[
                    JinjaElementPart(
                        tag=JinjaTag(
                            name="foo",
                            content="",
                            left_minus=True,
                            right_minus=True,
                        ),
                        content=None,
                    )
                ],
                closing_tag=None,
            ),
        )

        self.assertEqual(str(jinja.parse("{%- foo -%}")), "{%- foo -%}")
        self.assertEqual(str(jinja.parse("{%- foo %}")), "{%- foo %}")
        self.assertEqual(str(jinja.parse("{{- bar -}}")), "{{- bar -}}")
        self.assertEqual(str(jinja.parse("{{ bar -}}")), "{{ bar -}}")
        self.assertEqual(str(jinja.parse("{%+ foo %}")), "{%+ foo %}")
        self.assertEqual(str(jinja.parse("{{+ bar }}")), "{{+ bar }}")

    def test_doctype(self):
        self.assertEqual(
            content.parse("<!DOCTYPE html>"), Interp("<!DOCTYPE html>")
        )

    def test_attrs(self):
        attrs = make_attributes_parser({}, jinja)
        parse = attrs.parse

        self.assertEqual(
            str(parse("{% if %}{% endif %}")), "{% if %}{% endif %}"
        )
        self.assertEqual(
            str(parse("{% if %}  {% endif %}")), "{% if %}{% endif %}"
        )
        self.assertEqual(
            str(parse("{% if %}a=b{% endif %}")), "{% if %}a=b{% endif %}"
        )
        self.assertEqual(
            str(parse("{% if %} a=b {% endif %}")), "{% if %}a=b{% endif %}"
        )

    def test_optional_container(self):
        src = '{% if a %}<a href="b">{% endif %}c<b>d</b>{% if a %}</a>{% endif %}'
        self.assertEqual(src, str(content.parse(src)))

        src = """
        {% if a %} <a href="b"> {% endif %}
            c <b> d </b>
        {% if a %} </a> {% endif %}
        """
        content.parse(src)

    def test_whole_document(self):
        src = '<html lang="fr"><body>Hello<br></body></html>'
        self.assertEqual(src, str(element.parse(src)))
