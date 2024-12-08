import re
from pathlib import Path
from types import TracebackType
from typing import Protocol, Any, TYPE_CHECKING, Optional, Union, cast

from fpdf import FPDF

from musurgia.musurgia_types import ConvertibleToFloat, check_type, PageOrientation, PageFormat
from musurgia.pdf.pdfunit import PdfUnit

if TYPE_CHECKING:
    from musurgia.pdf.drawobject import DrawObject  # pragma: no cover

__all__ = ['Pdf']


def sprintf(fmt: str, *args: Any) -> str: return fmt % args


class SavedState:
    def __init__(self, pdf: 'Pdf') -> None:
        self.pdf = pdf

    def __enter__(self) -> None:
        self.pdf._push_state()

    def __exit__(self, exc_type: Optional[type[BaseException]], exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self.pdf._pop_state()


class PdfDrawObjectTranslations:
    def __init__(self, pdf: 'Pdf', draw_object: 'DrawObject', translate_positions: bool = True,
                 translate_margins: bool = True) -> None:
        self.pdf = pdf
        self.draw_object = draw_object
        self.translate_positions = translate_positions
        self.translate_margins = translate_margins

    def __enter__(self) -> None:
        self.pdf._push_state()
        if self.translate_positions:
            self.pdf.translate(self.draw_object.relative_x, self.draw_object.relative_y)
        if self.translate_margins:
            self.pdf.translate(self.draw_object.left_margin, self.draw_object.top_margin)

    def __exit__(self, exc_type: Optional[type[BaseException]], exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self.pdf._pop_state()


class HasOutProtocol(Protocol):
    def _out(self, s: str) -> None: ...


class Pdf(FPDF, HasOutProtocol):
    """
    Child of fpdf.FPDF class
    """

    def __init__(self, r_margin: ConvertibleToFloat = 10, t_margin: ConvertibleToFloat = 10,
                 l_margin: ConvertibleToFloat = 10, b_margin: ConvertibleToFloat = 10, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.r_margin = float(r_margin)
        self.t_margin = float(t_margin)
        self.l_margin = float(l_margin)
        self.b_margin = float(b_margin)
        self._absolute_positions: dict[int, list[float]] = {}
        self.add_page()

        self._state: list[str] = []

        self.set_font("Helvetica", "", 10)

    # private

    def _pop_state(self) -> None:
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        self._state.pop()
        self._out(sprintf('Q\n'))

    def _push_state(self) -> None:
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        self._state.append('push')
        self._out(sprintf('q\n'))

    # public properties
    @property
    def absolute_positions(self) -> dict[int, list[float]]:
        return self._absolute_positions

    @property
    def absolute_x(self) -> float:
        return self._absolute_positions[self.page][0]

    @property
    def absolute_y(self) -> float:
        return self._absolute_positions[self.page][1]

    @property
    def k(self) -> float:
        return PdfUnit.get_k()

    @k.setter
    def k(self, val: float) -> None:
        pass

    def add_page(self, orientation: PageOrientation = "", format: Union[PageFormat, tuple[float, float]] = "",
                 same: bool = False,
                 duration: int = 0,
                 transition: Optional[Any] = None,
                 ) -> None:
        check_type(orientation, 'PageOrientation', class_name='PageOrientation', method_name='add_page',
                   argument_name='orientation')
        if not isinstance(format, tuple):
            check_type(format, 'PageFormat', class_name='PageOrientation', method_name='add_page',
                       argument_name='format')
        check_type(same, bool, class_name='PageOrientation', method_name='add_page', argument_name='same')
        check_type(duration, int, class_name='PageOrientation', method_name='add_page', argument_name='duration')

        if orientation == "":
            orientation = self.cur_orientation
        super().add_page(orientation=orientation, format=format, same=same, duration=duration, transition=transition)
        self._absolute_positions[self.page] = [0, 0.]

    def clip_rect(self, x: ConvertibleToFloat, y: ConvertibleToFloat, w: ConvertibleToFloat,
                  h: ConvertibleToFloat) -> None:
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        check_type(x, 'ConvertibleToFloat', class_name=self.__class__.__name__, method_name='clip_rect',
                   argument_name='x')
        check_type(y, 'ConvertibleToFloat', class_name=self.__class__.__name__, method_name='clip_rect',
                   argument_name='y')
        check_type(w, 'ConvertibleToFloat', class_name=self.__class__.__name__, method_name='clip_rect',
                   argument_name='w')
        check_type(h, 'ConvertibleToFloat', class_name=self.__class__.__name__, method_name='clip_rect',
                   argument_name='h')
        x = float(x)
        y = float(y)
        w = float(w)
        h = float(h)
        self._out(sprintf('%.2f %.2f %.2f %.2f re W n',
                          x * self.k, (self.h - y) * self.k,
                          w * self.k, -h * self.k))

    def pdf_draw_object_translate(self, draw_object: 'DrawObject', **kwargs: Any) -> PdfDrawObjectTranslations:
        return PdfDrawObjectTranslations(self, draw_object=draw_object, **kwargs)

    def reset_font(self) -> None:
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        self._out(sprintf('BT /F%d %.2f Tf ET',
                          self.current_font.i,  # type: ignore
                          self.font_size_pt))

    def reset_position(self) -> None:
        self.translate(-self.absolute_x, -self.absolute_y)

    def saved_state(self) -> SavedState:
        return SavedState(self)

    def translate(self, dx: ConvertibleToFloat, dy: ConvertibleToFloat) -> None:
        check_type(dx, 'ConvertibleToFloat', class_name=self.__class__.__name__, method_name='translate',
                   argument_name='dx')
        check_type(dy, 'ConvertibleToFloat', class_name=self.__class__.__name__, method_name='translate',
                   argument_name='dy')
        dx, dy = float(dx), float(dy)
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        if not self._state:
            self._absolute_positions[self.page][0] += dx
            self._absolute_positions[self.page][1] += dy
        dx, dy = dx * self.k, dy * self.k
        self._out(sprintf('1.0 0.0 0.0 1.0 %.2F %.2F cm',
                          dx, -dy))

    def translate_page_margins(self) -> None:
        self.translate(self.l_margin, self.t_margin)

    def write_to_path(self, path: Path) -> None:
        buffer = self.output()
        new_buffer = re.sub(rb'CreationDate \(D:[0-9]{14}Z[0-9]{2}\'[0-9]{2}\'\)', b'CreationDate (none)',
                            bytes(buffer))
        new_buffer = bytearray(
            re.sub(rb'ID \[<([0-9A-F]{32})><\1>]', b'ID [<1><2>]', new_buffer))
        path.write_bytes(new_buffer)
