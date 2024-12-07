from abc import abstractmethod, ABC
from typing import Any, cast, Union

from musurgia.musurgia_exceptions import SegmentedLineSegmentHasMarginsError, SegmentedLineLengthsCannotBeSetError
from musurgia.musurgia_types import HorizontalVertical, check_type, ConvertibleToFloat, MarkLinePlacement, PositionType, \
    MarginType
from musurgia.pdf.drawobject import SlaveDrawObject, MasterDrawObject, DrawObject, HasShowProtocol
from musurgia.pdf.labeled import Labeled
from musurgia.pdf.margined import Margined
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.positioned import Positioned, HasPositionsProtocol
from musurgia.pdf.rowcolumn import DrawObjectRow, DrawObjectColumn, DrawObjectContainer

__all__ = ['HorizontalLineSegment', 'VerticalLineSegment', 'StraightLine', 'HorizontalSegmentedLine',
           'VerticalSegmentedLine']


class AbstractStraightLine(Labeled, ABC, HasPositionsProtocol, HasShowProtocol):
    def __init__(self, mode: HorizontalVertical, length: ConvertibleToFloat, *args: Any,
                 **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._mode: HorizontalVertical
        self._length: float

        self.mode = mode
        self.length = length  # type: ignore

    @property
    def mode(self) -> HorizontalVertical:
        return self._mode

    @mode.setter
    def mode(self, val: HorizontalVertical) -> None:
        check_type(val, 'HorizontalVertical', class_name=self.__class__.__name__, property_name='mode')
        self._mode = val

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='length')
        self._length = float(val)

    @property
    def is_vertical(self) -> bool:
        if self.mode in ['v', 'vertical']:
            return True
        else:
            return False

    @property
    def is_horizontal(self) -> bool:
        if self.mode in ['h', 'horizontal']:
            return True
        else:
            return False

    @staticmethod
    def get_opposite_mode(mode: HorizontalVertical) -> HorizontalVertical:
        if mode == 'h':
            return 'v'
        elif mode == 'v':
            return 'h'
        elif mode == 'horizontal':
            return 'vertical'
        elif mode == 'vertical':
            return 'horizontal'
        else:
            raise NotImplementedError  # pragma: no cover

    def get_relative_x2(self) -> float:
        if self.is_horizontal:
            return self.relative_x + self.length
        else:
            return self.relative_x

    def get_relative_y2(self) -> float:
        if self.is_vertical:
            return self.relative_y + self.length
        else:
            return self.relative_y

    def draw(self, pdf: Pdf) -> None:
        if self.show:
            with pdf.pdf_draw_object_translate(cast(DrawObject, self)):
                self.draw_above_text_labels(pdf)
                self.draw_left_text_labels(pdf)
                self.draw_below_text_labels(pdf)
                x2 = self.get_relative_x2() - self.relative_x
                y2 = self.get_relative_y2() - self.relative_y
                pdf.line(0, 0, x2, y2)


class StraightLine(AbstractStraightLine, DrawObject, Positioned, Margined):
    pass


class SlaveStraightLine(AbstractStraightLine, SlaveDrawObject):
    pass


class MarkLine(SlaveStraightLine):
    def __init__(self, placement: MarkLinePlacement, mode: HorizontalVertical, length: ConvertibleToFloat = 3,
                 *args: Any, **kwargs: Any):
        super().__init__(length=length, mode=mode, *args, **kwargs)  # type: ignore
        self._placement: MarkLinePlacement
        self.placement = placement

    @property
    def placement(self) -> MarkLinePlacement:
        return self._placement

    @placement.setter
    def placement(self, val: MarkLinePlacement) -> None:
        check_type(val, 'MarkLinePlacement', class_name=self.__class__.__name__, property_name='placement')
        self._placement = val


