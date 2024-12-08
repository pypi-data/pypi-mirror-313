from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree
from musurgia.tests.utils_for_tests import node_info_with_permutation_order


class TestGenerateChildrenReduce(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2),
                              permutation_index=(1, 1))

    def test_number_of_children_0(self):
        self.ft.generate_children(number_of_children=0)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [None]

    def test_number_of_children_1(self):
        self.ft.generate_children(number_of_children=1)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [3]

    def test_number_of_children_2(self):
        self.ft.generate_children(number_of_children=2)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [3, 2]

    def test_number_of_children_3(self):
        self.ft.generate_children(number_of_children=3)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [3, 1, 2]

    def test_with_children_error(self):
        self.ft.generate_children(number_of_children=3)
        with self.assertRaises(ValueError):
            self.ft.generate_children(number_of_children=1)

    def test_tuple_number_of_children_1(self):
        self.ft.generate_children(number_of_children=(1, 1, 1))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[3], [3], [3]]

    def test_tuple_number_of_children_2(self):
        self.ft.generate_children(number_of_children=(2, 2, 2))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[2, 3], [3, 2], [2, 3]]

    def test_tuple_number_of_children_3(self):
        self.ft.generate_children(number_of_children=(3, 3, 3))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[1, 2, 3], [3, 1, 2], [2, 3, 1]]

    def test_tuple_number_of_children_mixed_1_to_3(self):
        self.ft.generate_children(number_of_children=(1, 2, 3))
        # print(self.ft.get_tree_representation(node_info_with_permutation_order))
        assert self.ft.get_tree_representation(node_info_with_permutation_order) == """└── None: (1, 1): (3, 1, 2): 10.0
    ├── 3: (2, 1): (1, 2, 3): 5.0
    │   ├── 1: (3, 1): (2, 3, 1): 0.83
    │   ├── 2: (3, 2): (1, 2, 3): 1.67
    │   └── 3: (3, 3): (3, 1, 2): 2.5
    ├── 1: (2, 2): (3, 1, 2): 1.67
    │   └── 3: (1, 1): (3, 1, 2): 1.67
    └── 2: (2, 3): (2, 3, 1): 3.33
        ├── 2: (2, 1): (1, 2, 3): 1.33
        └── 3: (2, 2): (3, 1, 2): 2.0
"""

    def test_tuple_number_of_children_mixed_0_to_2(self):
        self.ft.generate_children(number_of_children=(0, 1, 2))
        # print(self.ft.get_tree_representation(node_info_with_permutation_order))
        assert self.ft.get_tree_representation(node_info_with_permutation_order) == """└── None: (1, 1): (3, 1, 2): 10.0
    ├── 3: (2, 1): (1, 2, 3): 5.0
    │   ├── 2: (3, 2): (1, 2, 3): 2.0
    │   └── 3: (3, 3): (3, 1, 2): 3.0
    ├── 1: (2, 2): (3, 1, 2): 1.67
    └── 2: (2, 3): (2, 3, 1): 3.33
        └── 3: (2, 2): (3, 1, 2): 3.33
"""

    def test_tuple_number_of_children_mixed_tuples(self):
        self.ft.generate_children(number_of_children=(1, (1, 2, 3), 3))
        # print(self.ft.get_tree_representation(node_info_with_permutation_order))
        assert self.ft.get_tree_representation(node_info_with_permutation_order) == """└── None: (1, 1): (3, 1, 2): 10.0
    ├── 3: (2, 1): (1, 2, 3): 5.0
    │   ├── 1: (3, 1): (2, 3, 1): 0.83
    │   ├── 2: (3, 2): (1, 2, 3): 1.67
    │   └── 3: (3, 3): (3, 1, 2): 2.5
    ├── 1: (2, 2): (3, 1, 2): 1.67
    │   └── 3: (1, 1): (3, 1, 2): 1.67
    └── 2: (2, 3): (2, 3, 1): 3.33
        ├── 2: (2, 1): (1, 2, 3): 1.11
        │   ├── 2: (3, 2): (1, 2, 3): 0.44
        │   └── 3: (3, 3): (3, 1, 2): 0.67
        ├── 3: (2, 2): (3, 1, 2): 1.67
        │   ├── 3: (1, 1): (3, 1, 2): 0.83
        │   ├── 1: (1, 2): (2, 3, 1): 0.28
        │   └── 2: (1, 3): (1, 2, 3): 0.56
        └── 1: (2, 3): (2, 3, 1): 0.56
            └── 3: (2, 2): (3, 1, 2): 0.56
"""

    def test_tuple_number_of_children_mixed_tuples_2(self):
        self.ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)))
        # print(self.ft.get_tree_representation(node_info_with_permutation_order))
        assert self.ft.get_tree_representation(node_info_with_permutation_order) == """└── None: (1, 1): (3, 1, 2): 10.0
    ├── 3: (2, 1): (1, 2, 3): 5.0
    │   ├── 1: (3, 1): (2, 3, 1): 0.83
    │   │   └── 3: (1, 2): (2, 3, 1): 0.83
    │   ├── 2: (3, 2): (1, 2, 3): 1.67
    │   │   ├── 2: (2, 2): (3, 1, 2): 0.67
    │   │   │   └── 3: (1, 1): (3, 1, 2): 0.67
    │   │   └── 3: (2, 3): (2, 3, 1): 1.0
    │   │       ├── 2: (2, 1): (1, 2, 3): 0.33
    │   │       ├── 3: (2, 2): (3, 1, 2): 0.5
    │   │       └── 1: (2, 3): (2, 3, 1): 0.17
    │   └── 3: (3, 3): (3, 1, 2): 2.5
    │       ├── 3: (3, 1): (2, 3, 1): 1.25
    │       ├── 1: (3, 2): (1, 2, 3): 0.42
    │       └── 2: (3, 3): (3, 1, 2): 0.83
    ├── 1: (2, 2): (3, 1, 2): 1.67
    │   ├── 3: (1, 1): (3, 1, 2): 1.0
    │   │   ├── 3: (2, 1): (1, 2, 3): 0.5
    │   │   ├── 1: (2, 2): (3, 1, 2): 0.17
    │   │   └── 2: (2, 3): (2, 3, 1): 0.33
    │   └── 2: (1, 3): (1, 2, 3): 0.67
    │       └── 3: (1, 3): (1, 2, 3): 0.67
    └── 2: (2, 3): (2, 3, 1): 3.33
        ├── 2: (2, 1): (1, 2, 3): 1.33
        └── 3: (2, 2): (3, 1, 2): 2.0
"""

    def test_tuple_number_of_children_mixed_tuples_2_forwards(self):
        self.ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)), reduce_mode='forwards')
        # print(self.ft.get_tree_representation(node_info_with_permutation_order))
        assert self.ft.get_tree_representation(node_info_with_permutation_order) == """└── None: (1, 1): (3, 1, 2): 10.0
    ├── 3: (2, 1): (1, 2, 3): 5.0
    │   ├── 1: (3, 1): (2, 3, 1): 1.67
    │   │   └── 1: (1, 3): (1, 2, 3): 1.67
    │   └── 2: (3, 2): (1, 2, 3): 3.33
    │       ├── 1: (2, 1): (1, 2, 3): 0.56
    │       ├── 2: (2, 2): (3, 1, 2): 1.11
    │       └── 3: (2, 3): (2, 3, 1): 1.67
    ├── 1: (2, 2): (3, 1, 2): 1.67
    │   ├── 1: (1, 2): (2, 3, 1): 0.56
    │   └── 2: (1, 3): (1, 2, 3): 1.11
    └── 2: (2, 3): (2, 3, 1): 3.33
        ├── 2: (2, 1): (1, 2, 3): 1.11
        │   └── 1: (3, 1): (2, 3, 1): 1.11
        ├── 3: (2, 2): (3, 1, 2): 1.67
        │   ├── 1: (1, 2): (2, 3, 1): 0.56
        │   │   └── 1: (3, 3): (3, 1, 2): 0.56
        │   └── 2: (1, 3): (1, 2, 3): 1.11
        │       ├── 1: (1, 1): (3, 1, 2): 0.19
        │       ├── 2: (1, 2): (2, 3, 1): 0.37
        │       └── 3: (1, 3): (1, 2, 3): 0.56
        └── 1: (2, 3): (2, 3, 1): 0.56
            ├── 2: (2, 1): (1, 2, 3): 0.19
            ├── 3: (2, 2): (3, 1, 2): 0.28
            └── 1: (2, 3): (2, 3, 1): 0.09
"""

    def test_tuple_number_of_children_mixed_tuples_2_sieve(self):
        self.ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)), reduce_mode='sieve')
        # print(self.ft.get_tree_representation(node_info_with_permutation_order))
        assert self.ft.get_tree_representation(node_info_with_permutation_order) == """└── None: (1, 1): (3, 1, 2): 10.0
    ├── 3: (2, 1): (1, 2, 3): 5.0
    │   ├── 1: (3, 1): (2, 3, 1): 1.25
    │   │   └── 1: (1, 3): (1, 2, 3): 1.25
    │   └── 3: (3, 3): (3, 1, 2): 3.75
    │       ├── 3: (3, 1): (2, 3, 1): 1.88
    │       ├── 1: (3, 2): (1, 2, 3): 0.62
    │       └── 2: (3, 3): (3, 1, 2): 1.25
    ├── 1: (2, 2): (3, 1, 2): 1.67
    │   ├── 3: (1, 1): (3, 1, 2): 1.25
    │   └── 1: (1, 2): (2, 3, 1): 0.42
    └── 2: (2, 3): (2, 3, 1): 3.33
        ├── 2: (2, 1): (1, 2, 3): 1.11
        │   └── 1: (3, 1): (2, 3, 1): 1.11
        ├── 3: (2, 2): (3, 1, 2): 1.67
        │   ├── 3: (1, 1): (3, 1, 2): 1.25
        │   │   └── 1: (2, 2): (3, 1, 2): 1.25
        │   └── 1: (1, 2): (2, 3, 1): 0.42
        │       ├── 2: (3, 1): (2, 3, 1): 0.14
        │       ├── 3: (3, 2): (1, 2, 3): 0.21
        │       └── 1: (3, 3): (3, 1, 2): 0.07
        └── 1: (2, 3): (2, 3, 1): 0.56
            ├── 2: (2, 1): (1, 2, 3): 0.19
            ├── 3: (2, 2): (3, 1, 2): 0.28
            └── 1: (2, 3): (2, 3, 1): 0.09
"""

    def test_tuple_number_of_children_mixed_tuples_2_merge(self):
        self.ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)), reduce_mode='merge', merge_index=1)
        # print(self.ft.get_tree_representation(node_info_with_permutation_order))
        assert self.ft.get_tree_representation(node_info_with_permutation_order) == """└── None: (1, 1): (3, 1, 2): 10.0
    ├── 3: (2, 1): (1, 2, 3): 5.0
    │   ├── 1: (3, 1): (2, 3, 1): 0.83
    │   │   └── 2: (1, 1): (3, 1, 2): 0.83
    │   └── 2: (3, 2): (1, 2, 3): 4.17
    │       ├── 1: (2, 1): (1, 2, 3): 0.69
    │       ├── 2: (2, 2): (3, 1, 2): 1.39
    │       └── 3: (2, 3): (2, 3, 1): 2.08
    ├── 1: (2, 2): (3, 1, 2): 1.67
    │   ├── 3: (1, 1): (3, 1, 2): 0.83
    │   └── 1: (1, 2): (2, 3, 1): 0.83
    └── 2: (2, 3): (2, 3, 1): 3.33
        ├── 2: (2, 1): (1, 2, 3): 1.11
        │   └── 1: (3, 1): (2, 3, 1): 1.11
        ├── 3: (2, 2): (3, 1, 2): 1.67
        │   ├── 3: (1, 1): (3, 1, 2): 0.83
        │   │   └── 3: (2, 1): (1, 2, 3): 0.83
        │   └── 1: (1, 2): (2, 3, 1): 0.83
        │       ├── 2: (3, 1): (2, 3, 1): 0.28
        │       ├── 3: (3, 2): (1, 2, 3): 0.42
        │       └── 1: (3, 3): (3, 1, 2): 0.14
        └── 1: (2, 3): (2, 3, 1): 0.56
            ├── 2: (2, 1): (1, 2, 3): 0.19
            ├── 3: (2, 2): (3, 1, 2): 0.28
            └── 1: (2, 3): (2, 3, 1): 0.09
"""
