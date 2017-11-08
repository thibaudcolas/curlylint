import attr


@attr.s(frozen=True)
class File:
    lines = attr.ib()  # [str]
    source = attr.ib()  # str
    tree = attr.ib()  # ast.Node
    path = attr.ib()  # Path
