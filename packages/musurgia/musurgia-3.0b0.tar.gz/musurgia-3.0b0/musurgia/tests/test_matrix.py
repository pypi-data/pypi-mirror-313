from pprint import pprint
from unittest import TestCase

from musurgia.matrix.matrix import Matrix, MatrixIsEmptyError, SquareMatrix, \
    PermutationOrderMatrix, PermutationOrderMatrixGenerator, \
    MatrixIndexController
from musurgia.musurgia_exceptions import MatrixIndexOutOfRangeError, MatrixIndexEndOfRowError, \
    MatrixIndexEndOfMatrixError, SquareMatrixDataError, PermutationOrderMatrixDataError, \
    MatrixIndexControllerReadingDirectionError
from musurgia.permutation.permutation import permute


class TestMatrix(TestCase):
    def setUp(self):
        self.mat = Matrix(
            [[1, 2, 3],
             [4, 5, 6]]
        )
        self.big_mat = Matrix([[(1, 1), (1, 2), (1, 3), (1, 4)],
                               [(2, 1), (2, 2), (2, 3), (2, 4)],
                               [(3, 1), (3, 2), (3, 3), (3, 4)],
                               [(4, 1), (4, 2), (4, 3), (4, 4)],
                               [(5, 1), (5, 2), (5, 3), (5, 4)]])

    def test_matrix(self):
        assert Matrix(None).matrix_data == []
        m = [[1, 2, 3], [4, 5, 6]]
        mat = Matrix(m)
        assert mat.matrix_data == m
        with self.assertRaises(TypeError):
            mat.matrix_data = [1, 2, 3]

    def test_add_row(self):
        mat = Matrix()
        # wrong type
        with self.assertRaises(TypeError):
            mat.add_row(1)
        # adding two rows
        row_1 = [1, 2, 3]
        mat.add_row(row_1)
        assert mat.matrix_data == [row_1]
        row_2 = [4, 5, 6]
        mat.add_row(row_2)
        assert mat.matrix_data == [row_1, row_2]
        # wrong lengths
        with self.assertRaises(ValueError):
            mat.add_row([1, 2, 3, 4, 5])
        with self.assertRaises(ValueError):
            mat.add_row([1, 2])

    def test_remove_row(self):
        with self.assertRaises(MatrixIsEmptyError):
            Matrix().remove_row(1)
        with self.assertRaises(TypeError):
            self.mat.remove_row(0)
        with self.assertRaises(TypeError):
            self.mat.remove_row(1.2)
        with self.assertRaises(TypeError):
            self.mat.remove_row(-1)
        with self.assertRaises(ValueError):
            self.mat.remove_row(5)
        assert self.mat.remove_row(1) == [1, 2, 3]
        assert self.mat.matrix_data == [[4, 5, 6]]
        assert self.mat.get_row_size() == 3
        assert self.mat.get_column_size() == 1
        self.mat.remove_row(1)
        assert self.mat.is_empty
        assert self.mat.get_row_size() == 0
        assert self.mat.get_column_size() == 0

    def test_get_row_size(self):
        assert self.mat.get_row_size() == 3

    def test_get_column_size(self):
        assert self.mat.get_column_size() == 2

    def test_get_row(self):
        with self.assertRaises(MatrixIsEmptyError):
            Matrix().get_row(1)
        assert self.mat.get_row(1) == [1, 2, 3]
        assert self.mat.get_row(2) == [4, 5, 6]
        with self.assertRaises(TypeError):
            self.mat.get_row(0)
        with self.assertRaises(ValueError):
            self.mat.get_row(3)

    def test_get_column(self):
        with self.assertRaises(MatrixIsEmptyError):
            Matrix().get_column(1)
        assert self.mat.get_column(1) == [1, 4]
        assert self.mat.get_column(2) == [2, 5]
        assert self.mat.get_column(3) == [3, 6]
        with self.assertRaises(TypeError):
            self.mat.get_column(0)
        with self.assertRaises(ValueError):
            self.mat.get_column(4)

    def test_get_element(self):
        with self.assertRaises(MatrixIsEmptyError):
            Matrix().get_element((1, 1))
        with self.assertRaises(TypeError):
            self.mat.get_element(1)
        with self.assertRaises(ValueError):
            self.mat.get_element((3, 3))
        assert self.mat.get_element((1, 2)) == 2
        assert self.mat.get_element((2, 2)) == 5
        assert self.big_mat.get_element((1, 2)) == (1, 2)
        assert self.big_mat.get_element((3, 4)) == (3, 4)

        with self.assertRaises(MatrixIndexOutOfRangeError):
            self.mat.get_element((20, 30))

    def test_transpose(self):
        expected = [[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)],
                    [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)],
                    [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3)],
                    [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4)]]
        self.assertEqual(expected, self.big_mat.get_transposed_matrix().matrix_data)

    def test_transpose_regular(self):
        expected = [[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)],
                    [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)],
                    [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3)],
                    [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4)]]

        self.assertEqual(expected, self.big_mat.get_transposed_matrix(mode='regular').matrix_data)

    def test_transpose_diagonal(self):
        expected = [[(1, 1), (2, 2), (3, 3), (4, 4), (5, 1)],
                    [(1, 2), (2, 3), (3, 4), (4, 1), (5, 2)],
                    [(1, 3), (2, 4), (3, 1), (4, 2), (5, 3)],
                    [(1, 4), (2, 1), (3, 2), (4, 3), (5, 4)]]
        assert self.big_mat.get_transposed_matrix(mode='diagonal').matrix_data == expected

    def test_permute_matrix_data(self):
        permutation_order = (3, 1, 2, 5, 4)
        expected = [[(3, 1), (3, 2), (3, 3), (3, 4)],
                    [(1, 1), (1, 2), (1, 3), (1, 4)],
                    [(2, 1), (2, 2), (2, 3), (2, 4)],
                    [(5, 1), (5, 2), (5, 3), (5, 4)],
                    [(4, 1), (4, 2), (4, 3), (4, 4)]]
        assert permute(input_list=self.big_mat.matrix_data, permutation_order=permutation_order) == expected

    #
    # def test_permute_columns(self):
    #     assert False


