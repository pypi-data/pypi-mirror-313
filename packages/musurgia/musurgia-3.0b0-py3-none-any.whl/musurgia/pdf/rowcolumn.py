from abc import ABC
from typing import Any, Iterator

from fpdf.drawing import DeviceGray

from musurgia.musurgia_exceptions import DrawObjectInContainerHasNegativePositionError
from musurgia.musurgia_types import create_error_message
from musurgia.pdf.drawobject import DrawObject
from musurgia.pdf.labeled import Labeled
from musurgia.pdf.margined import Margined
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.positioned import Positioned

__all__ = ['DrawObjectColumn', 'DrawObjectRow']


class DrawObjectContainer(DrawObject, Labeled, Positioned, Margined, ABC):
    def __init__(self, show_borders: bool = False, show_margins: bool = False, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._draw_objects: list[DrawObject] = []
        self._show_borders: bool
        self.show_borders = show_borders
        self._show_margins: bool
        self.show_margins = show_margins

    @property
    def show_borders(self) -> bool:
        return self._show_borders

    @show_borders.setter
    def show_borders(self, val: bool) -> None:
        self._show_borders = val

    @property
    def show_margins(self) -> bool:
        return self._show_margins

    @show_margins.setter
    def show_margins(self, val: bool) -> None:
        self._show_margins = val

    def draw_margins(self, pdf: Pdf) -> None:
        if self.show_margins:
            with pdf.local_context(draw_color=DeviceGray(0.5), dash_pattern={'dash': 1, 'gap': 1}):
                pdf.rect(*self.get_margin_rectangle_coordinates())

    def draw_borders(self, pdf: Pdf) -> None:
        if self.show_borders:
            with pdf.local_context(draw_color=DeviceGray(0.5), dash_pattern={'dash': 2, 'gap': 1}):
                pdf.rect(*self.get_border_rectangle_coordinates())

    def add_draw_object(self, draw_object: DrawObject) -> DrawObject:
        if not isinstance(draw_object, DrawObject):
            raise TypeError(create_error_message(class_name=self.__class__.__name__, method_name='add_draw_object',
                                                 argument_name='draw_object',
                                                 message=f'draw_object must be of type DrawObject, not {type(draw_object)}'))
        self._draw_objects.append(draw_object)
        return draw_object

    def get_border_rectangle_coordinates(self) -> tuple[float, float, float, float]:
        return self.relative_x, self.relative_y, self.get_relative_x2() - self.relative_x, self.get_relative_y2() - self.relative_y

    def get_margin_rectangle_coordinates(self) -> tuple[float, float, float, float]:
        return self.relative_x, self.relative_y, self.get_relative_x2() - self.relative_x + self.right_margin + self.left_margin, self.get_relative_y2() - self.relative_y + self.bottom_margin + self.top_margin

    def get_draw_objects(self) -> list[DrawObject]:
        return self._draw_objects

    def traverse(self) -> Iterator['DrawObject']:
        yield self
        for do in self.get_draw_objects():
            if isinstance(do, DrawObjectContainer):
                for dodo in do.traverse():
                    yield dodo
            else:
                yield do

    def _check_draw_objects_positions(self) -> None:
        for do in self.get_draw_objects():
            if do.relative_y < 0 or do.relative_x < 0:
                raise DrawObjectInContainerHasNegativePositionError()


class DrawObjectRow(DrawObjectContainer):

    def get_relative_x2(self) -> float:
        return self.relative_x + sum([do.relative_x + do.get_width() for do in self.get_draw_objects()])

    def get_relative_y2(self) -> float:
        return self.relative_y + max([do.relative_y + do.get_height() for do in self.get_draw_objects()])

    def draw(self, pdf: Pdf) -> None:
        self._check_draw_objects_positions()
        self.draw_margins(pdf)
        with pdf.pdf_draw_object_translate(self, translate_positions=False):
            self.draw_borders(pdf)
        with pdf.pdf_draw_object_translate(self):
            self.draw_above_text_labels(pdf)
            self.draw_left_text_labels(pdf)
            self.draw_below_text_labels(pdf)
            for do in self.get_draw_objects():
                do.draw(pdf)
                pdf.translate(do.get_width(), 0)


class DrawObjectColumn(DrawObjectContainer):
    def get_relative_x2(self) -> float:
        return self.relative_x + max([do.get_width() for do in self.get_draw_objects()])

    def get_relative_y2(self) -> float:
        return self.relative_y + sum([do.relative_y + do.get_height() for do in self.get_draw_objects()])

    def draw(self, pdf: Pdf) -> None:
        self._check_draw_objects_positions()
        self.draw_margins(pdf)
        with pdf.pdf_draw_object_translate(self, translate_positions=False):
            self.draw_borders(pdf)
        with pdf.pdf_draw_object_translate(self):
            self.draw_above_text_labels(pdf)
            self.draw_left_text_labels(pdf)
            self.draw_below_text_labels(pdf)
            for do in self.get_draw_objects():
                do.draw(pdf)
                pdf.translate(0, do.relative_y + do.get_height())
