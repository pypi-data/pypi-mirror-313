from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment, HorizontalSegmentedLine, VerticalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestMarkLineLabels(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.ls = HorizontalLineSegment(length=20)
        self.ls.set_straight_line_relative_y(0)

    def test_draw_above(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label above')
        ml.add_text_label('second text label above')
        ml.add_text_label('third  text label above')
        self.ls.relative_x = 10
        self.ls.relative_y = 20
        with self.file_path(path, 'above', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')

            self.ls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_one_above(self):
        ml = self.ls.start_mark_line
        ml.length = 20
        ml.add_text_label('first text label above')

        with self.file_path(path, 'one_above', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.translate(30, 30)
            self.ls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_below(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label below', placement='below')
        ml.add_text_label('second text label below', placement='below')
        self.ls.relative_x = 10
        self.ls.relative_y = 20
        with self.file_path(path, 'below', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.ls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_left(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label left', placement='left')
        ml.add_text_label('second text label left left left', placement='left')
        ml.add_text_label('third text label left left left', placement='left')
        ml.get_left_text_labels()[1].font.size = 8
        self.ls.relative_x = 40
        self.ls.relative_y = 10
        with self.file_path(path, 'left', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.ls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_different_sizes(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label above', font_size=7)
        ml.add_text_label('second text label above', font_size=8)
        ml.add_text_label('third text label above', font_size=9)
        with self.file_path(path, 'different_sizes', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 20)
            self.ls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_font_size_8(self):
        ml = self.ls.start_mark_line

        ml.add_text_label('first text label above', font_size=8, bottom_margin=2)
        ml.add_text_label('second text label above', font_size=8, bottom_margin=4)
        ml.add_text_label('third text label above', font_size=8)
        with self.file_path(path, 'font_size_8', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 20)
            self.ls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_below_with_different_mark_line_lengths(self):
        hsl = HorizontalSegmentedLine(lengths=[10, 15, 20])
        hsl.segments[0].start_mark_line.length = 6
        hsl.segments[0].start_mark_line.add_label(1, placement='below', font_size=8)
        hsl.segments[1].start_mark_line.add_label(2, placement='below', font_size=8)
        hsl.segments[2].start_mark_line.add_label(3, placement='below', font_size=8)
        hsl.set_straight_line_relative_y(0)
        with self.file_path(path, 'below_with_different_mark_line_lengths', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            hsl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_vertical_with_left_text_labels(self):
        vsl = VerticalSegmentedLine(lengths=[10, 15, 20])
        vsl.segments[0].start_mark_line.length = 6
        vsl.segments[0].start_mark_line.add_label(1, placement='left', font_size=8)
        vsl.segments[1].start_mark_line.add_label(2, placement='left', font_size=8)
        vsl.segments[2].start_mark_line.add_label(3, placement='left', font_size=8)
        with self.file_path(path, 'vertical_with_left_text_labels', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            vsl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_above_with_different_bottom_margins(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label above', bottom_margin=2)
        ml.add_text_label('second text label above', bottom_margin=4)
        ml.add_text_label('third  text label above', bottom_margin=15)
        self.ls.relative_x = 10
        self.ls.relative_y = 40
        with self.file_path(path, 'above_with_different_bottom_margins', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')

            self.ls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_left_position(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('left one', placement='left')
        ml.add_text_label('left two', placement='left')
        ml.add_text_label('left three', placement='left')
        ml.add_text_label('left four', placement='left')

        with self.file_path(path, 'left_position', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(30, 30)
            self.ls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
