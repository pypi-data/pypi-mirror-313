from typing import Any, Optional


# arithmetic progression
class ArithmeticProgressionException(Exception):
    pass


class DAndSError(ArithmeticProgressionException):
    def __init__(self, *args: Any):
        msg = 'you cannot set both d an s!'
        super().__init__(msg, *args)


# matrix

class MatrixIndexException(Exception):
    pass


class MatrixIndexControllerException(Exception):
    pass


class MatrixIndexOutOfRangeError(MatrixIndexException, ValueError):
    pass


class MatrixIndexEndOfRowError(MatrixIndexException, StopIteration):
    pass


class MatrixIndexEndOfMatrixError(MatrixIndexEndOfRowError, StopIteration):
    pass


class MatrixIndexControllerReadingDirectionError(MatrixIndexControllerException):
    def __init__(self, *args: Any):
        super().__init__('MatrixIndexController.get_next_in_row() works only for reading_direction horizontal.', *args)


class MatrixException(Exception):
    pass


class MatrixIsEmptyError(MatrixException):
    def __init__(self) -> None:
        msg = 'Matrix is empty!'
        super().__init__(msg)


class SquareMatrixException(MatrixException):
    pass


class SquareMatrixDataError(SquareMatrixException):
    pass


# permutation order matrix

class PermutationOrderMatrixException(MatrixException):
    pass


class PermutationOrderMatrixDataError(PermutationOrderMatrixException):
    pass


# permutation order

class PermutationOrderException(Exception):
    pass


class PermutationOrderError(PermutationOrderException):
    pass


class PermutationOrderTypeError(PermutationOrderError, TypeError):
    pass


class PermutationOrderValueError(PermutationOrderError, ValueError):
    pass


# permutation index

class PermutationIndexCalculatorException(Exception):
    pass


class PermutationIndexCalculaterNoParentIndexError(PermutationIndexCalculatorException, ValueError):
    pass


# fractal tree

class FractalTreeException(Exception):
    pass


class FractalTreePermutationOrderError(FractalTreeException):
    pass


class FractalTreePermutationIndexError(FractalTreeException, ValueError):
    pass


class FractalTreeSetMainPermutationOrderFirstError(FractalTreeException, ValueError):
    msg = "set root's main_permutation_order first"

    def __init__(self, msg: Optional[str] = None):
        if msg is None:
            msg = self.msg
        super().__init__(msg)


class FractalTreeMergeWrongValuesError(FractalTreeException, ValueError):
    pass


class FractalTreeHasNoChildrenError(FractalTreeException):
    pass


class FractalTreeHasChildrenError(FractalTreeException):
    pass


class FractalTreeNonRootCannotSetMainPermutationOrderError(FractalTreeException):
    pass


# pdf

class PdfException(Exception):
    pass


class PdfAttributeError(PdfException, AttributeError):
    pass


# pdf draw object margins

class MarginedObjectException(Exception):
    pass


class MarginNotSettableError(MarginedObjectException):
    pass


# pdf draw object positions

class PositionedObjectException(AttributeError):
    pass


class RelativePositionNotSettableError(PositionedObjectException):
    pass


class RelativeXNotSettableError(RelativePositionNotSettableError):
    pass


class RelativeYNotSettableError(RelativePositionNotSettableError):
    pass


class DrawObjectInContainerHasNegativePositionError(PositionedObjectException):
    pass


# pdf segmented line
class SegmentedLineException(Exception):
    pass


class SegmentedLineSegmentHasMarginsError(SegmentedLineException, AttributeError):
    pass


class SegmentedLineLengthsCannotBeSetError(SegmentedLineException):
    pass


# pdf ruler

class RulerException(SegmentedLineException):
    pass


class RulerCannotSetLengthsError(RulerException, AttributeError):
    pass


class RulerLengthNotPositiveError(RulerException, AttributeError):
    pass


# time ruler

class TimeRulerException(RulerException):
    pass


class TimeRulerCannotSetLength(TimeRulerException, AttributeError):
    pass



# clock
class ClockException(Exception):
    pass


class ClockWrongSecondsValueError(ClockException, ValueError):
    pass


class ClockWrongMinutesValueError(ClockException, ValueError):
    pass


class ClockWrongSecondsTypeError(ClockException, TypeError):
    pass


class ClockWrongMinutesTypeError(ClockException, TypeError):
    pass


class ClockWrongHoursTypeError(ClockException, TypeError):
    pass
