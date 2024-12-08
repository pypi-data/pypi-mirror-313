from typing import Any, Optional

from musurgia.musurgia_exceptions import ClockWrongSecondsTypeError, ClockWrongSecondsValueError, \
    ClockWrongMinutesTypeError, ClockWrongHoursTypeError, ClockWrongMinutesValueError
from musurgia.musurgia_types import check_type, create_error_message, ClockMode, ConvertibleToFloat


class Clock:
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: float = 0, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._hours: int
        self._minutes: int
        self._seconds: float

        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @property
    def hours(self) -> int:
        return self._hours

    @hours.setter
    def hours(self, val: int) -> None:
        try:
            check_type(val, int, class_name=self.__class__.__name__, property_name='hours')
        except TypeError as err:
            raise ClockWrongHoursTypeError(err)
        self._hours = val

    @property
    def minutes(self) -> int:
        return self._minutes

    @minutes.setter
    def minutes(self, val: int) -> None:
        try:
            check_type(val, int, class_name=self.__class__.__name__, property_name='minutes')
        except TypeError as err:
            raise ClockWrongMinutesTypeError(err)
        if -60 <= val >= 60:
            msg = create_error_message(message=f'{val} must be between -60 and 60', class_name=self.__class__.__name__,
                                       property_name='minutes')
            raise ClockWrongMinutesValueError(msg)
        self._minutes = val

    @property
    def seconds(self) -> float:
        return self._seconds

    @seconds.setter
    def seconds(self, val: float) -> None:
        try:
            check_type(val, float, class_name=self.__class__.__name__, property_name='seconds')
        except TypeError as err:
            raise ClockWrongSecondsTypeError(err)
        if -60 <= val >= 60:
            msg = create_error_message(message=f'{val} must be between -60 and 60', class_name=self.__class__.__name__,
                                       property_name='seconds')
            raise ClockWrongSecondsValueError(msg)
        self._seconds = val

    def get_values(self) -> tuple[int, int, float]:
        return self.hours, self.minutes, self.seconds

    def set_values(self, hours: int, minutes: int, seconds: float) -> None:
        self.hours, self.minutes, self.seconds = hours, minutes, seconds

    def get_as_string(self, mode: ClockMode = 'hms', round_: Optional[int] = None) -> str:
        check_type(mode, 'ClockMode', class_name=self.__class__.__name__, method_name='get_as_string',
                   argument_name='mode')
        s, m, h = self.seconds, self.minutes, self.hours

        if round_:
            s = round(s, round_)

        if m // 10 == 0 and mode != 'msreduced':
            string_m = '0' + str(m)
        else:
            string_m = str(m)

        if int(s // 10) == 0 and mode != 'msreduced':
            string_s = '0' + str(s)
        else:
            string_s = str(s)

        string_h = str(h)

        if not mode or mode == 'hms':
            return string_h + ':' + string_m + ':' + string_s

        elif mode == 'ms':
            return string_m + ':' + string_s
        elif mode == 'msreduced':
            if string_m == '0':
                return string_s
            else:
                return string_m + ':' + string_s

    def calculate_in_seconds(self) -> float:
        return self.convert_clock_to_seconds(self.hours, self.minutes, self.seconds)

    @staticmethod
    def convert_clock_to_seconds(hours: ConvertibleToFloat, minutes: ConvertibleToFloat,
                                 seconds: ConvertibleToFloat) -> float:
        check_type(hours, 'ConvertibleToFloat', class_name='Clock',
                   method_name='convert_clock_to_seconds', argument_name='hours')
        check_type(minutes, 'ConvertibleToFloat', class_name='Clock',
                   method_name='convert_clock_to_seconds', argument_name='minutes')
        check_type(seconds, 'ConvertibleToFloat', class_name='Clock',
                   method_name='convert_clock_to_seconds', argument_name='seconds')
        return float(seconds) + (60 * float(minutes)) + (3600 * float(hours))

    @staticmethod
    def convert_seconds_to_clock(seconds: float) -> 'Clock':
        h = int(seconds / 3600.0)
        s = seconds - h * 3600
        m = int(s / 60.)
        s = s - m * 60

        return Clock(hours=h, minutes=m, seconds=s)

    def add_clock(self, clock: 'Clock') -> 'Clock':
        seconds = self.calculate_in_seconds() + clock.calculate_in_seconds()
        return self.convert_seconds_to_clock(seconds)

    def __add__(self, other: 'Clock') -> 'Clock':
        return self.add_clock(other)

    def subtract_clock(self, clock: 'Clock') -> 'Clock':
        seconds = self.calculate_in_seconds() - clock.calculate_in_seconds()
        return self.convert_seconds_to_clock(seconds)

    def __sub__(self, other: 'Clock') -> 'Clock':
        return self.subtract_clock(other)
