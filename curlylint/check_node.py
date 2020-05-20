class CheckNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self, level=0):
        name = getattr(self.value, "name", None)

        attributes = []
        if getattr(self.value, "opening_tag", None):
            attributes = [
                (str(n.name), str(n.value).strip("\"'"))
                for n in self.value.opening_tag.attributes.nodes
            ]

        result = (
            "  " * level
            + "{}: name={!r} attributes={!r}".format(
                type(self.value), name, attributes
            )
            + "\n"
        )

        for child in self.children:
            result += child.__str__(level + 1)

        return result


def build_tree(root, node):
    if isinstance(node, str) or node is None:
        return

    for child in node.nodes:
        new_node = CheckNode(child)
        if getattr(child, "content", None):
            build_tree(new_node, child.content)
        root.children.append(new_node)
