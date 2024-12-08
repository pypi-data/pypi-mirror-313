from pathlib import Path
from unittest import TestCase

from musurgia.musurgia_exceptions import RelativePositionNotSettableError
from musurgia.pdf.line import SlaveStraightLine, StraightLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase, DummyMaster

path = Path(__file__)


class TestStraightLine(TestCase):
    def setUp(self):
        self.sl_h = StraightLine(length=10, mode='h', relative_x=10, relative_y=20)
        self.sl_v = StraightLine(length=10, mode='v', relative_x=30, relative_y=40)

    def test_infos(self):
        assert self.sl_h.relative_x == 10
        assert self.sl_h.relative_y == 20
        assert self.sl_v.relative_x == 30
        assert self.sl_v.relative_y == 40

        assert self.sl_h.get_relative_x2() == 20
        assert self.sl_h.get_relative_y2() == 20
        assert self.sl_v.get_relative_x2() == 30
        assert self.sl_v.get_relative_y2() == 50

        assert self.sl_h.get_height() == 0
        assert self.sl_h.get_width() == 10
        assert self.sl_v.get_height() == 10
        assert self.sl_v.get_width() == 0

    def test_width_and_height(self):
        sl = StraightLine('h', 30)
        sl.margins = (10, 10, 10, 10)
        assert sl.get_width() == 50
        assert sl.get_height() == 20

class TestStraightLineDraw(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        h_lines = [StraightLine(length=10, mode='h') for _ in range(3)]
        v_lines = [StraightLine(length=10, mode='v') for _ in range(3)]
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            for l in h_lines:
                l.draw(self.pdf)
                self.pdf.translate(20, 0)
            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(10, 20)
            for l in v_lines:
                l.draw(self.pdf)
                self.pdf.translate(20, 0)
            self.pdf.write_to_path(pdf_path)


class TestSlaveStraightLine(TestCase):
    def setUp(self) -> None:
        self.master = DummyMaster()
        self.sl = SlaveStraightLine(mode='h', length=20, name='straight_test', master=self.master)

    def test_position_not_settable(self):
        with self.assertRaises(RelativePositionNotSettableError):
            SlaveStraightLine(relative_x=0, mode='h', length=20, name='straight_test', master=self.master)
        with self.assertRaises(RelativePositionNotSettableError):
            self.sl.relative_x = 10

    def test_relative_x(self):
        actual = self.sl.relative_x
        expected = self.master.get_slave_position(self.sl, 'x')
        self.assertEqual(expected, actual)

    def test_get_relative_x(self):
        actual = self.sl.get_relative_x2()
        expected = self.sl.relative_x + self.sl.length
        self.assertEqual(expected, actual)

    def test_get_width(self):
        actual = self.sl.get_width()
        expected = self.sl.left_margin + self.sl.length + self.sl.right_margin
        self.assertEqual(expected, actual)

    def test_get_height(self):
        actual = self.sl.get_height()
        expected = self.sl.top_margin + self.sl.bottom_margin
        self.assertEqual(expected, actual)

    pass


class TestSlaveStraightLineDraw(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.master = DummyMaster()
        self.sl = SlaveStraightLine(mode='h', length=20, name='straight_test', master=self.master)


    def test_draw(self):
        with self.file_path(path, 'draw_slave', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.sl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
