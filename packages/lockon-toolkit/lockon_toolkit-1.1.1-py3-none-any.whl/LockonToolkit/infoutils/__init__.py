#!/opt/homebrew/anaconda3/envs/quantfin/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 下午4:51
# @Author  : @Zhenxi Zhang
# @File    : __init__.py.py
# @Software: PyCharm

import logging
from typing import Any, Dict, Optional
import colorlog
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import typing
from logging.handlers import RotatingFileHandler
import configparser


def setup_logger(
    log_file: str = "", name: typing.Optional[str] = __name__, level: int = logging.DEBUG
) -> logging.Logger:
    """设置日志记录器，并根据需要添加一个RotatingFileHandler来处理日志文件的滚动。

    Args:
        log_file (str, optional): 日志文件的路径。如果提供，则会添加一个RotatingFileHandler。
            Defaults to "".
        name (str, optional): 日志记录器的名字。如果为None，则默认使用根记录器。
            Defaults to None.
        level (int, optional): 日志记录级别。Defaults to logging.INFO.

    Returns:
        logging.Logger: 配置好的日志记录器对象。
    """
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if log_file:
        handler = RotatingFileHandler(
            log_file, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
        )
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def init_zlogger(
    logger_name: str,
    log_level: int,
    log_file_path: str = '',
    log_method: str = 'streamer',
    **kwargs: Any,
) -> logging.Logger:
    """
    初始化并配置一个日志记录器。

    Args:
        logger_name (str): 日志记录器名称。
        log_level (int): 日志级别，例如 logging.DEBUG, logging.INFO 等。
        log_file_path (str, optional): 日志文件路径。默认为空字符串，表示不写入文件。
        log_method (str, optional): 日志文件处理方法，可选值有 'streamer', 'time_rotation', 'rotation'。
            默认为 'streamer'。
        **kwargs: 其他关键字参数，用于配置特定的日志文件处理方法。

    Returns:
        logging.Logger: 配置好的日志记录器实例。

    Raises:
        ValueError: 如果 log_method 不是支持的方法之一。
        KeyError: 如果缺少某个必需的关键字参数。
    """
    _method_list = ['streamer', 'time_rotation', 'rotation']
    if log_method not in _method_list:
        raise ValueError(f'log_method 必须是 {_method_list} 中的一个')

    # 创建日志记录器
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # 设置日志格式
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        },
    )

    # 添加控制台处理器
    streamer = logging.StreamHandler()
    streamer.setFormatter(formatter)
    logger.addHandler(streamer)

    # 根据 log_method 添加文件处理器
    if log_file_path:
        if log_method == 'time_rotation':
            try:
                _when: str = kwargs['when']
                suffix: str = kwargs['suffix']
            except KeyError as e:
                raise KeyError('使用 time_rotation 方法时必须提供 when 和 suffix 参数') from e
            handler = TimedRotatingFileHandler(log_file_path, when=_when, encoding="utf-8")
            handler.suffix = suffix
        elif log_method == 'rotation':
            try:
                backup_count: int = kwargs['backup_count']
                max_bytes: int = kwargs['max_bytes']
            except KeyError as e:
                raise KeyError('使用 rotation 方法时必须提供 backup_count 和 max_bytes 参数') from e
            handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        else:
            handler = logging.FileHandler(log_file_path, encoding="utf-8")

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger




def read_config(config_file: str, encoding: str = "utf-8") -> configparser.ConfigParser:
    """读取配置文件，并处理可能发生的异常。

    Args:
        config_file (str): 配置文件的路径。
        encoding (str, optional): 配置文件的编码方式。Defaults to "utf-8".

    Returns:
        configparser.ConfigParser: 读取的配置文件内容。

    Raises:
        Exception: 如果读取配置文件失败，则抛出此异常。
    """
    config = configparser.ConfigParser()
    try:
        config.read(config_file, encoding=encoding)
    except Exception as e:
        raise Exception(f"读取配置文件 {config_file} 失败：{e}")
    return config
