import math
from typing import Union


def int_ceil(num: float) -> int:
    """
    >>> int_ceil(10 / 3)
    4

    :param num:
    :return:
    """
    return math.ceil(num)


def decimal_ceil(num: float, places: int = 2) -> float:
    """
    >>> decimal_ceil(3.14159)
    3.15

    :param num:
    :param places:
    :return:
    """
    if places >= 0:
        scale = 10.0 ** places
        return math.ceil(num * scale) / scale
    else:
        raise ValueError(f"places：{places} 必须大于等于 0 ！")


def format_number(number: Union[int, float, str], places: int = 2) -> str:
    """
    >>> format_number(3.1)
    '3.10'

    :param number:
    :param places:
    :return:
    """
    integer_str, decimal_str = str(float(number)).split('.')
    decimal_str = (decimal_str + '0' * (places - len(decimal_str)))[:places]
    number_str = '.'.join([integer_str, decimal_str])
    return number_str
