from pathlib import Path

from musurgia.pdf import Pdf, StraightLine, draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase, add_control_positions_to_draw_object, add_test_labels

path = Path(__file__)


class TestPdfUtil(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.line = StraightLine(length=100, mode='h', relative_x=10, relative_y=10)
        self.line.margins = (5, 10, 15, 20)

    def test_add_control_positions(self):
        add_control_positions_to_draw_object(self.line)

        with self.file_path(path, 'add_control_positions', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'v')
            draw_ruler(self.pdf, 'h')
            self.pdf.translate(10, 10)
            self.line.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_add_test_labels(self):
        add_test_labels(self.line)
        with self.file_path(path, 'add_test_labels', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            # draw_ruler(self.pdf, 'v')
            # draw_ruler(self.pdf, 'h')
            self.pdf.translate(10, 10)
            self.line.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
