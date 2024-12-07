import copy
from pathlib import Path
from unittest import skip, TestCase

from musurgia.musurgia_exceptions import DrawObjectInContainerHasNegativePositionError
from musurgia.pdf.line import HorizontalLineSegment, VerticalSegmentedLine, VerticalLineSegment, StraightLine, \
    HorizontalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.rowcolumn import DrawObjectRow, DrawObjectColumn
from musurgia.pdf.labeled import TextLabel
from musurgia.tests.utils_for_tests import PdfTestCase, add_control_positions_to_draw_object, create_simple_column

path = Path(__file__)


def _make_draw_objects():
    h_segments = [HorizontalLineSegment(10), HorizontalLineSegment(20)]
    h_segments[1].start_mark_line.length = 6

    vsl = VerticalSegmentedLine(lengths=[5, 6, 7, 8])
    return h_segments, vsl


def make_row():
    r = DrawObjectRow()
    h_segments, vsl = _make_draw_objects()
    for segment in h_segments:
        r.add_draw_object(segment)
    r.add_draw_object(vsl)
    r.add_text_label(TextLabel('row', placement='left'))
    return r


def make_column():
    c = DrawObjectColumn()
    h_segments, vsl = _make_draw_objects()
    for segment in h_segments:
        c.add_draw_object(segment)
    c.add_draw_object(vsl)
    return c


class TestRowPositionAndMargins(TestCase):
    def setUp(self):
        self.r = DrawObjectRow()
        self.hls = HorizontalLineSegment(length=10)
        self.hls.start_mark_line.length = 5
        self.r.add_draw_object(self.hls)

    def test_default_positions(self):
        assert self.r.positions == self.hls.positions == (0, 0)
        assert self.r.get_relative_x2() == self.hls.get_relative_x2() == 10
        assert self.r.get_relative_y2() == self.hls.get_relative_y2() == 5

    def test_change_row_positions(self):
        self.r.positions = (20, 30)
        assert self.hls.positions == (0, 0)
        assert self.r.get_relative_x2() == 30
        assert self.r.get_relative_y2() == 35
        assert self.hls.positions == (0, 0)
        assert self.hls.get_relative_x2() == 10
        assert self.hls.get_relative_y2() == 5

    def test_change_hls_positions(self):
        self.hls.positions = (20, 30)
        assert self.hls.get_relative_x2() == 30
        assert self.hls.get_relative_y2() == 35
        assert self.hls.get_width() == 10

        assert self.r.positions == (0, 0)
        assert self.r.get_relative_x2() == 30
        assert self.r.get_relative_y2() == 35

    def test_change_hls_negative_positions_error(self):
        self.hls.positions = (-20, -30)
        assert self.hls.get_relative_x2() == -10
        assert self.hls.get_relative_y2() == -25

        with self.assertRaises(DrawObjectInContainerHasNegativePositionError):
            self.r.draw(Pdf())

    def test_change_hls_and_row_positions(self):
        self.r.positions = (20, 30)
        self.hls.positions = (40, 50)
        assert self.hls.length == 10
        assert self.hls.get_end_positions() == (50, 55)
        assert self.r.get_end_positions() == (70, 85)

    def test_change_one_hls_positions(self):
        hl2 = copy.deepcopy(self.hls)
        self.r.add_draw_object(hl2)
        hl2.positions = (20, 30)
        assert self.hls.positions == (0, 0)
        assert self.hls.get_relative_x2(), self.hls.get_relative_y2() == (10, 5)
        assert hl2.positions == (20, 30)
        assert (hl2.get_relative_x2(), hl2.get_relative_y2()) == (30, 35)

        assert self.r.get_relative_x2() == 40
        assert self.r.get_relative_y2() == 35

    def test_relative_y_inside_column(self):
        c = DrawObjectColumn()
        hsl = HorizontalSegmentedLine([10, 20, 30])
        c.add_draw_object(hsl)
        assert c.get_end_positions() == (60, 3)
        hsl.relative_y = 10
        hsl.margins = (5, 0, 15, 0)
        assert hsl.get_height() == 23
        assert hsl.get_relative_y2() == 13
        assert c.get_end_positions() == (60, 33)

    def test_two_simple_lines_column_draw(self):
        c = DrawObjectColumn()
        s1 = StraightLine('h', 30)
        s1.relative_y = 5
        s1.margins = (10, 10, 10, 10)
        s2 = StraightLine('h', 30)
        s2.margins = (10, 10, 10, 10)
        s2.relative_y = 5
        c.add_draw_object(s1)
        c.add_draw_object(s2)
        assert c.get_end_positions() == (50, 50)

    def test_get_border_rectangle_coordinates(self):
        assert self.r.get_border_rectangle_coordinates() == (0, 0, 10, 5)

    def test_get_margin_rectangle_coordinates(self):
        assert self.r.get_margin_rectangle_coordinates() == (0, 0, 10, 5)


