from __future__ import annotations

import os
import sys
from enum import IntEnum, unique
from math import ceil, floor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from typing_extensions import Self  # py3.10: import from typing

TRUE_VAR = {"0", "false", "no"}


@unique
class SGRCodes(IntEnum):
    RESET = 0

    BOLD = 1
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    CONCEAL = 8

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    GREY = 37

    BG_BLACK = 40
    BG_RED = 41
    BG_GREEN = 42
    BG_YELLOW = 43
    BG_BLUE = 44
    BG_MAGENTA = 45
    BG_CYAN = 46
    BG_GREY = 47

    BLACK_BRIGHT = 90
    RED_BRIGHT = 91
    GREEN_BRIGHT = 92
    YELLOW_BRIGHT = 93
    BLUE_BRIGHT = 94
    MAGENTA_BRIGHT = 95
    CYAN_BRIGHT = 96
    WHITE_BRIGHT = 97

    BG_BLACK_BRIGHT = 100
    BG_RED_BRIGHT = 101
    BG_GREEN_BRIGHT = 102
    BG_YELLOW_BRIGHT = 103
    BG_BLUE_BRIGHT = 104
    BG_MAGENTA_BRIGHT = 105
    BG_CYAN_BRIGHT = 106
    BG_WHITE_BRIGHT = 107

    @property
    def sequence(self) -> str:
        return f"\033[{self.value}m"


class SGRString(str):
    _sgr: tuple[SGRCodes, ...]
    _string: str
    _prefix: str
    _suffix: str
    __slots__ = ("_prefix", "_sgr", "_string", "_suffix")

    def __new__(
        cls,
        obj: object,
        *,
        prefix: str = "",
        suffix: str = "",
        params: Iterable[SGRCodes] = (),
    ) -> Self:
        string = super().__new__(cls, obj)
        params = tuple(params)
        object.__setattr__(string, "_prefix", prefix)
        object.__setattr__(string, "_string", str(obj))
        object.__setattr__(string, "_sgr", params)
        object.__setattr__(string, "_suffix", suffix)
        return string

    def __setattr__(self, name: str, value: object) -> None:
        msg = "SGRString is immutable"
        raise AttributeError(msg)

    def __delattr__(self, name: str) -> None:
        msg = "SGRString is immutable"
        raise AttributeError(msg)

    def __str__(self) -> str:
        sgr_prefix = "".join(code.sequence for code in self._sgr)
        sgr_suffix = SGRCodes.RESET.sequence if self._sgr else ""
        return f"{self._prefix}{sgr_prefix}{self._string}{sgr_suffix}{self._suffix}"

    def __len__(self) -> int:
        return len(self._prefix) + len(self._string) + len(self._suffix)

    def __mul__(self, other: object) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        return type(self)(
            self._string * other,
            prefix=self._prefix,
            suffix=self._suffix,
            params=self._sgr,
        )

    def __rmul__(self, other: object) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        return type(self)(
            self._string * other,
            prefix=self._prefix,
            suffix=self._suffix,
            params=self._sgr,
        )

    def print(
        self,
        end: str = "\n",
        *,
        force_prefix: bool = False,
        force_sgr: bool = False,
        is_error: bool = False,
    ) -> None:
        """Print the command output.

        The command will be printed to stdout if it's not the output of an error,
        otherwise to stderr.

        If the output stream isn't a tty, it will strip the SGR codes and the prefix,
        unless forced to keep them.
        """
        file = sys.stderr if is_error else sys.stdout
        if file.isatty():  # type: ignore[misc]
            prefix = self._prefix
            sgr_prefix = "".join(code.sequence for code in self._sgr)
            sgr_suffix = SGRCodes.RESET.sequence
            suffix = self._suffix
        else:
            prefix = ""
            sgr_prefix = ""
            sgr_suffix = ""
            suffix = ""
            if force_sgr or os.getenv("PY_UTIL_FORCE_SGR", "").lower() in TRUE_VAR:
                sgr_prefix = "".join(code.sequence for code in self._sgr)
                sgr_suffix = SGRCodes.RESET.sequence if self._sgr else ""
            if (
                force_prefix
                or os.getenv("PY_UTIL_FORCE_OUTFIX", "").lower() in TRUE_VAR
            ):
                prefix = self._prefix
                suffix = self._suffix

        print(
            prefix,
            sgr_prefix,
            self._string,
            sgr_suffix,
            suffix,
            sep="",
            end=end,
            file=file,
        )

    def header(
        self,
        *,
        padding: str = " ",
        left_spaces: int = 1,
        right_spaces: int = 1,
        space: str = " ",
        force_sgr: bool = False,
        is_error: bool = False,
    ) -> None:
        try:
            terminal_size = os.get_terminal_size()
        except OSError:
            # in pseudo-terminals an OSError is thrown
            self.print(force_prefix=True, force_sgr=force_sgr, is_error=is_error)
            return

        columns = terminal_size.columns
        title_length = left_spaces + len(self) + right_spaces
        if title_length >= columns:
            self.print(is_error=is_error)
            return

        half = (columns - title_length) / 2
        prefix = f"{padding * ceil(half)}{space * left_spaces}{self._prefix}"
        suffix = f"{self._suffix}{space * right_spaces}{padding * floor(half)}"
        type(self)(self._string, prefix=prefix, suffix=suffix, params=self._sgr).print()
