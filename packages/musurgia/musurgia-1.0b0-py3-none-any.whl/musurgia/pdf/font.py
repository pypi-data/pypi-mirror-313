from pathlib import Path
from typing import Any

import matplotlib as mpl
from matplotlib._afm import AFM
from musurgia.musurgia_types import FontFamily, FontWeight, FontStyle, check_type

__all__ = ['Font']


def _make_afm_path_dictionary() -> 'dict[tuple[Any, Any, str], AFM]':
    def check_entry() -> bool:
        old_afm = output.get((family, weight, style))
        if old_afm is not None:
            old_header = old_afm._header
            new_header = afm._header
            diff = set(old_header) ^ set(new_header)
            if diff == set():
                return False
            else:
                return True
            # if diff == {b'CapHeight'}:
            #     if new_header.get(b'CapHeight'):
            #         return True
            # elif diff == set():
            #     return False
            # else:
            #     raise AttributeError(
            #         f'{family}, {weight}, {style} already in dict: {old_afm} difference: {diff}')
        else:
            return True

    output = {}
    directory = Path(mpl.get_data_path(), 'fonts', 'afm')
    for file in directory.iterdir():
        afm_path = file
        with afm_path.open('rb') as fh:
            afm = AFM(fh)  # type: ignore
        family = afm.get_familyname()  # type: ignore
        weight = afm.get_weight().lower()  # type: ignore
        if afm.get_angle() < 0:  # type: ignore
            style = 'italic'
        else:
            style = 'regular'
        if check_entry():
            output[family, weight, style] = afm

    return output


class Font:
    """
    Class representing a font. It is used in class Text to set font family, weight, style and size.
    It accesses matplotlib._afm.AFM class (Adobe Font Metrics) to be able to determine the exact height and width of
    the text in pixels via two methods: :obj:`get_text_pixel_height()` and :obj:`get_text_pixel_width()`

    Attributes:
        family: Default value is ``Courier``.
        weight: Default value is ``medium``
        style: Default value is ``regular``
        size: Default value is `10`
    """

    __AFM_PATH_DICTIONARY = _make_afm_path_dictionary()

    # pprint(__AFM_PATH_DICTIONARY)
    # _FAMILY = ['Courier']
    # _WEIGHT = ['bold', 'medium']
    # _STYLE = ['italic', 'regular']

    def __init__(self, family: FontFamily = 'Courier', weight: FontWeight = 'medium', style: FontStyle = 'regular',
                 size: int = 10, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._family: FontFamily
        self._weight: FontWeight
        self._style: FontStyle
        self._size: int
        self._afm: AFM

        self.family = family
        self.weight = weight
        self.style = style
        self.size = size

    def _set_afm(self) -> None:
        self._afm = self.__AFM_PATH_DICTIONARY[self.family, self.weight, self.style]

    @property
    def family(self) -> FontFamily:
        """
        Set and get font family. Currently valid values are [``Helvetica``, ``Courier``, ``Times``]
        """
        return self._family

    @family.setter
    def family(self, val: FontFamily) -> None:
        check_type(val, 'FontFamily', class_name=self.__class__.__name__, property_name='family')
        self._family = val
        try:
            self._set_afm()
        except AttributeError:
            pass

    @property
    def size(self) -> int:
        """
        Set and get font size
        """
        return self._size

    @size.setter
    def size(self, val: int) -> None:
        check_type(val, int, class_name=self.__class__.__name__, property_name='size')
        self._size = val

    @property
    def style(self) -> FontStyle:
        """
        Set and get font style. Valid values are [``italic``, ``regular``]
        """
        return self._style

    @style.setter
    def style(self, val: FontStyle) -> None:
        check_type(val, 'FontStyle', class_name=self.__class__.__name__, property_name='style')
        self._style = val
        try:
            self._set_afm()
        except AttributeError:  # pragma: no cover
            pass

    @property
    def weight(self) -> FontWeight:
        """
        Set and get font weight. Valid values are [``bold``, ``medium``]
        """
        return self._weight

    @weight.setter
    def weight(self, val: FontWeight) -> None:
        check_type(val, 'FontWeight', class_name=self.__class__.__name__, property_name='weight')
        self._weight = val
        try:
            self._set_afm()
        except AttributeError:
            pass

    def get_text_pixel_width(self, value: str) -> float:
        """
        :param value: text as str
        :return: width of text in pixels

        >>> round(Font().get_text_pixel_width('Test'), 2)
        24.0
        >>> round(Font(size=12).get_text_pixel_width('Test'), 2)
        28.8
        """
        return (self._afm.string_width_height(value)[0] / 1000) * self.size  # type: ignore

    def get_text_pixel_height(self, val: str) -> float:
        """
        :param val: text as str
        :return: height of text in pixels

        >>> round(Font().get_text_pixel_height('Test'), 2)
        5.77
        >>> round(Font(size=12).get_text_pixel_height('Test'), 2)
        6.92
        >>> round(Font(size=12, weight='bold', style='italic').get_text_pixel_height('Test'), 2)
        6.95
        """
        return (self._afm.string_width_height(val)[1] / 1000) * self.size  # type: ignore
