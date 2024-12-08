from unittest import TestCase

from musurgia.fractal.fractaltree import PermutationIndexCalculater


class TestPermutationMatrixIndexCalculator(TestCase):
    def test_calculate_permutation_matrix_index(self):
        """
        pos_indices = {
            'root': (1, 1),
            '1.1': (3, 1), '1.2': (3, 2), '1.3': (3, 3),

            '2.1.1': (1, 1), '2.1.2': (1, 2), '2.1.3': (1, 3),
            '2.2.1': (2, 1), '2.2.2': (2, 2), '2.2.3': (2, 3),
            '2.3.1': (3, 1), '2.3.2': (3, 2), '2.3.3': (3, 3),

            '3.1.1.1': (2, 1), '3.1.1.2': (2, 2), '3.1.1.3': (2, 3),
            '3.1.2.1': (3, 1), '3.1.2.2': (3, 2), '3.1.2.3': (3, 3),
            '3.1.3.1': (1, 1), '3.1.3.2': (1, 2), '3.1.3.3': (1, 3),

            '3.2.1.1': (3, 1), '3.2.1.2': (3, 2), '3.2.1.3': (3, 3),
            '3.2.2.1': (1, 1), '3.2.2.2': (1, 2), '3.2.2.3': (1, 3),
            '3.2.3.1': (2, 1), '3.2.3.2': (2, 2), '3.2.3.3': (2, 3),

            '3.3.1.1': (1, 1), '3.3.1.2': (1, 2), '3.3.1.3': (1, 3),
            '3.3.2.1': (2, 1), '3.3.2.2': (2, 2), '3.3.2.3': (2, 3),
            '3.3.3.1': (3, 1), '3.3.3.2': (3, 2), '3.3.3.3': (3, 3),
        }
        """
        pic = PermutationIndexCalculater(3)

        pic.parent_index = (1, 1)
        assert pic.get_index(column_number=1) == (2, 1)
        assert pic.get_index(column_number=2) == (2, 2)
        assert pic.get_index(column_number=3) == (2, 3)

        pic.parent_index = (1, 2)
        assert pic.get_index(column_number=1) == (3, 1)
        assert pic.get_index(column_number=2) == (3, 2)
        assert pic.get_index(column_number=3) == (3, 3)

        pic.parent_index = (1, 3)
        assert pic.get_index(column_number=1) == (1, 1)
        assert pic.get_index(column_number=2) == (1, 2)
        assert pic.get_index(column_number=3) == (1, 3)

        pic.parent_index = (2, 1)
        assert pic.get_index(column_number=1) == (3, 1)
        assert pic.get_index(column_number=2) == (3, 2)
        assert pic.get_index(column_number=3) == (3, 3)
        pic.parent_index = (2, 2)
        assert pic.get_index(column_number=1) == (1, 1)
        assert pic.get_index(column_number=2) == (1, 2)
        assert pic.get_index(column_number=3) == (1, 3)

        pic.parent_index = (2, 3)
        assert pic.get_index(column_number=1) == (2, 1)
        assert pic.get_index(column_number=2) == (2, 2)
        assert pic.get_index(column_number=3) == (2, 3)

        pic.parent_index = (3, 1)
        assert pic.get_index(column_number=1) == (1, 1)
        assert pic.get_index(column_number=2) == (1, 2)
        assert pic.get_index(column_number=3) == (1, 3)

        pic.parent_index = (3, 2)
        assert pic.get_index(column_number=1) == (2, 1)
        assert pic.get_index(column_number=2) == (2, 2)
        assert pic.get_index(column_number=3) == (2, 3)

        pic.parent_index = (3, 3)
        assert pic.get_index(column_number=1) == (3, 1)
        assert pic.get_index(column_number=2) == (3, 2)
        assert pic.get_index(column_number=3) == (3, 3)
