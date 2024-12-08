from typing import Union, Any

from musurgia.musurgia_types import check_type, HorizontalVertical
from musurgia.pdf.ruler import HorizontalRuler, VerticalRuler
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import PageText

__all__ = ['draw_page_numbers', 'draw_ruler']


def draw_page_numbers(pdf: Pdf, **kwargs: Any) -> None:
    for page in pdf.pages:
        pdf.page = page
        pdf.reset_position()
        page_number = PageText(page, **kwargs)
        page_number.draw(pdf)


def draw_ruler(pdf: Pdf, mode: HorizontalVertical = 'h', unit: int = 10, first_label: int = 0,
               show_first_label: bool = False, label_show_interval: int = 1, **kwargs: Any) -> None:
    check_type(mode, 'HorizontalVertical', function_name='draw_ruler', argument_name='mode')
    ruler: Union[HorizontalRuler, VerticalRuler]
    if mode in ['h', 'horizontal']:
        length = pdf.w - pdf.l_margin - pdf.r_margin
        ruler = HorizontalRuler(length=length, unit=unit, first_label=first_label,
                                show_first_label=show_first_label, label_show_interval=label_show_interval, **kwargs)
        ruler.set_straight_line_relative_y(0)
    elif mode in ['v', 'vertical']:
        length = pdf.h - pdf.t_margin - pdf.b_margin
        ruler = VerticalRuler(length=length, unit=unit, first_label=first_label,
                              show_first_label=show_first_label, label_show_interval=label_show_interval, **kwargs)
        ruler.set_straight_line_relative_x(0)
    else:
        raise NotImplementedError  # pragma: no cover

    ruler.draw(pdf)
