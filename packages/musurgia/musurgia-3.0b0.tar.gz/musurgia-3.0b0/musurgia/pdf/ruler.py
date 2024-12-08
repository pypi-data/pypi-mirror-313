from abc import ABC
from typing import Any, cast, Optional, Callable

from musurgia.musurgia_exceptions import RulerCannotSetLengthsError, RulerLengthNotPositiveError, \
    TimeRulerCannotSetLength
from musurgia.musurgia_types import ConvertibleToFloat, check_type, ClockMode
from musurgia.pdf import TextLabel
from musurgia.pdf.line import AbstractSegmentedLine, MarkLine, VerticalSegmentedLine, HorizontalSegmentedLine
from musurgia.timing.duration import Duration

__all__ = ['HorizontalRuler', 'VerticalRuler', 'TimeRuler']


class AbstractRuler(AbstractSegmentedLine, ABC):
    def __init__(self, length: ConvertibleToFloat, unit: ConvertibleToFloat = 10.0, first_label: int = 0,
                 label_show_interval: int = 1, show_first_label: bool = True, *args: Any, **kwargs: Any):
        if 'lengths' in kwargs:
            raise RulerCannotSetLengthsError
        check_type(length, 'ConvertibleToFloat', class_name='AbstractRuler', property_name='length')
        length = float(length)
        if length < 0:
            raise RulerLengthNotPositiveError
        check_type(unit, 'ConvertibleToFloat', class_name='AbstractRuler', property_name='unit')
        check_type(first_label, int, class_name='AbstractRuler', property_name='first_label')
        check_type(label_show_interval, int, class_name='AbstractRuler', property_name='label_show_interval')
        check_type(show_first_label, bool, class_name='AbstractRuler', property_name='show_first_label')

        unit = float(unit)
        number_of_units = float(length) / unit
        partial_segment_length = number_of_units - int(number_of_units)
        lengths = int(number_of_units) * [unit]
        if partial_segment_length:
            lengths += [partial_segment_length * unit]
        super().__init__(lengths=lengths, *args, **kwargs)  # type: ignore
        if partial_segment_length:
            self.segments[-1].end_mark_line.show = False

        self._unit = unit
        self._first_label = first_label
        self._label_show_interval = label_show_interval
        self._show_first_label = show_first_label
        self._set_labels()

    def _set_labels(self) -> None:
        def _add_label(mark_line: MarkLine, txt: str) -> None:
            tl = TextLabel(txt, master=mark_line)
            if isinstance(self, VerticalSegmentedLine):
                tl.placement = 'left'
                tl.right_margin = 1
                tl.top_margin = 0
            else:
                tl.bottom_margin = 1
            mark_line.add_text_label(tl)

        for index, segment in enumerate(self.segments):
            if not self.get_show_first_label() and index == 0:
                pass
            else:
                if index % self.get_label_show_interval() == 0:
                    mark_line = segment.start_mark_line
                    _add_label(mark_line, str(index + self.get_first_label()))

        if self.segments:
            last_segment_end_mark_line = self.segments[-1].end_mark_line
            if last_segment_end_mark_line.show and (len(self.segments)) % self.get_label_show_interval() == 0:
                _add_label(last_segment_end_mark_line, str(len(self.segments) + self.get_first_label()))

    def get_markline_text_labels(self) -> list[TextLabel]:
        return [label for seg in self.segments for label in
                seg.start_mark_line.get_text_labels() + seg.end_mark_line.get_text_labels()]

    def change_labels(self, condition: Optional[Callable[[TextLabel], bool]] = None, **kwargs: Any) -> None:
        if condition is None:
            condition = lambda label: True
        labels = [l for l in self.get_markline_text_labels() if condition(l)]
        for label in labels:
            for key, value in kwargs.items():
                setattr(label, key, value)

    @property
    def length(self) -> None:
        raise AttributeError('use get_length() instead')

    @length.setter
    def length(self, val: Any) -> None:
        raise AttributeError('length is not settable after initialization.')

    @property
    def unit(self) -> None:
        raise AttributeError('use get_unit() instead')

    @unit.setter
    def unit(self, val: Any) -> None:
        raise AttributeError('unit is not settable after initialization.')

    @property
    def first_label(self) -> None:
        raise AttributeError('use get_first_label() instead')

    @first_label.setter
    def first_label(self, val: Any) -> None:
        raise AttributeError('first_label is not settable after initialization.')

    @property
    def label_show_interval(self) -> None:
        raise AttributeError('use get_label_show_interval() instead')

    @label_show_interval.setter
    def label_show_interval(self, val: Any) -> None:
        raise AttributeError('label_show_interval is not settable after initialization.')

    @property
    def show_first_label(self) -> None:
        raise AttributeError('use get_show_first_label() instead')

    @show_first_label.setter
    def show_first_label(self, val: Any) -> None:
        raise AttributeError('show_first_label is not settable after initialization.')

    def get_unit(self) -> float:
        return float(self._unit)

    def get_length(self) -> float:
        return float(sum([seg.length for seg in self.segments]))

    def get_first_label(self) -> int:
        return self._first_label

    def get_label_show_interval(self) -> int:
        return self._label_show_interval

    def get_show_first_label(self) -> bool:
        return self._show_first_label


