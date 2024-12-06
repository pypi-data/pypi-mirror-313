from dataclasses import dataclass


@dataclass(frozen=True)
class Timebase:
    frame_rate: int = 24
    drop_frame: bool = False

    @property
    def milliseconds_per_frame(self) -> int:
        return round(1.0 / float(self.frame_rate) * 1000)

    def is_valid(self) -> bool:
        if self.frame_rate <= 0:
            return False
        return True
