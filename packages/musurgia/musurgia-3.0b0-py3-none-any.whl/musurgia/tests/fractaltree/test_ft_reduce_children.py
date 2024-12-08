from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree
from musurgia.tests.utils_for_tests import node_info
from musurgia.utils import flatten


class TestFractalTreeReduceChildrenByCondition(TestCase):
    def test_reduce_first_layer(self):
        ft = FractalTree(proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), value=20, permutation_index=(1, 1))
        ft.add_layer()
        ft.add_layer()
        for node in ft.get_layer(1):
            node.reduce_children_by_condition(condition=lambda node: node.get_fractal_order() == 1)
        assert [node.get_fractal_order() for node in ft.iterate_leaves()] == [2, 3, 3, 2, 2, 3]

    def test_value(self):
        ft = FractalTree(proportions=[1, 2, 3, 4, 5, 6], main_permutation_order=(4, 1, 5, 3, 6, 2), value=20,
                         permutation_index=(1, 1))
        ft.add_layer()
        ft.reduce_children_by_condition(lambda child: child.get_fractal_order() not in [2, 3])
        self.assertEqual([3, 2], [node.get_fractal_order() for node in ft.iterate_leaves()])
        self.assertEqual([12, 8], [node.get_value() for node in ft.get_children()])


