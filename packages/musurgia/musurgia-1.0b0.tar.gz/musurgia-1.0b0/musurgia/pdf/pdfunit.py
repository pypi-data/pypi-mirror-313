from typing import Any

from musurgia.musurgia_types import check_type, PdfUnitType

__all__ = []  # type: ignore


class PdfUnitTypeCheckMeta(type):
    def __setattr__(cls, key: str, value: Any) -> None:
        if key == 'GLOBAL_UNIT':
            check_type(value, 'PdfUnitType', class_name='PdfUnit', class_attribute_name='GLOBAL_UNIT')
        super().__setattr__(key, value)


class PdfUnit(metaclass=PdfUnitTypeCheckMeta):
    _DEFAULT_UNIT = 'mm'
    GLOBAL_UNIT = _DEFAULT_UNIT

    @staticmethod
    def get_k() -> float:
        k_dict = {'pt': 1., 'mm': 72 / 25.4, 'cm': 72 / 2.54, 'in': 72.}
        k = k_dict[PdfUnit.GLOBAL_UNIT]
        return k

    @staticmethod
    def reset() -> None:
        PdfUnit.GLOBAL_UNIT = PdfUnit._DEFAULT_UNIT

    @staticmethod
    def change(val: PdfUnitType) -> None:
        PdfUnit.GLOBAL_UNIT = val
