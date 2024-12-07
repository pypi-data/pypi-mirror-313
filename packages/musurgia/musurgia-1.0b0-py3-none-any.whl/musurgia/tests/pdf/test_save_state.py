from unittest import TestCase

from musurgia.pdf import Pdf
from musurgia.pdf.line import HorizontalLineSegment


class TestPdfSaveState(TestCase):
    def test_save_state(self):
        pdf = Pdf()
        assert (pdf.absolute_x, pdf.absolute_y) == (0, 0)
        pdf.translate_page_margins()
        assert (pdf.absolute_x, pdf.absolute_y) == (10, 10)
        pdf.translate(10, 10)
        assert (pdf.absolute_x, pdf.absolute_y) == (20, 20)
        line = HorizontalLineSegment(length=10, top_margin=10, bottom_margin=20)
        line.draw(pdf)
        assert (pdf.absolute_x, pdf.absolute_y) == (20, 20)

        with pdf.saved_state():
            pdf.translate(10, 10)

        assert (pdf.absolute_x, pdf.absolute_y) == (20, 20)
