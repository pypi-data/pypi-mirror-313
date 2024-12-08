import copy
from pathlib import Path
from unittest import TestCase

from musurgia.musurgia_exceptions import SegmentedLineSegmentHasMarginsError, SegmentedLineLengthsCannotBeSetError
from musurgia.pdf import DrawObjectRow
from musurgia.pdf.line import HorizontalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


def change_markline_lengths(hsl):
    for index, sg in enumerate(hsl.segments):
        sg.start_mark_line.length += index * 5
    hsl.segments[-1].end_mark_line.length = hsl.segments[-1].start_mark_line.length + 5
    hsl.segments[-1].end_mark_line.show = True


class TestHorizontalSegmentedLine(TestCase):
    def setUp(self) -> None:
        self.hsl = HorizontalSegmentedLine(lengths=[10, 15, 20, 25])

    def test_segments(self):
        assert [seg.length for seg in self.hsl.segments] == [10, 15, 20, 25]
        assert self.hsl.segments[-1].end_mark_line.show is True
        assert set([seg.end_mark_line.show for seg in self.hsl.segments[:-1]]) == {False}
        assert set([seg.start_mark_line.show for seg in self.hsl.segments]) == {True}

    def test_lengths(self):
        with self.assertRaises(SegmentedLineLengthsCannotBeSetError):
            self.hsl.lengths = [10, 15, 20, 25]
        with self.assertRaises(AttributeError):
            assert self.hsl.lengths == [10, 15, 20, 25]
        assert self.hsl.get_lengths() == [10, 15, 20, 25]

    def test_get_height(self):
        self.hsl.segments[1].start_mark_line.length = 5
        assert self.hsl.get_height() == 5

    def test_set_straight_line_y_x(self):
        self.hsl.set_straight_line_relative_y(0)
        assert self.hsl.relative_y == -1.5
        with self.assertRaises(NotImplementedError):
            self.hsl.set_straight_line_relative_x(0)

    def test_align_segments(self):
        change_markline_lengths(self.hsl)
        self.hsl._align_segments()
        for seg in self.hsl.segments:
            assert seg.relative_y >= 0
            assert seg.relative_x >= 0
        assert 0 in set([seg.relative_y for seg in self.hsl.segments])

    def test_no_margin_error(self):
        self.hsl.segments[0].margins = (1, 2, 3, 4)
        with self.assertRaises(SegmentedLineSegmentHasMarginsError):
            self.hsl.draw(Pdf())

    def test_relative_y(self):
        assert isinstance(self.hsl, DrawObjectRow)
        assert self.hsl.positions == (0, 0)
        assert self.hsl.get_end_positions() == (70, 3)
        self.hsl.relative_y = 10
        assert self.hsl.positions == (0, 10)
        assert self.hsl.get_end_positions() == (70, 13)

    def test_borders(self):
        assert self.hsl.get_border_rectangle_coordinates() == (0, 0, 70, 3)

        self.hsl.set_straight_line_relative_y(0)
        assert self.hsl.get_border_rectangle_coordinates() == (0, -1.5, 70, 3)

        self.hsl.relative_y = -5
        assert self.hsl.get_border_rectangle_coordinates() == (0, -5, 70, 3)

        self.hsl.relative_y = 5
        assert self.hsl.get_border_rectangle_coordinates() == (0, 5, 70, 3)


class TestHorizontalSegmentedLineDraw(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.hsl = HorizontalSegmentedLine(lengths=[10, 15, 20, 25])

    def test_draw(self):
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.hsl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_add_label_left(self):
        self.hsl.add_label('first left label', placement='left')
        self.hsl.add_label('second left label', placement='left')
        self.hsl.add_label('third left label', placement='left')
        self.hsl.add_label('fourth left label', placement='left')
        self.hsl.segments[0].start_mark_line.length = 10
        self.pdf.translate_page_margins()
        self.pdf.translate(40, 20)
        self.hsl.draw(self.pdf)
        with self.file_path(path, 'add_label_left', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_change_markline_lengths(self):
        assert set([sg.start_mark_line.length for sg in self.hsl.segments] + [sg.end_mark_line.length for sg in
                                                                              self.hsl.segments]) == {3}
        change_markline_lengths(self.hsl)

        assert set([sg.relative_y for sg in self.hsl.segments]) == {0}

        with self.file_path(path, 'change_markline_lengths', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 30)
            for sg in self.hsl.segments:
                copied = copy.deepcopy(sg)
                copied.straight_line.add_text_label(f'{copied.straight_line.get_positions()}', font_size=5,
                                                    placement='below')
                copied.start_mark_line.add_text_label(f'{copied.start_mark_line.get_positions()}', font_size=5,
                                                      placement='above')
                copied.draw(self.pdf)
                self.pdf.translate(30, 0)
            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 60)
            self.hsl._align_segments()
            self.hsl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_margins(self):
        copy_1 = copy.deepcopy(self.hsl)
        copy_1.margins = (10, 10, 10, 10)
        dos = [self.hsl, copy_1]
        for do in dos:
            do.show_borders = True
            do.show_margins = True
        with self.file_path(parent_path=path, name='margins', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v')
            draw_ruler(self.pdf, mode='h')
            self.pdf.translate(20, 20)
            for do in dos:
                do.draw(self.pdf)
                self.pdf.translate(0, 20)
            self.pdf.write_to_path(pdf_path)

    def test_borders(self):
        def add_positions(do):
            do.add_text_label(f'{do.positions}', placement='left', font_size=8)

        copied_1 = copy.deepcopy(self.hsl)
        copied_2 = copy.deepcopy(self.hsl)
        copied_3 = copy.deepcopy(self.hsl)

        copied_1.set_straight_line_relative_y(0)
        copied_2.relative_y = -5
        copied_3.relative_y = 5

        assert isinstance(copied_3, DrawObjectRow)

        assert self.hsl.positions == (0, 0)
        assert [seg.positions for seg in self.hsl.segments] == [(0, 0), (0, 0), (0, 0), (0, 0)]
        assert self.hsl.get_end_positions() == (70, 3)
        assert [seg.get_end_positions() for seg in self.hsl.segments] == [(10, 3), (15, 3), (20, 3), (25, 3)]

        assert copied_1.positions == (0, -1.5)
        assert copied_1.get_end_positions() == (70, 1.5)
        assert [seg.positions for seg in copied_1.segments] == [(0, 0), (0, 0), (0, 0), (0, 0)]
        assert [seg.get_end_positions() for seg in copied_1.segments] == [(10, 3), (15, 3), (20, 3), (25, 3)]

        assert copied_2.positions == (0, -5)
        assert copied_2.get_end_positions() == (70, -2)

        assert copied_3.positions == (0, 5)
        assert copied_3.get_end_positions() == (70, 8)

        dos = [self.hsl, copied_1, copied_2, copied_3]
        for do in dos:
            do.show_borders = True

            add_positions(do)

        with self.file_path(parent_path=path, name='borders', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v')
            draw_ruler(self.pdf, mode='h')
            self.pdf.translate(20, 20)
            for do in dos:
                do.draw(self.pdf)
                self.pdf.translate(0, 20)
            self.pdf.write_to_path(pdf_path)