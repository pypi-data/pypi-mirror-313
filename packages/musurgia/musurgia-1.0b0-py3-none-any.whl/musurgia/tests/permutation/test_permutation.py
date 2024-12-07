from unittest import TestCase

from musurgia.permutation.permutation import permute, get_self_permutation_2d, get_self_permutation_3d


class TestPermutation(TestCase):
    def test_simple_permute(self):
        # wrong lengths
        with self.assertRaises(TypeError):
            permute([10, 20, 30, 40], (3, 2, 4))
        with self.assertRaises(TypeError):
            permute([10, 20, 30, 40], (3, 2, 4, 1, 3))
        # wrong orders
        with self.assertRaises(TypeError):
            permute([10, 20, 30, 40], (3, 2, 4, 5))

        with self.assertRaises(ValueError):
            permute([10, 20, 30, 40], (2, 3, 1))

        with self.assertRaises(ValueError):
            permute([10, 20, 30, 40], (2, 3, 1, 4, 5))

        assert permute([10, 20, 30, 40], (3, 2, 4, 1)) == [30, 20, 40, 10]

    def test_get_self_permutation_2d(self):
        with self.assertRaises(TypeError):
            get_self_permutation_2d([4, 2, 3, 1])

        assert get_self_permutation_2d((3, 1, 2)) == [(3, 1, 2), (2, 3, 1), (1, 2, 3)]

        assert get_self_permutation_2d((1, 3, 2)) == [(1, 3, 2), (1, 2, 3), (1, 3, 2)]

        assert get_self_permutation_2d((1, 2, 3)) == [(1, 2, 3), (1, 2, 3), (1, 2, 3)]

        assert get_self_permutation_2d((3, 1, 4, 2)) == [(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)]

        assert get_self_permutation_2d((4, 2, 3, 1)) == [(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)]

    def test_get_self_permutation_3d(self):
        with self.assertRaises(TypeError):
            get_self_permutation_3d([4, 2, 3, 1])

    assert get_self_permutation_3d((3, 1, 2)) == [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
                                                  [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
                                                  [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]

    assert get_self_permutation_3d((1, 3, 2)) == [[(1, 3, 2), (1, 2, 3), (1, 3, 2)],
                                                  [(1, 3, 2), (1, 3, 2), (1, 2, 3)],
                                                  [(1, 3, 2), (1, 2, 3), (1, 3, 2)]]

    assert get_self_permutation_3d((1, 2, 3)) == [[(1, 2, 3), (1, 2, 3), (1, 2, 3)],
                                                  [(1, 2, 3), (1, 2, 3), (1, 2, 3)],
                                                  [(1, 2, 3), (1, 2, 3), (1, 2, 3)]]

    assert get_self_permutation_3d((3, 1, 4, 2)) == [[(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)],
                                                     [(2, 4, 1, 3), (3, 1, 4, 2), (1, 2, 3, 4), (4, 3, 2, 1)],
                                                     [(1, 2, 3, 4), (2, 4, 1, 3), (4, 3, 2, 1), (3, 1, 4, 2)],
                                                     [(4, 3, 2, 1), (1, 2, 3, 4), (3, 1, 4, 2), (2, 4, 1, 3)]]

    assert get_self_permutation_3d((3, 4, 2, 1)) == [[(3, 4, 2, 1), (2, 1, 4, 3), (4, 3, 1, 2), (1, 2, 3, 4)],
                                                     [(4, 3, 1, 2), (1, 2, 3, 4), (2, 1, 4, 3), (3, 4, 2, 1)],
                                                     [(2, 1, 4, 3), (3, 4, 2, 1), (1, 2, 3, 4), (4, 3, 1, 2)],
                                                     [(1, 2, 3, 4), (4, 3, 1, 2), (3, 4, 2, 1), (2, 1, 4, 3)]]

    assert get_self_permutation_3d((4, 2, 3, 1)) == [[(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)],
                                                     [(1, 2, 3, 4), (1, 2, 3, 4), (4, 2, 3, 1), (4, 2, 3, 1)],
                                                     [(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)],
                                                     [(1, 2, 3, 4), (1, 2, 3, 4), (4, 2, 3, 1), (4, 2, 3, 1)]]
