from pathlib import Path

from musurgia.pdf.line import VerticalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler, draw_page_numbers
from musurgia.pdf.text import Text
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestAddPage(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_absolute_y(self):
        self.pdf.translate(10, 10)
        self.pdf.add_page()
        actual = self.pdf.absolute_positions
        expected = {1: [10, 10], 2: [0, 0]}
        self.assertEqual(expected, actual)

    def test_draw(self):
        self.pdf.translate_page_margins()
        draw_ruler(self.pdf, mode='h')
        draw_ruler(self.pdf, mode='v')
        self.pdf.translate(10, 10)
        vsl = VerticalSegmentedLine(lengths=[10, 20, 30, 40])
        vsl.draw(self.pdf)
        self.pdf.add_page()
        self.pdf.translate_page_margins()
        draw_ruler(self.pdf, mode='h')
        draw_ruler(self.pdf, mode='v')
        self.pdf.translate(10, 10)
        # print(self.pdf.absolute_positions)
        vsl.draw(self.pdf)
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_page_number(self):
        for i in range(3):
            self.pdf.add_page()
        draw_page_numbers(self.pdf, v_position='bottom', h_position='center')

        with self.file_path(path, 'page_number', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_draw_in_reversed_order(self):
        self.pdf.translate(30, 30)
        self.pdf.add_page()
        self.pdf.translate(80, 80)
        self.pdf.add_page()
        self.pdf.page = 2
        text = Text('second page')
        text.draw(self.pdf)
        self.pdf.page = 1
        text = Text('first page')
        text.draw(self.pdf)

        for page in self.pdf.pages:
            self.pdf.page = page
            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')

        draw_page_numbers(self.pdf, v_position='bottom', h_position='center')

        with self.file_path(path, 'draw_in_reversed_order', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)
