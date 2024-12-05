#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 上午11:32
# @Author  : @Zhenxi Zhang
# @File    : __init__.py.py
# @Software: PyCharm

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("binary4fun")
except PackageNotFoundError:
    __version__ = "unknown version"
