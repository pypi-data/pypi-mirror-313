from musurgia.pdf.pdfunit import PdfUnit
from musurgia.tests.utils_for_tests import PdfTestCase


class TestPdfK(PdfTestCase):
    def test_get_k(self):
        actual = PdfUnit.get_k()
        expected = 2.834645669291339
        self.assertEqual(expected, actual)

    def test_new_unit(self):

        PdfUnit.GLOBAL_UNIT = 'cm'
        actual = PdfUnit.get_k()
        expected = 28.346456692913385
        self.assertEqual(expected, actual)
        PdfUnit.reset()

    def test_change_unit(self):
        PdfUnit.change('mm')
        old_k = PdfUnit.get_k()
        PdfUnit.change('cm')
        new_k = PdfUnit.get_k()
        actual = new_k / old_k
        expected = 10
        self.assertAlmostEqual(expected, actual)
        PdfUnit.reset()


