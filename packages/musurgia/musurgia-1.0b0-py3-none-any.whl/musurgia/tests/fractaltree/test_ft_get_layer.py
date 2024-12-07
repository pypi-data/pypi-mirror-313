from fractions import Fraction
from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree


class TestGetLayer(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2),
                              permutation_index=(1, 1))

    def test_wrong_layer(self):
        with self.assertRaises(Exception):
            self.ft.get_layer(1)

    def test_layer_0(self):
        self.assertEqual(self.ft, self.ft.get_layer(0))

    def test_layer_1(self):
        self.ft.add_layer()
        self.assertEqual(self.ft.get_children(), self.ft.get_layer(1))

    def test_layer_1_of_3(self):
        for i in range(3):
            self.ft.add_layer()
        self.assertEqual(self.ft.get_children(), self.ft.get_layer(1))

    def test_layer_2_of_3(self):
        for i in range(3):
            self.ft.add_layer()
        result = [child.get_children() for child in self.ft.get_children()]

        self.assertEqual(result, self.ft.get_layer(2))

    def test_layer_3_of_3(self):
        for i in range(3):
            self.ft.add_layer()
        result = self.ft.get_leaves()

        self.assertEqual(result, self.ft.get_layer(3))

    def test_layer_wrong_layer_2(self):
        for i in range(3):
            self.ft.add_layer()

        with self.assertRaises(ValueError):
            self.ft.get_layer(4)

    def test_complex_layers(self):
        self.ft.add_layer()
        self.ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        self.ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        self.ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        self.ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        assert self.ft.get_layer(1, key=lambda node: node.get_fractal_order()) == [3, 1, 2]
        assert self.ft.get_layer(2, key=lambda node: node.get_fractal_order()) == [[1, 2, 3], 1, [2, 3, 1]]
        assert self.ft.get_layer(3, key=lambda node: node.get_fractal_order()) == [[1, [1, 2, 3], [3, 1, 2]], 1,
                                                                                   [[1, 2, 3], [3, 1, 2], 1]]
        assert self.ft.get_layer(4, key=lambda node: node.get_fractal_order()) == [
            [1, [1, [3, 1, 2], [2, 3, 1]], [[2, 3, 1], 1, [3, 1, 2]]],
            1,
            [[1, [1, 2, 3], [3, 1, 2]], [[3, 1, 2], 1, [1, 2, 3]], 1]]

    def test_layer_values(self):
        self.ft.add_layer()
        self.ft.add_layer()
        # print(self.ft.get_tree_representation(key=lambda node: round(float(node.get_value()), 2)))
        assert self.ft.get_tree_representation(key=lambda node: round(float(node.get_value()), 2)) == """└── 10.0
    ├── 5.0
    │   ├── 0.83
    │   ├── 1.67
    │   └── 2.5
    ├── 1.67
    │   ├── 0.83
    │   ├── 0.28
    │   └── 0.56
    └── 3.33
        ├── 1.11
        ├── 1.67
        └── 0.56
"""
