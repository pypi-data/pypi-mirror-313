from unittest import TestCase

from fractions import Fraction

from musurgia.fractal.fractaltree import FractalTree
from musurgia.tests.utils_for_tests import node_info
from musurgia.utils import flatten


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2),
                              permutation_index=(1, 1))

    def test_change_root_value_without_children(self):
        self.ft.change_value(15)
        self.assertEqual(15, self.ft.get_value())

    def test_change_root_value_with_children(self):
        self.ft.add_layer()
        self.ft.change_value(15)
        self.assertEqual(15, self.ft.get_value())
        self.assertEqual(15, sum([child.get_value() for child in self.ft.get_children()]))
        self.assertEqual([Fraction(15, 2), Fraction(5, 2), Fraction(5, 1)],
                         [child.get_value() for child in self.ft.get_children()])

    def test_change_leaf_value(self):
        self.ft.add_layer()
        self.ft.get_children()[0].change_value(10)
        self.assertEqual(15, self.ft.get_value())
        self.assertEqual(15, sum([child.get_value() for child in self.ft.get_layer(1)]))
        self.assertEqual([Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)],
                         [child.get_value() for child in self.ft.get_children()])

    def test_two_layers_change_child_value(self):
        self.ft.add_layer()
        self.ft.add_layer()
        self.ft.get_children()[0].change_value(10)
        assert self.ft.get_value() == 15
        assert sum(flatten(self.ft.get_layer(1, key=lambda node: node.get_value()))) == 15
        assert sum(flatten(self.ft.get_layer(2, key=lambda node: node.get_value()))) == 15

    def test_with_remove(self):
        self.ft.add_layer()
        first_child = self.ft.get_children()[0]
        first_child.add_layer()
        first_child.add_layer()
        # print(self.ft.get_tree_representation(node_info))
        assert self.ft.get_tree_representation(node_info) == """└── None: (1, 1): 10.0
    ├── 3: (2, 1): 5.0
    │   ├── 1: (3, 1): 0.83
    │   │   ├── 2: (1, 1): 0.28
    │   │   ├── 3: (1, 2): 0.42
    │   │   └── 1: (1, 3): 0.14
    │   ├── 2: (3, 2): 1.67
    │   │   ├── 1: (2, 1): 0.28
    │   │   ├── 2: (2, 2): 0.56
    │   │   └── 3: (2, 3): 0.83
    │   └── 3: (3, 3): 2.5
    │       ├── 3: (3, 1): 1.25
    │       ├── 1: (3, 2): 0.42
    │       └── 2: (3, 3): 0.83
    ├── 1: (2, 2): 1.67
    └── 2: (2, 3): 3.33
"""
        first_child.remove(first_child.get_children()[1])
        # print(self.ft.get_tree_representation(node_info))
        assert self.ft.get_tree_representation(node_info) == """└── None: (1, 1): 10.0
    ├── 3: (2, 1): 5.0
    │   ├── 1: (3, 1): 0.83
    │   │   ├── 2: (1, 1): 0.28
    │   │   ├── 3: (1, 2): 0.42
    │   │   └── 1: (1, 3): 0.14
    │   └── 3: (3, 3): 2.5
    │       ├── 3: (3, 1): 1.25
    │       ├── 1: (3, 2): 0.42
    │       └── 2: (3, 3): 0.83
    ├── 1: (2, 2): 1.67
    └── 2: (2, 3): 3.33
"""
        first_child.get_children()[0].change_value(2.5)
        # print(self.ft.get_tree_representation(node_info))
        assert self.ft.get_tree_representation(node_info) == """└── None: (1, 1): 10.0
    ├── 3: (2, 1): 5.0
    │   ├── 1: (3, 1): 2.5
    │   │   ├── 2: (1, 1): 0.83
    │   │   ├── 3: (1, 2): 1.25
    │   │   └── 1: (1, 3): 0.42
    │   └── 3: (3, 3): 2.5
    │       ├── 3: (3, 1): 1.25
    │       ├── 1: (3, 2): 0.42
    │       └── 2: (3, 3): 0.83
    ├── 1: (2, 2): 1.67
    └── 2: (2, 3): 3.33
"""
