from musurgia.pdf.line import VerticalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.tests.utils_for_tests import PdfTestCase


class TestAbsoluteY(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_translate(self):
        self.pdf.translate(10, 30)
        self.pdf.translate(20, 10)
        actual = self.pdf.absolute_y
        expected = 40
        self.assertEqual(expected, actual)

    def test_draw_objects(self):
        vls = VerticalLineSegment(length=20)
        vls.draw(self.pdf)
        actual = self.pdf.absolute_y
        expected = 0
        self.assertEqual(expected, actual)

    def test_draw_objects_and_translate(self):
        vls = VerticalLineSegment(length=20)
        self.pdf.translate(10, 30)
        vls.draw(self.pdf)
        self.pdf.translate(20, 10)
        actual = self.pdf.absolute_y
        expected = 40
        self.assertEqual(expected, actual)

