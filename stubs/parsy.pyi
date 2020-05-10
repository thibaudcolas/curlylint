from typing import Any, Optional

def string(  # noqa: E704, E302
    expected_string: str, transform: Optional[Any] = None
) -> Any: ...  # noqa: E704
def regex(exp: str, flags: int = 0) -> Any: ...  # noqa: E704
def success(val: Any) -> Any: ...  # noqa: E704
def letter() -> Any: ...  # noqa: E704
def decimal_digit() -> Any: ...  # noqa: E704
def any_char() -> Any: ...  # noqa: E704
def char_from(characters: str) -> Any: ...  # noqa: E704, E302

class ParseError(RuntimeError):  # noqa: E704, E302
    def line_info(self) -> str: ...  # noqa: E704
