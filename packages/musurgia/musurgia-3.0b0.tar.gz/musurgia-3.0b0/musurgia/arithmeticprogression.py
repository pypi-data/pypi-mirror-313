from typing import Optional, Union, cast

from fractions import Fraction

from musurgia.musurgia_exceptions import DAndSError
from musurgia.musurgia_types import check_type


class ArithmeticProgression:
    def __init__(self, a1: Optional[Union[int, float, Fraction]] = None,
                 an: Optional[Union[int, float, Fraction]] = None,
                 n: Optional[int] = None, d: Optional[Union[int, float, Fraction]] = None,
                 s: Optional[Union[int, float, Fraction]] = None, correct_s: bool = False):
        self._a1: Optional[Union[int, float, Fraction]] = None
        self._an: Optional[Union[int, float, Fraction]] = None
        self._n: Optional[Union[int, float, Fraction]] = None
        self._d: Optional[Union[int, float, Fraction]] = None
        self._s: Optional[Union[int, float, Fraction]] = None
        self._current: Fraction
        self._index: int
        self._correction_factor: Optional[Fraction] = None
        self._correct_s: bool

        self.a1 = a1  # type: ignore
        self.an = an  # type: ignore
        self.n = n  # type: ignore
        self.d = d  # type: ignore
        self.s = s  # type: ignore
        self.correct_s = correct_s

    # private methods

    def _check_args(self, arg: Optional[str] = None) -> None:
        if arg is None:
            err = 'Not enough attributes are set. Three are needed!'
            if len([v for v in self._get_private_parameters_dict().values() if v is not None]) < 3:
                raise AttributeError(err)
        else:
            if self._get_private_parameters_dict()[arg] is None and len(
                    [v for v in self._get_private_parameters_dict().values() if v is not None]) > 2:
                err = 'attribute cannot be set. Three parameters are already set. ArithmeticProgression is already ' \
                      'created!'
                raise AttributeError(err)

    def _calculate_a1(self) -> Fraction:
        if self._d is None:
            return Fraction(2 * self.s, self.n) - self.an
        else:
            return self.an - ((self.n - 1) * self.d)

    def _calculate_an(self) -> Fraction:
        if self._s is None:
            return self.a1 + (self.n - 1) * self.d
        else:
            return Fraction(2 * self.s, self.n) - self.a1

    def _calculate_n(self) -> int:
        if self._s is None:
            output = Fraction((self.an - self.a1), self.d) + 1
        else:
            output = 2 * Fraction(self.s, (self.a1 + self.an))
        return int(output)

    def _calculate_d(self) -> Fraction:
        if self.n == 1:
            output = Fraction(0)
        elif self._a1 is None:
            self._a1 = self._calculate_a1()
            output = Fraction((self.an - self.a1), (self.n - 1))
        elif self._an is None:
            output = Fraction(((self.s - (self.n * self.a1)) * 2), ((self.n - 1) * self.n))
        # elif self._n is None:
        #     self._n = self._calculate_n()
        #     output = Fraction((self.an - self.a1), (self.n - 1))
        else:
            output = Fraction((self.an - self.a1), (self.n - 1))
        return output

    def _calculate_s(self) -> Fraction:
        if self._a1 is None:
            self._a1 = self._calculate_a1()
            output = (self.a1 + self.an) * Fraction(self.n, 2)
        elif self._an is None:
            output = self.n * self.a1 + ((self.n - 1) * Fraction(self.n, 2)) * self.d
        elif self._n is None:
            self._n = self._calculate_n()
            output = (self.a1 + self.an) * Fraction(self.n, 2)
        else:
            output = (self.a1 + self.an) * Fraction(self.n, 2)
        return output

    def _get_private_parameters_dict(self) -> dict[str, Optional[Union[int, Fraction, float]]]:
        return {'a1': self._a1, 'an': self._an, 'n': self._n, 'd': self._d, 's': self._s}

    def _to_fraction(self, value: Union[int, float, Fraction]) -> Fraction:
        if not isinstance(value, Fraction):
            value = Fraction(value)
        return value

    # public properties

    @property
    def a1(self) -> Fraction:
        """
        >>> arith = ArithmeticProgression(n=3, an=15, d=4)
        >>> arith.a1
        Fraction(7, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]


        >>> arith = ArithmeticProgression(n=3, an=15, s=33)
        >>> arith.a1
        Fraction(7, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]


        :return:
        """
        if self._a1 is None:
            self._a1 = self._calculate_a1()
        else:
            self._a1 = self._to_fraction(self._a1)
        return self._a1

    @a1.setter
    def a1(self, value: Optional[Union[int, float, Fraction]]) -> None:
        if value is not None:
            self._check_args('a1')
        self._a1 = value

    @property
    def an(self) -> Fraction:
        """
        >>> arith = ArithmeticProgression(n=3, a1=7, d=4)
        >>> arith.an
        Fraction(15, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(n=3, a1=7, s=33)
        >>> arith.an
        Fraction(15, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        :return:
        """
        if self._an is None:
            self._an = self._calculate_an()
        else:
            self._an = self._to_fraction(self._an)
        return self._an

    @an.setter
    def an(self, value: Optional[Union[int, float, Fraction]]) -> None:
        if value is not None:
            self._check_args('an')
        self._an = value

    @property
    def correct_s(self) -> bool:
        """
        >>> arith = ArithmeticProgression(a1= 3, an=6, s=21)
        >>> arith.get_parameters_dict()
        {'a1': Fraction(3, 1), 'an': Fraction(6, 1), 'n': 4, 'd': Fraction(1, 1), 's': Fraction(21, 1)}
        >>> arith.get_actual_s()
        Fraction(18, 1)
        >>> result = list(arith)
        >>> result
        [Fraction(3, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1)]
        >>> sum(result)
        Fraction(18, 1)

        >>> arith.correct_s = True
        >>> arith.reset_iterator()
        >>> arith.get_correction_factor()
        Fraction(7, 6)
        >>> result = list(arith)
        >>> result
        [Fraction(7, 2), Fraction(14, 3), Fraction(35, 6), Fraction(7, 1)]
        >>> sum(result)
        Fraction(21, 1)

        """
        return self._correct_s

    @correct_s.setter
    def correct_s(self, val: bool) -> None:
        check_type(val, bool, class_name=self.__class__.__name__, property_name='correct_s')
        self._correct_s = val
        self._correction_factor = None

    @property
    def d(self) -> Fraction:
        """"
        >>> arith = ArithmeticProgression(a1= 7, an=15, s=33)
        >>> arith.d
        Fraction(4, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(a1= 7, an=15, n=3)
        >>> arith.d
        Fraction(4, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(a1= 7, n=3, s=33)
        >>> arith.d
        Fraction(4, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(an= 15, n=3, s=33)
        >>> arith.d
        Fraction(4, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]
        """
        if self._d is None:
            self._d = self._calculate_d()
        else:
            self._d = self._to_fraction(self._d)
        return self._d

    @d.setter
    def d(self, value: Optional[Union[int, float, Fraction]]) -> None:
        if value is not None:
            self._check_args('d')
            if self._s is not None:
                raise DAndSError()
        self._d = value

    @property
    def n(self) -> int:
        """
        >>> arith = ArithmeticProgression(an=15, a1=7, d=4)
        >>> arith.n
        3
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(an=15, a1=7, s=33)
        >>> arith.n
        3
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        :return:
        """

        if self._n is None:
            self._n = self._calculate_n()
        return int(self._n)

    @n.setter
    def n(self, value: Optional[int]) -> None:
        if value is not None:
            if not isinstance(value, int):
                raise AttributeError('n {} must be int'.format(value))
            self._check_args('n')
        self._n = value

    @property
    def s(self) -> Fraction:
        """
        >>> arith = ArithmeticProgression(a1= 7, an=15, d=4)
        >>> arith.s
        Fraction(33, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(a1= 7, an=15, n=3)
        >>> arith.s
        Fraction(33, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(a1= 7, n=3, d=4)
        >>> arith.s
        Fraction(33, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(an= 15, n=3, d=4)
        >>> arith.s
        Fraction(33, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        """

        if self._s is None:
            self._s = self._calculate_s()
        else:
            self._s = self._to_fraction(self._s)
        return self._s

    @s.setter
    def s(self, value: Optional[Union[int, float, Fraction]]) -> None:
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('s')
            if self._d is not None:
                raise DAndSError()
        self._s = value

    # public methods

    def get_actual_s(self) -> Fraction:
        return self.n * Fraction((self.a1 + self.an), 2)

    def get_correction_factor(self) -> Fraction:
        def _calculate_correction_factor() -> Fraction:
            if self.correct_s:
                return Fraction(self.s, self.get_actual_s())
            else:
                return Fraction(1, 1)

        if self._correction_factor is None:
            self._correction_factor = _calculate_correction_factor()
        return self._correction_factor

    def get_current_index(self) -> Optional[int]:
        """
        >>> arith = ArithmeticProgression(a1=1, d=2, n=3)
        >>> next(arith)
        Fraction(1, 1)
        >>> arith.get_current_index()
        0
        >>> next(arith)
        Fraction(3, 1)
        >>> arith.get_current_index()
        1
        >>> next(arith)
        Fraction(5, 1)
        >>> arith.get_current_index()
        2
        >>> next(arith)
        Traceback (most recent call last):
            ...
        StopIteration
        >>> arith.get_current_index()
        2
        """
        return self._index

    def get_parameters_dict(self) -> dict[str, Union[int, Fraction]]:
        """
        >>> ArithmeticProgression(n=15, a1=1, d=2).get_parameters_dict()
        {'a1': Fraction(1, 1), 'an': Fraction(29, 1), 'n': 15, 'd': Fraction(2, 1), 's': Fraction(225, 1)}

        :return:
        """
        return {'a1': self.a1, 'an': self.an, 'n': self.n, 'd': self.d, 's': self.s}

    def reset_iterator(self) -> None:
        del self._current
        del self._index

    def __iter__(self) -> 'ArithmeticProgression':
        return self

    def __next__(self) -> Fraction:
        try:
            self._current
        except AttributeError:
            self._check_args()
            self._current = self.a1
        try:
            if self._index + 1 >= self.n:
                raise StopIteration()
            self._index += 1
            self._current += self.d
        except AttributeError:
            self._index = 0

        return self._current * self.get_correction_factor()