class TestFractalTreeReduceChildrenByNumberOfChildren(TestCase):
    def setUp(self):
        self.ft = FractalTree(proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2), value=20,
                              permutation_index=(1, 1))
        self.ft.add_layer()
        self.ft.add_layer()

        # print(self.ft.get_tree_representation(node_info))
        """
        └── None:(1, 1): 20.0
            ├── 3:(2, 1): 6.0
            │   ├── 2:(3, 1): 1.2
            │   ├── 4:(3, 2): 2.4
            │   ├── 1:(3, 3): 0.6
            │   └── 3:(3, 4): 1.8
            ├── 1:(2, 2): 2.0
            │   ├── 3:(4, 1): 0.6
            │   ├── 1:(4, 2): 0.2
            │   ├── 4:(4, 3): 0.8
            │   └── 2:(4, 4): 0.4
            ├── 4:(2, 3): 8.0
            │   ├── 1:(1, 1): 0.8
            │   ├── 2:(1, 2): 1.6
            │   ├── 3:(1, 3): 2.4
            │   └── 4:(1, 4): 3.2
            └── 2:(2, 4): 4.0
                ├── 4:(2, 1): 1.6
                ├── 3:(2, 2): 1.2
                ├── 2:(2, 3): 0.8
                └── 1:(2, 4): 0.4
        """

    def test_reduce_backward(self):
        self.ft.reduce_children_by_size(size=3)
        for child in self.ft.get_children():
            child.reduce_children_by_size(size=3)
        # print(self.ft.get_tree_representation(node_info))
        assert self.ft.get_tree_representation(node_info) == """└── None: (1, 1): 20.0
    ├── 3: (2, 1): 6.67
    │   ├── 2: (3, 1): 1.48
    │   ├── 4: (3, 2): 2.96
    │   └── 3: (3, 4): 2.22
    ├── 4: (2, 3): 8.89
    │   ├── 2: (1, 2): 1.98
    │   ├── 3: (1, 3): 2.96
    │   └── 4: (1, 4): 3.95
    └── 2: (2, 4): 4.44
        ├── 4: (2, 1): 1.98
        ├── 3: (2, 2): 1.48
        └── 2: (2, 3): 0.99
"""

    def test_reduce_forwards(self):
        self.ft.reduce_children_by_size(size=3, mode='forwards')
        for child in self.ft.get_children():
            child.reduce_children_by_size(size=3, mode='forwards')
        # print(self.ft.get_tree_representation(node_info))
        assert self.ft.get_tree_representation(node_info) == """└── None: (1, 1): 20.0
    ├── 3: (2, 1): 10.0
    │   ├── 2: (3, 1): 3.33
    │   ├── 1: (3, 3): 1.67
    │   └── 3: (3, 4): 5.0
    ├── 1: (2, 2): 3.33
    │   ├── 3: (4, 1): 1.67
    │   ├── 1: (4, 2): 0.56
    │   └── 2: (4, 4): 1.11
    └── 2: (2, 4): 6.67
        ├── 3: (2, 2): 3.33
        ├── 2: (2, 3): 2.22
        └── 1: (2, 4): 1.11
"""

    def test_reduce_sieve(self):
        self.ft.reduce_children_by_size(size=3, mode='sieve')
        for child in self.ft.get_children():
            child.reduce_children_by_size(size=3, mode='sieve')

        # print(self.ft.get_tree_representation(node_info))
        assert self.ft.get_tree_representation(node_info) == """└── None: (1, 1): 20.0
    ├── 1: (2, 2): 2.86
    │   ├── 1: (4, 2): 0.41
    │   ├── 4: (4, 3): 1.63
    │   └── 2: (4, 4): 0.82
    ├── 4: (2, 3): 11.43
    │   ├── 1: (1, 1): 1.63
    │   ├── 2: (1, 2): 3.27
    │   └── 4: (1, 4): 6.53
    └── 2: (2, 4): 5.71
        ├── 4: (2, 1): 3.27
        ├── 2: (2, 3): 1.63
        └── 1: (2, 4): 0.82
"""

    def test_merge(self):
        ft_1 = FractalTree(proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2), value=20,
                           permutation_index=(1, 1))
        ft_2 = FractalTree(proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2), value=20,
                           permutation_index=(1, 1))
        ft_3 = FractalTree(proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2), value=20,
                           permutation_index=(1, 1))
        for i in range(2):
            ft_1.add_layer()
            ft_2.add_layer()
            ft_3.add_layer()
        # print(self.ft.get_tree_representation(node_info))
        """
        └── None: (1, 1): 20.0
            ├── 3: (2, 1): 6.0
            │   ├── 2: (3, 1): 1.2
            │   ├── 4: (3, 2): 2.4
            │   ├── 1: (3, 3): 0.6
            │   └── 3: (3, 4): 1.8
            ├── 1: (2, 2): 2.0
            │   ├── 3: (4, 1): 0.6
            │   ├── 1: (4, 2): 0.2
            │   ├── 4: (4, 3): 0.8
            │   └── 2: (4, 4): 0.4
            ├── 4: (2, 3): 8.0
            │   ├── 1: (1, 1): 0.8
            │   ├── 2:(1, 2): 1.6
            │   ├── 3: (1, 3): 2.4
            │   └── 4: (1, 4): 3.2
            └── 2: (2, 4): 4.0
                ├── 4: (2, 1): 1.6
                ├── 3: (2, 2): 1.2
                ├── 2: (2, 3): 0.8
                └── 1: (2, 4): 0.4
        """
        assert ft_1._get_merge_lengths(size=2, merge_index=0) == [3, 1]
        assert ft_2._get_merge_lengths(size=2, merge_index=2) == [2, 2]
        assert ft_3._get_merge_lengths(size=2, merge_index=3) == [3, 1]

        for index, ft in zip([0, 2, 3], [ft_1, ft_2, ft_3]):
            ft.reduce_children_by_size(size=2, mode='merge', merge_index=index)
            for child in ft.get_children():
                child.reduce_children_by_size(size=3, mode='merge', merge_index=index)
        # print(ft_1.get_tree_representation(node_info))
        assert ft_1.get_tree_representation(node_info) == """└── None: (1, 1): 20.0
    ├── 3: (2, 1): 16.0
    │   ├── 2: (3, 1): 9.6
    │   ├── 1: (3, 3): 1.6
    │   └── 3: (3, 4): 4.8
    └── 2: (2, 4): 4.0
        ├── 4: (2, 1): 2.8
        ├── 2: (2, 3): 0.8
        └── 1: (2, 4): 0.4
"""
        # print(ft_2.get_tree_representation(node_info))
        assert ft_2.get_tree_representation(node_info) == """└── None: (1, 1): 20.0
    ├── 3: (2, 1): 8.0
    │   ├── 2: (3, 1): 1.6
    │   ├── 4: (3, 2): 3.2
    │   └── 1: (3, 3): 3.2
    └── 4: (2, 3): 12.0
        ├── 1: (1, 1): 1.2
        ├── 2: (1, 2): 2.4
        └── 3: (1, 3): 8.4
"""
        # print(ft_3.get_tree_representation(node_info))
        assert ft_3.get_tree_representation(node_info) == """└── None: (1, 1): 20.0
    ├── 3: (2, 1): 16.0
    │   ├── 2: (3, 1): 9.6
    │   ├── 1: (3, 3): 1.6
    │   └── 3: (3, 4): 4.8
    └── 2: (2, 4): 4.0
        ├── 4: (2, 1): 2.8
        ├── 2: (2, 3): 0.8
        └── 1: (2, 4): 0.4
"""

        for ft in [ft_1, ft_2, ft_3]:
            assert ft.get_value() == sum(flatten(ft.get_layer(1, key=lambda node: node.get_value()))) == sum(
                flatten(ft.get_layer(2, key=lambda node: node.get_value())))
