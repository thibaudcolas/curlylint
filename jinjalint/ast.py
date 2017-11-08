import attr


@attr.s(frozen=True)
class Location:
    line = attr.ib()  # 0-based
    column = attr.ib()
    index = attr.ib()

    def __str__(self):
        return '{}:{}'.format(self.line + 1, self.column)


@attr.s
class Node:
    begin = attr.ib()  # Location
    end = attr.ib()  # Location


@attr.s(frozen=True)
class Slash(Node):
    def __str__(self):
        return '/'


@attr.s(frozen=True)
class OpeningTag(Node):
    name = attr.ib()
    attributes = attr.ib()  # Interpolated<Attribute>
    slash = attr.ib(default=None)  # Slash | None

    def __str__(self):
        name = str(self.name)
        inner = ' '.join([name] + [str(a) for a in self.attributes])
        if self.slash:
            inner += ' /'
        return '<' + inner + '>'


@attr.s(frozen=True)
class ClosingTag(Node):
    name = attr.ib()

    def __str__(self):
        return '</{}>'.format(self.name)


@attr.s(frozen=True)
class Element(Node):
    opening_tag = attr.ib()  # OpeningTag
    closing_tag = attr.ib()  # ClosingTag | None
    content = attr.ib()  # Text | None

    def __attrs_post_init__(self):
        if self.closing_tag is not None:
            if isinstance(self.opening_tag.name, str):
                assert str(self.opening_tag.name) == self.closing_tag.name

    @property
    def name(self):
        return self.opening_tag.name

    @property
    def attributes(self):
        return self.opening_tag.attributes

    def __str__(self):
        if self.content is None:
            content_str = ''
        else:
            content_str = ''.join(str(n) for n in self.content)
        return ''.join([
            str(self.opening_tag),
            content_str,
            str(self.closing_tag or ''),
        ])


@attr.s(frozen=True)
class String(Node):
    value = attr.ib()  # str
    quote = attr.ib()  # '"' | "'" | None

    def __str__(self):
        if self.quote is None:
            return str(self.value)
        return self.quote + str(self.value) + self.quote


@attr.s(frozen=True)
class Integer(Node):
    value = attr.ib()  # int
    has_percent = attr.ib()  # bool

    def __str__(self):
        return self.value + ('%' if self.has_percent else '')


@attr.s(frozen=True)
class Attribute(Node):
    name = attr.ib()  # str
    value = attr.ib()  # String | Integer

    def __str__(self):
        return '{}={}'.format(self.name, self.value)


@attr.s(frozen=True)
class Comment(Node):
    text = attr.ib()  # str

    def __str__(self):
        return '<!--{}-->'.format(self.text)


@attr.s(frozen=True)
class Jinja(Node):
    pass


@attr.s(frozen=True)
class JinjaVariable(Jinja):
    content = attr.ib()  # str

    def __str__(self):
        return '{{ ' + self.content + ' }}'


@attr.s(frozen=True)
class JinjaComment(Jinja):
    text = attr.ib()  # str

    def __str__(self):
        return '{##}'


@attr.s(frozen=True)
class JinjaTag(Jinja):
    name = attr.ib()
    content = attr.ib()  # str | None

    def __str__(self):
        s = '{% ' + self.name
        if self.content:
            s += ' ' + self.content

        return s + ' %}'


@attr.s(frozen=True)
class JinjaElementPart(Jinja):
    tag = attr.ib()  # JinjaTag
    content = attr.ib()  # Interpolated | None

    def __str__(self):
        return str(self.tag) + str(self.content or '')


@attr.s(frozen=True)
class JinjaElement(Jinja):
    parts = attr.ib()  # [JinjaElementPart]
    closing_tag = attr.ib()  # JinjaTag

    def __str__(self):
        return (
            ''.join(str(p) for p in self.parts) +
            str(self.closing_tag or '')
        )


@attr.s(frozen=True)
class InterpolatedBase(Node):
    nodes = attr.ib()  # [any | Jinja]

    @property
    def single_node(self):
        return self.nodes[0] if len(self.nodes) == 1 else None

    @property
    def single_str(self):
        node = self.single_node
        return node if isinstance(node, str) else None

    def __getitem__(self, index):
        return self.nodes.__getitem__(index)

    def __iter__(self):
        return self.nodes.__iter__()

    def __len__(self):
        return len(self.nodes)

    def __str__(self):
        return ''.join(str(n) for n in self.nodes)


def _concat_strings(nodes):
    if len(nodes) <= 1:
        return nodes
    a, b, *rest = nodes
    if isinstance(a, str) and isinstance(b, str):
        return _concat_strings([a + b] + rest)
    return [a] + _concat_strings([b] + rest)


def _normalize_nodes(thing):
    if not isinstance(thing, list):
        nodes = [thing]
    else:
        nodes = thing
    return _concat_strings(nodes)


class Interpolated(InterpolatedBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            assert 'nodes' not in kwargs
            nodes = _normalize_nodes(args[0])
            super().__init__(nodes=nodes, **kwargs)
            return

        assert len(args) == 0
        kwargs = kwargs.copy()
        kwargs['nodes'] = _normalize_nodes(kwargs['nodes'])
        super().__init__(**kwargs)


NODE_TYPE_LIST = [
    Node, Slash, OpeningTag, ClosingTag, Element, String, Integer,
    Attribute, Comment, JinjaVariable, JinjaComment, JinjaTag,
    JinjaElement, JinjaElementPart, InterpolatedBase, Interpolated,
]
