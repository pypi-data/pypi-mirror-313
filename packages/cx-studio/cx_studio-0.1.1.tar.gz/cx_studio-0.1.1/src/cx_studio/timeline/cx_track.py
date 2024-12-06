from ..core import DataPackage, Time, TimeRangeSupport


class Track(TimeRangeSupport):
    def __init__(self) -> None:
        super().__init__()
        self._items: list[TimeRangeSupport] = []
        self._data = DataPackage()

    @property
    def start(self) -> Time:
        return Time(0)

    @property
    def duration(self) -> Time:
        if len(self.items) == 0:
            return Time(0)
        else:
            return self._items[-1].end

    @property
    def items(self) -> list[TimeRangeSupport]:
        return self._items

    @property
    def data(self):
        return self._data

    def __getitem__(self, item):
        assert isinstance(item, int)
        return self._items[item]

    def __setitem__(self, key, value):
        assert isinstance(key, int)
        assert isinstance(value, TimeRangeSupport)
        self._items[key] = value

    def __delitem__(self, key):
        assert isinstance(key, int)
        del self._items[key]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return self._items.__iter__()

    def find_insert_point(self, item):
        if len(self._items) == 0:
            return 0

        start_time = item.start if isinstance(item, TimeRangeSupport) else Time(
            item)
        for i in range(0, len(self._items)):
            if self._items[i].start > start_time:
                return i
        return len(self._items)

    def available_for(self, item: TimeRangeSupport):
        assert isinstance(item, TimeRangeSupport)
        for x in self._items:
            if x.intersects(item):
                return False
        return True

    def sort(self):
        self._items.sort(key=lambda x: x.start)
