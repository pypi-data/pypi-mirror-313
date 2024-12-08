from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree
from musurgia.matrix.matrix import PermutationOrderMatrix
from musurgia.musurgia_exceptions import FractalTreeSetMainPermutationOrderFirstError


class TestFractalTreeInit(TestCase):

    def test_init(self):
        with self.assertRaises(TypeError):
            FractalTree()
        with self.assertRaises(TypeError):
            FractalTree(value=10)
        with self.assertRaises(TypeError):
            FractalTree(proportions=(1, 2, 3))
        ft = FractalTree(value=10, proportions=(1, 2, 3))
        with self.assertRaises(FractalTreeSetMainPermutationOrderFirstError):
            ft.get_permutation_order_matrix()

    def test_init_creates_matrix(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        assert isinstance(ft.get_permutation_order_matrix(), PermutationOrderMatrix)
        assert ft.get_permutation_order_matrix().matrix_data == [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
                                                                 [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
                                                                 [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        ft.main_permutation_order = (3, 1, 2)
        assert isinstance(ft.get_permutation_order_matrix(), PermutationOrderMatrix)
        assert ft.get_permutation_order_matrix().matrix_data == [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
                                                                 [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
                                                                 [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        ft.add_child(FractalTree(value=10, proportions=(1, 2, 3)))
