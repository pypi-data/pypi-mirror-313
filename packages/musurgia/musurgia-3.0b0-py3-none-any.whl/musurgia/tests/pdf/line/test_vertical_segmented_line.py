from pathlib import Path

from musurgia.pdf.line import VerticalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestVerticalSegmentedLine(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.vsl = VerticalSegmentedLine(lengths=[10, 15, 20, 25])

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.vsl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_get_width(self):
        self.vsl.segments[1].start_mark_line.length = 5
        actual = self.vsl.get_width()
        expected = 5
        self.assertEqual(expected, actual)

    def test_align_segments(self):
        for index, sg in enumerate(self.vsl.segments):
            sg.start_mark_line.length += index * 5
        self.vsl.segments[-1].end_mark_line.length = self.vsl.segments[-1].start_mark_line.length + 5
        self.vsl.segments[-1].end_mark_line.show = True
        self.vsl._align_segments()
        for seg in self.vsl.segments:
            assert seg.relative_y >= 0
            assert seg.relative_x >= 0
        assert 0 in set([seg.relative_x for seg in self.vsl.segments])
