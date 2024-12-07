from unittest import TestCase

from musurgia.musurgia_exceptions import RelativePositionNotSettableError, MarginNotSettableError
from musurgia.pdf.drawobject import PositionedSlave, MarginedSlave
from musurgia.pdf.margined import Margined, AbstractMargined
from musurgia.pdf.positioned import Positioned
from musurgia.tests.utils_for_tests import DummyMaster


class Human(Positioned, Margined):
    pass


class Master(DummyMaster):
    def get_slave_position(self, slave: 'PositionedSlave', position: str) -> float:
        positions = {'x': 1.0, 'y': 2.0}
        return positions[position]

    def get_slave_margin(self, slave: 'MarginedSlave', margin: str) -> float:
        margins = {'top': 1.0, 'right': 2.0, 'bottom': 3.0, 'left': 4.0}
        return margins[margin]


class Slave(PositionedSlave, MarginedSlave):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master = Master()

    @property
    def master(self) -> Master:
        return self._master


class WrongMaster(AbstractMargined):
    pass


class TestPositioned(TestCase):
    def setUp(self) -> None:
        self.s = Slave()

    def test_slave_positions(self):
        assert self.s.get_positions() == {'x': 1.0, 'y': 2.0}

    def test_slave_set_position(self):
        with self.assertRaises(RelativePositionNotSettableError):
            Slave(relative_x=3)
        with self.assertRaises(RelativePositionNotSettableError):
            self.s.relative_x = 3
        with self.assertRaises(RelativePositionNotSettableError):
            Slave(relative_y=3)
        with self.assertRaises(RelativePositionNotSettableError):
            self.s.relative_y = 3

    def test_master_positions(self):
        m = Master()
        assert m.get_positions() == {'x': 0.0, 'y': 0.0}
        m = Master(relative_x=10, relative_y=20)
        assert m.get_positions() == {'x': 10.0, 'y': 20.0}
        assert m.get_slave_position(self.s, 'x') == 1.0

    def test_human_positions(self):
        h = Human()
        assert h.get_positions() == {'x': 0.0, 'y': 0.0}
        h = Human(relative_x=10, relative_y=20)
        assert h.get_positions() == {'x': 10.0, 'y': 20.0}
        with self.assertRaises(AttributeError):
            h.get_slave_position()


class TestMargined(TestCase):
    def setUp(self) -> None:
        self.s = Slave()

    def test_slave_margins(self):
        assert self.s.get_margins() == {'bottom': 3.0, 'left': 4.0, 'right': 2.0, 'top': 1.0}

    def test_slave_set_margin(self):
        with self.assertRaises(MarginNotSettableError):
            Slave(bottom_margin=3.0)
        with self.assertRaises(MarginNotSettableError):
            self.s.right_margin = 3
        with self.assertRaises(MarginNotSettableError):
            self.s.left_margin = 3
        with self.assertRaises(MarginNotSettableError):
            self.s.top_margin = 3
        with self.assertRaises(MarginNotSettableError):
            self.s.bottom_margin = 3

    def test_master_margins(self):
        m = Master()
        assert m.get_margins() == {'bottom': 0.0, 'left': 0.0, 'right': 0.0, 'top': 0.0}
        m = Master(left_margin=10, right_margin=20)
        assert m.get_margins() == {'bottom': 0.0, 'left': 10.0, 'right': 20.0, 'top': 0.0}
        assert m.get_slave_margin(self.s, 'top') == 1.0

    def test_human_margins(self):
        h = Human()
        assert h.get_margins() == {'bottom': 0.0, 'left': 0.0, 'right': 0.0, 'top': 0.0}
        h = Human(left_margin=10, right_margin=20)
        assert h.get_margins() == {'bottom': 0.0, 'left': 10.0, 'right': 20.0, 'top': 0.0}
        with self.assertRaises(AttributeError):
            h.get_slave_margin()

    def test_wrong_master(self):
        with self.assertRaises(TypeError):
            WrongMaster()
