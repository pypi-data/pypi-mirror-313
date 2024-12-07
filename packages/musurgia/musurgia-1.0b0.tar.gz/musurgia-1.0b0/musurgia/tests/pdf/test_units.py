from unittest import TestCase

from musurgia.musurgia_exceptions import PdfAttributeError
from musurgia.musurgia_types import MusurgiaTypeError
from musurgia.pdf.drawobject import ClippingArea
from musurgia.pdf.labeled import TextLabel, Labeled
from musurgia.pdf.line import MarkLine, StraightLine
from musurgia.pdf.ruler import HorizontalRuler
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdfunit import PdfUnit
from musurgia.pdf.text import Text
from musurgia.tests.utils_for_tests import DummyMaster


class TestClippingArea(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.ruler = HorizontalRuler(length=2000)
        self.ca = ClippingArea(self.pdf, self.ruler)

    def test_get_row_height(self):
        x = self.ruler.get_height()
        assert self.ca.get_row_height() == x
        self.ruler.top_margin = 10
        assert self.ca.get_row_height() == x + 10

    def test_no_pdf(self):
        with self.assertRaises(PdfAttributeError):
            ClippingArea(pdf=None, draw_object=self.ruler).get_row_width()

        with self.assertRaises(PdfAttributeError):
            ClippingArea(pdf=None, draw_object=self.ruler).draw()


class TestPdfUnit(TestCase):
    def test_setting_global_unit(self):
        assert PdfUnit._DEFAULT_UNIT == 'mm'
        assert PdfUnit.GLOBAL_UNIT == 'mm'
        PdfUnit.GLOBAL_UNIT = 'pt'
        assert PdfUnit.GLOBAL_UNIT == 'pt'
        PdfUnit.reset()
        assert PdfUnit.GLOBAL_UNIT == 'mm'
        with self.assertRaises(MusurgiaTypeError):
            PdfUnit.GLOBAL_UNIT = 'bla'


class TestLabeled(TestCase):
    def test_no_master_error(self):
        t = TextLabel('bla')
        t.placement = 'above'
        with self.assertRaises(AttributeError):
            assert t.placement == 'above'

    def test_false_master_errr(self):
        t = TextLabel('bla', master=DummyMaster())
        l = Labeled()
        with self.assertRaises(AttributeError):
            l.add_text_label(t)
        t.master = l
        l.add_text_label(t)
        assert t.master == l

    def test_get_slave_position_wrong_type_or_slave_with_wrong_master(self):
        t = TextLabel('bla', master=DummyMaster())
        l = Labeled()
        with self.assertRaises(AttributeError):
            l.get_slave_position(t, 'x')
        with self.assertRaises(TypeError):
            l.get_slave_position('slave', 'y')
        t.master = l
        assert l.get_slave_position(t, 'x') == 0


class TestSlaveErrors(TestCase):
    def test_no_master_error(self):
        ml = MarkLine(placement='start', mode='horizontal')
        with self.assertRaises(AttributeError):
            ml.relative_x

        with self.assertRaises(AttributeError):
            ml.relative_y

        with self.assertRaises(AttributeError):
            ml.top_margin

        with self.assertRaises(AttributeError):
            ml.left_margin

        with self.assertRaises(AttributeError):
            ml.bottom_margin

        with self.assertRaises(AttributeError):
            ml.right_margin

    def test_wrong_master(self):
        ml = MarkLine(placement='start', mode='horizontal')
        with self.assertRaises(TypeError):
            ml.master = TextLabel('something')


class TestNoPdfError(TestCase):
    def test_draw_with_no_pdf_error(self):
        t = Text('bla')
        with self.assertRaises(TypeError):
            t.draw(pdf=None)


class TestMarginsPositions(TestCase):
    def test_set_get_margins(self):
        l = StraightLine(mode='h', length=10)
        l.margins = (1, 2, 3, 4)
        assert l.get_margins() == {'bottom': 3.0, 'left': 4.0, 'right': 2.0, 'top': 1.0}
        assert l.margins == (1, 2, 3, 4)

    def test_set_get_positions(self):
        l = StraightLine(mode='h', length=10)
        l.positions = (10, 20)
        assert l.get_positions() == {'x': 10.0, 'y': 20.0}
        assert l.positions == (10, 20)
