# -*- coding: utf-8 -*-

"""
模块初始化文件

@Time    : 2024/9/25 上午11:32
@Author  : @Zhenxi Zhang
@File    : __init__.py.py
@Software: PyCharm
"""

import datetime
import json
import pkgutil
import typing

import pandas as pd


# 加载股票交易日历数据
bytes_flow = pkgutil.get_data(__name__, "./trade_days_calendar/a_stock_calendar.json")
a_stock_calendar = pd.Series(json.loads(bytes_flow))
a_stock_calendar.index = pd.to_datetime(a_stock_calendar.index)
_a_stock_trading_days = set(a_stock_calendar.keys())
_start_date = a_stock_calendar.index[0]
_end_date = a_stock_calendar.index[-1]


def _check_in_drange(date: typing.Union[str, pd.Timestamp]) -> None:
    """
    检查给定日期是否在交易日范围内。

    参数:
      date (Union[str, pd.Timestamp]): 需要验证的日期，可以是字符串形式或pd.Timestamp类型。

    异常:
      ValueError: 如果提供的日期不在交易日范围内，则抛出此异常。
    """
    date_ts: pd.Timestamp = pd.to_datetime(date)

    if _start_date <= date_ts <= _end_date:
        return
    else:
        raise ValueError(f"{date} is not in the trading days range.")


def date2dtdate(
    date_input: typing.Union[str, pd.Timestamp, datetime.date]
) -> datetime.date:
    """
    将输入日期转换为 Pandas Timestamp 的日期部分。

    Args:
        date_input (Union[str, pd.Timestamp, datetime.date]): 输入日期，可以是字符串、Pandas Timestamp 或 datetime.date 类型。

    Returns:
        datetime.date: 转换后的日期部分。

    Examples:
        >>> date2dtdate('2023-01-01')
        Timestamp('2023-01-01 00:00:00')

        >>> date2dtdate(pd.Timestamp('2023-01-01'))
        Timestamp('2023-01-01 00:00:00')
    """
    dt64 = pd.to_datetime(date_input)
    return dt64.date()


def date2str(date_input: typing.Union[str, pd.Timestamp]) -> str:
    """
    将日期输入转换成字符串 YYYY-MM-DD 表示形式。

    Args:
        date_input (Union[str, pd.Timestamp]): 需要转换的日期输入。这可以是一个表示日期的字符串，或者是一个 Pandas Timestamp 对象。

    Returns:
        str: 日期的字符串表示形式。

    Examples:
        >>> date2str('2024-09-25')
        '2024-09-25'

        >>> date2str(pd.Timestamp('2024-09-25'))
        '2024-09-25'
    """
    dt64 = pd.to_datetime(date_input)
    return str(dt64.date())


def date2str_no_sep(date_input: typing.Union[str, pd.Timestamp]) -> str:
    """
    将日期输入转换成无分隔符的字符串表示形式。

    Args:
        date_input (Union[str, pd.Timestamp]): 需要转换的日期输入。这可以是一个表示日期的字符串，或者是一个 Pandas Timestamp 对象。

    Returns:
        str: 去掉日期分隔符（如短横线）的日期字符串。

    Examples:
        >>> date2str_no_sep('2024-09-25')
        '20240925'

        >>> date2str_no_sep(pd.Timestamp('2024-09-25'))
        '20240925'
    """
    dt64 = pd.to_datetime(date_input)
    return str(dt64.date()).replace("-", "")


def get_next_trade_date(
    date_input: typing.Union[str, pd.Timestamp, datetime.date]
) -> datetime.date:
    """
    获取输入日期的下一个交易日。

    Args:
        date_input (Union[str, pd.Timestamp, datetime.date]): 输入的日期，可以是字符串、Pandas Timestamp 或 datetime.date 类型。

    Returns:
        datetime.date: 输入日期之后的下一个交易日的日期。

    Examples:
        >>> get_next_trade_date('2024-09-25')
        datetime.date(2024, 9, 26)
    """
    date_dt64 = pd.to_datetime(date_input)
    _check_in_drange(date_dt64)

    while date_dt64 not in _a_stock_trading_days:
        date_dt64 += datetime.timedelta(days=1)
    # 如果输入日期已经是交易日，返回下一个交易日
    current_index = a_stock_calendar[str(date_dt64.date())]
    if current_index < len(a_stock_calendar) - 1:
        next_date_str = list(a_stock_calendar.keys())[current_index + 1]
        return date2dtdate(next_date_str)
    else:
        # 如果已经是最后一个交易日，返回当前日期
        return date2dtdate(str(date_dt64.date()))


