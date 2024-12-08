from pprint import pprint
from typing import Any

from musurgia.musurgia_exceptions import PermutationOrderTypeError, PermutationOrderValueError
from musurgia.musurgia_types import check_type, PermutationOrder, check_permutation_order_values, \
    MatrixData


def permute(input_list: list[Any], permutation_order: PermutationOrder) -> list[Any]:
    """
    Permutes a list of values by reference to another list named permutation_order.
    :param input_list: A list of values to permute
    :param permutation_order: A tuple consisting of all integers between 1 and lenght of input_list - 1 without duplications.
    :return: permuted list of values

    >>> permute([10, 20, 30, 40], (3, 2, 4, 1))
    [30, 20, 40, 10]
    """
    check_type(input_list, list, function_name='permute', argument_name='input_list')
    try:
        check_type(permutation_order, 'PermutationOrder', function_name='permute', argument_name='permutation_order')
    except TypeError as err:
        raise PermutationOrderTypeError(err)

    try:
        check_permutation_order_values(permutation_order, len(input_list))
    except ValueError as err:
        raise PermutationOrderValueError(err)

    return [input_list[m - 1] for m in permutation_order]


def get_self_permutation_2d(permutation_order: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    This is a function for applying the `permutation_order` to itself.

    :param permutation_order: A tuple consisting of all integers between 1 and a higher integer

    :return: A list of `permutations_orders`  as a result of applying the `permutation_order` to itself recursively. The
    result has always a length equal to `len(permutation_order)`.
    Each permuted permutation order will be permuted again. If all integers of the original permuation are not in their
    natural order (natural orders=`(1, 2, 3, 4, ...)`) the resulted list will be distinctive. Otherwise there will be duplicates.

    >>> get_self_permutation_2d((3, 1, 2))
    [(3, 1, 2), (2, 3, 1), (1, 2, 3)]

    >>> get_self_permutation_2d((1, 3, 2))
    [(1, 3, 2), (1, 2, 3), (1, 3, 2)]

    >>> get_self_permutation_2d((1, 2, 3))
    [(1, 2, 3), (1, 2, 3), (1, 2, 3)]

    >>> get_self_permutation_2d((3, 1, 4, 2))
    [(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)]

    >>> get_self_permutation_2d((4, 2, 3, 1))
    [(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)]

    """
    output = [permutation_order]

    for i in range(1, len(permutation_order)):
        output.append(tuple(permute(list(output[i - 1]), permutation_order)))

    return output


def get_self_permutation_3d(permutation_order: tuple[int, ...]) -> MatrixData:
    """
    This is a function for applying the `permutation_order` to itself in a higher order compared to :obj:`get_self_permutation_2d`.
    If :obj:`get_self_permutation_2d` is a two dimensional reflexive operation, :obj:`get_self_permutation_3d` is a three
    dimensional one. 
    
    :param permutation_order: A list consisting of all integers between 1 and a higher integer
    
    :return:

    >>> pprint(get_self_permutation_3d((3, 1, 2)))
    [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
     [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
     [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]

    >>> pprint(get_self_permutation_3d((1, 3, 2)))
    [[(1, 3, 2), (1, 2, 3), (1, 3, 2)],
     [(1, 3, 2), (1, 3, 2), (1, 2, 3)],
     [(1, 3, 2), (1, 2, 3), (1, 3, 2)]]

    >>> pprint(get_self_permutation_3d((1, 2, 3)))
    [[(1, 2, 3), (1, 2, 3), (1, 2, 3)],
     [(1, 2, 3), (1, 2, 3), (1, 2, 3)],
     [(1, 2, 3), (1, 2, 3), (1, 2, 3)]]

    >>> pprint(get_self_permutation_3d((3, 1, 4, 2)))
    [[(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)],
     [(2, 4, 1, 3), (3, 1, 4, 2), (1, 2, 3, 4), (4, 3, 2, 1)],
     [(1, 2, 3, 4), (2, 4, 1, 3), (4, 3, 2, 1), (3, 1, 4, 2)],
     [(4, 3, 2, 1), (1, 2, 3, 4), (3, 1, 4, 2), (2, 4, 1, 3)]]

    >>> pprint(get_self_permutation_3d((3, 4, 2, 1)))
    [[(3, 4, 2, 1), (2, 1, 4, 3), (4, 3, 1, 2), (1, 2, 3, 4)],
     [(4, 3, 1, 2), (1, 2, 3, 4), (2, 1, 4, 3), (3, 4, 2, 1)],
     [(2, 1, 4, 3), (3, 4, 2, 1), (1, 2, 3, 4), (4, 3, 1, 2)],
     [(1, 2, 3, 4), (4, 3, 1, 2), (3, 4, 2, 1), (2, 1, 4, 3)]]

    >>> pprint(get_self_permutation_3d((4, 2, 3, 1)))
    [[(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)],
     [(1, 2, 3, 4), (1, 2, 3, 4), (4, 2, 3, 1), (4, 2, 3, 1)],
     [(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)],
     [(1, 2, 3, 4), (1, 2, 3, 4), (4, 2, 3, 1), (4, 2, 3, 1)]]
    """

    self_permuted_order = get_self_permutation_2d(permutation_order)
    output = [self_permuted_order]

    for i in range(1, len(self_permuted_order)):
        output.append(permute(list(output[i - 1]), permutation_order))
    return output
