import copy
from unittest import TestCase
from musurgia.pdf import HorizontalLineSegment, StraightLine


class TestDeepCopy(TestCase):
    def test_horizontal_line_segment(self):
        hls = HorizontalLineSegment(length=10)
        hls.bottom_margin = 30
        hls.relative_x = 20
        hls.start_mark_line.add_text_label('start', font_size=15, bottom_margin=50)
        hls.end_mark_line.add_text_label('stop', font_size=25, position='below', top_margin=40)

        copied = copy.deepcopy(hls)
        assert copied != hls
        assert copied.length == hls.length
        assert copied.mode == hls.mode
        assert copied.straight_line != hls.straight_line
        assert copied.start_mark_line != hls.start_mark_line
        assert copied.end_mark_line != hls.end_mark_line
        assert copied.get_positions() == hls.get_positions()
        assert copied.get_margins() == hls.get_margins()
        start_mark_text_label = hls.start_mark_line.get_text_labels()[0]
        copied_start_mark_text_label = copied.start_mark_line.get_text_labels()[0]
        end_mark_text_label = hls.end_mark_line.get_text_labels()[0]
        copied_end_mark_text_label = copied.end_mark_line.get_text_labels()[0]

        assert start_mark_text_label != copied_start_mark_text_label
        assert end_mark_text_label != copied_end_mark_text_label
        assert start_mark_text_label.get_positions() == copied_start_mark_text_label.get_positions()
        assert end_mark_text_label.get_positions() == copied_end_mark_text_label.get_positions()
        assert start_mark_text_label.get_margins() == copied_start_mark_text_label.get_margins()
        assert end_mark_text_label.get_margins() == copied_end_mark_text_label.get_margins()

        assert start_mark_text_label.value == copied_start_mark_text_label.value
        assert end_mark_text_label.value == copied_end_mark_text_label.value

    def test_margins_and_positions(self):
        line = StraightLine(length=20, mode='h')
        line.margins = (10, 20, 30, 40)
        line.positions = (5, 10)

        copied = copy.deepcopy(line)

        line.margins = (1, 2, 3, 4)
        line.positions = (1, 2)

        assert copied.length == 20
        assert copied.mode == 'h'
        assert copied.margins == (10, 20, 30, 40)
        assert copied.positions == (5, 10)

        copied.length = 10
        copied.margins = (0, 0, 0, 0)
        copied.positions = (0, 0)
        copied.mode = 'v'

        assert copied.length == 10
        assert copied.mode == 'v'
        assert copied.margins == (0, 0, 0, 0)
        assert copied.positions == (0, 0)

        assert line.length == 20
        assert line.mode == 'h'
        assert line.margins == (1, 2, 3, 4)
        assert line.positions == (1, 2)
