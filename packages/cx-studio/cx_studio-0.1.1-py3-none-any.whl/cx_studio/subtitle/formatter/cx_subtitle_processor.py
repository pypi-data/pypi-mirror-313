from abc import ABC, abstractmethod
from typing import Union

from ..cx_subtitle import StaticSubtitle


class SubtitleProcessor(ABC):

    @abstractmethod
    def __call__(self,
                 subtitle: StaticSubtitle) -> Union[StaticSubtitle | None]:
        return subtitle
