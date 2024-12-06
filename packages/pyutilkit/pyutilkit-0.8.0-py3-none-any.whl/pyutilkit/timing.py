from __future__ import annotations  # py3.9: remove this line

from dataclasses import dataclass
from time import perf_counter_ns
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self  # py3.10: import Self from typing

METRIC_MULTIPLIER = 1000
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY


@dataclass(frozen=True, order=True)
class Timing:
    __slots__ = ("nanoseconds",)  # py3.9: remove this line

    nanoseconds: int

    def __init__(
        self,
        *,
        days: int = 0,
        seconds: int = 0,
        milliseconds: int = 0,
        microseconds: int = 0,
        nanoseconds: int = 0,
    ) -> None:
        total_nanoseconds = (
            nanoseconds
            + METRIC_MULTIPLIER * microseconds
            + METRIC_MULTIPLIER**2 * milliseconds
            + METRIC_MULTIPLIER**3 * seconds
            + SECONDS_PER_DAY * METRIC_MULTIPLIER**3 * days
        )
        object.__setattr__(self, "nanoseconds", total_nanoseconds)

    def __str__(self) -> str:
        if self.nanoseconds < METRIC_MULTIPLIER:
            return f"{self.nanoseconds}ns"
        microseconds = self.nanoseconds / METRIC_MULTIPLIER
        if microseconds < METRIC_MULTIPLIER:
            return f"{microseconds:.1f}µs"
        milliseconds = microseconds / METRIC_MULTIPLIER
        if milliseconds < METRIC_MULTIPLIER:
            return f"{milliseconds:.1f}ms"
        seconds = milliseconds / METRIC_MULTIPLIER
        if seconds < SECONDS_PER_MINUTE:
            return f"{seconds:.2f}s"
        round_seconds = int(seconds)
        minutes, seconds = divmod(round_seconds, SECONDS_PER_MINUTE)
        hours, minutes = divmod(minutes, MINUTES_PER_HOUR)
        if hours < HOURS_PER_DAY:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        days, hours = divmod(hours, HOURS_PER_DAY)
        return f"{days:,}d {hours:02d}:{minutes:02d}:{seconds:02d}"

    def __bool__(self) -> bool:
        return bool(self.nanoseconds)

    def __add__(self, other: object) -> Timing:
        if not isinstance(other, Timing):
            return NotImplemented
        return Timing(nanoseconds=self.nanoseconds + other.nanoseconds)

    def __radd__(self, other: object) -> Timing:
        if not isinstance(other, Timing):
            return NotImplemented
        return Timing(nanoseconds=self.nanoseconds + other.nanoseconds)

    def __mul__(self, other: object) -> Timing:
        if not isinstance(other, int):
            return NotImplemented
        return Timing(nanoseconds=self.nanoseconds * other)

    def __rmul__(self, other: object) -> Timing:
        if not isinstance(other, int):
            return NotImplemented
        return Timing(nanoseconds=self.nanoseconds * other)

    def __floordiv__(self, other: object) -> Timing:
        if not isinstance(other, int):
            return NotImplemented
        return Timing(nanoseconds=self.nanoseconds // other)

    def __truediv__(self, other: object) -> Timing:
        if not isinstance(other, int):
            return NotImplemented
        return Timing(nanoseconds=self.nanoseconds // other)


class Stopwatch:
    _start: int
    laps: list[Timing]

    def __init__(self) -> None:
        self._start = 0
        self.laps: list[Timing] = []

    def __enter__(self) -> Self:
        self._start = perf_counter_ns()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        _end = perf_counter_ns()
        self.laps.append(Timing(nanoseconds=_end - self._start))

    def __bool__(self) -> bool:
        return bool(self.elapsed)

    @property
    def elapsed(self) -> Timing:
        return sum(self.laps, Timing())

    @property
    def average(self) -> Timing:
        if not self.laps:
            msg = "No laps recorded"
            raise ZeroDivisionError(msg)
        return self.elapsed // len(self.laps)
