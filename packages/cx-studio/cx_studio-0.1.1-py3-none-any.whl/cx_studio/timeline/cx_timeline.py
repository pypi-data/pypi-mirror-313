from .cx_track import Track
from ..core import DataPackage, Time, TimeRangeSupport


class Timeline(TimeRangeSupport):
    def __init__(self) -> None:
        super().__init__()
        self._tracks: list[Track] = [Track()]
        self._data = DataPackage()

    @property
    def data(self):
        return self._data

    @property
    def tracks(self):
        return self._tracks

    @property
    def start(self):
        return Time(0)

    @property
    def duration(self):
        return max(t.duration for t in self._tracks)
