import copy
from pathlib import Path
from unittest import TestCase

from musurgia.pdf.line import HorizontalLineSegment, StraightLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestHorizontalLineSegment(TestCase):
    def setUp(self) -> None:
        self.hls = HorizontalLineSegment(length=10)

    def test_relative_y(self):
        assert self.hls.start_mark_line.relative_y == 0
        assert self.hls.end_mark_line.relative_y == 0

        self.hls.start_mark_line.length = 10
        self.hls.end_mark_line.length = 6

        assert self.hls.relative_y == 0
        assert self.hls.start_mark_line.relative_y == 0
        assert self.hls.end_mark_line.relative_y == 2
        assert self.hls.straight_line.relative_y == 5

        assert self.hls.get_relative_y2() == 10

        assert self.hls.get_height() == 10
        assert self.hls.get_relative_y2() == 10

        self.hls.relative_y = 10
        assert self.hls.relative_y == 10
        assert self.hls.start_mark_line.relative_y == 10
        assert self.hls.end_mark_line.relative_y == 12
        assert self.hls.straight_line.relative_y == 15
        assert self.hls.get_height() == 10
        assert self.hls.get_relative_y2() == 20

        self.hls.set_straight_line_relative_y(0)
        assert self.hls.relative_y == -5
        assert self.hls.start_mark_line.relative_y == -5
        assert self.hls.end_mark_line.relative_y == -3
        assert self.hls.straight_line.relative_y == 0
        assert self.hls.get_height() == 10
        assert self.hls.get_relative_y2() == 5

        self.hls.start_mark_line.length = 6
        self.hls.end_mark_line.length = 10
        assert self.hls.start_mark_line.relative_y == -3
        assert self.hls.end_mark_line.relative_y == -5

        self.hls.relative_y = 0
        assert self.hls.start_mark_line.relative_y == 2
        assert self.hls.end_mark_line.relative_y == 0

    def test_relative_x(self):
        self.hls.relative_x = 10
        self.hls.right_margin = 5

        assert self.hls.straight_line.relative_x == self.hls.start_mark_line.relative_x == self.hls.relative_x == 10
        assert self.hls.end_mark_line.relative_x == 10 + self.hls.length

        assert self.hls.get_relative_x2() == 20
        assert self.hls.get_width() == 15

    def test_straight_line_top_margin(self):
        actual = self.hls.straight_line.top_margin
        expected = 0
        self.assertEqual(expected, actual)

    def test_start_mark_line_top_margin(self):
        actual = self.hls.start_mark_line.top_margin
        expected = 0
        self.assertEqual(expected, actual)

    def test_set_and_get_length(self):
        assert self.hls.length == 10
        self.hls.length = 20
        assert self.hls.length == 20

    def test_infos(self):
        hls = HorizontalLineSegment(length=100)
        hls.start_mark_line.length = 6
        hls.end_mark_line.length = 10
        hls.relative_x = 5
        hls.relative_y = 5
        assert hls.get_positions() == {'x': 5.0, 'y': 5.0}
        assert (hls.get_relative_x2(), hls.get_relative_y2()) == (105.0, 15.0)
        assert hls.get_height() == 10
        assert hls.get_width() == 100

    def test_set_straight_line_y(self):
        self.hls.start_mark_line.length = self.hls.end_mark_line.length = 5
        self.hls.relative_y = 10
        assert self.hls.straight_line.relative_y == 12.5
        self.hls.set_straight_line_relative_y(0)
        assert self.hls.relative_y == -2.5
        self.hls.set_straight_line_relative_y(5)
        assert self.hls.relative_y == 2.5
        self.hls.relative_y = 0
        self.hls.start_mark_line.length = 10
        assert self.hls.straight_line.relative_y == 5
        self.hls.end_mark_line.length = 15
        assert self.hls.straight_line.relative_y == 7.5
        self.hls.set_straight_line_relative_y(0)
        assert self.hls.straight_line.relative_y == 0


class TestTestHorizontalLineSegment(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.hls = HorizontalLineSegment(length=10)

    def test_draw(self):
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.hls.end_mark_line.show = True
            self.hls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_list(self):
        segments = [HorizontalLineSegment(length) for length in range(10, 30, 5)]
        segments[-1].end_mark_line.show = True
        with self.file_path(parent_path=path, name='draw_list', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            for segment in segments:
                segment.draw(self.pdf)
                self.pdf.translate(segment.get_width(), 0)

            self.pdf.write_to_path(pdf_path)

    def test_labels(self):
        self.hls.relative_x = 30
        self.hls.length = 30
        self.hls.start_mark_line.length = 10
        self.hls.end_mark_line.length = 10
        self.hls.end_mark_line.add_label('end top')
        self.hls.end_mark_line.add_label('end top')
        self.hls.start_mark_line.add_label('start top')
        self.hls.start_mark_line.add_label('start top')
        self.hls.end_mark_line.add_label('end below', placement='below')
        self.hls.end_mark_line.add_label('end below', placement='below')
        self.hls.start_mark_line.add_label('start below', placement='below')
        self.hls.start_mark_line.add_label('start below', placement='below')
        self.hls.straight_line.add_label('straight above', placement='above')
        self.hls.straight_line.add_label('straight below', placement='below')
        self.hls.straight_line.add_label('straight left', placement='left')
        self.hls.straight_line.add_label('straight left', placement='left')
        self.hls.straight_line.add_label('straight left', placement='left')

        with self.file_path(parent_path=path, name='labels', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.hls.end_mark_line.show = True
            self.hls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_with_relative_y(self):
        copied_1 = copy.deepcopy(self.hls)
        copied_1.relative_y = 5
        control = StraightLine(mode='h', length=10, relative_y=5)
        control.add_text_label('control', font_size=8, bottom_margin=2)

        with self.file_path(parent_path=path, name='draw_with_relative_y', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            # self.hls.start_mark_line.add_text_label(str(self.pdf.absolute_positions), placement='above', font_size=8)
            self.hls.draw(self.pdf)
            self.pdf.translate(20, 0)
            control.draw(self.pdf)
            # copied_1.start_mark_line.add_text_label(str(self.pdf.absolute_positions), placement='above', font_size=8)
            copied_1.start_mark_line.add_text_label(f'hls: {copied_1.positions}', placement='below', font_size=8)
            copied_1.start_mark_line.add_text_label(f'straight: {copied_1.straight_line.positions}', placement='below',
                                                    font_size=8)
            copied_1.start_mark_line.add_text_label(f'start: {copied_1.start_mark_line.positions}', placement='below',
                                                    font_size=8)
            copied_1.start_mark_line.add_text_label(f'end: {copied_1.end_mark_line.positions}', placement='below',
                                                    font_size=8)

            copied_1.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
