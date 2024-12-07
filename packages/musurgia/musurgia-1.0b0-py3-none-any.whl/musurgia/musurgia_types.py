from fractions import Fraction
from typing import Any, Optional, Union, Literal, Callable, cast, get_args

from musurgia.musurgia_exceptions import MatrixIndexOutOfRangeError

MUSURGIA_TYPES = ['MatrixData', 'MatrixIndex', 'MatrixTransposeMode', 'NonNegativeInteger', 'PermutationOrder',
                  'PositiveInteger', 'ConvertibleToFraction', 'FractalTreeReduceChildrenMode', 'MatrixReadingDirection',
                  'ConvertibleToFloat', 'LabelPlacement', 'HorizontalVertical', 'PdfUnitType', 'PositionType',
                  'FontFamily', 'FontWeight', 'FontStyle', 'VerticalPosition', 'HorizontalPosition',
                  'MarkLinePlacement', 'PageOrientation', 'PageFormat', 'PageOrientation', 'MarginType', 'ClockMode']

MusurgiaType = Literal[
    'MatrixData', 'MatrixIndex', 'MatrixTransposeMode', 'NonNegativeInteger', 'PermutationOrder', 'PositiveInteger',
    'ConvertibleToFraction', 'ConvertibleToFloat', 'FractalTreeReduceChildrenMode', 'MatrixReadingDirection',
    'LabelPlacement', 'HorizontalVertical', 'PdfUnitType', 'PositionType', 'FontFamily', 'FontWeight', 'FontStyle',
    'VerticalPosition', 'HorizontalPosition', 'MarkLinePlacement', 'PageOrientation', 'PageFormat', 'PageOrientation', 'MarginType', 'ClockMode']


class LiteralCheckGenerator:
    def __init__(self, literal_type: Any, type_name: str):
        self.type_name = type_name
        self.permitted = get_args(literal_type)

    def generate_checker(self) -> Callable[[str], bool]:
        def checker(value: str) -> bool:
            if value not in self.permitted:
                raise TypeError(f"{self.type_name} value must be in {self.permitted}, got {value}")
            return True

        return checker


def create_error_message(v: Optional[Any] = None, t: Optional[Union[type, str]] = None,
                         function_name: Optional[str] = None,
                         class_name: Optional[str] = None,
                         method_name: Optional[str] = None, argument_name: Optional[str] = None,
                         property_name: Optional[str] = None, class_attribute_name: Optional[str] = None,
                         message: Optional[str] = None) -> str:
    if not message and not (v or t):
        raise AttributeError('if no message provided v and t must be set')

    if message and (v or t):
        raise AttributeError('if message is provided no v and t can be set')

    if function_name and (property_name or method_name or class_name):
        raise AttributeError('function_name cannot be set with property_name or method_name or class_name')

    if function_name and not argument_name:
        raise AttributeError('After setting function_name argument_name must be set.')

    if class_name and not (property_name or method_name or class_attribute_name):
        raise AttributeError('After setting class_name property_name, method_name or class_attribute_name must be set.')

    if class_attribute_name and not class_name:
        raise AttributeError('After setting class_attribute_name class_name must be set.')

    if class_attribute_name and (property_name or method_name or argument_name):
        raise AttributeError(
            'class_attribute_name and property_name, method_name or argument_name cannot be set together.')

    if method_name and (property_name or class_attribute_name):
        raise AttributeError('method_name and property_name or class_attribute_name cannot be set together.')

    if method_name and not message and not (argument_name and class_name):
        raise AttributeError('After setting method_name class_name and argument_name must be set.')

    if method_name and message and not class_name:
        raise AttributeError('After setting message and method_name class_name must be set.')

    if argument_name and not (function_name or method_name):
        raise AttributeError('After setting argument_name method_name or function_name must be set.')

    if argument_name and property_name:
        raise AttributeError('argument_name and property_name cannot be set together.')

    if property_name and not class_name:
        raise AttributeError('After setting property_name class_name must be set.')

    if not message:
        if isinstance(t, str):
            _type = t
        else:
            _type = cast(type, t).__name__
        message = f'Value {v} must be of type {_type} not {v.__class__.__name__}'

    if property_name and class_name:
        msg = f'{class_name}.{property_name}: {message}'

    elif function_name and argument_name:
        msg = f'{function_name}:{argument_name}: {message}'

    elif argument_name and method_name and class_name:
        msg = f'{class_name}.{method_name}:{argument_name}: {message}'

    elif argument_name and method_name and not class_name:
        msg = f'{method_name}:{argument_name}: {message}'

    elif argument_name and not method_name and not class_name:
        msg = f'{argument_name}: {message}'
    else:
        msg = f'{message}'
    return msg


def check_musurgia_type_type(value: str) -> bool:
    if not isinstance(value, str):
        raise TypeError(f"MusurgiaType value must be of type str,  got {type(value)}")
    if value not in MUSURGIA_TYPES:
        raise TypeError(f"MusurgiaType value must be in {MUSURGIA_TYPES}, got {value}")
    return True


