from numbers import Number
from typing import SupportsInt


class Time:
    SECOND_MS: int = 1000
    MINUTE_MS: int = SECOND_MS * 60
    HOUR_MS: int = MINUTE_MS * 60

    def __init__(self, milliseconds=0) -> None:
        if not isinstance(milliseconds, Number | Time):
            raise NotImplemented("Input is not a acceptable number.")

        self._ms: int = int(milliseconds)

    @property
    def milliseconds(self) -> int:
        return self._ms

    @property
    def seconds(self) -> float:
        return self._ms / self.SECOND_MS

    @property
    def hours(self) -> float:
        return self._ms / self.HOUR_MS

    @property
    def minutes(self) -> float:
        return self._ms / self.MINUTE_MS

    def __eq__(self, other):
        if isinstance(other, Time):
            return self._ms == other._ms
        elif isinstance(other, SupportsInt):
            return self._ms == int(other)
        else:
            raise NotImplemented("Comparing type not supported.")

    def __hash__(self) -> int:
        return hash(f"CXTIME:{self._ms}")

    def __lt__(self, other):
        if isinstance(other, Time):
            return self._ms < other._ms
        elif isinstance(other, SupportsInt):
            return self._ms < int(other)
        else:
            raise NotImplemented("Comparing type not supported.")

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __add__(self, other):
        if isinstance(other, Time):
            return Time(self._ms + other._ms)
        elif isinstance(other, SupportsInt):
            return Time(self._ms + int(other))
        else:
            raise NotImplemented()

    def __sub__(self, other):
        if isinstance(other, Time):
            return Time(self._ms - other._ms)
        elif isinstance(other, SupportsInt):
            return Time(self._ms - int(other))
        else:
            raise NotImplemented()

    def __mul__(self, other):
        if isinstance(other, SupportsInt):
            return Time(self._ms * int(other))
        else:
            raise NotImplemented()

    def __truediv__(self, other):
        if isinstance(other, SupportsInt):
            return Time(round(self._ms / int(other)))
        else:
            raise NotImplemented()

    def __repr__(self):
        return f"CXTime[{self._ms}]"

    def __int__(self):
        return self._ms
