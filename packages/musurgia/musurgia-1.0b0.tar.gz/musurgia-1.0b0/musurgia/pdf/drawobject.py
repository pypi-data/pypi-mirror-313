from abc import ABC, abstractmethod
from math import ceil
from typing import Optional, Protocol, Any

from musurgia.musurgia_exceptions import PdfAttributeError, RelativePositionNotSettableError, MarginNotSettableError
from musurgia.musurgia_types import create_error_message, check_type, MusurgiaTypeError, PositionType, MarginType
from musurgia.pdf.margined import AbstractMargined, Margined
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.positioned import AbstractPositioned, Positioned

__all__ = ['ClippingArea']


class HasGetHeightProtocol(Protocol):
    def get_height(self) -> float: ...


class HasShowProtocol(Protocol):
    @property
    def show(self) -> bool: ...


class DrawObject(AbstractPositioned, AbstractMargined, ABC):
    def __init__(self, show: bool = True, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._show: bool
        self.show = show
        self._clipping_area = ClippingArea(pdf=None, draw_object=self)

    def get_clipping_area(self) -> 'ClippingArea':
        return self._clipping_area

    @property
    def show(self) -> bool:
        return self._show

    @show.setter
    def show(self, val: bool) -> None:
        check_type(val, bool, class_name=self.__class__.__name__, property_name='show')
        self._show = val

    @abstractmethod
    def get_relative_x2(self) -> float:
        """ this property is needed to get relative_x2 """

    @abstractmethod
    def get_relative_y2(self) -> float:
        """ this property is needed to get relative_y2 """

    def get_end_positions(self) -> tuple[float, float]:
        return self.get_relative_x2(), self.get_relative_y2()

    def get_height(self) -> float:
        return self.top_margin + self.get_relative_y2() - self.relative_y + self.bottom_margin

    def get_width(self) -> float:
        return self.left_margin + self.get_relative_x2() - self.relative_x + self.right_margin

    @abstractmethod
    def draw(self, pdf: Pdf) -> None:
        """ this property is needed draw the DrawObject to pdf """

    def clipped_draw(self, pdf: Pdf) -> None:
        self.get_clipping_area().pdf = pdf
        self.get_clipping_area().draw()


class Master(ABC):
    @abstractmethod
    def get_slave_position(self, slave: Any, position: PositionType) -> float:
        """get_slave_position must be provided"""

    @abstractmethod
    def get_slave_margin(self, slave: Any, margin: MarginType) -> float:
        """get_slave_margin must be provided"""


class HasMasterProtocol(Protocol):
    @property
    def master(self) -> Optional['Master']: ...


class PositionedSlave(AbstractPositioned, HasMasterProtocol):
    @property
    def relative_x(self) -> float:
        if not self.master:
            raise AttributeError(create_error_message(message='set master first', class_name=self.__class__.__name__,
                                                      property_name='relative_x'))
        return self.master.get_slave_position(slave=self, position='x')

    @relative_x.setter
    def relative_x(self, val: Optional[float]) -> None:
        if val is not None:
            raise RelativePositionNotSettableError()

    @property
    def relative_y(self) -> float:
        if not self.master:
            raise AttributeError(create_error_message(message='set master first', class_name=self.__class__.__name__,
                                                      property_name='relative_y'))
        return self.master.get_slave_position(slave=self, position='y')

    @relative_y.setter
    def relative_y(self, val: Optional[float]) -> None:
        if val is not None:
            raise RelativePositionNotSettableError()


class MarginedSlave(AbstractMargined, HasMasterProtocol):
    @property
    def left_margin(self) -> float:
        if not self.master:
            raise AttributeError(create_error_message(message='set master first', class_name=self.__class__.__name__,
                                                      property_name='left_margin'))
        return self.master.get_slave_margin(slave=self, margin='left')

    @left_margin.setter
    def left_margin(self, val: Optional[float]) -> None:
        if val is not None:
            raise MarginNotSettableError()

    @property
    def top_margin(self) -> float:
        if not self.master:
            raise AttributeError(create_error_message(message='set master first', class_name=self.__class__.__name__,
                                                      property_name='top_margin'))
        return self.master.get_slave_margin(slave=self, margin='top')

    @top_margin.setter
    def top_margin(self, val: Optional[float]) -> None:
        if val is not None:
            raise MarginNotSettableError()

    @property
    def right_margin(self) -> float:
        if not self.master:
            raise AttributeError(create_error_message(message='set master first', class_name=self.__class__.__name__,
                                                      property_name='right_margin'))
        return self.master.get_slave_margin(slave=self, margin='right')

    @right_margin.setter
    def right_margin(self, val: Optional[float]) -> None:
        if val is not None:
            raise MarginNotSettableError()

    @property
    def bottom_margin(self) -> float:
        if not self.master:
            raise AttributeError(create_error_message(message='set master first', class_name=self.__class__.__name__,
                                                      property_name='bottom_margin'))
        return self.master.get_slave_margin(slave=self, margin='bottom')

    @bottom_margin.setter
    def bottom_margin(self, val: Optional[float]) -> None:
        if val is not None:
            raise MarginNotSettableError()


class MasterDrawObject(Master, DrawObject, Positioned, Margined, ABC):
    pass


class SlaveDrawObject(DrawObject, PositionedSlave, MarginedSlave, ABC):
    def __init__(self, master: Optional[MasterDrawObject] = None, simple_name: Optional[str] = None, *args: Any,
                 **kwargs: Any):
        self._master: Optional[MasterDrawObject]
        self.master = master
        super().__init__(*args, **kwargs)

        self._simple_name: Optional[str]
        self.simple_name = simple_name

    @property
    def master(self) -> Optional[MasterDrawObject]:
        return self._master

    @master.setter
    def master(self, val: Optional[MasterDrawObject]) -> None:
        if val is not None and not isinstance(val, MasterDrawObject):
            raise MusurgiaTypeError(message=f"master.value must be of type {MasterDrawObject} not {type(val)}",
                                    class_name=self.__class__.__name__, property_name='master')
        self._master = val


class ClippingArea:
    def __init__(self, pdf: Optional[Pdf], draw_object: DrawObject, left_margin: float = 0, right_margin: float = 0,
                 top_margin: float = 0):
        self.pdf: Optional[Pdf] = pdf
        self.draw_object: DrawObject = draw_object
        self.left_margin: float = left_margin
        self.right_margin: float = right_margin
        self.top_margin: float = top_margin

    # private methods
    def _add_page(self) -> None:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('_add_page'))  # pragma: no cover
        self.pdf.add_page()
        self._prepare_page()

    def _get_pdf_not_exists_message(self, method_name: str) -> str:
        return create_error_message(message='pdf must be set first', class_name=self.__class__.__name__,
                                    method_name=method_name)

    def _draw_with_clip(self, index: int) -> None:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('_draw_with_clip'))  # pragma: no cover
        with self.pdf.saved_state():
            self.pdf.clip_rect(-1, -5, self.get_row_width() + 1.14, self.get_row_height())
            self.pdf.translate(index * -self.get_row_width(), 0)
            self.draw_object.draw(self.pdf)

    def _prepare_page(self) -> None:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('_prepare_page'))  # pragma: no cover
        self.pdf.translate_page_margins()
        self.pdf.translate(self.left_margin, self.top_margin)

    # public methods
    def draw(self) -> None:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('draw'))
        self.pdf.translate(self.left_margin, self.top_margin)
        for index in range(self.get_number_of_rows()):
            if index != 0:
                self.pdf.translate(0, self.draw_object.get_height())
            if self.pdf.absolute_y > self.pdf.h - self.pdf.b_margin:
                self._add_page()
            self._draw_with_clip(index)

    def get_number_of_rows(self) -> int:
        return int(ceil(self.draw_object.get_width() / self.get_row_width()))

    def get_row_height(self) -> float:
        return self.draw_object.get_height()

    def get_row_width(self) -> float:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('get_row_width'))
        return self.pdf.w - self.pdf.l_margin - self.pdf.r_margin - self.left_margin - self.right_margin