class MusurgiaTypeError(TypeError):
    """
    :param t: ``type``
    :param v: ``value``
    :param argument_name: name of the argument which is being checked.
    :param method_name: name of the method which is executing this checking.
    :param obj: ``object`` which the executing method is a part of

    If ``argument_name`` is not set ``method_name`` and ``obj`` have no impact.
    If ``method_name`` is not set ``obj`` has no impact.
    """

    def __init__(self, v: Optional[Any] = None, t: Optional[Union[type, str]] = None,
                 function_name: Optional[str] = None,
                 class_name: Optional[str] = None,
                 method_name: Optional[str] = None, argument_name: Optional[str] = None,
                 property_name: Optional[str] = None, class_attribute_name: Optional[str] = None,
                 message: Optional[str] = None):
        msg = create_error_message(v, t, function_name, class_name, method_name, argument_name, property_name,
                                   class_attribute_name, message)
        super().__init__(msg)

    def __setattr__(self, attr: str, value: Any) -> Any:
        raise AttributeError("Trying to set attribute on a frozen instance MusurgiaTypeError")


NonNegativeInteger = int


def check_non_negative_integer_type(value: NonNegativeInteger) -> bool:
    if not isinstance(value, int) or value < 0:
        raise TypeError(f"NonNegativeInteger value must be a non-negative integer, got {value}")
    return True


PositiveInteger = int


def check_positive_integer_type(value: PositiveInteger) -> bool:
    if not isinstance(value, int) or value <= 0:
        raise TypeError(f"PositiveInteger value must be a positive integer, got {value}")
    return True


ConvertibleToFraction = Union[float, int, Fraction]


def check_convertible_to_fraction_type(value: ConvertibleToFraction) -> bool:
    if not isinstance(value, int) and not isinstance(value, Fraction) and not isinstance(value, float):
        raise TypeError
    return True


def convert_to_fraction(value: ConvertibleToFraction) -> Fraction:
    if isinstance(value, Fraction):
        return value
    else:
        return Fraction(value)


ConvertibleToFloat = Union[float, int, Fraction, str]


def check_convertible_to_float_type(value: ConvertibleToFloat) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        raise TypeError
    return True


PermutationOrder = tuple[int, ...]


def check_permutation_order_type(value: PermutationOrder) -> bool:
    if not isinstance(value, tuple) or len(value) != len(set(value)) or set(value) != set(range(1, len(value) + 1)):
        raise TypeError(
            f"PermutationOrder value must be a tuple with all integers from 1 to an upper limit corresponding the size of input_list, got {value}")
    return True


def check_permutation_order_values(permutation_order: PermutationOrder, size: NonNegativeInteger) -> bool:
    check_type(v=size, t='NonNegativeInteger', function_name='check_permutation_order_values', argument_name='size')
    if len(permutation_order) != size:
        raise ValueError(f"PermutationOrder {permutation_order} must be of size {size}")
    return True


MatrixData = list[list[Any]]


def check_matrix_data_type(matrix_data: MatrixData) -> bool:
    row_size = None
    for i, row in enumerate(matrix_data):
        if not isinstance(row, list):
            raise TypeError(f"row {row} is not a list")
        if i == 0:
            row_size = len(row)
        else:
            if len(row) != row_size:
                raise TypeError(f"row {row} must be of length {row_size}")
    return True


MatrixIndex = tuple[PositiveInteger, PositiveInteger]


def check_matrix_index_type(index: MatrixIndex) -> bool:
    if not isinstance(index, tuple) or len(index) != 2 or not check_positive_integer_type(
            index[0] or not check_positive_integer_type(index[1])):
        raise TypeError(f"MatrixIndex: index {index} must be a tuple with two positive integers")
    return True


def check_matrix_index_values(index: MatrixIndex, number_of_rows: PositiveInteger,
                              number_of_columns: PositiveInteger) -> bool:
    check_positive_integer_type(number_of_rows)
    check_positive_integer_type(number_of_columns)
    if index[0] > number_of_rows or index[1] > number_of_columns:
        raise MatrixIndexOutOfRangeError(
            f"MatrixIndex: index {index} must be in ranges (1..{number_of_rows}, 1..{number_of_columns}) ")

    return True


MatrixTransposeMode = Literal['regular', 'diagonal']
check_matrix_transpose_mode_type = LiteralCheckGenerator(MatrixTransposeMode, 'MatrixTransposeMode').generate_checker()

MatrixReadingDirection = Literal['horizontal', 'diagonal', 'vertical']
check_matrix_reading_direction_type = LiteralCheckGenerator(MatrixReadingDirection,
                                                            'MatrixReadingDirection').generate_checker()
FractalTreeReduceChildrenMode = Literal['backwards', 'forwards', 'sieve', 'merge']
check_fractal_tree_reduce_children_mode_type = LiteralCheckGenerator(FractalTreeReduceChildrenMode,
                                                                     'FractalTreeReduceChildrenMode').generate_checker()

