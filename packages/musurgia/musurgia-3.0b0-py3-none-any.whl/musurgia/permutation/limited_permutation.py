from typing import Any

from musurgia.musurgia_types import PermutationOrder, check_type, MatrixData
from musurgia.permutation.permutation import get_self_permutation_3d


class LimitedPermutationOrders:
    """
    LimitedPermutationOrders is inspired from Gérard Grisey's permutation technique.
    """

    def __init__(self, main_permutation_order: PermutationOrder, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._main_permutation_order: tuple[int, ...]
        self._permutation_orders: MatrixData
        self.main_permutation_order = main_permutation_order

    @property
    def main_permutation_order(self) -> PermutationOrder:
        return self._main_permutation_order

    @main_permutation_order.setter
    def main_permutation_order(self, val: PermutationOrder) -> None:
        check_type(val, 'PermutationOrder', class_name=self.__class__.__name__, property_name='main_permutation_order')
        self._main_permutation_order = val
        self._permutation_orders = get_self_permutation_3d(self.main_permutation_order)

    def get_permutation_orders(self) -> MatrixData:
        return self._permutation_orders
