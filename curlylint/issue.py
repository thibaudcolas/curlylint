import attr

from .file import File


@attr.s(frozen=True)
class IssueLocation:
    file_path = attr.ib()  # Path
    column = attr.ib()
    line = attr.ib()

    def __str__(self):
        return "{}:{}:{}".format(self.file_path, self.line + 1, self.column)

    @staticmethod
    def from_ast(file_path, ast_location):
        if isinstance(file_path, File):
            file_path = file_path.path

        return IssueLocation(
            file_path=file_path,
            column=ast_location.column,
            line=ast_location.line,
        )


@attr.s(frozen=True)
class Issue:
    location = attr.ib()
    message = attr.ib()
    code = attr.ib()

    def __str__(self):
        return f"{self.location}: {self.message} ({self.code})"

    def __attrs_post_init__(self):
        assert isinstance(self.location, IssueLocation)

    @staticmethod
    def from_ast(file_path, ast_location, message, code):
        return Issue(
            IssueLocation.from_ast(file_path, ast_location), message, code
        )
