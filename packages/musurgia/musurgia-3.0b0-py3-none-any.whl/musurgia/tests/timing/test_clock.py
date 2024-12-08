from unittest import TestCase

from musurgia.musurgia_exceptions import ClockWrongSecondsValueError, ClockWrongMinutesValueError, \
    ClockWrongSecondsTypeError, ClockWrongMinutesTypeError, ClockWrongHoursTypeError
from musurgia.timing.clock import Clock


class TestClock(TestCase):
    def test_clock_errors(self):
        with self.assertRaises(ClockWrongSecondsValueError):
            Clock(0, 0, 70.0)
        with self.assertRaises(ClockWrongMinutesValueError):
            Clock(0, 70, 0.0)
        with self.assertRaises(ClockWrongSecondsTypeError):
            Clock(0, 0, 30)
        with self.assertRaises(ClockWrongMinutesTypeError):
            Clock(0, 30.0, 0.0)
        with self.assertRaises(ClockWrongHoursTypeError):
            Clock(1.0, 0, 0.0)

    def test_clock_mode(self):
        c = Clock(4, 2, 0.5)
        assert c.get_as_string(mode='hms') == '4:02:00.5'
        assert c.get_as_string(mode='ms') == '02:00.5'
        assert c.get_as_string(mode='msreduced') == '2:0.5'
        assert c.get_as_string(mode='msreduced') == '2:0.5'

        c.set_values(0, 0, 1.5)
        assert c.get_as_string(mode='msreduced') == '1.5'

    def test_get_as_string_round(self):
        c = Clock(4, 2, 1.2568)
        assert c.get_as_string(mode='hms', round_=2) == '4:02:01.26'

    def test_get_and_set_values(self):
        c = Clock(4, 2, 0.5)
        assert c.get_values() == (4, 2, 0.5)
        c.set_values(3, 1, 10.5)
        assert c.get_as_string() == '3:01:10.5'
        c.minutes = 5
        assert c.get_as_string() == '3:05:10.5'

    def test_add_clocks(self):
        c1 = Clock(1, 2, 0.5)
        c2 = Clock(2, 59, 59.5)
        c = c1 + c2
        assert c.get_values() == (4, 2, 0.0)

    def test_subtract_clocks(self):
        c1 = Clock(4, 2, 0.0)
        c2 = Clock(2, 59, 59.5)
        c = c1 - c2
        assert c.get_values() == (1, 2, 0.5)