def get_last_trade_date(
    date_input: typing.Union[str, pd.Timestamp, datetime.date]
) -> datetime.date:
    """
    获取输入日期的上一个交易日。

    Args:
        date_input (Union[str, pd.Timestamp, datetime.date]): 输入的日期，可以是字符串、Pandas Timestamp 或 datetime.date 类型。

    Returns:
        datetime.date: 输入日期之前的上一个交易日的日期。

    Examples:
        >>> get_last_trade_date('2024-09-25')
        datetime.date(2024, 9, 24)
    """
    date_dt64 = pd.to_datetime(date_input)
    _check_in_drange(date_dt64)
    while date_dt64 not in _a_stock_trading_days:
        date_dt64 -= datetime.timedelta(days=1)
    # 如果输入日期已经是交易日，返回上一个交易日
    current_index = a_stock_calendar[str(date_dt64.date())]
    if current_index > 0:
        prev_date_str = list(a_stock_calendar.keys())[current_index - 1]
        return date2dtdate(prev_date_str)
    else:
        # 如果已经是第一个交易日，返回当前日期
        return date2dtdate(str(date_dt64.date()))


def get_trade_days_series(
    start_date: typing.Union[str, pd.Timestamp], series_len: int
) -> typing.List[datetime.date]:
    """
    获取一系列连续的交易日。

    Args:
        start_date (Union[str, pd.Timestamp]): 开始日期，可以是字符串或 Pandas Timestamp 类型。
        series_len (int): 交易日序列的长度。

    Returns:
        List[datetime.date]: 包含一系列连续交易日的列表。

    Examples:
        >>> get_trade_days_series('2024-09-25', 5)
        [datetime.date(2024, 9, 26), datetime.date(2024, 9, 27), ...]
    """
    _check_in_drange(start_date)
    current_date = date2dtdate(start_date)
    trade_days = []
    for _ in range(series_len):
        current_date = get_next_trade_date(current_date)
        trade_days.append(current_date)
    return trade_days


def is_trade_date(date_input: typing.Union[str, pd.Timestamp, datetime.date]) -> bool:
    """
    判断给定日期是否为交易日。

    Args:
        date_input (Union[str, pd.Timestamp, datetime.date]): 需要判断的日期，可以是字符串、Pandas Timestamp 或 datetime.date 类型。

    Returns:
        bool: 如果给定日期是交易日则返回 True，否则返回 False。

    Examples:
        >>> is_trade_date('2024-09-25')
        True
    """
    date_dt64 = pd.to_datetime(date_input)
    return date_dt64 in a_stock_calendar.index


def get_trade_days_range(start_date: typing.Union[str, pd.Timestamp],
                         end_date: typing.Union[str, pd.Timestamp]) -> pd.Series:
    """
    获取两个日期之间的交易日列表。

    参数:
        start_date (Union[str, pd.Timestamp]): 开始日期，可以是字符串或pandas Timestamp类型。
        end_date (Union[str, pd.Timestamp]): 结束日期，可以是字符串或pandas Timestamp类型。

    返回:
        pd.Series: 在[start_date, end_date]范围内的交易日列表。

    注意:
        - 字符串格式的日期应该符合'%Y-%m-%d'格式。
        - start_date和end_date会被转换成datetime.date类型进行比较。
        - 该函数假设'a_stock_calendar'已经定义并且包含交易日信息。
    """
    # 假设a_stock_calendar已经被定义并且它有一个index属性，该属性是一个DatetimeIndex，
    # 其中包含了所有的交易日信息
    dt_series = pd.Series(a_stock_calendar.index)

    # 将开始和结束日期转换成pd.datetime64ns
    start_date_converted = pd.to_datetime(start_date)
    end_date_converted = pd.to_datetime(end_date)

    # 筛选出在指定日期范围内的交易日
    filtered_dates = dt_series[(dt_series >= start_date_converted) & (dt_series <= end_date_converted)]

    # 转换为datetime.date类型并返回
    return filtered_dates.dt.date
