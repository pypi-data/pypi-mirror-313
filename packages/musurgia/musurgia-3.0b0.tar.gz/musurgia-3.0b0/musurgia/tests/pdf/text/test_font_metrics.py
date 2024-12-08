from pathlib import Path

import matplotlib as mpl
import pytest

from musurgia.pdf.font import _make_afm_path_dictionary
from musurgia.tests.utils_for_tests import PdfTestCase

afm_path = Path(mpl.get_data_path(), 'fonts', 'afm', 'ptmr8a.afm')


class Test(PdfTestCase):
    def test_afm_dict(self):
        actual = sorted(list(_make_afm_path_dictionary().keys()))
        expected = [
            ('Computer Modern', 'medium', 'italic'),
            ('Computer Modern', 'medium', 'regular'),
            ('Courier', 'bold', 'italic'),
            ('Courier', 'bold', 'regular'),
            ('Courier', 'medium', 'italic'),
            ('Courier', 'medium', 'regular'),
            ('Helvetica', 'bold', 'italic'),
            ('Helvetica', 'bold', 'regular'),
            ('Helvetica', 'light', 'italic'),
            ('Helvetica', 'light', 'regular'),
            ('Helvetica', 'medium', 'italic'),
            ('Helvetica', 'medium', 'regular'),
            ('ITC Avant Garde Gothic', 'book', 'italic'),
            ('ITC Avant Garde Gothic', 'book', 'regular'),
            ('ITC Avant Garde Gothic', 'demi', 'italic'),
            ('ITC Avant Garde Gothic', 'demi', 'regular'),
            ('ITC Bookman', 'demi', 'italic'),
            ('ITC Bookman', 'demi', 'regular'),
            ('ITC Bookman', 'light', 'italic'),
            ('ITC Bookman', 'light', 'regular'),
            ('ITC Zapf Chancery', 'medium', 'italic'),
            ('ITC Zapf Dingbats', 'medium', 'regular'),
            ('New Century Schoolbook', 'bold', 'italic'),
            ('New Century Schoolbook', 'bold', 'regular'),
            ('New Century Schoolbook', 'medium', 'italic'),
            ('New Century Schoolbook', 'roman', 'regular'),
            ('Palatino', 'bold', 'italic'),
            ('Palatino', 'bold', 'regular'),
            ('Palatino', 'medium', 'italic'),
            ('Palatino', 'roman', 'regular'),
            ('Symbol', 'medium', 'regular'),
            ('Times', 'bold', 'italic'),
            ('Times', 'bold', 'regular'),
            ('Times', 'medium', 'italic'),
            ('Times', 'roman', 'regular'),
            ('Utopia', 'bold', 'italic'),
            ('Utopia', 'bold', 'regular'),
            ('Utopia', 'regular', 'italic'),
            ('Utopia', 'regular', 'regular')]
        self.assertEqual(expected, actual)

    @pytest.mark.skip(reason="ci fails due to OS differences")
    def test_afm_dict_families(self):
        actual = list(dict.fromkeys([key[0] for key in _make_afm_path_dictionary().keys()]))
        expected = ['New Century Schoolbook',
                    'Times',
                    'ITC Bookman',
                    'Helvetica',
                    'ITC Avant Garde Gothic',
                    'Palatino',
                    'Computer Modern',
                    'Symbol',
                    'ITC Zapf Dingbats',
                    'Utopia',
                    'Courier',
                    'ITC Zapf Chancery']
        self.assertEqual(expected, actual)

    def test_load_afm(self):
        afm = _make_afm_path_dictionary()['Times', 'medium', 'italic']
        actual = afm.get_familyname()
        expected = 'Times'
        self.assertEqual(expected, actual)

    @pytest.mark.skip(reason="ci fails due to OS differences: (7370.0, 741) != (6040.0, 741)")
    def test_width_height(self):
        afm = _make_afm_path_dictionary()['Helvetica', 'bold', 'italic']
        actual = afm.string_width_height('What the heck?')
        expected = (7370.0, 741)
        self.assertEqual(expected, actual)
