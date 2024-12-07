from musurgia.musurgia_types import check_matrix_data_type
from musurgia.tests.utils_for_tests import PdfTestCase
from musurgia.permutation.limited_permutation import LimitedPermutationOrders


class TestLimitedPermutationOrders(PdfTestCase):
    def test_init_errors(self):
        with self.assertRaises(TypeError):
            LimitedPermutationOrders(main_permutation_order=[3])

        LimitedPermutationOrders(main_permutation_order=(3, 1, 2))

    def test_set_errors(self):
        lt = LimitedPermutationOrders(main_permutation_order=(3, 1, 2))
        with self.assertRaises(TypeError):
            lt.main_permutation_order = [3, 1, 2]

    def test_get_permutation_orders(self):
        lt = LimitedPermutationOrders(main_permutation_order=(3, 1, 4, 2))
        assert lt.get_permutation_orders() == [[(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)],
                                               [(2, 4, 1, 3), (3, 1, 4, 2), (1, 2, 3, 4), (4, 3, 2, 1)],
                                               [(1, 2, 3, 4), (2, 4, 1, 3), (4, 3, 2, 1), (3, 1, 4, 2)],
                                               [(4, 3, 2, 1), (1, 2, 3, 4), (3, 1, 4, 2), (2, 4, 1, 3)]]
        assert check_matrix_data_type(lt.get_permutation_orders())
        lt.main_permutation_order = (3, 1, 2)
        assert lt.get_permutation_orders() == [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
                                               [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
                                               [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