LabelPlacement = Literal['above', 'below', 'left']
check_label_placement_type = LiteralCheckGenerator(LabelPlacement, 'LabelPlacement').generate_checker()

HorizontalVertical = Literal['horizontal', 'h', 'vertical', 'v']
check_horizontal_vertical_type = LiteralCheckGenerator(HorizontalVertical, 'HorizontalVertical').generate_checker()

PdfUnitType = Literal['pt', 'mm', 'cm', 'in']
check_pdf_unit_type_type = LiteralCheckGenerator(PdfUnitType, 'PdfUnitType').generate_checker()

PositionType = Literal['x', 'y']
check_position_type_type = LiteralCheckGenerator(PositionType, 'PositionType').generate_checker()

FontFamily = Literal['Courier']
check_font_family_type = LiteralCheckGenerator(FontFamily, 'FontFamily').generate_checker()

FontWeight = Literal['medium', 'bold']
check_font_weight_type = LiteralCheckGenerator(FontWeight, 'FontWeight').generate_checker()

FontStyle = Literal['regular', 'italic']
check_font_style_type = LiteralCheckGenerator(FontStyle, 'FontStyle').generate_checker()

VerticalPosition = Literal['top', 'bottom']
check_vertical_position_type = LiteralCheckGenerator(VerticalPosition, 'VerticalPosition').generate_checker()

HorizontalPosition = Literal['left', 'center', 'right']
check_horizontal_position_type = LiteralCheckGenerator(HorizontalPosition, 'HorizontalPosition').generate_checker()

MarkLinePlacement = Literal['start', 'end']
check_mark_line_placement_type = LiteralCheckGenerator(MarkLinePlacement, 'MarkLinePlacement').generate_checker()

PageOrientation = Literal["", "portrait", "p", "P", "landscape", "l", "L"]
check_page_orientation_type = LiteralCheckGenerator(PageOrientation, 'PageOrientation').generate_checker()

PageFormat = Literal["", "a3", "A3", "a4", "A4", "a5", "A5", "letter", "Letter", "legal", "Legal"]
check_page_format_type = LiteralCheckGenerator(PageFormat, 'PageFormat').generate_checker()

MarginType = Literal['left', 'right', 'top', 'bottom']
check_margin_type_type = LiteralCheckGenerator(MarginType, 'MarginType').generate_checker()

ClockMode = Literal['hms', 'ms', 'msreduced']
check_clock_mode_type = LiteralCheckGenerator(ClockMode, 'ClockMode').generate_checker()


def _get_name_of_check_type_function(musurgia_type: MusurgiaType) -> str:
    """
    >>> _get_name_of_check_type_function("MatrixIndex")
    'check_matrix_index_type'
    """
    return 'check' + ''.join([f'_{x.lower()}' if x.isupper() else x for x in musurgia_type]) + '_type'


def get_check_musurgia_type(musurgia_type: MusurgiaType) -> Callable[[Any], bool]:
    if musurgia_type not in MUSURGIA_TYPES:
        raise TypeError(f'check_musurgia_type: invalid musurgia_type {musurgia_type}')
    check_function_name = _get_name_of_check_type_function(musurgia_type)
    try:
        func: Callable[[Any], bool] = globals()[check_function_name]
    except KeyError:
        raise AttributeError(f'get_check_musurgia_type: {check_function_name} does not exist')
    return func


def check_type(v: Any, t: Union[type, str], function_name: Optional[str] = None, class_name: Optional[str] = None,
               method_name: Optional[str] = None, argument_name: Optional[str] = None,
               property_name: Optional[str] = None, class_attribute_name: Optional[str] = None) -> bool:
    """
    :param v: ``value`` to be checked.
    :param t: ``type``.
    :param function_name: see :obj:`MusurgiaTypeError`
    :param class_name: see :obj:`MusurgiaTypeError`
    :param method_name: see :obj:`MusurgiaTypeError`
    :param argument_name: see :obj:`MusurgiaTypeError`
    :param property_name: see :obj:`MusurgiaTypeError`
    :param class_attribute_name: see :obj:`MusurgiaTypeError`

    :raise: :obj:`MusurgiaTypeError`
    """

    def _create_error(message: Optional[str] = None) -> MusurgiaTypeError:
        if not message:
            return MusurgiaTypeError(v, t, function_name, class_name, method_name, argument_name, property_name,
                                     class_attribute_name)
        else:
            return MusurgiaTypeError(None, None, function_name, class_name, method_name, argument_name, property_name,
                                     class_attribute_name, message)

    if isinstance(t, type):
        if t == int and isinstance(v, bool):
            # in python bool is a subclass of int
            raise _create_error()
        elif not isinstance(v, t):
            raise _create_error()
    else:
        check_musurgia_type_type(t)
        try:
            get_check_musurgia_type(cast(MusurgiaType, t))(v)
        except TypeError as err:
            raise _create_error(message=str(err))
    return True
