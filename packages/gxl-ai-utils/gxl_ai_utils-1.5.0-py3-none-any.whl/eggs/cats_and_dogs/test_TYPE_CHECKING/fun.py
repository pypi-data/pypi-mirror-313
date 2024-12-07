from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .test import GxlHa


def print_name(obj: "GxlHa"):
    """
    TYPE_CHECKING中引入的内容需要加上“”才能使用
    :param obj:
    :return:
    """
    print(obj.name)
