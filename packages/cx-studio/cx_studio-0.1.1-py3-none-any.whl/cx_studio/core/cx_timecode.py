import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Union

from .cx_time import Time
from .cx_timebase import Timebase


class TCMode(StrEnum):
    Code = "timecode"
    Stamp = "timestamp"


TC_PATTERN = re.compile(r"(\d\d):(\d\d):(\d\d)([:;,\.])(\d\d\d?)")


@dataclass
class TimeCodeInfo:
    hh: int = 0
    mm: int = 0
    ss: int = 0
    ff: int = 0
    mode: TCMode = TCMode.Code
    timebase: Timebase = None

    @staticmethod
    def is_tc(s: str) -> bool:
        s = str(s)
        return TC_PATTERN.fullmatch(s) is not None

    @classmethod
    def from_timecode(cls, tc: str):
        if not isinstance(tc, str):
            raise TypeError("TimeCodeInfo can only parse timecode from str.")
        match = TC_PATTERN.fullmatch(tc.strip())
        if match is None:
            return TimeCodeInfo()
        groups = match.groups()
        sep = groups[3]
        parts = [int(groups[x]) for x in [0, 1, 2, 4]]
        is_frame = len(groups[4]) == 2
        return TimeCodeInfo(
            hh=parts[0],
            mm=parts[1],
            ss=parts[2],
            ff=parts[3],
            timebase=Timebase(frame_rate=-1, drop_frame=sep == ";"),
            mode=TCMode.Code if is_frame else TCMode.Stamp,
        )

    @classmethod
    def from_time(
            cls, t: Time, tc_mode: TCMode = TCMode.Code,
            timebase: Timebase = None
    ):
        if not isinstance(t, Time):
            raise TypeError("TimeCodeInfo can only handle time by Time type.")
        millisecond = t.milliseconds
        seconds = millisecond // 1000
        ss = seconds % 60
        minutes = seconds // 60
        mm = minutes % 60
        hours = minutes // 60
        hh = hours % 24
        fff = millisecond % 1000
        if tc_mode is TCMode.TC:
            if timebase is None:
                timebase = Timebase(24, False)
            rate = timebase.fps
            fff = int((millisecond / 1000) * rate) % rate
        return TimeCodeInfo(
            hh=hh, mm=mm, ss=ss, ff=fff, mode=tc_mode, timebase=timebase
        )

    @property
    def milliseconds(self) -> int:
        fff = self.ff
        if self.mode is TCMode.Code:
            rate = 24 if self.timebase is None else self.timebase.frame_rate
            fff = self.ff / rate * 1000
        return int(
            round(
                self.hh * 60 * 60 * 1000 + self.mm * 60 * 1000 + self.ss * 1000 + fff)
        )

    @property
    def segments(self):
        return tuple(self.hh, self.mm, self.ss, self.ff)


class TimeCode:
    __STR_TEMPLATE = {
        TCMode.Code: "{0[0]:0>2}{sep}{0[1]:0>2}{sep}{0[2]:0>2}{sep1}{0[3]:0>2}",
        TCMode.Stamp: "{0[0]:0>2}{sep}{0[1]:0>2}{sep}{0[2]:0>2}{sep1}{0[3]:0>3}",
    }

    __DEF_SEP = {
        TCMode.Code: ":;",
        TCMode.Stamp: ".,",
    }

    def __init__(
            self,
            input_data: Union[Time | int | float | str | TimeCodeInfo],
            tc_mode: TCMode = TCMode.Code,
            timebase: Timebase = None,
            custom_seps: str = None,
    ) -> None:
        """初始化时间码对象

        Args:
            input_time (Union[Time  |  int  |  float  |  str]): 支持多种格式的自动识别
            timebase (Timebase, optional): 指定时基，如果为Stamp模式则不需要. Defaults to None.
            tc_mode (TCMode, optional): 时间码模式，是帧数模式还是毫秒模式. Defaults to TCMode.Code.
            custom_seps (str, optional): 应该提供字符串，其中的第一个字符用作普通的分隔符，
            第二个字符（如果有的话）用作丢帧的分隔符. Defaults to None.
        """
        if isinstance(input_data, TimeCodeInfo):
            self._time = Time(input_data.milliseconds)
            self._mode = input_data.mode
            self._timebase = input_data.timebase
        if isinstance(input_data, str) and TimeCodeInfo.is_tc(input_data):
            info = TimeCodeInfo.from_timecode(input_data)
            self._time = Time(info.milliseconds)
        elif isinstance(input_data, Time):
            self._time = input_data
        elif isinstance(input_data, int | float):
            self._time = Time(input_data)
        else:
            self._time = Time()

        self._timebase = timebase if timebase is not None else None
        self._mode = tc_mode
        self._custom_seps = str(
            custom_seps) if custom_seps is not None else None

    @property
    def seps(self) -> str:
        if self._custom_seps:
            return self._custom_seps
        return self.__DEF_SEP[self._mode]

    @property
    def time(self) -> Time:
        return self._time

    def render(self) -> str:
        info = TimeCodeInfo.from_time(self._time, self._mode, self._timebase)
        seps = self.seps
        sep = seps[0]
        sep1 = sep
        if self._timebase.drop_frame and len(seps) > 1:
            sep1 = seps[1]

        return self.__STR_TEMPLATE[self._mode].format(
            info.segements, sep=sep, sep1=sep1
        )

    def __str__(self):
        return self.render()

    def __repr__(self):
        return "TimeCode{0}{1}".format(
            self._time, "DF" if self._timebase.drop_frame else ""
        )
