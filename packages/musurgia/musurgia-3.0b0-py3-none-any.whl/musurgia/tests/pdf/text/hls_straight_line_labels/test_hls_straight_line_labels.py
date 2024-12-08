from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment, VerticalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestHLSSStraighLineLabels(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.hls = HorizontalLineSegment(length=20)
        self.hls.start_mark_line.show = False

    def test_horizontal_above(self):
        self.hls.straight_line.add_text_label('one above')
        self.hls.straight_line.add_text_label('two above')
        self.hls.straight_line.add_text_label('three above')
        with self.file_path(path, 'above', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(20, 20)
            self.hls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_horizontal_below(self):
        self.hls.straight_line.add_text_label('one below', placement='below')
        self.hls.straight_line.add_text_label('two below', placement='below')
        self.hls.straight_line.add_text_label('three below', placement='below')
        with self.file_path(path, 'below', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(20, 20)
            self.hls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_horizontal_left(self):
        self.hls.straight_line.add_text_label('one left', placement='left')
        self.hls.straight_line.add_text_label('two left', placement='left')
        self.hls.straight_line.add_text_label('three left', placement='left')
        with self.file_path(path, 'left', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(20, 20)
            self.hls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
