from abc import ABC
from typing import Optional, Any, Literal

from musurgia.musurgia_exceptions import RelativePositionNotSettableError
from musurgia.musurgia_types import check_type, FontStyle, FontFamily, FontWeight, ConvertibleToFloat, \
    VerticalPosition, HorizontalPosition, create_error_message
from musurgia.pdf.drawobject import DrawObject
from musurgia.pdf.font import Font
from musurgia.pdf.margined import Margined
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdfunit import PdfUnit
from musurgia.pdf.positioned import Positioned

__all__ = ['Text', 'PageText']


class AbstractText(DrawObject, ABC):
    DEFAULT_FONT_FAMILY: FontFamily = 'Courier'
    DEFAULT_FONT_SIZE: int = 10
    DEFAULT_FONT_WEIGHT: FontWeight = 'medium'
    DEFAULT_FONT_STYLE: FontStyle = 'regular'

    def __init__(self, value: Any, font_family: FontFamily = DEFAULT_FONT_FAMILY,
                 font_weight: FontWeight = DEFAULT_FONT_WEIGHT,
                 font_style: FontStyle = DEFAULT_FONT_STYLE,
                 font_size: int = DEFAULT_FONT_SIZE, *args: Any,
                 **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.font = Font(font_family, font_weight, font_style, font_size)
        self._value: str
        self.value = value

    @property
    def font_family(self) -> FontFamily:
        return self.font.family

    @font_family.setter
    def font_family(self, val: FontFamily) -> None:
        # check_type(val, 'FontFamily', class_name=self.__class__.__name__, property_name='font_family')
        self.font.family = val

    @property
    def font_size(self) -> int:
        return self.font.size

    @font_size.setter
    def font_size(self, val: int) -> None:
        # check_type(val, int, class_name=self.__class__.__name__, property_name='font_size')
        self.font.size = val

    @property
    def font_weight(self) -> FontWeight:
        return self.font.weight

    @font_weight.setter
    def font_weight(self, val: FontWeight) -> None:
        # check_type(val, 'FontWeight', class_name=self.__class__.__name__, property_name='font_weight')
        self.font.weight = val

    @property
    def font_style(self) -> FontStyle:
        return self.font.style

    @font_style.setter
    def font_style(self, val: FontStyle) -> None:
        # check_type(val, 'FontStyle', class_name=self.__class__.__name__, property_name='font_style')
        self.font.style = val

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, val: Any) -> None:
        self._value = str(val)

    def get_text_width(self) -> float:
        return self.font.get_text_pixel_width(self.value) / PdfUnit.get_k()

    def get_text_height(self) -> float:
        return self.font.get_text_pixel_height(self.value) / PdfUnit.get_k()

    def get_relative_x2(self) -> float:
        return self.relative_x + self.get_text_width()

    def get_relative_y2(self) -> float:
        return self.relative_y + self.get_text_height()

    def draw(self, pdf: Pdf) -> None:
        if not isinstance(pdf, Pdf):
            raise TypeError(create_error_message(message=f"{pdf} must be of type Pdf not {type(pdf)}",
                                                 class_name=self.__class__.__name__, method_name='draw',
                                                 argument_name='pdf'))
        if self.show:
            pdf.reset_font()
            style: Literal[
                '', 'B', 'I', 'U', 'BU', 'UB', 'BI', 'IB', 'IU', 'UI', 'BIU', 'BUI', 'IBU', 'IUB', 'UBI', 'UIB']
            if self.font_style == 'italic' and self.font_weight == 'bold':
                style = 'IB'
            elif self.font_style == 'italic':
                style = 'I'
            elif self.font_weight == 'bold':
                style = 'B'
            else:
                style = ''
            pdf.set_font(self.font.family, style=style, size=self.font_size)
            with pdf.pdf_draw_object_translate(self):
                pdf.text(x=0, y=0, text=self.value)


class Text(AbstractText, Positioned, Margined):
    pass


class PageText(Text):
    def __init__(self, value: Any, v_position: VerticalPosition = 'top', h_position: HorizontalPosition = 'left',
                 *args: Any,
                 **kwargs: Any):
        super().__init__(value=value, *args, **kwargs)  # type: ignore
        self._v_position: VerticalPosition
        self._h_position: HorizontalPosition
        self.v_position = v_position
        self.h_position = h_position

    @Text.relative_y.setter  # type: ignore
    def relative_y(self, val: ConvertibleToFloat) -> None:
        if val:
            raise RelativePositionNotSettableError

    @Text.relative_x.setter  # type: ignore
    def relative_x(self, val: ConvertibleToFloat) -> None:
        if val:
            raise RelativePositionNotSettableError

    @property
    def v_position(self) -> VerticalPosition:
        return self._v_position

    @v_position.setter
    def v_position(self, val: VerticalPosition) -> None:
        check_type(val, 'VerticalPosition')
        self._v_position = val

    @property
    def h_position(self) -> HorizontalPosition:
        return self._h_position

    @h_position.setter
    def h_position(self, val: HorizontalPosition) -> None:
        check_type(val, 'HorizontalPosition')
        self._h_position = val

    def draw(self, pdf: Pdf) -> None:
        pdf.reset_position()
        if self.h_position == 'center':
            self._relative_x = ((pdf.w - pdf.l_margin - pdf.r_margin) / 2) - self.get_width() / 2
        elif self.h_position == 'left':
            self._relative_x = pdf.l_margin
        elif self.h_position == 'right':
            self._relative_x = pdf.w - pdf.r_margin - self.get_width()
        else:
            raise NotImplementedError  # pragma: no cover

        if self.v_position == 'top':
            self._relative_y = pdf.t_margin
        elif self.v_position == 'bottom':
            self._relative_y = pdf.h - pdf.b_margin
        else:
            raise NotImplementedError  # pragma: no cover
        super().draw(pdf)
