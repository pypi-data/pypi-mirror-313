from math import ceil
from pathlib import Path

from musurgia.pdf.line import HorizontalSegmentedLine
from musurgia.pdf.ruler import HorizontalRuler
from musurgia.pdf.drawobject import ClippingArea
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.rowcolumn import DrawObjectColumn
from musurgia.pdf.text import PageText
from musurgia.tests.utils_for_tests import PdfTestCase, create_test_path

path = Path(__file__)


class TestClip(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_line(self):
        pdf_path = create_test_path(path, 'line.pdf')
        self.pdf.rect(0, 0, 50, 50)
        self.pdf.clip_rect(0, 0, 50, 50)
        self.pdf.line(10, 20, 100, 100)
        self.pdf.write_to_path(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_line_break(self):
        def draw_with_clip(index):
            with self.pdf.saved_state():
                self.pdf.clip_rect(-1, -5, 196, 50)
                self.pdf.translate(index * -190, 0)
                ruler.draw(self.pdf)

        ruler = HorizontalRuler(length=800, unit=10)
        with self.file_path(path, 'line_break', 'pdf') as pdf_path:
            self.pdf.translate(10, 10)
            number_of_rows = int(ceil(ruler.get_length() / 190))
            for index in range(number_of_rows):
                if index != 0:
                    self.pdf.translate(0, 30)
                draw_with_clip(index)
            self.pdf.write_to_path(pdf_path)
            self.assertCompareFiles(pdf_path)

    def test_column_line_break(self):
        def draw_with_clip(index):
            with self.pdf.saved_state():
                self.pdf.clip_rect(-1, -5, 196, 50)
                self.pdf.translate(index * -190, 0)
                c.draw(self.pdf)

        c = DrawObjectColumn()
        c.bottom_margin = 10
        c.add_draw_object(HorizontalRuler(length=800))
        c.add_draw_object(HorizontalSegmentedLine(lengths=400 * [2]))
        with self.file_path(path, 'column_line_break', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            number_of_rows = int(ceil(c.get_width() / 190))
            for index in range(number_of_rows):
                if index != 0:
                    self.pdf.translate(0, c.get_height())
                draw_with_clip(index)
            self.pdf.write_to_path(pdf_path)
            self.assertCompareFiles(pdf_path)

    def test_column_page_break(self):
        self.pdf.t_margin = 15

        def _prepare_page():
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'v')
            draw_ruler(self.pdf, 'h')
            self.pdf.translate(clip_area_left_margin, clip_area_top_margin)

        def _add_page():
            self.pdf.add_page()
            _prepare_page()

        def draw_with_clip(index):
            with self.pdf.saved_state():
                self.pdf.clip_rect(-1, -5, clip_area_width + 1.14, clip_area_height)
                self.pdf.translate(index * -clip_area_width, 0)
                c.draw(self.pdf)

        c = DrawObjectColumn()
        c.bottom_margin = 60
        c.add_draw_object(HorizontalRuler(length=1200, bottom_margin=5))
        c.add_draw_object(HorizontalSegmentedLine(lengths=600 * [2]))

        clip_area_left_margin = 10
        clip_area_top_margin = 10
        clip_area_width = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin - clip_area_left_margin
        clip_area_height = c.get_height()

        with self.file_path(path, 'column_page_break', 'pdf') as pdf_path:
            _prepare_page()
            number_of_rows = int(ceil(c.get_width() / clip_area_width))
            for index in range(number_of_rows):
                if index != 0:
                    self.pdf.translate(0, c.get_height())
                if self.pdf.absolute_y > self.pdf.h - self.pdf.b_margin:
                    _add_page()
                draw_with_clip(index)
            self.pdf.write_to_path(pdf_path)

    def test_with_clipping_area(self):
        c = DrawObjectColumn()
        c.bottom_margin = 60
        c.add_draw_object(HorizontalRuler(length=1200, bottom_margin=5))
        c.add_draw_object(HorizontalSegmentedLine(lengths=600 * [2]))
        ca = ClippingArea(self.pdf, draw_object=c)
        ca.left_margin = 10
        self.pdf.translate_page_margins()
        ca.draw()
        with self.file_path(path, 'with_clipping_area', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)
            self.assertCompareFiles(pdf_path)

    def test_clipped_draw(self):
        c = DrawObjectColumn()
        c.get_clipping_area().top_margin = c.get_clipping_area().left_margin = 10
        c.bottom_margin = 60
        c.add_draw_object(HorizontalRuler(length=1200, bottom_margin=0, show_borders=True))
        c.add_draw_object(HorizontalSegmentedLine(lengths=600 * [2]))
        title = PageText('A very nice title', h_position='center', font_weight='bold', font_size=12, top_margin=10)
        title.draw(self.pdf)

        self.pdf.translate_page_margins()
        self.pdf.translate(0, 20)
        c.clipped_draw(self.pdf)

        for page in self.pdf.pages:
            self.pdf.page = page
            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
        with self.file_path(path, 'clipped_draw', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)
