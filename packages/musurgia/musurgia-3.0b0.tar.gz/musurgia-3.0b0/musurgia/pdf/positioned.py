from abc import abstractmethod, ABC
from typing import Optional, Protocol, Any

from musurgia.musurgia_types import ConvertibleToFloat, check_type

__all__ = []  # type: ignore


class HasPositionsProtocol(Protocol):
    @property
    def relative_x(self) -> float: ...

    @property
    def relative_y(self) -> float: ...

    def get_relative_x2(self) -> float: ...

    def get_relative_y2(self) -> float: ...


class AbstractPositioned(ABC):
    """
    An interface for setting and getting DrawObject's position attributes.
    """

    def __init__(self, relative_x: Optional[ConvertibleToFloat] = None, relative_y: Optional[ConvertibleToFloat] = None,
                 *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._relative_x: float = 0
        self._relative_y: float = 0
        self.relative_x = relative_x  # type: ignore
        self.relative_y = relative_y  # type: ignore

    @property
    @abstractmethod
    def relative_x(self) -> float:
        """relative_x getter must be provided"""

    @relative_x.setter
    @abstractmethod
    def relative_x(self, val: Optional[ConvertibleToFloat]) -> None:
        """relative_x setter must be provided"""

    @property
    @abstractmethod
    def relative_y(self) -> float:
        """relative_y getter must be provided"""

    @relative_y.setter
    @abstractmethod
    def relative_y(self, val: Optional[ConvertibleToFloat]) -> None:
        """relative_y setter must be provided"""

    def get_positions(self) -> dict[str, float]:
        return {'x': self.relative_x, 'y': self.relative_y}

    @property
    def positions(self) -> tuple[float, float]:
        return self.relative_x, self.relative_y

    @positions.setter
    def positions(self, val: tuple[float, float]) -> None:
        self.relative_x, self.relative_y = val


class Positioned(AbstractPositioned):
    def __init__(self, relative_x: ConvertibleToFloat = 0, relative_y: ConvertibleToFloat = 0, *args: Any,
                 **kwargs: Any):
        super().__init__(relative_x=relative_x, relative_y=relative_y, *args, **kwargs)  # type: ignore

    @property
    def relative_x(self) -> float:
        return self._relative_x

    @relative_x.setter
    def relative_x(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='relative_x')
        self._relative_x = float(val)

    @property
    def relative_y(self) -> float:
        return self._relative_y

    @relative_y.setter
    def relative_y(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='relative_y')
        self._relative_y = float(val)
