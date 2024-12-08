from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment, VerticalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestVLSSStraighLineLabels(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.vls = VerticalLineSegment(length=20)
        self.vls.start_mark_line.show = False
        self.vls.set_straight_line_relative_x(0)

    def test_vertical_above(self):
        self.vls.straight_line.add_text_label('one above')
        self.vls.straight_line.add_text_label('two above')
        self.vls.straight_line.add_text_label('three above')
        with self.file_path(path, 'above', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_vertical_above_with_relative_y(self):
        self.vls.relative_y = -10
        self.vls.straight_line.add_text_label('one above')
        self.vls.straight_line.add_text_label('two above')
        self.vls.straight_line.add_text_label('three above')
        with self.file_path(path, 'above_with_relative_y', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_vertical_below(self):
        self.vls.straight_line.add_text_label('one below', placement='below')
        self.vls.straight_line.add_text_label('two below', placement='below')
        self.vls.straight_line.add_text_label('three below', placement='below')
        with self.file_path(path, 'below', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_vertical_left(self):
        self.vls.straight_line.add_text_label('one left', placement='left')
        self.vls.straight_line.add_text_label('two left', placement='left')
        self.vls.straight_line.add_text_label('three left', placement='left')
        with self.file_path(path, 'left', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_vertical_left_with_top_margin(self):
        self.vls.top_margin = 200
        self.vls.straight_line.add_text_label('one left', placement='left')
        self.vls.straight_line.add_text_label('two left', placement='left')
        self.vls.straight_line.add_text_label('three left', placement='left')
        with self.file_path(path, 'left_with_top_margin', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
