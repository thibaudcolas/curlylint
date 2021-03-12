import sys
from contextlib import contextmanager
from io import BytesIO, TextIOWrapper
from typing import (
    Any,
    BinaryIO,
    Generator,
)

from click.testing import CliRunner


class BlackRunner(CliRunner):
    """Borrowed from black.
    https://github.com/psf/black/blob/5446a92f0161e398de765bf9532d8c76c5652333/tests/test_black.py#L101
    Modify CliRunner so that stderr is not merged with stdout.
    This is a hack that can be removed once we depend on Click 7.x"""

    def __init__(self) -> None:
        self.stderrbuf = BytesIO()
        self.stdoutbuf = BytesIO()
        self.stdout_bytes = b""
        self.stderr_bytes = b""
        super().__init__()

    @contextmanager
    def isolation(
        self, *args: Any, **kwargs: Any
    ) -> Generator[BinaryIO, None, None]:
        with super().isolation(*args, **kwargs) as output:
            try:
                hold_stderr = sys.stderr
                sys.stderr = TextIOWrapper(
                    self.stderrbuf, encoding=self.charset
                )
                yield output
            finally:
                self.stdout_bytes = sys.stdout.buffer.getvalue()  # type: ignore
                self.stderr_bytes = sys.stderr.buffer.getvalue()  # type: ignore
                sys.stderr = hold_stderr
