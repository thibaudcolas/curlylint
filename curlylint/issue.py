import attr

from .file import File


@attr.s(frozen=True)
class IssueLocation:
    """Location inside a file: file path, and line/col offsets."""

    file_path = attr.ib()  # Path
    column = attr.ib()
    line = attr.ib()

    def __str__(self):
        return "{}:{}:{}".format(self.file_path, self.line + 1, self.column)

    @staticmethod
    def from_ast(file_path, line, column):
        if isinstance(file_path, File):
            file_path = file_path.path

        return IssueLocation(
            file_path=file_path,
            line=line,
            column=column,
        )


@attr.s(frozen=True)
class Issue:
    """A problem to report on a given location of a file."""

    location = attr.ib()
    message = attr.ib()
    code = attr.ib()

    def __str__(self):
        return f"{self.location}: {self.message} ({self.code})"

    def __attrs_post_init__(self):
        assert isinstance(self.location, IssueLocation)

    @staticmethod
    def from_ast(file, line, column, message, code):
        return Issue(IssueLocation.from_ast(file, line, column), message, code)

    @staticmethod
    def from_node(file, node, message, code):
        return Issue.from_ast(
            file.path,
            node.value.begin.line + 1,
            node.value.begin.column + 1,
            message,
            code,
        )

    @staticmethod
    def from_dict(issue):
        return Issue.from_ast(**issue)
