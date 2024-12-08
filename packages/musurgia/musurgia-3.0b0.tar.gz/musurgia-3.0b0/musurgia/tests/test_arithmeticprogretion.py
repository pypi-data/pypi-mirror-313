from fractions import Fraction
from unittest import TestCase

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.musurgia_exceptions import DAndSError


class TestArithmeticProgression(TestCase):
    def test_a1(self):
        arith = ArithmeticProgression(n=3, an=15, d=4)
        assert arith.a1 == Fraction(7, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(n=3, an=15, s=33)
        assert arith.a1 == Fraction(7, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

    def test_an(self):
        arith = ArithmeticProgression(n=3, a1=7, d=4)
        assert arith.an == Fraction(15, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(n=3, a1=7, s=33)
        assert arith.an == Fraction(15, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

    def test_correct_s(self):
        arith = ArithmeticProgression(a1=3, an=6, s=21)
        assert arith.get_parameters_dict() == {'a1': Fraction(3, 1), 'an': Fraction(6, 1), 'n': 4, 'd': Fraction(1, 1),
                                               's': Fraction(21, 1)}
        assert arith.get_actual_s() == Fraction(18, 1)
        result = list(arith)
        assert result == [Fraction(3, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1)]
        assert sum(result) == Fraction(18, 1)

        arith.correct_s = True
        arith.reset_iterator()
        assert arith.get_correction_factor() == Fraction(7, 6)
        result = list(arith)
        assert result == [Fraction(7, 2), Fraction(14, 3), Fraction(35, 6), Fraction(7, 1)]
        assert sum(result) == Fraction(21, 1)

    def test_d(self):
        arith = ArithmeticProgression(a1=7, an=15, s=33)
        assert arith.d == Fraction(4, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(a1=7, an=15, n=3)
        assert arith.d == Fraction(4, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(a1=7, n=3, s=33)
        assert arith.d == Fraction(4, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(an=15, n=3, s=33)
        assert arith.d == Fraction(4, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(an=15, s=33)
        with self.assertRaises(DAndSError):
            arith.d = 2

    def test_n(self):
        arith = ArithmeticProgression(an=15, a1=7, d=4)
        assert arith.n == 3
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(an=15, a1=7, s=33)
        assert arith.n == 3
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(a1=15, n=1, an=30)
        assert arith.d == 0

        with self.assertRaises(AttributeError):
            ArithmeticProgression(a1=15, n=1.4, an=30)

    def test_s(self):
        arith = ArithmeticProgression(a1=7, an=15, d=4)
        assert arith.s == Fraction(33, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(a1=7, an=15, n=3)
        assert arith.s == Fraction(33, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(a1=7, n=3, d=4)
        assert arith.s == Fraction(33, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(an=15, n=3, d=4)
        assert arith.s == Fraction(33, 1)
        assert list(arith) == [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        arith = ArithmeticProgression(an=15, d=4)
        with self.assertRaises(DAndSError):
            arith.s = 30

    def test_get_current_index(self):
        arith = ArithmeticProgression(a1=1, d=2, n=3)
        with self.assertRaises(AttributeError):
            assert arith.get_current_index() is None
        assert next(arith) == Fraction(1, 1)
        assert arith.get_current_index() == 0
        assert next(arith) == Fraction(3, 1)
        assert arith.get_current_index() == 1
        assert next(arith) == Fraction(5, 1)
        assert arith.get_current_index() == 2
        with self.assertRaises(StopIteration):
            next(arith)
        assert arith.get_current_index() == 2

    def test_get_dict(self):
        assert ArithmeticProgression(n=15, a1=1, d=2).get_parameters_dict() == {'a1': Fraction(1, 1),
                                                                                'an': Fraction(29, 1), 'n': 15,
                                                                                'd': Fraction(2, 1),
                                                                                's': Fraction(225, 1)}

    def test_check_args_error(self):
        with self.assertRaises(AttributeError):
            ArithmeticProgression(n=15, a1=1).__next__()

        with self.assertRaises(AttributeError):
            ArithmeticProgression(n=15, a1=1, an=20, d=10).__next__()


