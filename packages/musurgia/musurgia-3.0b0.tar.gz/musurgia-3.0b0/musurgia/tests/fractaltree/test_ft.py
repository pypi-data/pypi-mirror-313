from unittest import TestCase

from musurgia.fractal import FractalTree
from musurgia.musurgia_exceptions import FractalTreePermutationIndexError, FractalTreeSetMainPermutationOrderFirstError, \
    FractalTreeHasChildrenError, FractalTreeMergeWrongValuesError, \
    FractalTreeHasNoChildrenError
from musurgia.tests.utils_for_tests import create_test_fractal_tree


class TestFt(TestCase):
    def setUp(self) -> None:
        self.ft = create_test_fractal_tree()

    def test_add_wrong_child(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3))
        with self.assertRaises(TypeError):
            ft.add_child('something')

    def test_non_root_main_permutation_order(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3))
        assert ft.main_permutation_order is None
        assert self.ft.main_permutation_order == (3, 1, 4, 2)
        for node in self.ft.traverse():
            assert node.main_permutation_order == self.ft.main_permutation_order

    def test_calculate_permutation_index_error(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3))
        # ft.calculate_permutation_index()
        with self.assertRaises(FractalTreePermutationIndexError):
            ft.calculate_permutation_index()

        child = ft.add_child(FractalTree(value=5, proportions=(1, 2, 3)))
        with self.assertRaises(FractalTreeSetMainPermutationOrderFirstError):
            child.calculate_permutation_index()
        with self.assertRaises(FractalTreeHasChildrenError):
            ft.main_permutation_order = (3, 1, 2)

    def test_generate_children_wrong_size(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        with self.assertRaises(ValueError):
            ft.generate_children(4)
        with self.assertRaises(ValueError):
            ft.generate_children(-1)
        with self.assertRaises(TypeError):
            ft.generate_children('string')

    def test_get_children_fractal_orders_error(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3))
        with self.assertRaises(FractalTreeSetMainPermutationOrderFirstError):
            ft.get_children_fractal_orders()

    def test_merge_reduce_error(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        with self.assertRaises(FractalTreeHasNoChildrenError):
            ft.merge_children(1, 3)
        with self.assertRaises(FractalTreeHasNoChildrenError):
            ft.reduce_children_by_condition(lambda node: node.get_value() == 10)
        ft.generate_children(3)
        with self.assertRaises(FractalTreeMergeWrongValuesError):
            ft.merge_children(1, 3)
        with self.assertRaises(ValueError):
            ft.reduce_children_by_size(2, mode='merge')
        with self.assertRaises(ValueError):
            ft.reduce_children_by_size(2, mode='merge', merge_index=20)

        with self.assertRaises(ValueError):
            ft.reduce_children_by_size(5)
        with self.assertRaises(ValueError):
            ft.reduce_children_by_size(-1)
        ft.reduce_children_by_size(0)
        assert len(ft.get_children()) == 3
        ft.reduce_children_by_size(2, mode='merge', merge_index=2)
        assert len(ft.get_children()) == 2

    def test_split_iter(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        ft.split([1, 3, 1])
        assert len(ft.get_children()) == 3

    def test_split_error(self):
        with self.assertRaises(FractalTreeHasChildrenError):
            self.ft.split(1, 2, 3)

    def test_calculate_permutation_index(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3))
        with self.assertRaises(FractalTreePermutationIndexError):
            ft.calculate_permutation_index()