class HorizontalRuler(AbstractRuler, HorizontalSegmentedLine):
    pass


class VerticalRuler(AbstractRuler, VerticalSegmentedLine):
    pass


class TimeRuler(HorizontalRuler):
    def __init__(self, duration: int, unit: ConvertibleToFloat = 2, label_show_interval: int = 10,
                 shrink_factor: ConvertibleToFloat = 0.6, mark_line_size: ConvertibleToFloat = 4,
                 clock_mode: ClockMode = 'hms',
                 *args: Any,
                 **kwargs: Any):
        if 'length' in kwargs:
            raise TimeRulerCannotSetLength
        check_type(duration, 'PositiveInteger', class_name='TimeRuler', property_name='duration')
        super().__init__(length=duration * unit, unit=unit, label_show_interval=label_show_interval, *args,
                         **kwargs)  # type: ignore
        self._clock_mode: ClockMode = clock_mode
        self._change_label_texts()
        self._shrink_factor: ConvertibleToFloat
        self._mark_line_size: ConvertibleToFloat
        self.shrink_factor = shrink_factor  # type: ignore
        self.mark_line_size = mark_line_size  # type: ignore

    def _change_label_texts(self) -> None:
        for label in self.get_markline_text_labels():
            duration = Duration(float(label.value))
            label.value = duration.get_clock_as_string(mode=self._clock_mode, round_=1)
            if label.value[-2:] == '.0':
                label.value = label.value[:-2]

    def _change_mark_line_lengths(self) -> None:
        try:
            sf = self.shrink_factor
            mls = self.mark_line_size
            for i, seg in enumerate(self.segments):
                if i % self.get_label_show_interval() == 0:
                    seg.start_mark_line.length = mls
                else:
                    seg.start_mark_line.length = mls * sf

            if len(self.segments) % self.get_label_show_interval() == 0:
                self.segments[-1].end_mark_line.length = mls
            else:
                self.segments[-1].end_mark_line.length = mls * sf

        except AttributeError:
            pass

    def get_duration(self) -> float:
        return self.get_length() / self.get_unit()

    @property
    def shrink_factor(self) -> float:
        return cast(float, self._shrink_factor)

    @shrink_factor.setter
    def shrink_factor(self, val: ConvertibleToFloat) -> None:
        self._shrink_factor = float(val)
        self._change_mark_line_lengths()

    @property
    def mark_line_size(self) -> float:
        return cast(float, self._mark_line_size)

    @mark_line_size.setter
    def mark_line_size(self, val: ConvertibleToFloat) -> None:
        self._mark_line_size = float(val)
        self._change_mark_line_lengths()
