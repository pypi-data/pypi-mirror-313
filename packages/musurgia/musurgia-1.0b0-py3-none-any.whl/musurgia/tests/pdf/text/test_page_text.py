from pathlib import Path

from musurgia.musurgia_exceptions import RelativePositionNotSettableError
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import PageText
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestPageText(PdfTestCase):
    def setUp(self):
        self.pdf = Pdf()

    def test_defaults(self):
        pt = PageText(value='nothing')
        assert pt.v_position == 'top'
        assert pt.h_position == 'left'
        assert pt.get_margins() == {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}
        assert pt.get_positions() == {'x': 0.0, 'y': 0.0}

    def test_positions(self):
        pt = PageText(value='left top')
        pt.draw(self.pdf)
        pt = PageText(value='center top', h_position='center')
        pt.draw(self.pdf)
        pt = PageText(value='right top', h_position='right')
        pt.draw(self.pdf)

        pt = PageText(value='left bottom', v_position='bottom')
        pt.draw(self.pdf)
        pt = PageText(value='center bottom', h_position='center', v_position='bottom')
        pt.draw(self.pdf)
        pt = PageText(value='right bottom', h_position='right', v_position='bottom')
        pt.draw(self.pdf)

        with self.file_path(path, 'positions', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_setting_position_error(self):
        with self.assertRaises(RelativePositionNotSettableError):
            PageText(value='left top', relative_x=10)
        with self.assertRaises(RelativePositionNotSettableError):
            PageText(value='something').relative_y = 10

