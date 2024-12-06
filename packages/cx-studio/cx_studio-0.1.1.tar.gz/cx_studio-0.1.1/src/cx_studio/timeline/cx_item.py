from typing import Union

from ..core import DataPackage, Time, TimeRangeSupport


class Item(TimeRangeSupport):
    def __init__(self, start: Union[int, Time] = Time(),
                 duration: Union[Time, int] = Time()) -> None:
        super().__init__()
        self._start = Time(start)
        self._duration = Time(duration)
        self._data = DataPackage()

    @classmethod
    def from_time_range(cls, time_range: TimeRangeSupport):
        assert isinstance(time_range, TimeRangeSupport)
        return cls(time_range.start, time_range.duration)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        value = Time(value)
        self._start = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        value = Time(value)
        self._duration = value

    @property
    def end(self):
        return self.start + self.duration

    @end.setter
    def end(self, value):
        value = Time(value)
        self.duration = value - self.start

    @property
    def data(self):
        return self._data
