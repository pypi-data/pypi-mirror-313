import itertools
from fractions import Fraction
from typing import Union, Optional, List, Callable, Any, cast, Sequence, TypeVar

from verysimpletree.tree import Tree

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.matrix.matrix import PermutationOrderMatrix, PermutationOrderMatrixGenerator
from musurgia.musurgia_exceptions import FractalTreeHasChildrenError, \
    FractalTreeNonRootCannotSetMainPermutationOrderError, PermutationIndexCalculaterNoParentIndexError, \
    FractalTreePermutationIndexError, FractalTreeSetMainPermutationOrderFirstError, FractalTreeMergeWrongValuesError, \
    FractalTreeHasNoChildrenError
from musurgia.musurgia_types import ConvertibleToFraction, FractalTreeReduceChildrenMode, convert_to_fraction, \
    MatrixIndex, PermutationOrder, check_type, PositiveInteger, check_matrix_index_values, create_error_message
from musurgia.permutation.permutation import permute

__all__ = ['FractalTree']

T = TypeVar('T', bound='FractalTree')


def node_info(node: 'FractalTree') -> str:
    return f'{node.get_fractal_order()}: {node.get_permutation_index()}: {round(float(node.get_value()), 2)}'


class PermutationIndexCalculater:
    def __init__(self, size: PositiveInteger, parent_index: Optional[MatrixIndex] = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._size: PositiveInteger
        self._parent_index: Optional[MatrixIndex] = None

        self.size = size
        self.parent_index = parent_index

    @property
    def size(self) -> PositiveInteger:
        return self._size

    @size.setter
    def size(self, value: PositiveInteger) -> None:
        check_type(value, 'PositiveInteger', class_name=self.__class__.__name__, property_name='size')
        self._size = value

    @property
    def parent_index(self) -> Optional[MatrixIndex]:
        return self._parent_index

    @parent_index.setter
    def parent_index(self, value: MatrixIndex) -> None:
        if value is not None:
            check_type(value, 'MatrixIndex', class_name=self.__class__.__name__, property_name='parent_index')
        self._parent_index = value

    def get_index(self, column_number: PositiveInteger) -> MatrixIndex:
        if self.parent_index is None:
            raise PermutationIndexCalculaterNoParentIndexError
        check_type(column_number, 'PositiveInteger', class_name=self.__class__.__name__, method_name='get_index',
                   argument_name='column_number')
        if column_number > self.size:
            raise ValueError(create_error_message(class_name=self.__class__.__name__, method_name='get_index',
                                                  argument_name='column_number',
                                                  message=f'Column number {column_number} cannot be less than size {self.size}'))
        r = sum(self.parent_index) % self.size
        if r == 0:
            r = self.size
        return r, column_number


class FractalTree(Tree[Any]):
    """
    FractalTree represents the node of a fractal tree with a mechanism of limited permutations.
    """

    def __init__(self, value: ConvertibleToFraction,
                 proportions: Sequence[ConvertibleToFraction],
                 main_permutation_order: Optional[PermutationOrder] = None,
                 permutation_index: Optional[MatrixIndex] = None,
                 fertile: bool = True,
                 *args: Any,
                 **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._permutation_order_matrix: Optional[PermutationOrderMatrix] = None
        self._value: Fraction
        self._proportions: Sequence[ConvertibleToFraction] = []
        self._main_permutation_order: Optional[PermutationOrder] = None
        self._permutation_index: Optional[MatrixIndex] = None
        self._fertile: bool

        self._fractal_order: Optional[int] = None
        self._children_fractal_values: list[Fraction]
        self._children_permutation_order_matrices = None
        self._permutation_order: tuple[int, int]
        self._set_value(value)

        self.proportions = proportions
        self.main_permutation_order = main_permutation_order
        self.set_permutation_index(permutation_index)
        self.fertile = fertile

        self._pic: PermutationIndexCalculater

    # private methods

    def _check_child_to_be_added(self, child: 'FractalTree') -> bool:
        if isinstance(child, FractalTree):
            if child._main_permutation_order is not None:
                raise FractalTreeNonRootCannotSetMainPermutationOrderError
            return True
        else:
            raise TypeError(f'Wrong child type. Child must be of type FractalTree not {type(child)}')

    def _calculate_children_fractal_values(self) -> list['Fraction']:
        return permute([self.get_value() * prop for prop in self.proportions], self.get_permutation_order())

    def _change_children_value(self, factor: Union[int, float, Fraction]) -> None:
        for child in self.get_children():
            child._set_value(child._value * factor)
            child._change_children_value(factor)

    def _get_children_fractal_values(self) -> list['Fraction']:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft._get_children_fractal_values()
        [Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)]
        """
        try:
            return self._children_fractal_values
        except AttributeError:
            self._children_fractal_values = self._calculate_children_fractal_values()
            return self._children_fractal_values

    def _get_merge_lengths(self, size: int, merge_index: int) -> list[int]:
        if size == 1:
            return [self.get_size()]

        lengths = self.get_size() * [1]
        pointer = merge_index
        sliced_lengths = [lengths[:pointer], lengths[pointer:]]

        if not sliced_lengths[0]:
            sliced_lengths = sliced_lengths[1:]

        while len(sliced_lengths) < size and len(sliced_lengths[0]) > 1:
            temp = sliced_lengths[0]
            sliced_lengths[0] = temp[:-1]
            sliced_lengths.insert(1, temp[-1:])

        while len(sliced_lengths) < size and len(sliced_lengths[pointer]) > 1:
            temp = sliced_lengths[pointer]
            sliced_lengths[pointer] = temp[:-1]
            sliced_lengths.insert(pointer + 1, temp[-1:])

        output = [len(x) for x in sliced_lengths]

        return output

    def _get_pic(self) -> PermutationIndexCalculater:
        if self.is_root:
            try:
                return self._pic
            except AttributeError:
                raise FractalTreeSetMainPermutationOrderFirstError
            # except AttributeError:
            #     self._pic = PermutationIndexCalculater(self.get_permutation_order_matrix().get_size())
            #     return self._pic

        return cast(PermutationIndexCalculater, self.get_root()._get_pic())

    def _set_value(self, val: ConvertibleToFraction) -> None:
        if not isinstance(val, Fraction):
            val = Fraction(val)
        self._value = val

    # properties
    @property
    def fertile(self) -> bool:
        return self._fertile

    @fertile.setter
    def fertile(self, val: bool) -> None:
        self._fertile = val

    @property
    def main_permutation_order(self) -> Optional[PermutationOrder]:
        if self.is_root:
            return self._main_permutation_order
        else:
            return cast(FractalTree, self.get_root()).main_permutation_order

    @main_permutation_order.setter
    def main_permutation_order(self, value: Optional[PermutationOrder]) -> None:
        if self.get_children():
            raise FractalTreeHasChildrenError
        if value is not None:
            if not self.is_root:
                raise FractalTreeNonRootCannotSetMainPermutationOrderError
            check_type(value, 'PermutationOrder', class_name=self.__class__.__name__,
                       property_name='main_permutation_order')
            self._permutation_order_matrix = PermutationOrderMatrixGenerator(
                main_permutation_order=value).generate_permutation_order_matrix()
            self._pic = PermutationIndexCalculater(self.get_permutation_order_matrix().get_size())
        else:
            self._permutation_order_matrix = None
        self._main_permutation_order = value

    @property
    def proportions(self) -> Sequence[ConvertibleToFraction]:
        return self._proportions

    @proportions.setter
    def proportions(self, values: Sequence[ConvertibleToFraction]) -> None:
        converted_values: List[Fraction] = [convert_to_fraction(val) for val in list(values)]
        total = sum(converted_values)
        self._proportions = [Fraction(value, total) for value in converted_values]

    # public methods
    def add_layer(self, *conditions: Optional[Callable[['FractalTree'], bool]]) -> None:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [3, 1, 2]
        >>> ft.get_leaves(key=lambda leaf: leaf.get_permutation_index())
        [(2, 1), (2, 2), (2, 3)]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [5.0, 1.67, 3.33]
        >>> ft.add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[1, 2, 3], [3, 1, 2], [2, 3, 1]]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [[0.83, 1.67, 2.5], [0.83, 0.28, 0.56], [1.11, 1.67, 0.56]]


        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.get_children()[0].add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[1, 2, 3], 1, 2]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [[0.83, 1.67, 2.5], 1.67, 3.33]
        """

        leaves = list(self.iterate_leaves())

        if conditions is not None:
            for leaf in leaves:
                for condition in conditions:
                    if cast(Callable[['FractalTree'], bool], condition)(leaf) is False:
                        leaf.fertile = False
                        break

        for leaf in leaves:
            if leaf.fertile is True:
                for i in range(leaf.get_size()):
                    value = leaf._get_children_fractal_values()[i]
                    new_node = self.__class__(value=value, proportions=self.get_root().proportions,
                                              permutation_index=None)
                    leaf.add_child(new_node)
                    new_node.calculate_permutation_index()
                    new_node._fractal_order = leaf.get_children_fractal_orders()[i]
            else:
                pass

    def calculate_permutation_index(self: T) -> None:
        if self.is_root:
            raise FractalTreePermutationIndexError(
                f'{self.__class__.__name__}:calculate_permutation_index: Set permutation_index of root')
        pic = self._get_pic()
        parent = cast(T, self.up)
        pic.parent_index = parent.get_permutation_index()
        self._permutation_index = pic.get_index(cast(list[T], parent.get_children()).index(self) + 1)

    def change_value(self, new_value: Union[int, float, Fraction]) -> None:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.change_value(20)
        >>> ft.get_value()
        Fraction(20, 1)
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.get_children()[0].change_value(10)
        >>> ft.get_value()
        Fraction(15, 1)
        >>> [child.get_value() for child in ft.get_children()]
        [Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)]
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.change_value(15)
        >>> [child.get_value() for child in ft.get_children()]
        [Fraction(15, 2), Fraction(5, 2), Fraction(5, 1)]
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.add_layer()
        >>> ft.get_children()[0].change_value(10)
        >>> print(ft.get_tree_representation(key=lambda node: node.get_value()))
        └── 15
            ├── 10
            │   ├── 5/3
            │   ├── 10/3
            │   └── 5
            ├── 5/3
            │   ├── 5/6
            │   ├── 5/18
            │   └── 5/9
            └── 10/3
                ├── 10/9
                ├── 5/3
                └── 5/9
        <BLANKLINE>
        """
        factor = Fraction(Fraction(new_value), self.get_value())
        self._set_value(new_value)
        for node in self.get_reversed_path_to_root()[1:]:
            node._set_value(sum([child.get_value() for child in node.get_children()]))

        self._change_children_value(factor)

    def generate_children(self, number_of_children: Union[int, tuple[int, ...], tuple[tuple[int, ...], ...]],
                          reduce_mode: FractalTreeReduceChildrenMode = 'backwards',
                          merge_index: int = 0) -> None:
        """
        :param number_of_children:
        :param mode:
        :param merge_index:

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)))
        >>> print(ft.get_tree_representation(key=lambda node: str(node.get_fractal_order())))
        └── None
            ├── 3
            │   ├── 1
            │   │   └── 3
            │   ├── 2
            │   │   ├── 2
            │   │   │   └── 3
            │   │   └── 3
            │   │       ├── 2
            │   │       ├── 3
            │   │       └── 1
            │   └── 3
            │       ├── 3
            │       ├── 1
            │       └── 2
            ├── 1
            │   ├── 3
            │   │   ├── 3
            │   │   ├── 1
            │   │   └── 2
            │   └── 2
            │       └── 3
            └── 2
                ├── 2
                └── 3
        <BLANKLINE>
        """
        # check_generate_children_mode(reduce_mode)
        # this error must be moved to add_layer()
        if self.get_children():
            raise ValueError(
                f'FractalTree.generate_children: node has already children: {[ch.get_value() for ch in self.get_children()]}')

        if isinstance(number_of_children, int):
            if number_of_children > self.get_size():
                raise ValueError(
                    f'generate_children.number_of_children {number_of_children} can not be a greater than size {self.get_size()}')
            if number_of_children < 0:
                raise ValueError(
                    'generate_children.number_of_children {} must be a positive int'.format(number_of_children))
            elif number_of_children == 0:
                pass
            else:
                self.add_layer()
                self.reduce_children_by_size(size=number_of_children, mode=reduce_mode, merge_index=merge_index)

        elif isinstance(number_of_children, tuple):
            self.generate_children(len(number_of_children), reduce_mode=reduce_mode, merge_index=merge_index)

            for index, child in enumerate(self.get_children()):
                if reduce_mode == 'backwards':
                    number_of_grand_children = number_of_children[
                        child.get_fractal_order() - child.get_size() + len(number_of_children) - 1]
                else:
                    number_of_grand_children = number_of_children[index]
                child.generate_children(number_of_grand_children, reduce_mode=reduce_mode, merge_index=merge_index)

        else:
            raise TypeError('generate_children.number_of_children must be of type int or tuple')

    def get_children_fractal_orders(self) -> list[int]:
        if self.is_root:
            if self.main_permutation_order is None:
                raise FractalTreeSetMainPermutationOrderFirstError(
                    create_error_message(message='Set main_permutation_order first', class_name=self.__class__.__name__,
                                         method_name='get_children_fractal_orders'))
            else:
                return permute(list(range(1, self.get_size() + 1)), self.main_permutation_order)
        return permute(list(range(1, self.get_size() + 1)), self.get_permutation_order())

    def get_fractal_order(self) -> Optional[int]:
        """
        :return:

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> [node.get_fractal_order() for node in ft.traverse()]
        [None, 3, 1, 2]
        """
        return self._fractal_order

    def get_layer(self, layer: int, key: Optional[Callable[['FractalTree'], Any]] = None) -> Any:
        """
        :param layer:
        :param key:
        :return:

        >>> ft = FractalTree(10, (1, 2, 3), (3, 1, 2), (1, 1))
        >>> ft.add_layer()
        >>> for i in range(3):
        ...     ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        >>> print(ft.get_layer(0, key=lambda node: node.get_fractal_order()))
        None
        >>> ft.get_layer(1, key=lambda node: node.get_fractal_order())
        [3, 1, 2]
        >>> ft.get_layer(2, key=lambda node: node.get_fractal_order())
        [[1, 2, 3], 1, [2, 3, 1]]
        >>> ft.get_layer(3, key=lambda node: node.get_fractal_order())
        [[1, [1, 2, 3], [3, 1, 2]], 1, [[1, 2, 3], [3, 1, 2], 1]]
        >>> ft.get_layer(4, key=lambda node: node.get_fractal_order())
        [[1, [1, [3, 1, 2], [2, 3, 1]], [[2, 3, 1], 1, [3, 1, 2]]], 1, [[1, [1, 2, 3], [3, 1, 2]], [[3, 1, 2], 1, [1, 2, 3]], 1]]
        """
        if layer > self.get_root().get_number_of_layers():
            raise ValueError(f'FractalTree.get_layer: max layer number={self.get_number_of_layers()}')
        else:
            if layer == 0:
                return cast('FractalTree', self.get_self_with_key(key))
            else:
                if self.is_leaf:
                    return self.get_layer(layer=layer - 1, key=key)
                output = []
                for child in self.get_children():
                    if child.get_farthest_leaf().get_distance() == 1:
                        output.append(child.get_self_with_key(key))
                    else:
                        output.append(child.get_layer(layer - 1, key))
                return output

    def get_number_of_layers(self) -> int:
        if self.get_leaves() == [self]:
            return 0
        else:
            return cast(int, self.get_farthest_leaf().get_distance(self))

    def get_permutation_index(self) -> Optional[MatrixIndex]:
        return self._permutation_index

    def get_permutation_order(self) -> tuple[int, int]:
        try:
            return self._permutation_order
        except AttributeError:
            self._permutation_order = self.get_permutation_order_matrix().get_element(
                cast(MatrixIndex, self.get_permutation_index()))
            return self._permutation_order

    def get_permutation_order_matrix(self) -> PermutationOrderMatrix:
        if self.is_root:
            if self._permutation_order_matrix is None:
                raise FractalTreeSetMainPermutationOrderFirstError(
                    create_error_message(message=FractalTreeSetMainPermutationOrderFirstError.msg,
                                         class_name=self.__class__.__name__,
                                         method_name='get_permutation_order_matrix'))
            return self._permutation_order_matrix
        else:
            return cast(FractalTree, self.get_root()).get_permutation_order_matrix()

    def get_size(self) -> int:
        """
        >>> ft = FractalTree(10, (1, 2, 3), (3, 1, 2))
        >>> ft.get_size()
        3
        """
        return len(self.proportions)

    def get_value(self) -> Fraction:
        return self._value

    def merge_children(self, *lengths: int) -> None:
        """

        :param lengths:
        :return:

        >>> ft = FractalTree(proportions=(1, 2, 3, 4, 5), main_permutation_order=(3, 5, 1, 2, 4), value=10, permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> print(ft.get_tree_representation(node_info))
        └── None: (1, 1): 10.0
            ├── 3: (2, 1): 2.0
            ├── 5: (2, 2): 3.33
            ├── 1: (2, 3): 0.67
            ├── 2: (2, 4): 1.33
            └── 4: (2, 5): 2.67
        <BLANKLINE>
        >>> ft.merge_children(1, 2, 2)
        >>> print(ft.get_tree_representation(node_info))
        └── None: (1, 1): 10.0
            ├── 3: (2, 1): 2.0
            ├── 5: (2, 2): 4.0
            └── 2: (2, 4): 4.0
        <BLANKLINE>
        """
        children = self.get_children()
        if not children:
            raise FractalTreeHasNoChildrenError('FractalTree.merge_children: There are no children to be merged')
        if sum(lengths) != len(children):
            raise FractalTreeMergeWrongValuesError(
                f'FractalTree.merge_children: Sum of lengths {sum(lengths)} must be the same as length of children {len(children)}')

        def _merge(nodes: list['FractalTree']) -> None:
            node_values = [node.get_value() for node in nodes]
            new_value = sum(node_values)
            for node in nodes[1:]:
                self.remove(node)
            nodes[0].change_value(new_value)

        iter_children = iter(children)
        chunks = [list(itertools.islice(iter_children, l)) for l in lengths]

        for chunk in chunks:
            _merge(chunk)

    def reduce_children_by_condition(self, condition: Callable[['FractalTree'], bool]) -> None:
        if not self.get_children():
            raise FractalTreeHasNoChildrenError(f'{self} has no children to be reduced')
        for child in [child for child in self.get_children() if condition(child)]:
            self.remove(child)
            del child
        reduced_value = sum([child.get_value() for child in self.get_children()])
        factor = self.get_value() / reduced_value
        for child in self.get_children():
            new_value = child.get_value() * factor
            child.change_value(new_value)

        self._children_fractal_values = [child.get_value() for child in self.get_children()]

    def reduce_children_by_size(self, size: int, mode: FractalTreeReduceChildrenMode = 'backwards',
                                merge_index: Optional[int] = None) -> None:
        check_type(mode, 'FractalTreeReduceChildrenMode', class_name=self.__class__.__name__,
                   method_name='reduce_children_by_size', argument_name='mode')

        if size > self.get_size() or size < 0:
            raise ValueError(
                f'reduce_children_by_size.size {size} must be a positive int not greater than {self.get_size()}')
        if size == 0:
            pass
        else:
            if mode == 'backwards':
                self.reduce_children_by_condition(
                    lambda child: cast(int, child.get_fractal_order()) < self.get_size() - size + 1)
            elif mode == 'forwards':
                self.reduce_children_by_condition(
                    lambda child: cast(int, child.get_fractal_order()) > size)
            elif mode == 'sieve':
                if size == 1:
                    self.reduce_children_by_condition(condition=lambda child: child.get_fractal_order() not in [1])
                else:
                    ap = ArithmeticProgression(a1=1, an=self.get_size(), n=size)
                    selection = [int(round(x)) for x in ap]
                    self.reduce_children_by_condition(
                        condition=lambda child: child.get_fractal_order() not in selection)
            elif mode == 'merge':
                if merge_index is None:
                    raise ValueError(f'reduce_children.merge_index must be set for mode merge')
                if merge_index > self.get_size() - 1:
                    raise ValueError(
                        f'reduce_children_by_size.merge_index {merge_index} must be a positive int not greater than {self.get_size() - 1}')
                merge_lengths = self._get_merge_lengths(size, merge_index)
                self.merge_children(*merge_lengths)

    def set_permutation_index(self, index: Optional[MatrixIndex]) -> None:
        if index is not None:
            check_type(index, 'MatrixIndex', class_name=self.__class__.__name__,
                       method_name='set_permutation_index',
                       argument_name='index')
            size = self.get_permutation_order_matrix().get_size()
            check_matrix_index_values(index, size, size)
        self._permutation_index = index

    def split(self: 'T', *proportions: Any) -> list['T']:
        if self.get_children():
            raise FractalTreeHasChildrenError

        if hasattr(proportions[0], '__iter__'):
            proportions = proportions[0]

        proportions_list = [Fraction(prop) for prop in proportions]

        for prop in proportions_list:
            value = self.get_value() * prop / sum(proportions_list)
            new_node = self.__class__(value=value, proportions=self.get_root().proportions, permutation_index=None)
            new_node._fractal_order = self.get_fractal_order()
            self.add_child(new_node)
            new_node.calculate_permutation_index()

        return self.get_children()
