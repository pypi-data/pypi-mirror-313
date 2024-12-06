import dataclasses
from numbers import Number
from typing import Union

from cx_studio.core import Time, Timebase
from .cx_subtitle_processor import SubtitleProcessor
from ..cx_subtitle import StaticSubtitle


class SubtitleFrameRateShifter(SubtitleProcessor):
    def __init__(self, from_rate: Union[Number, Timebase],
                 to_rate: Union[Number,
                 Timebase]):
        super().__init__()
        self._from_rate = self.__unpack_rate(from_rate)
        self._to_rate = self.__unpack_rate(to_rate)

    @staticmethod
    def __unpack_rate(rate: Union[Number, Timebase]) -> Timebase:
        if isinstance(rate, Number):
            return Timebase(int(rate))
        if isinstance(rate, Timebase):
            return rate
        raise NotImplementedError('Unsupported frame rate format')

    def transform_time_with_fixed_frames(self, time: Time) -> Time:
        frames = int(round(time.milliseconds /
                           self._from_rate.milliseconds_per_frame))
        new_milliseconds = frames * self._to_rate.milliseconds_per_frame
        return Time(new_milliseconds)

    def __call__(self, subtitle: StaticSubtitle):
        start = self.transform_time_with_fixed_frames(subtitle.start)
        end = self.transform_time_with_fixed_frames(subtitle.end)
        return dataclasses.replace(subtitle, start=start, end=end)
