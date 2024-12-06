from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from plum import dispatch
from whenever import Time

from whenever_time_period.abstract import AbstractTimePeriod


@dataclass
class LinearTimePeriod(AbstractTimePeriod):
    """A LinearTimePeriod is a right-open clock interval of whenever.Time objects,
    [start_time, end_time) wherein start_time < end_time.

    Example:
    >> LinearTimePeriod(start_time=Time(5), end_time=Time(10))
    """

    def __post_init__(self):
        if not self.start_time < self.end_time:
            raise ValueError

    def __contains__(self, other: Time) -> bool:
        return self.start_time <= other < self.end_time

    @dispatch
    def __and__(self, other: LinearTimePeriod) -> Optional[LinearTimePeriod]:
        start_inter = max(self.start_time, other.start_time)
        end_inter = min(self.end_time, other.end_time)

        if start_inter < end_inter:
            return LinearTimePeriod(start_inter, end_inter)

        return None

    @dispatch
    def __and__(  # noqa F811
        self, other: ModularTimePeriod
    ) -> list[LinearTimePeriod] | LinearTimePeriod | None:
        intr = []

        # region 1
        if max(self.start_time, other.start_time) < self.end_time:
            intr.append(
                LinearTimePeriod(max(self.start_time, other.start_time), self.end_time)
            )

        # region 2
        if self.start_time < min(self.end_time, other.end_time):
            intr.append(
                LinearTimePeriod(self.start_time, min(self.end_time, other.end_time))
            )

        if len(intr) > 1:
            return sorted(intr)
        elif len(intr) > 0:
            return intr[0]
        return None

    @dispatch
    def __and__(self, other: InfiniteTimePeriod) -> LinearTimePeriod:  # noqa F811
        return self

    def __repr__(self) -> str:
        return super().__repr__()


@dataclass
class ModularTimePeriod(AbstractTimePeriod):
    """A ModularTimePeriod is a right-open clock interval of whenever.Time objects,
    [start_time, end_time) wherein end_time < start_time. Used for intervals which wrap
    around midnight.

    Example:
    >> ModularTimePeriod(start_time=Time(10), end_time=Time(5))
    """

    def __post_init__(self):
        if not self.end_time < self.start_time:
            raise ValueError

    def __contains__(self, other: Time) -> bool:
        return self.start_time <= other or other < self.end_time

    @dispatch
    def __and__(
        self, other: LinearTimePeriod
    ) -> list[LinearTimePeriod] | LinearTimePeriod | None:
        return LinearTimePeriod.__and__(other, self)

    @dispatch
    def __and__(self, other: ModularTimePeriod) -> Optional[ModularTimePeriod]:  # noqa F811
        start_inter = max(self.start_time, other.start_time)
        end_inter = min(self.end_time, other.end_time)
        if start_inter >= end_inter:
            return ModularTimePeriod(start_inter, end_inter)
        return None

    @dispatch
    def __and__(self, other: InfiniteTimePeriod) -> ModularTimePeriod:  # noqa F811
        return self

    def __repr__(self) -> str:
        return super().__repr__()


@dataclass
class InfiniteTimePeriod(AbstractTimePeriod):
    """An InfiniteTimePeriod is a right-open clock interval of whenever.Time objects,
    [start_time, end_time) wherein start_time == end_time. Used to represent intervals
    which span all possible clock times to nanosecond precision."""

    def __post_init__(self):
        if not self.start_time == self.end_time:
            raise ValueError

    def __contains__(self, other: Time) -> bool:
        if not isinstance(other, Time):
            return False
        return True

    def __eq__(self, value: object) -> bool:
        if isinstance(value, InfiniteTimePeriod):
            return True
        return False

    @dispatch
    def __and__(self, other: LinearTimePeriod) -> LinearTimePeriod:
        return other

    @dispatch
    def __and__(self, other: ModularTimePeriod) -> ModularTimePeriod:  # noqa F811
        return other

    @dispatch
    def __and__(self, other: InfiniteTimePeriod) -> InfiniteTimePeriod:  # noqa F811
        return other

    def __repr__(self) -> str:
        return super().__repr__()
