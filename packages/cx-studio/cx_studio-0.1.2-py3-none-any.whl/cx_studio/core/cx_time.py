from ctypes import ArgumentError
from numbers import Number
from typing import SupportsInt, Union
from .cx_timebase import Timebase
import re
from dataclasses import dataclass


@dataclass
class TimeParts:
    day: int = 0
    hour: int = 0
    minute: int = 0
    second: int = 0
    millisecond: int = 0

    def __str__(self):
        return f"{self.hour:02}:{self.minute:02}:{self.second:02}:{self.millisecond:03}"


class Time:
    SECOND_MS: int = 1000
    MINUTE_MS: int = SECOND_MS * 60
    HOUR_MS: int = MINUTE_MS * 60
    TC_PATTERN = re.compile(r"(\d\d):(\d\d):(\d\d)([:;,\.])(\d\d\d?)")

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

    def to_timeparts(self) -> TimeParts:
        ms = self._ms % 1000
        seconds = self._ms // 1000
        ss = seconds % 60
        minutes = seconds // 60
        mm = minutes % 60
        hours = minutes // 60
        hh = hours % 24
        dd = hours // 24
        return TimeParts(dd, hh, mm, ss, ms)

    def to_timestamp(self, sep=".") -> str:
        parts = self.to_timeparts()
        return f"{parts.hour:02}:{parts.minute:02}:{parts.second:02}{sep}{parts.millisecond:03}"

    def to_timecode(self, timebase: Union[Number, Timebase] = Timebase()) -> str:
        if isinstance(timebase, Number):
            int_fps = int(round(timebase))
            timebase = Timebase(int_fps, False if int_fps == int(timebase) else True)
        parts = self.to_timeparts()
        ff = round(parts.millisecond / timebase.milliseconds_per_frame)
        return f"{parts.hour:02}:{parts.minute:02}:{parts.second:02}{';' if timebase.drop_frame else ':'}{ff:02}"

    @classmethod
    def from_seconds(cls, seconds: float):
        ms = round(seconds * 1000)
        return cls(ms)

    @classmethod
    def from_timecode(cls, timecode: str, timebase: Union[Timebase, Number] = None):
        # 预处理时间码
        tc = timecode.strip()
        tc_match = cls.TC_PATTERN.fullmatch(tc)
        if tc_match is None:
            raise ArgumentError(f"Invalid timecode:{tc}")

        tc_groups = tc_match.groups()
        tc_sep = tc_groups[3]

        # 预处理时基
        tb = Timebase()
        if isinstance(timebase, Timebase):
            tb = timebase
        elif isinstance(timebase, Number):
            if timebase <= 0:
                raise ArgumentError(f"Invalid timebase:{timebase}")
            int_fps = int(round(timebase))
            if int_fps == int(timebase):
                tb = Timebase(int_fps, True if tc_sep == ";" else False)
            else:
                tb = Timebase(int_fps, True)

        # 解析时间码
        hh = int(tc_groups[0])
        mm = int(tc_groups[1])
        ss = int(tc_groups[2])
        ff = int(tc_groups[4])

        seconds = hh * 60 * 60 + mm * 60 + ss + ff / tb.frame_rate
        return cls.from_seconds(seconds)

    @classmethod
    def from_timestamp(cls, timestamp: str):
        # 预处理时间码
        ts = timestamp.strip()
        ts_match = cls.TC_PATTERN.fullmatch(ts)
        if ts_match is None:
            raise ArgumentError(f"Invalid timecode:{ts}")

        ts_groups = ts_match.groups()
        hh = int(ts_groups[0])
        mm = int(ts_groups[1])
        ss = int(ts_groups[2])
        ff = int(ts_groups[4])

        ms = (hh * 60 * 60 + mm * 60 + ss) * 1000 + ff
        return cls(ms)
