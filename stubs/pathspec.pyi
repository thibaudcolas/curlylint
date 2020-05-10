from typing import Any, Iterable

class PathSpec:  # noqa: E302
    def match_file(self, file: str) -> bool: ...  # noqa: E704
    @classmethod
    def from_lines(  # noqa: E704
        cls, pattern_factory: str, lines: Iterable[str]
    ) -> Any: ...
