from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from plum import dispatch
from whenever import Time


@dataclass
class AbstractTimePeriod(ABC):
    """A TimePeriod is an abstract right-open clock interval of whenever.Time objects,
    [start_time, end_time). There is no restriction on the relationship between start_time
    and end_time."""

    start_time: Time
    end_time: Time

    @abstractmethod
    def __contains__(self, other: AbstractTimePeriod) -> bool: ...

    @abstractmethod
    def __and__(self, other: AbstractTimePeriod) -> AbstractTimePeriod | None: ...

    # The sorted ordering of Sequence[AbstractTimePeriod] is
    # arbitrarily defined by the value of the start_time relative
    # to the value being compared (or it's start time)
    @dispatch
    def __lt__(self, other: Time) -> bool:
        return self.start_time < other

    @dispatch
    def __lt__(self, other: AbstractTimePeriod) -> bool:  # noqa: F811
        return self.start_time < other.start_time

    @dispatch
    def __gt__(self, other: Time) -> bool:
        return self.start_time > other

    @dispatch
    def __gt__(self, other: AbstractTimePeriod) -> bool:  # noqa: F811
        return self.start_time > other.start_time

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.start_time}, {self.end_time})"
