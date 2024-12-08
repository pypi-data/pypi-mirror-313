from abc import abstractmethod, ABC
from typing import Optional, Protocol, Any

from musurgia.musurgia_types import ConvertibleToFloat, check_type, MarginType

__all__ = []  # type: ignore


class HasMarginsProtocol(Protocol):
    @property
    def left_margin(self) -> float: ...

    @property
    def top_margin(self) -> float: ...

    @property
    def right_margin(self) -> float: ...

    @property
    def bottom_margin(self) -> float: ...


class AbstractMargined(ABC):
    """
    An interface for setting and getting DrawObject's margin attributes.
    """

    def __init__(self, top_margin: Optional[ConvertibleToFloat] = None,
                 bottom_margin: Optional[ConvertibleToFloat] = None, left_margin: Optional[ConvertibleToFloat] = None,
                 right_margin: Optional[ConvertibleToFloat] = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._top_margin: float = 0
        self._left_margin: float = 0
        self._bottom_margin: float = 0
        self._right_margin: float = 0

        self.top_margin = top_margin  # type: ignore
        self.left_margin = left_margin  # type: ignore
        self.bottom_margin = bottom_margin  # type: ignore
        self.right_margin = right_margin  # type: ignore

    @property
    @abstractmethod
    def bottom_margin(self) -> float:
        """bottom_margin getter must be provided"""

    @bottom_margin.setter
    @abstractmethod
    def bottom_margin(self, val: Optional[ConvertibleToFloat]) -> None:
        """bottom_margin setter must be provided"""

    @property
    @abstractmethod
    def left_margin(self) -> float:
        """left_margin getter must be provided"""

    @left_margin.setter
    @abstractmethod
    def left_margin(self, val: Optional[ConvertibleToFloat]) -> None:
        """left_margin setter must be provided"""

    @property
    @abstractmethod
    def top_margin(self) -> float:
        """top_margin getter must be provided"""

    @top_margin.setter
    @abstractmethod
    def top_margin(self, val: Optional[ConvertibleToFloat]) -> None:
        """top_margin setter must be provided"""

    @property
    @abstractmethod
    def right_margin(self) -> float:
        """right_margin getter must be provided"""

    @right_margin.setter
    @abstractmethod
    def right_margin(self, val: Optional[ConvertibleToFloat]) -> None:
        """right_margin setter must be provided"""

    def get_margins(self) -> dict[MarginType, float]:
        return {'top': self.top_margin, 'right': self.right_margin, 'bottom': self.bottom_margin,
                'left': self.left_margin}

    @property
    def margins(self) -> tuple[float, float, float, float]:
        return self.top_margin, self.right_margin, self.bottom_margin, self.left_margin

    @margins.setter
    def margins(self, value: tuple[float, float, float, float]) -> None:
        self.top_margin, self.right_margin, self.bottom_margin, self.left_margin = value


class Margined(AbstractMargined):
    """
        An interface for setting and getting DrawObject's margin attributes.
        """

    def __init__(self, top_margin: ConvertibleToFloat = 0,
                 bottom_margin: ConvertibleToFloat = 0, left_margin: ConvertibleToFloat = 0,
                 right_margin: ConvertibleToFloat = 0, *args: Any, **kwargs: Any):
        super().__init__(top_margin=top_margin, bottom_margin=bottom_margin, left_margin=left_margin,
                         right_margin=right_margin, *args, **kwargs)  # type: ignore

    @property
    def bottom_margin(self) -> float:
        return self._bottom_margin

    @bottom_margin.setter
    def bottom_margin(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='bottom_margin')
        self._bottom_margin = float(val)

    @property
    def left_margin(self) -> float:
        return self._left_margin

    @left_margin.setter
    def left_margin(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='left_margin')
        self._left_margin = float(val)

    @property
    def top_margin(self) -> float:
        return self._top_margin

    @top_margin.setter
    def top_margin(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='top_margin')
        self._top_margin = float(val)

    @property
    def right_margin(self) -> float:
        return self._right_margin

    @right_margin.setter
    def right_margin(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='right_margin')
        self._right_margin = float(val)
