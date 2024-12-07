import os
from unittest import TestCase

from fractions import Fraction

from musurgia.fractal.fractaltree import FractalTree

path = os.path.abspath(__file__).split('.')[0]


class TestAddLayer(TestCase):
    def setUp(self):
        self.ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2),
                              permutation_index=(1, 1))

    def test_two_layers(self):
        self.ft.add_layer()
        self.ft.add_layer()
        self.assertEqual(self.ft.get_number_of_layers(), 2)
        self.assertEqual([[1, 2, 3], [3, 1, 2], [2, 3, 1]],
                         self.ft.get_leaves(key=lambda node: node.get_fractal_order()))
        self.assertEqual([[0.83, 1.67, 2.5], [0.83, 0.28, 0.56], [1.11, 1.67, 0.56]],
                         self.ft.get_leaves(key=lambda node: round(float(node.get_value()), 2)))

    def test_with_condition(self):
        self.ft.add_layer()
        self.ft.add_layer()
        self.ft.add_layer(lambda node: node.get_fractal_order() != 1, lambda node: node.get_value() > 0.6)
        self.assertEqual([[1, [1, 2, 3], [3, 1, 2]], [[3, 1, 2], 1, 2], [[1, 2, 3], [3, 1, 2], 1]],
                         self.ft.get_leaves(key=lambda node: node.get_fractal_order()))

    def test_child_add_layer(self):
        self.ft.add_layer()
        self.ft.get_children()[0].add_layer()
        expected = [[0.83, 1.67, 2.5], 1.67, 3.33]
        self.assertEqual(expected, self.ft.get_leaves(key=lambda leaf: round(float(leaf.get_value()), 2)))
