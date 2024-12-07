from pathlib import Path
from unittest import TestCase

from musurgia.musurgia_exceptions import RulerCannotSetLengthsError, SegmentedLineLengthsCannotBeSetError, \
    RulerLengthNotPositiveError
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.ruler import HorizontalRuler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestRuler(TestCase):
    def setUp(self) -> None:
        self.r = HorizontalRuler(length=10, unit=1, label_show_interval=5)

    def test_setting_length_and_lengths(self):
        with self.assertRaises(RulerCannotSetLengthsError):
            HorizontalRuler(lengths=[3, 2, 1], length=100)

        with self.assertRaises(SegmentedLineLengthsCannotBeSetError):
            self.r.lengths = [3, 2, 1]

    def test_length(self):
        hsl = HorizontalRuler(length=0)
        assert hsl.get_length() == 0
        with self.assertRaises(AttributeError):
            hsl.length = 1
        with self.assertRaises(RulerLengthNotPositiveError):
            HorizontalRuler(length=-100)

    def test_get_labels(self):
        assert [l.value for l in self.r.get_markline_text_labels()] == ['0', '5', '10']
        assert [l.font_size for l in self.r.get_markline_text_labels()] == [10, 10, 10]
        assert [l.font_weight for l in self.r.get_markline_text_labels()] == ['medium', 'medium', 'medium']

    def test_change_labels(self):
        self.r.change_labels(font_size=6, font_weight='bold')
        assert [l.value for l in self.r.get_markline_text_labels()] == ['0', '5', '10']
        assert [l.font_size for l in self.r.get_markline_text_labels()] == [6, 6, 6]
        assert [l.font_weight for l in self.r.get_markline_text_labels()] == ['bold', 'bold', 'bold']

        self.r.change_labels(condition=lambda label: True if self.r.segments.index(label.master.master) == 5 else False,
                             font_size=8)
        assert [l.font_size for l in self.r.get_markline_text_labels()] == [6, 8, 6]

    def test_getter_setters_errors(self):
        with self.assertRaises(AttributeError):
            self.r.length
        with self.assertRaises(AttributeError):
            self.r.length = 2

        with self.assertRaises(AttributeError):
            self.r.unit
        with self.assertRaises(AttributeError):
            self.r.unit = 2

        with self.assertRaises(AttributeError):
            self.r.show_first_label
        with self.assertRaises(AttributeError):
            self.r.show_first_label = 2

        with self.assertRaises(AttributeError):
            self.r.label_show_interval
        with self.assertRaises(AttributeError):
            self.r.label_show_interval = 2

        with self.assertRaises(AttributeError):
            self.r.first_label
        with self.assertRaises(AttributeError):
            self.r.first_label = 2


class TestRulerPdf(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_h_ruler(self):
        r = HorizontalRuler(length=50)
        with self.file_path(path, 'h_ruler', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            r.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_h_ruler_A4(self):
        with self.file_path(path, 'h_ruler_A4', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='h')
            self.pdf.write_to_path(pdf_path)

    def test_both_rulers_A4(self):
        with self.file_path(path, 'both_rulers_A4', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='h')
            draw_ruler(self.pdf, mode='v')
            self.pdf.write_to_path(pdf_path)

    def test_rulers_borders_and_margins(self):
        with self.file_path(path, 'both_rulers_borders_and_margins', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='h', show_borders=True, show_margins=True)
            draw_ruler(self.pdf, mode='v', show_borders=True, show_margins=True)
            self.pdf.write_to_path(pdf_path)
