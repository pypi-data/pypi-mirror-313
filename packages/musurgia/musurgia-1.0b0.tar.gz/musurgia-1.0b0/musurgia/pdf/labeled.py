from typing import Union, Any, Optional

from musurgia.musurgia_types import check_type, PositionType, create_error_message, LabelPlacement, MarginType
from musurgia.pdf.drawobject import HasGetHeightProtocol, PositionedSlave, Master
from musurgia.pdf.margined import Margined
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.positioned import HasPositionsProtocol
from musurgia.pdf.text import AbstractText

__all__ = ['TextLabel']


class TextLabel(PositionedSlave, AbstractText, Margined):
    def __init__(self, value: Any, master: Optional[Master] = None, placement: LabelPlacement = 'above',
                 *args: Any,
                 **kwargs: Any) -> None:
        self._master: Optional[Master]
        self.master = master
        super().__init__(value=value, *args, **kwargs)  # type: ignore
        self._placement: LabelPlacement
        self.placement = placement

    @property
    def master(self) -> Optional[Master]:
        return self._master

    @master.setter
    def master(self, value: Optional[Master]) -> None:
        self._master = value

    @property
    def placement(self) -> LabelPlacement:
        if not self.master:
            raise AttributeError(create_error_message(message='set master first', class_name=self.__class__.__name__,
                                                      property_name='placement'))
        return self._placement

    @placement.setter
    def placement(self, val: LabelPlacement) -> None:
        check_type(val, 'LabelPlacement', class_name=self.__class__.__name__, property_name='placement')
        self._placement = val


class Labeled(Master, HasPositionsProtocol, HasGetHeightProtocol):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._above_text_labels: list[TextLabel] = []
        self._below_text_labels: list[TextLabel] = []
        self._left_text_labels: list[TextLabel] = []

    def add_text_label(self, label: Union[TextLabel, str], **kwargs: Any) -> TextLabel:
        if not isinstance(label, TextLabel):
            label = TextLabel(label, self, **kwargs)
        else:
            if label.master:
                if label.master != self:
                    raise AttributeError(
                        create_error_message(message=f"label.master {label.master} must be the same as {self}"))
            else:
                label.master = self
        if label.placement == 'above':
            self._above_text_labels.append(label)
        elif label.placement == 'below':
            self._below_text_labels.append(label)
        elif label.placement == 'left':
            self._left_text_labels.append(label)

        return label

    def add_label(self, label: Union[TextLabel, str], **kwargs: Any) -> TextLabel:
        return self.add_text_label(label, **kwargs)

    def get_above_text_labels(self) -> list[TextLabel]:
        return self._above_text_labels

    def get_below_text_labels(self) -> list[TextLabel]:
        return self._below_text_labels

    def get_left_text_labels(self) -> list[TextLabel]:
        return self._left_text_labels

    def get_text_labels(self) -> list[TextLabel]:
        return self.get_left_text_labels() + self.get_above_text_labels() + self.get_below_text_labels()

    def draw_above_text_labels(self, pdf: Pdf) -> None:
        if self.get_above_text_labels():
            with pdf.saved_state():
                translate_y = -self.get_above_text_labels_height() + self.get_above_text_labels()[-1].get_text_height()
                pdf.translate(0, translate_y)
                for text_label in self.get_above_text_labels():
                    text_label.draw(pdf)
                    pdf.translate(0, text_label.get_height())

    def draw_below_text_labels(self, pdf: Pdf) -> None:
        if self.get_below_text_labels():
            with pdf.saved_state():
                pdf.translate(0, self.get_relative_y2() - self.relative_y)
                for text_label in self.get_below_text_labels():
                    pdf.translate(0, text_label.get_height())
                    text_label.draw(pdf)

    def draw_left_text_labels(self, pdf: Pdf) -> None:
        if self.get_left_text_labels():
            with pdf.saved_state():
                pdf.translate(0, -self.get_left_text_labels_height() / 2)
                for text_label in self.get_left_text_labels():
                    pdf.translate(0, text_label.get_height())
                    with pdf.saved_state():
                        pdf.translate(-(text_label.get_width()), 0)
                        text_label.draw(pdf)

    def get_slave_position(self, slave: TextLabel, position: PositionType) -> float:
        check_type(position, 'PositionType', class_name=self.__class__.__name__, method_name='get_slave_position',
                   argument_name='position')
        if not isinstance(slave, TextLabel):
            raise TypeError(
                create_error_message(message=f'slave must be of type TextLabel not {type(slave)}',
                                     class_name=self.__class__.__name__, method_name='get_slave_position',
                                     argument_name='slave'))
        if not slave.master == self:
            raise AttributeError(create_error_message(message=f'slave hat wrong master'))
        if position == 'x':
            return 0
        elif position == 'y':
            if slave.placement in ['l', 'left']:
                return (self.get_relative_y2() - self.relative_y) / 2
            return 0

    def get_above_text_labels_height(self) -> float:
        return sum([tl.get_height() for tl in self.get_above_text_labels()])

    def get_left_text_labels_height(self) -> float:
        return sum([tl.get_height() for tl in self.get_left_text_labels()])

    def get_slave_margin(self, slave: Any, margin: MarginType) -> float:
        raise NotImplementedError  # pragma: no cover
