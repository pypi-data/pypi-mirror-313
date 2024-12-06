from abc import ABC, abstractmethod

from .cx_time import Time


class TimeRangeSupport(ABC):
    @property
    @abstractmethod
    def start(self) -> Time:
        pass

    @property
    @abstractmethod
    def duration(self) -> Time:
        pass

    @property
    def end(self) -> Time:
        return self.start + self.duration

    def intersects(self, other) -> bool:
        assert isinstance(other, TimeRangeSupport)
        return self.start <= other.end and self.end >= other.start

    def contains_time(self, time: Time) -> bool:
        assert isinstance(time, Time)
        return self.start <= time <= self.end
