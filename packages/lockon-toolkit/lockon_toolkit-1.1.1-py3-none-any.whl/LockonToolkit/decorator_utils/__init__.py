#!/opt/homebrew/anaconda3/envs/quantfin/bin/python
# -*- coding: utf-8 -*-

"""
装饰器工具模块

@Time    : 2024/9/25 下午4:21
@Author  : @Zhenxi Zhang
@File    : decorator_utils.py
@Software: PyCharm
"""

import logging
import typing
import functools
from .cache import cached


def func_logging(
    func: typing.Callable, logger_name: str = __name__, logger_level: int = logging.DEBUG
) -> typing.Callable:
    """
    装饰器：记录函数调用的日志。

    Args:
        func (Callable): 被装饰的函数。
        logger_name (str): 日志记录器的名字，默认为模块名。
        logger_level (int): 日志记录级别，默认为 logging.INFO。

    Returns:
        Callable: 包装后的函数。
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        return result

    return wrapper


def class_method_logger(
    cls_method: typing.Callable,
    logger_name: str = __name__,
    logger_level: int = logging.DEBUG,
) -> typing.Callable:
    """
    装饰器：记录类方法调用的日志。

    Args:
        cls_method (Callable): 被装饰的类方法。
        logger_name (str): 日志记录器的名字，默认为模块名。
        logger_level (int): 日志记录级别，默认为 logging.INFO。

    Returns:
        Callable: 包装后的类方法。
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    @functools.wraps(cls_method)
    def wrapper(self, *args, **kwargs):
        logger.debug(
            f"Calling method '{cls_method.__name__}' on {self.__class__.__name__}"
        )
        result = cls_method(self, *args, **kwargs)
        logger.debug(
            f"Method '{cls_method.__name__}' on {self.__class__.__name__} returned: {result}"
        )
        return result

    return wrapper