class TestSquareMatrix(TestCase):
    def test_init_errors(self):
        with self.assertRaises(TypeError):
            SquareMatrix()
        with self.assertRaises(SquareMatrixDataError):
            SquareMatrix(matrix_data=[])
        with self.assertRaises(SquareMatrixDataError):
            SquareMatrix(matrix_data=[[1, 2, 3]])

    def test_get_size(self):
        assert SquareMatrix(matrix_data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]).get_size() == 3


class TestGeneratePermutationOrderMatrix(TestCase):
    def test_wrong_size(self):
        with self.assertRaises(TypeError):
            PermutationOrderMatrixGenerator(main_permutation_order=[1, 2])

    def test_generation(self):
        assert PermutationOrderMatrixGenerator(
            main_permutation_order=(2, 1)).generate_permutation_order_matrix().matrix_data == [[(2, 1), (1, 2)],
                                                                                               [(1, 2), (2, 1)]]
        assert PermutationOrderMatrixGenerator(
            main_permutation_order=(3, 1, 2)).generate_permutation_order_matrix().matrix_data == [
                   [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
                   [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
                   [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        assert PermutationOrderMatrixGenerator(
            main_permutation_order=(3, 1, 4, 2)).generate_permutation_order_matrix().matrix_data == [
                   [(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)],
                   [(2, 4, 1, 3), (3, 1, 4, 2), (1, 2, 3, 4), (4, 3, 2, 1)],
                   [(1, 2, 3, 4), (2, 4, 1, 3), (4, 3, 2, 1), (3, 1, 4, 2)],
                   [(4, 3, 2, 1), (1, 2, 3, 4), (3, 1, 4, 2), (2, 4, 1, 3)]]
        pomg = PermutationOrderMatrixGenerator(
            main_permutation_order=(3, 1, 4, 2))
        assert pomg.main_permutation_order == (3, 1, 4, 2)
        pomg.main_permutation_order = (1, 2)
        assert pomg.main_permutation_order == (1, 2)


class TestPermutationOrderMatrix(TestCase):
    def setUp(self):
        self.pom = PermutationOrderMatrixGenerator(
            main_permutation_order=(3, 1, 2)).generate_permutation_order_matrix()
        """
        [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        """

    def test_init_errors(self):
        with self.assertRaises(TypeError):
            PermutationOrderMatrix()
        with self.assertRaises(SquareMatrixDataError):
            PermutationOrderMatrix(matrix_data=[])
        # wrong type
        with self.assertRaises(PermutationOrderMatrixDataError):
            PermutationOrderMatrix(matrix_data=[[1, 2, 3]])
        # wrong permutation order
        with self.assertRaises(PermutationOrderMatrixDataError):
            PermutationOrderMatrix(matrix_data=[[(1, 2, 4)]])
        with self.assertRaises(PermutationOrderMatrixDataError):
            PermutationOrderMatrix(matrix_data=[[(2, 4, 3)]])
        # wrong lengths
        with self.assertRaises(PermutationOrderMatrixDataError):
            PermutationOrderMatrix(matrix_data=[[(1, 2, 3), (1, 2, 3, 4)], [(3, 2, 1), (3, 2, 1)]])
        PermutationOrderMatrix(matrix_data=[[(1, 2), (1, 2)], [(2, 1), (1, 2)]])


class TestMatrixIndexController(TestCase):

    def test_get_next(self):
        with self.assertRaises(MatrixIndexOutOfRangeError):
            MatrixIndexController(number_of_columns=3, number_of_rows=5, first_index=(4, 7))
        controller = MatrixIndexController(number_of_columns=3, number_of_rows=5)
        controller.first_index = (1, 1)
        assert next(controller) == (1, 1)
        assert next(controller) == (1, 2)
        controller.reset()
        assert controller.first_index == (1, 1)
        controller.first_index = (1, 3)
        next(controller)
        assert next(controller) == (2, 1)
        controller.first_index = (3, 2)
        assert next(controller) == (3, 2)
        assert controller.get_next_in_row() == (3, 3)
        with self.assertRaises(MatrixIndexEndOfRowError):
            controller.get_next_in_row()
        assert next(controller) == (4, 1)
        with self.assertRaises(MatrixIndexOutOfRangeError):
            controller.first_index = (7, 2)
        controller.first_index = (5, 3)
        next(controller)
        with self.assertRaises(MatrixIndexEndOfRowError):
            next(controller)
        with self.assertRaises(MatrixIndexEndOfMatrixError):
            next(controller)
        controller.first_index = (1, 2)
        next(controller)
        controller.reset()
        assert next(controller) == (1, 2)

    def test_iterate(self):
        controller = MatrixIndexController(3, 4)
        assert [_ for _ in controller] == [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1),
                                           (3, 2), (3, 3),
                                           (3, 4)]

    def test_convert_flatten_index_to_index_horizontal(self):
        controller = MatrixIndexController(3, 4)
        indices = [controller._convert_flatten_index_to_index(flatten_index) for flatten_index in range(0, 12)]
        assert indices == [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3),
                           (3, 4)]
        with self.assertRaises(MatrixIndexEndOfMatrixError):
            controller._convert_flatten_index_to_index(12)

    def test_convert_flatten_index_to_index_diagonal(self):
        controller = MatrixIndexController(3, 4, reading_direction='diagonal')
        indices = [controller._convert_flatten_index_to_index(flatten_index) for flatten_index in range(0, 12)]
        assert indices == [(1, 1), (2, 2), (3, 3), (1, 2), (2, 3), (3, 4), (1, 3), (2, 4), (3, 1), (1, 4), (2, 1),
                           (3, 2)]
        with self.assertRaises(MatrixIndexEndOfMatrixError):
            controller._convert_flatten_index_to_index(12)

    def test_convert_flatten_index_to_index_vertical(self):
        controller = MatrixIndexController(3, 4, reading_direction='vertical')
        indices = [controller._convert_flatten_index_to_index(flatten_index) for flatten_index in range(0, 12)]
        assert indices == [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3), (1, 4), (2, 4),
                           (3, 4)]
        with self.assertRaises(MatrixIndexEndOfMatrixError):
            controller._convert_flatten_index_to_index(12)

    def test_convert_index_to_flatten_index(self):
        controller = MatrixIndexController(3, 4)
        for flatten_index in range(0, 12):
            assert controller._convert_index_to_flatten_index(
                controller._convert_flatten_index_to_index(flatten_index)) == flatten_index

        controller.reading_direction = 'diagonal'
        for flatten_index in range(0, 12):
            assert controller._convert_index_to_flatten_index(
                controller._convert_flatten_index_to_index(flatten_index)) == flatten_index

        controller.reading_direction = 'vertical'
        for flatten_index in range(0, 12):
            assert controller._convert_index_to_flatten_index(
                controller._convert_flatten_index_to_index(flatten_index)) == flatten_index

    def test_get_next_flatten_index(self):
        controller = MatrixIndexController(3, 4)
        for x in range(0, 12):
            assert controller.get_next_flatten_index() == x
            next(controller)
        controller.reading_direction = 'diagonal'
        for x in range(0, 12):
            assert controller.get_next_flatten_index() == x
            next(controller)

        controller = MatrixIndexController(3, 3)
        for x in range(0, 9):
            assert controller.get_next_flatten_index() == x
            next(controller)
        controller.reading_direction = 'diagonal'
        for x in range(0, 9):
            assert controller.get_next_flatten_index() == x
            next(controller)

    def test_reading_direction(self):
        controller = MatrixIndexController(2, 3)
        assert controller.reading_direction == 'horizontal'
        controller.reading_direction = 'diagonal'
        with self.assertRaises(MatrixIndexControllerReadingDirectionError):
            controller.get_next_in_row()
        controller.first_index = (1, 2)
        assert next(controller) == (1, 2)
        assert next(controller) == (2, 3)
        assert next(controller) == (1, 3)
        assert next(controller) == (2, 1)
        with self.assertRaises(MatrixIndexEndOfMatrixError):
            next(controller)
        controller = MatrixIndexController(3, 3, first_index=(1, 3), reading_direction='diagonal')
        assert next(controller) == (1, 3)
        assert next(controller) == (2, 1)
        assert next(controller) == (3, 2)
        with self.assertRaises(MatrixIndexEndOfMatrixError):
            next(controller)
        """
        [[(1, 1), (1, 2), (1, 3), (1, 4)],
         [(2, 1), (2, 2), (2, 3), (2, 4)],
         [(3, 1), (3, 2), (3, 3), (3, 4)],
         [(4, 1), (4, 2), (4, 3), (4, 4)],
         [(5, 1), (5, 2), (5, 3), (5, 4)]]
        """
        controller = MatrixIndexController(5, 4, reading_direction='diagonal')
        expected = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 1),
                    (1, 2), (2, 3), (3, 4), (4, 1), (5, 2),
                    (1, 3), (2, 4), (3, 1), (4, 2), (5, 3),
                    (1, 4), (2, 1), (3, 2), (4, 3), (5, 4)]
        assert list(controller) == expected
