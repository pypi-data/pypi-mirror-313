from pathlib import Path
from unittest import TestCase

from musurgia.musurgia_exceptions import TimeRulerCannotSetLength
from musurgia.pdf import Pdf
from musurgia.pdf.ruler import TimeRuler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestTimeRuler(TestCase):
    def setUp(self) -> None:
        self.tr = TimeRuler(duration=200, unit=2, shrink_factor=0.6, mark_line_size=5)

    def test_duration(self):
        assert self.tr.get_length() == 400
        assert self.tr.get_duration() == 200
        assert self.tr.get_unit() == 2

    def test_length_errors(self):
        with self.assertRaises(TimeRulerCannotSetLength):
            TimeRuler(duration=10, length=100)
        with self.assertRaises(AttributeError):
            self.tr.length = 20

    def test_shrink(self):
        assert self.tr.shrink_factor == 0.6
        assert self.tr.mark_line_size == 5
        for i, start_mark_line in enumerate([seg.start_mark_line for seg in self.tr.segments]):
            if i % 10 == 0:
                assert start_mark_line.length == 5
            else:
                assert start_mark_line.length == 3

        self.tr.mark_line_size = 10
        self.tr.shrink_factor = 0.5
        for i, start_mark_line in enumerate([seg.start_mark_line for seg in self.tr.segments]):
            if i % 10 == 0:
                assert start_mark_line.length == 10
            else:
                assert start_mark_line.length == 5
        assert self.tr.segments[-1].end_mark_line.length == 10

        tr = TimeRuler(duration=200, unit=2, label_show_interval=3, shrink_factor=0.5, mark_line_size=10)
        for i, start_mark_line in enumerate([seg.start_mark_line for seg in tr.segments]):
            if i % 3 == 0:
                assert start_mark_line.length == 10
            else:
                assert start_mark_line.length == 5

    def test_last_segment_end_mark_line(self):
        tr = TimeRuler(duration=200, mark_line_size=10, shrink_factor=0.5)
        assert tr.segments[-1].end_mark_line.length == 10
        tr = TimeRuler(duration=201, mark_line_size=10, shrink_factor=0.5)
        assert tr.segments[-1].end_mark_line.length == 5


class TestTimeRulerPdf(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_time_ruler(self):
        r = TimeRuler(duration=200, unit=2, label_show_interval=10, clock_mode='ms')
        r.change_labels(font_size=6, font_weight='bold')
        r.bottom_margin = 15
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            r.clipped_draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
