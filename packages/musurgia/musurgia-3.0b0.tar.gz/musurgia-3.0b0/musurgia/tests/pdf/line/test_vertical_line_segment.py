from pathlib import Path
from unittest import TestCase

from musurgia.pdf.line import VerticalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestVerticalLineSegment(TestCase):
    def setUp(self) -> None:
        self.vls = VerticalLineSegment(length=10)

    def test_get_relative_x2(self):
        assert self.vls.get_relative_x2() == self.vls.get_width()

    def test_start_mark_line_relative_x(self):
        assert self.vls.start_mark_line.relative_x == 0

    def test_start_mark_line_relative_y(self):
        assert self.vls.relative_y == self.vls.start_mark_line.relative_y

    def test_end_mark_line_relative_y(self):
        assert self.vls.end_mark_line.relative_y == self.vls.relative_y + self.vls.length

    def test_end_mark_line_relative_x(self):
        assert self.vls.end_mark_line.relative_x == 0

    def test_start_mark_line_top_margin(self):
        assert self.vls.start_mark_line.top_margin == 0

    def test_get_width(self):
        assert self.vls.get_width() == 3

    def test_set_straight_line_y_x(self):
        self.vls.set_straight_line_relative_x(0)
        assert self.vls.relative_x == -1.5
        with self.assertRaises(NotImplementedError):
            self.vls.set_straight_line_relative_y(0)


class TestVerticalLineSegmentDraw(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.vls = VerticalLineSegment(length=10)

    def test_draw(self):
        self.vls.set_straight_line_relative_x(0)
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v')
            draw_ruler(self.pdf, mode='h')
            self.pdf.translate(10, 10)
            self.vls.end_mark_line.show = True
            self.vls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
