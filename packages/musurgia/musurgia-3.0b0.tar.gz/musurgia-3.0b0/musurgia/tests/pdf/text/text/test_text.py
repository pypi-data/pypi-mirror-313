from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.text import Text
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestText(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_font_attributes(self):
        t = Text('Test')
        t.font_size = 20
        t.font_weight = 'medium'
        t.font_style = 'italic'
        t.font_family = 'Courier'
        assert t.font_size == 20
        assert t.font_weight == 'medium'
        assert t.font_style == 'italic'
        assert t.font_family == 'Courier'

        with self.assertRaises(TypeError):
            t.font_style = 'wrong'

    def test_draw(self):
        t = Text('The fox is going to be dead.')
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            t.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_with_top_margin(self):
        t = Text('The fox is going to be dead.')
        t.top_margin = 5
        with self.file_path(path, 'draw_with_top_margin', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            t.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_get_height(self):
        t = Text('fox is going to be dead.')
        t.font_size = 14
        t.top_margin = 3
        self.assertEqual(7.02, round(t.get_height(), 3))

    def test_height_graphical(self):
        t = Text('The fox is going to be dead.')
        with self.file_path(path, 'height_graphical', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            hls = HorizontalLineSegment(length=t.get_text_width())
            hls.relative_y = t.relative_y - 3 / 4 * t.get_height()
            hls.start_mark_line.length = t.get_height()
            hls.end_mark_line.show = True

            with self.pdf.saved_state():
                self.pdf.rect(hls.relative_x, hls.relative_y, hls.get_width(), t.get_height())
                hls.draw(self.pdf)
            t.draw(self.pdf)

            self.pdf.write_to_path(pdf_path)

    def test_draw_multiple(self):
        t1 = Text(value='Fox is going to be dead.')
        t2 = Text(value='What should we do??', relative_y=0)
        t3 = Text(value='What should we do??', relative_y=0)
        with self.file_path(path, 'draw_multiple', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            t1.draw(self.pdf)
            self.pdf.translate(0, t1.get_height())
            t2.draw(self.pdf)
            self.pdf.translate(0, t1.get_height())
            t3.draw(self.pdf)
            self.pdf.translate(0, t1.get_height())
            self.pdf.write_to_path(pdf_path)

    def test_draw_multiple_with_relative_y(self):
        t1 = Text(value='Fox is going to be dead.', relative_x=10, relative_y=10)
        t2 = Text(value='What should we do??', relative_x=10, relative_y=20)
        t3 = Text(value='What should we do??', relative_x=10, relative_y=30)

        with self.file_path(path, 'draw_multiple_with_relative_y', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')

            t1.draw(self.pdf)
            t2.draw(self.pdf)
            t3.draw(self.pdf)

            self.pdf.write_to_path(pdf_path)

    def test_text_font(self):
        t = Text(value='some text', font_family='Courier', font_weight='bold', font_style='italic')
        assert t.font_family == 'Courier'
        assert t.font_weight == 'bold'
        assert t.font_style == 'italic'

        t2 = Text(value='some text', font_style='italic')

        with self.file_path(path, 'font', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            t.draw(self.pdf)
            self.pdf.translate(dx=0, dy=10)
            t2.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
