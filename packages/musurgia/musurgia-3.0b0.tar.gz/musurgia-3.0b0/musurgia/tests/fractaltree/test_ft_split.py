from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree


class TestFtSplit(TestCase):
    def setUp(self):
        self.ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2),
                              permutation_index=(1, 1))
        self.ft.add_layer()
        self.first_child = self.ft.get_children()[0]

    def test_two(self):
        s = self.first_child.split(1, 1)
        actual = [x.get_value() for x in s]
        expected = [self.first_child.get_value() / 2, self.first_child.get_value() / 2]
        self.assertEqual(expected, actual)

    def test_three(self):
        s = self.first_child.split(1, 1, 1)
        actual = [x.get_value() for x in s]
        expected = [self.first_child.get_value() / 3, self.first_child.get_value() / 3,
                    self.first_child.get_value() / 3]
        self.assertEqual(expected, actual)

    def test_child_is_not_leaf(self):
        self.first_child.split(1, 1, 1)
        self.assertFalse(self.first_child.is_leaf)

    def test_split_is_leaf(self):
        s = self.first_child.split(1, 1, 1)
        actual = [x.is_leaf for x in s]
        expected = [True, True, True]
        self.assertEqual(expected, actual)