class LineSegment(MasterDrawObject, ABC):

    def __init__(self, mode: HorizontalVertical, length: ConvertibleToFloat, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._straight_line = SlaveStraightLine(simple_name='straight_line', mode=mode, length=length, master=self)
        marker_mode = SlaveStraightLine.get_opposite_mode(self.mode)
        self._start_mark_line = MarkLine(simple_name='start_mark_line', mode=marker_mode, master=self,
                                         placement='start')
        self._end_mark_line = MarkLine(simple_name='end_mark_line', mode=marker_mode, master=self, placement='end',
                                       show=False)

    @property
    def is_vertical(self) -> bool:
        if self.mode in ['v', 'vertical']:
            return True
        return False

    @property
    def is_horizontal(self) -> bool:
        if self.mode in ['h', 'horizontal']:
            return True
        return False

    @property
    def straight_line(self) -> SlaveStraightLine:
        return self._straight_line

    @property
    def start_mark_line(self) -> MarkLine:
        return self._start_mark_line

    @property
    def end_mark_line(self) -> MarkLine:
        return self._end_mark_line

    @property
    def mode(self) -> HorizontalVertical:
        return self.straight_line.mode

    @property
    def length(self) -> float:
        return self.straight_line.length

    @length.setter
    def length(self, value: ConvertibleToFloat) -> None:
        self.straight_line.length = value  # type: ignore

    def get_slave_margin(self, slave: SlaveStraightLine, margin: MarginType) -> float:
        check_type(margin, 'MarginType', class_name='self.__class__.__name__', method_name='get_slave_margin',
                   argument_name='margin')
        return 0

    def _get_max_markline_length(self) -> float:
        return max([self.start_mark_line.length, self.end_mark_line.length])

    def _get_slave_x(self, slave: SlaveStraightLine) -> float:
        max_markline_length = self._get_max_markline_length()
        if self.is_horizontal:
            if slave == self.end_mark_line:
                return self.get_relative_x2()
            else:
                return self.relative_x
        else:
            if slave == self.straight_line:
                return self.relative_x + max_markline_length / 2
            elif slave.length == max_markline_length:
                return self.relative_x
            else:
                return self.relative_x + (max_markline_length - slave.length) / 2

    def _get_slave_y(self, slave: SlaveStraightLine) -> float:
        max_markline_length = self._get_max_markline_length()
        if self.is_vertical:
            if slave == self.end_mark_line:
                return self.get_relative_y2()
            return self.relative_y
        else:
            if slave == self.straight_line:
                return self.relative_y + max_markline_length / 2
            elif slave.length == max_markline_length:
                return self.relative_y
            else:
                return self.relative_y + (max_markline_length - slave.length) / 2

    def get_slave_position(self, slave: SlaveStraightLine, position: PositionType) -> float:
        check_type(position, 'PositionType', class_name='self.__class__.__name__', method_name='get_slave_position',
                   argument_name='position')
        if position == 'x':
            return self._get_slave_x(slave)
        else:
            return self._get_slave_y(slave)

    def set_straight_line_relative_y(self, val: Union[int, float]) -> None:
        if self.is_vertical:
            raise NotImplementedError  # pragma: no cover
        self.relative_y = val - self._get_max_markline_length() / 2

    def set_straight_line_relative_x(self, val: Union[int, float]) -> None:
        if self.is_horizontal:
            raise NotImplementedError  # pragma: no cover
        self.relative_x = val - self._get_max_markline_length() / 2


class HorizontalLineSegment(LineSegment):
    def __init__(self, length: ConvertibleToFloat, *args: Any, **kwargs: Any):
        super().__init__(mode='horizontal', length=length, *args, **kwargs)  # type: ignore

    def get_relative_x2(self) -> float:
        return self.relative_x + self.length

    def get_relative_y2(self) -> float:
        return self.relative_y + self._get_max_markline_length()

    def draw(self, pdf: Pdf) -> None:
        self.start_mark_line.draw(pdf)
        self.straight_line.draw(pdf)
        self.end_mark_line.draw(pdf)


class VerticalLineSegment(LineSegment):
    def __init__(self, length: ConvertibleToFloat, *args: Any, **kwargs: Any):
        super().__init__(mode='vertical', length=length, *args, **kwargs)  # type: ignore

    def get_relative_x2(self) -> float:
        return self.relative_x + max([ml.get_width() for ml in [self.start_mark_line, self.end_mark_line]])

    def get_relative_y2(self) -> float:
        return self.relative_y + self.length

    def draw(self, pdf: Pdf) -> None:
        self.start_mark_line.draw(pdf)
        self.straight_line.draw(pdf)
        self.end_mark_line.draw(pdf)


class AbstractSegmentedLine(DrawObjectContainer):
    def __init__(self, lengths: list[ConvertibleToFloat], *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._make_segments(lengths)

    @property
    def lengths(self) -> None:
        raise AttributeError('use get_lengths instead')

    @lengths.setter
    def lengths(self, lengths: Any) -> None:
        raise SegmentedLineLengthsCannotBeSetError('lengths are not settable after initialization.')

    def _check_segment_margins(self) -> None:
        for seg in self.segments:
            if seg.margins != (0, 0, 0, 0):
                raise SegmentedLineSegmentHasMarginsError()

    @property
    def segments(self) -> list[LineSegment]:
        return cast(list[LineSegment], self.get_draw_objects())

    @abstractmethod
    def _make_segments(self, lengths: list[ConvertibleToFloat]) -> None:
        """private method for making segments"""

    @property
    def is_vertical(self) -> bool:
        return self.segments[0].is_vertical

    @property
    def is_horizontal(self) -> bool:
        return self.segments[0].is_horizontal

    def set_straight_line_relative_y(self, val: Union[float, int]) -> None:
        if self.is_horizontal:
            delta = val - self.segments[0].straight_line.relative_y
            self.relative_y += delta
        else:
            raise NotImplementedError  # pragma: no cover

    def set_straight_line_relative_x(self, val: Union[float, int]) -> None:
        if self.is_vertical:
            delta = val - self.segments[0].straight_line.relative_x
            self.relative_x += delta
        else:
            raise NotImplementedError  # pragma: no cover

    def get_lengths(self) -> list[float]:
        return [seg.length for seg in self.segments]


class HorizontalSegmentedLine(AbstractSegmentedLine, DrawObjectRow):

    def _make_segments(self, lengths: list[ConvertibleToFloat]) -> None:
        if lengths:
            for length in lengths:
                self.add_draw_object(HorizontalLineSegment(length))
            self.segments[-1].end_mark_line.show = True

    def _align_segments(self) -> None:
        reference_segment = max(self.segments, key=lambda seg: seg.get_height())
        for segment in self.segments:
            if segment != reference_segment:
                segment.set_straight_line_relative_y(reference_segment.straight_line.relative_y)

    def draw(self, pdf: Pdf) -> None:
        self._check_segment_margins()
        self._align_segments()
        super().draw(pdf)


class VerticalSegmentedLine(AbstractSegmentedLine, DrawObjectColumn):

    def _make_segments(self, lengths: list[ConvertibleToFloat]) -> None:
        if lengths:
            for length in lengths:
                self.add_draw_object(VerticalLineSegment(length))
            self.segments[-1].end_mark_line.show = True

    def _align_segments(self) -> None:
        reference_segment = max(self.segments, key=lambda seg: seg.get_width())
        for segment in self.segments:
            if segment != reference_segment:
                segment.set_straight_line_relative_x(reference_segment.straight_line.relative_x)

    def draw(self, pdf: Pdf) -> None:
        self._check_segment_margins()
        self._align_segments()
        super().draw(pdf)