class TestRowColumnSimpleLines(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')
        self.h_lines = [StraightLine(length=l, mode='h') for l in range(5, 20, 5)]
        self.v_lines = [StraightLine(length=l, mode='v') for l in range(5, 20, 5)]
        self.v_lines[-1].right_margin = 10

    def test_simple_line_row_positions(self):
        row = DrawObjectRow(show_margins=True, show_borders=True)
        for l in self.h_lines + self.v_lines:
            l.top_margin = 10
            l.left_margin = 10
            row.add_draw_object(l)

        assert self.v_lines[2].get_end_positions() == (0.0, 15.0)
        assert self.v_lines[2].get_height() == 25
        add_control_positions_to_draw_object(row)
        assert row.get_end_positions() == (100, 25)
        with self.file_path(path, 'simple_lines_row_positions', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(mode='v', pdf=self.pdf)
            draw_ruler(mode='h', pdf=self.pdf)
            self.pdf.translate(10, 10)
            row.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_simple_lines_row(self):
        row = DrawObjectRow(show_margins=True, show_borders=True)
        row.margins = (10, 10, 10, 10)
        end_line = StraightLine(mode='h', length=70)
        end_line.add_text_label('control end_line', bottom_margin=2)
        for l in self.h_lines + self.v_lines:
            row.add_draw_object(l)

        for l in self.h_lines + self.v_lines:
            copied = copy.deepcopy(l)
            copied.top_margin = 10
            copied.left_margin = 10
            row.add_draw_object(copied)

        add_control_positions_to_draw_object(row)
        row.add_text_label(f'{row.get_height()}', placement='left')
        with self.file_path(path, 'simple_lines_row', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(mode='v', pdf=self.pdf)
            draw_ruler(mode='h', pdf=self.pdf)
            self.pdf.translate(20, 20)
            row.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)


class TestRowColumn(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')
        self.row = make_row()
        self.column = make_column()

    def test_draw_row(self):
        self.pdf.translate_page_margins()
        draw_ruler(self.pdf, 'h')
        draw_ruler(self.pdf, 'v')
        self.pdf.translate(10, 10)
        r = self.row
        r.add_text_label(label=TextLabel('below label', placement='below'))

        r.draw(self.pdf)

        with self.file_path(path, 'row', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_wrong_add_draw_object(self):
        r = DrawObjectRow()
        with self.assertRaises(TypeError):
            r.add_draw_object('something')

    def test_draw_row_of_segments(self):
        draw_object_rows = [DrawObjectRow(show_segments=True, show_margins=True) for _ in range(4)]
        line_segments = [HorizontalLineSegment(l) for l in [30, 10, 20]]
        line_segments[-1].end_mark_line.show = True
        line_segments[-1].right_margin = 10
        for l in line_segments:
            draw_object_rows[0].add_draw_object(l)

        for i, l in enumerate(line_segments):
            copied = copy.deepcopy(l)
            copied.start_mark_line.length *= (i + 1)
            draw_object_rows[1].add_draw_object(copied)
            if i == len(line_segments) - 1:
                copied.end_mark_line.length += copied.start_mark_line.length
            copied.right_margin = 10

        for i, l in enumerate(line_segments):
            copied = copy.deepcopy(l)
            copied.start_mark_line.length *= (i + 1)
            draw_object_rows[2].add_draw_object(copied)
            if i == len(line_segments) - 1:
                copied.end_mark_line.length += copied.start_mark_line.length

        for i, l in enumerate(line_segments):
            copied = copy.deepcopy(l)
            copied.start_mark_line.length *= (i + 1)
            draw_object_rows[3].add_draw_object(copied)
            if i == len(line_segments) - 1:
                copied.end_mark_line.length += copied.start_mark_line.length

        with self.file_path(path, 'row_of_segments', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            for l in line_segments:
                copied = copy.deepcopy(l)
                copied.draw(self.pdf)
                self.pdf.translate(50, 0)

            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 30)
            for i, l in enumerate(line_segments):
                copied = copy.deepcopy(l)
                copied.start_mark_line.length *= (i + 1)
                copied.draw(self.pdf)
                self.pdf.translate(50, 0)

            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 60)
            for i, l in enumerate(line_segments):
                copied = copy.deepcopy(l)
                copied.start_mark_line.length *= (i + 1)
                copied.relative_y -= (i * 3)
                copied.start_mark_line.add_text_label(str(copied.relative_y), font_size=8)
                copied.start_mark_line.add_text_label(str(copied.start_mark_line.length), font_size=8, placement='left')
                copied.straight_line.add_text_label(str(copied.straight_line.length), font_size=8, placement='below',
                                                    top_margin=2)
                copied.draw(self.pdf)
                self.pdf.translate(50, 0)

            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 90)
            for do in draw_object_rows:
                do.draw(self.pdf)
                self.pdf.translate(0, 20)

            self.pdf.write_to_path(pdf_path)

    def test_draw_column_of_row_of_segments(self):
        r = DrawObjectRow()
        r.add_draw_object(HorizontalLineSegment(30))
        r.add_draw_object(HorizontalLineSegment(10))
        r.add_draw_object(HorizontalLineSegment(20))
        c = DrawObjectColumn()
        c.add_draw_object(HorizontalLineSegment(60))
        c.add_draw_object(r)

        with self.file_path(path, 'column_of_row_of_segments', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_row_of_column_of_segments(self):
        c = DrawObjectColumn()
        c.add_draw_object(HorizontalLineSegment(30))
        c.add_draw_object(HorizontalLineSegment(10))
        c.add_draw_object(HorizontalLineSegment(20))
        r = DrawObjectRow()
        r.add_draw_object(c)

        with self.file_path(path, 'row_of_column_of_segments', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_column(self):
        self.pdf.translate_page_margins()
        draw_ruler(self.pdf, 'h')
        draw_ruler(self.pdf, 'v')
        self.pdf.translate(10, 10)
        c = self.column
        c.add_text_label(TextLabel('below label', placement='below', top_margin=3))
        c.draw(self.pdf)
        with self.file_path(path, 'column', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_travers_column(self):
        c = DrawObjectColumn()
        r = DrawObjectRow()
        c.add_draw_object(r)
        c_1 = c.add_draw_object(HorizontalLineSegment(length=10))
        r_1 = r.add_draw_object(HorizontalLineSegment(length=20))
        assert list(c.traverse()) == [c, r, r_1, c_1]

    def test_travers_row(self):
        r = DrawObjectRow()
        c = DrawObjectColumn()
        cc = DrawObjectColumn()

        r.add_draw_object(c)
        r_1 = r.add_draw_object(HorizontalLineSegment(length=10))
        r.add_draw_object(cc)
        rr = DrawObjectRow()
        c.add_draw_object(rr)
        rr_1 = rr.add_draw_object(HorizontalLineSegment(length=10))
        c_1 = c.add_draw_object(HorizontalLineSegment(length=10))
        cc_1 = cc.add_draw_object(HorizontalLineSegment(length=10))
        cc_2 = cc.add_draw_object(HorizontalLineSegment(length=10))
        assert list(r.traverse()) == [r, c, rr, rr_1, c_1, r_1, cc, cc_1, cc_2]

    def test_row_column_borders_margins_and_labels(self):
        def add_text_labels(do):
            if isinstance(do, HorizontalLineSegment):
                do = do.start_mark_line
            do.add_text_label(label=TextLabel('below label', placement='below'))
            do.add_text_label(label=TextLabel(f'rel_x: {round(do.relative_x)}', placement='below'))
            do.add_text_label(label=TextLabel(f'rel_x2: {round(do.get_relative_x2())}', placement='below'))
            do.add_text_label(label=TextLabel('above label', placement='above'))
            do.add_text_label(label=TextLabel(f'rel_y: {round(do.relative_y)}', placement='above'))
            do.add_text_label(label=TextLabel(f'rel_y2: {round(do.get_relative_y2())}', placement='above'))
            do.add_text_label(label=TextLabel(f'left label', placement='left'))
            do.add_text_label(label=TextLabel(f'left label', placement='left'))
            do.add_text_label(label=TextLabel(f'left label', placement='left'))
            for tl in do.get_text_labels():
                tl.font_size = 8

        hls = HorizontalLineSegment(length=20)
        hls.start_mark_line.length = 10

        vls = VerticalLineSegment(length=15)
        vls.start_mark_line.length = vls.end_mark_line.length = 10

        control_hls = copy.deepcopy(hls)
        control_hls.top_margin = 10
        control_hls.left_margin = 20
        control_hls.bottom_margin = 20

        add_text_labels(control_hls)
        control_hls.straight_line.add_text_label('control_hsl')

        r = DrawObjectRow(show_borders=True, show_margins=True)
        r.relative_y = 10
        first_hls = copy.deepcopy(hls)
        first_hls.left_margin = 5
        second_hls = copy.deepcopy(hls)
        second_hls.start_mark_line.length *= 0.5
        second_hls.end_mark_line.show = True

        r.add_draw_object(first_hls)
        r.add_draw_object(second_hls)

        first_vls = copy.deepcopy(vls)
        second_vls = copy.deepcopy(vls)

        second_vls.end_mark_line.show = first_vls.end_mark_line.show = True
        first_vls.left_margin = 10
        first_vls.right_margin = 5
        r.add_draw_object(first_vls)
        r.add_draw_object(second_vls)

        r.top_margin = 10
        r.left_margin = 20
        r.bottom_margin = 20

        add_text_labels(r)

        c = DrawObjectColumn(show_borders=True, show_margins=True)
        first_hls = copy.deepcopy(hls)
        second_hls = copy.deepcopy(hls)
        first_hls.bottom_margin = 10
        c.add_draw_object(first_hls)
        c.add_draw_object(second_hls)
        c.top_margin = 10
        c.left_margin = 20

        add_text_labels(c)

        main_column = DrawObjectColumn()
        main_column.add_draw_object(control_hls)
        main_column.add_draw_object(r)
        main_column.add_draw_object(c)

        with self.file_path(path, 'borders_margins_and_labels', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v')
            draw_ruler(self.pdf, mode='h')
            self.pdf.translate(20, 20)
            main_column.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    # def test_complex_column(self):
    #     c1 = DrawObjectColumn()
    #     hl1 = HorizontalSegmentedLine([10, 20, 30, 40])
    #     c1.add_draw_object(hl1)
    #     first_row = DrawObjectRow()
    #     second_row = DrawObjectRow()
    #     c1.add_draw_object(first_row)
    #     c1.add_draw_object(second_row)
    #
    #     c2 = DrawObjectColumn()
    #     first_row.add_draw_object(c2)
    #     hl2 = HorizontalSegmentedLine([40, 30, 20, 10])
    #     c2.add_draw_object(hl2)
    #     c2.add_draw_object(second_row)
    #
    #     c3 = DrawObjectColumn()
    #     second_row.add_draw_object(c3)
    #     hl3 = HorizontalSegmentedLine([5, 10, 15, 20])
    #     hl4 = HorizontalSegmentedLine([20, 15, 10, 5])
    #     c3.add_draw_object(hl3)
    #     c3.add_draw_object(hl4)
    #
    #     c = DrawObjectColumn()
    #     c.add_draw_object(c1)
    #     hl5 = HorizontalSegmentedLine([50, 40, 30, 20, 10])
    #     c.add_draw_object(hl5)
    #
    #     hl1.bottom_margin = 10
    #     hl2.position = (30, 20)
    #     hl2.position = (10, 20)
    #     hl3.position = (40, 50)
    #     hl4.position = (20, 10)
    #
    #     hl1.add_text_label('hl1', placement='left')
    #     hl2.add_text_label('hl2', placement='left')
    #     hl3.add_text_label('hl3', placement='left')
    #     hl4.add_text_label('hl4', placement='left')
    #     hl5.add_text_label('hl5', placement='left')
    #
    #     with self.file_path(path, 'complex_column', 'pdf') as pdf_path:
    #         self.pdf.translate_page_margins()
    #         draw_ruler(self.pdf, mode='v', first_label=-1)
    #         draw_ruler(self.pdf, mode='h', first_label=-1)
    #         self.pdf.translate(20, 20)
    #         c.draw(self.pdf)
    #         self.pdf.write_to_path(pdf_path)

    def test_two_simple_lines_column_draw(self):
        c = create_simple_column([StraightLine('h', 30), StraightLine('h', 30)])

        with self.file_path(path, 'two_simple_lines_column', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v', first_label=-1)
            draw_ruler(self.pdf, mode='h', first_label=-1)
            self.pdf.translate(10, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_simple_and_segmented_lines_in_columns(self):
        control1 = HorizontalSegmentedLine([10, 20])
        control1.margins = (10, 10, 10, 10)
        control2 = StraightLine('h', 30)
        control2.margins = (10, 10, 10, 10)

        r = DrawObjectRow()
        c1 = create_simple_column([StraightLine('h', 30), StraightLine('h', 30)])
        c1.right_margin = 10
        c2 = create_simple_column([HorizontalSegmentedLine([10, 20]), HorizontalSegmentedLine([10, 20])])
        for c in [c1, c2]:
            r.add_draw_object(c)

        with self.file_path(path, 'simple_and_segmented_lines_in_columns', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v', first_label=-1)
            draw_ruler(self.pdf, mode='h', first_label=-1)
            self.pdf.translate(10, 10)
            control1.draw(self.pdf)
            self.pdf.translate(50, 0)
            control2.draw(self.pdf)
            self.pdf.translate(50, 0)
            r.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_two_horizontal_segmented_lines_column_draw(self):
        c = create_simple_column([HorizontalSegmentedLine([10, 20]), HorizontalSegmentedLine([10, 20])])

        with self.file_path(path, 'two_horizontal_segmented_lines_column', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v', first_label=-1)
            draw_ruler(self.pdf, mode='h', first_label=-1)
            self.pdf.translate(10, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_relative_y_inside_column_draw(self):
        c = DrawObjectColumn(show_borders=True, show_margins=True)
        hsl = HorizontalSegmentedLine([10, 20, 30])
        hsl.relative_y = 20
        hsl.margins = (10, 0, 20, 0)
        c.add_draw_object(hsl)

        line = StraightLine(length=60, mode='h')
        c.add_draw_object(line)
        with self.file_path(path, 'relative_y_inside_column', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v', first_label=-1)
            draw_ruler(self.pdf, mode='h', first_label=-1)
            self.pdf.translate(10, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
