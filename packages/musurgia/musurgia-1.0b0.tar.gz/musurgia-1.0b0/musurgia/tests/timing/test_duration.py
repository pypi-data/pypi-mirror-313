from math import ceil, floor
from unittest import TestCase

from musicscore import QuarterDuration

from musicscore import Metronome
from musurgia.timing.duration import Duration, convert_duration_to_quarter_duration, \
    convert_quarter_duration_to_duration


class TestDuration(TestCase):
    def test_seconds(self):
        d = Duration(seconds=10)
        assert d.seconds == 10
        assert d.minutes == 0
        assert d.hours == 0
        assert d.get_clock_as_string() == '0:00:10.0'

    def test_seconds_over_60(self):
        d = Duration(seconds=70)
        assert d.seconds == 10
        assert d.minutes == 1
        assert d.hours == 0
        assert d.get_clock_as_string() == '0:01:10.0'

    def test_seconds_over_3600(self):
        d = Duration(seconds=3610)
        assert d.seconds == 10
        assert d.minutes == 0
        assert d.hours == 1
        assert d.get_clock_as_string() == '1:00:10.0'

    def test_seconds_float(self):
        d = Duration(seconds=10.5)
        assert d.get_clock_as_string() == '0:00:10.5'

    def test_minutes(self):
        d = Duration(minutes=10)
        assert d.seconds == 0
        assert d.minutes == 10
        assert d.hours == 0
        assert d.get_clock_as_string() == '0:10:00.0'

    def test_minutes_over_60(self):
        d = Duration(minutes=75)
        assert d.seconds == 0
        assert d.minutes == 15
        assert d.hours == 1
        assert d.get_clock_as_string() == '1:15:00.0'

    def test_minutes_float(self):
        d = Duration(minutes=10.5)
        assert d.get_clock_as_string() == '0:10:30.0'

    def test_hours(self):
        d = Duration(hours=3)
        assert d.seconds == 0
        assert d.minutes == 0
        assert d.hours == 3
        assert d.get_clock_as_string() == '3:00:00.0'

    def test_no_arguments(self):
        d = Duration()
        assert d.seconds == 0
        assert d.minutes == 0
        assert d.hours == 0
        assert d.get_clock_as_string() == '0:00:00.0'

    def test_complex_input(self):
        d = Duration(hours=2.5, minutes=70.5, seconds=70.5)
        assert d.get_clock_as_string() == '3:41:40.5'

    def test_get_clock_modes(self):
        d = Duration(hours=2.5, minutes=90.5, seconds=90.5)
        assert d.get_clock_as_string(mode='hms') == '4:02:00.5'
        assert d.get_clock_as_string(mode='ms') == '02:00.5'
        assert d.get_clock_as_string(mode='msreduced') == '2:0.5'

    def test_calculate_in_seconds(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.calculate_in_seconds() == 5430.0

    def test_calculate_in_minutes(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.calculate_in_minutes() == 90.5

    def test_calculate_in_hours(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.calculate_in_hours() == 1.5083333333333333

    def test_convert_duration_to_quarter_duration(self):
        t = 60
        d = Duration(seconds=3)
        assert convert_duration_to_quarter_duration(d, t) == 3
        t = 30
        assert convert_duration_to_quarter_duration(d, t) == QuarterDuration(6)
        assert convert_duration_to_quarter_duration(3, 120) == 1.5
        t = Metronome(60, 2)
        assert convert_duration_to_quarter_duration(3, t) == 1.5

    def test_convert_quarter_duration_to_duration(self):
        qd = QuarterDuration(2)
        t = 60
        assert convert_quarter_duration_to_duration(qd, t) == Duration(seconds=2) == 2
        t = 120
        assert convert_quarter_duration_to_duration(qd, t) == Duration(seconds=1) == 1
        assert convert_quarter_duration_to_duration(2, t) == Duration(seconds=1) == 1

    def test_set_and_get_values(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.clock.get_values() == (1, 30, 30)
        d.hours = 2
        assert d.clock.get_values() == (2, 30, 30)
        d.minutes = 10
        assert d.clock.get_values() == (2, 10, 30)
        d.seconds = 20.0
        assert d.clock.get_values() == (2, 10, 20)
        d.minutes = 65
        assert d.clock.get_values() == (3, 5, 20)


class TestMagics(TestCase):
    cl = Duration

    def setUp(self):
        self.main = self.cl(70)
        self.equal = self.cl(70)
        self.equal_float = 70.0
        self.larger = self.cl(80)
        self.larger_float = 80.0
        self.smaller = self.cl(60)
        self.smaller_float = 60.0

    def test_abs(self):
        assert abs(self.cl(-70)).calculate_in_seconds() == 70

    def test_ceil(self):
        assert ceil(self.cl(70.2)).calculate_in_seconds() == 71

    def test_floor(self):
        assert floor(self.cl(70.2)).calculate_in_seconds() == 70

    def test_floor_division(self):
        a = self.cl(10)
        b = self.cl(4)
        c = self.cl(2)
        assert a // b == c
        assert a // 4 == c
        assert a // b == 2
        assert a // 4 == 2

    def test_gt(self):
        assert self.main > self.smaller
        assert self.main > self.smaller_float
        assert not self.main > self.equal
        assert not self.main > self.equal_float
        assert not self.main > self.larger
        assert not self.main > self.larger_float

    def test_ge(self):
        assert self.main >= self.smaller
        assert self.main >= self.smaller_float
        assert self.main >= self.equal
        assert self.main >= self.equal_float
        assert not self.main >= self.larger
        assert not self.main >= self.larger_float

    def test_le(self):
        assert not self.main <= self.smaller
        assert not self.main <= self.smaller_float
        assert self.main <= self.equal
        assert self.main <= self.equal_float
        assert self.main <= self.larger
        assert self.main <= self.larger_float

    def test_lt(self):
        assert not self.main < self.smaller
        assert not self.main < self.smaller_float
        assert not self.main < self.equal
        assert not self.main < self.equal_float
        assert self.main < self.larger
        assert self.main < self.larger_float

    def test_mod(self):
        a = self.cl(10)
        b = self.cl(3)
        c = self.cl(1)
        assert a % 3 == c
        assert a % 3 == 1
        assert a % b == c
        assert a % b == 1

    def test_mul(self):
        a = self.cl(10)
        b = self.cl(3)
        c = self.cl(30)
        assert a * b == 30
        assert a * b == c
        assert a * 3 == 30
        assert a * 3 == c

    def test_neg(self):
        a = self.cl(10)
        b = self.cl(-10)
        assert -a == b
        assert -a == -10
        assert -b == a
        assert -b == 10

    def test_pos(self):
        a = self.cl(10)
        assert +a == a

    def test_power(self):
        a = self.cl(10)
        b = self.cl(100)
        assert 10.0 ** 2 == 100
        assert a ** 2 == 100
        assert a ** 2 == b

    def test_radd(self):
        a = self.cl(10)
        b = self.cl(100)
        assert a.__radd__(b) == b + a

    def test_rmod(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rmod__(b) == b % a

    def test_rmul(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rmul__(b) == b * a

    def test_eq(self):
        a = self.cl(10)
        b = self.cl(10)
        c = self.cl(11)
        assert a == b
        assert a == 10
        assert 10 == a
        assert a == 10.0
        assert a != 11
        assert a != c
        assert not a == c
        assert not a == 11
        assert not 11 == a

    def test_round(self):
        assert self.cl(70.7) == self.cl(70.7)
        assert round(self.cl(70.67), 1) == 70.7
        assert round(self.cl(70.67), 1) == self.cl(70.7)
        assert round(self.cl(70.67), 1) != self.cl(70.6)
        assert round(self.cl(70.67), 1) != 70.6

    def test_rtruediv(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rtruediv__(b) == 10 / 3

    def test_truediv(self):
        a = self.cl(10)
        b = self.cl(3)
        assert a / b == 10 / 3

    def test_trunc(self):
        a = self.cl(10.233)
        assert a.__trunc__() == 10

    def test_rfloordiv(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rfloordiv__(b) == b // a
