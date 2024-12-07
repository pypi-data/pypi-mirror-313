from unittest import TestCase

from musurgia.fractal.fractaltree import PermutationIndexCalculater
from musurgia.musurgia_exceptions import PermutationIndexCalculaterNoParentIndexError


class TestFtUnit(TestCase):

    def test_get_index_error(self):
        pic = PermutationIndexCalculater(size=10)
        with self.assertRaises(PermutationIndexCalculaterNoParentIndexError):
            pic.get_index(1)
        pic = PermutationIndexCalculater(size=10, parent_index=(2, 3))
        with self.assertRaises(ValueError):
            pic.get_index(11)

