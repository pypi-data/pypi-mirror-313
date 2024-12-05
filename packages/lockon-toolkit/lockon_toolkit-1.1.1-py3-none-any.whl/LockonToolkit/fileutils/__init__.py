#!/opt/homebrew/anaconda3/envs/quantfin/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 下午3:47
# @Author  : @Zhenxi Zhang
# @File    : __init__.py.py
# @Software: PyCharm

import datetime
import os
import shutil
import typing


def get_fp_creation_time(fp: str) -> datetime.datetime:
    """获取文件或文件夹的创建时间。

    Args:
        fp: 文件或文件夹的路径。

    Returns:
        文件或文件夹的创建时间。

    Raises:
        ValueError: 如果提供的路径不存在，则抛出此异常。
    """
    if not os.path.exists(fp):
        raise ValueError("文件或文件夹路径不存在，请确认路径是否正确")

    creation_time = os.path.getctime(fp)
    dt_object = datetime.datetime.fromtimestamp(creation_time)

    return dt_object


def path2path(
    src_fp: os.PathLike,
    dst_fp: os.PathLike,
    operation: typing.Literal["COPY", "MOVE"],
    cpy_type: typing.Literal["replace", "append"] = "replace",
) -> str:
    """根据操作类型复制或移动文件/目录。

    Args:
        src_fp: 源文件或目录的路径。
        dst_fp: 目标文件或目录的路径。
        operation: 操作类型，可选值为 "COPY" 或 "MOVE"。
        cpy_type: 复制或移动类型，可选值为 "replace" 或 "append"。
            - "replace": 如果目标存在，则删除后再操作。
            - "append": 如果目标存在，则保留原文件/目录，不会覆盖。

    Returns:
        成功操作的消息。

    Raises:
        ValueError: 如果 `operation` 或 `cpy_type` 不是允许的选项之一，则抛出此异常。
    """
    src_fp_str = os.fspath(src_fp)
    dst_fp_str = os.fspath(dst_fp)

    operation_list = ["COPY", "MOVE"]
    if operation not in operation_list:
        raise ValueError(f"operation 必须是 {operation_list} 中的一个")

    if os.path.isdir(src_fp_str):
        fp_type = "DIR"
    else:
        fp_type = "FILE"

    if fp_type == "DIR":
        if operation == "COPY":
            return _copy_dir2path(src_fp_str, dst_fp_str, cpy_type)
        elif operation == "MOVE":
            return _move_dir2path(src_fp_str, dst_fp_str, cpy_type)
    elif fp_type == "FILE":
        if operation == "COPY":
            return _copy_file2path(src_fp_str, dst_fp_str, cpy_type)
        elif operation == "MOVE":
            return _move_file2path(src_fp_str, dst_fp_str, cpy_type)


def _copy_dir2path(
    src_dir_fp: os.PathLike,
    dst_dir_fp: os.PathLike,
    cpy_type: typing.Literal["replace", "append"] = "replace",
) -> str:
    """复制目录到指定路径。

    Args:
        src_dir_fp: 源目录的路径。
        dst_dir_fp: 目标目录的路径。
        cpy_type: 复制类型，可选值为 "replace" 或 "append"。
            - "replace": 如果目标目录存在，则删除后再复制。
            - "append": 如果目标目录存在，则保留原目录，不会覆盖。

    Returns:
        成功复制的消息。

    Raises:
        ValueError: 如果 `cpy_type` 不是允许的选项之一，则抛出此异常。
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_dir_fp):
        shutil.rmtree(dst_dir_fp)
    shutil.copytree(src_dir_fp, dst_dir_fp)
    return f"Successfully copied {src_dir_fp} to {dst_dir_fp}"


def _move_dir2path(
    src_dir_fp: os.PathLike,
    dst_dir_fp: os.PathLike,
    cpy_type: typing.Literal["replace", "append"] = "replace",
) -> str:
    """移动目录到指定路径。

    Args:
        src_dir_fp: 源目录的路径。
        dst_dir_fp: 目标目录的路径。
        cpy_type: 移动类型，可选值为 "replace" 或 "append"。
            - "replace": 如果目标目录存在，则删除后再移动。
            - "append": 如果目标目录存在，则保留原目录，不会覆盖。

    Returns:
        成功移动的消息。

    Raises:
        ValueError: 如果 `cpy_type` 不是允许的选项之一，则抛出此异常。
    """
    src_dir_fp_str = os.fspath(src_dir_fp)
    dst_dir_fp_str = os.fspath(dst_dir_fp)

    allowed_types = ["replace", "append"]
    if cpy_type not in allowed_types:
        raise ValueError(f"cpy_type 必须是 {allowed_types} 中的一个")

    if cpy_type == "replace" and os.path.exists(dst_dir_fp_str):
        shutil.rmtree(dst_dir_fp_str)

    shutil.move(src_dir_fp_str, dst_dir_fp_str)
    return f"成功将 {src_dir_fp_str} 移动到 {dst_dir_fp_str}"


def _move_file2path(
    src_fp: os.PathLike,
    dst_fp: os.PathLike,
    cpy_type: typing.Literal["replace", "append"] = "replace",
) -> str:
    """移动文件到指定路径。

    Args:
        src_fp: 源文件的路径。
        dst_fp: 目标文件的路径。
        cpy_type: 移动类型，可选值为 "replace" 或 "append"。
            - "replace": 如果目标文件存在，则删除后再移动。
            - "append": 如果目标文件存在，则保留原文件，不会覆盖。

    Returns:
        成功移动的消息。

    Raises:
        ValueError: 如果 `cpy_type` 不是允许的选项之一，则抛出此异常。
    """
    src_fp_str = os.fspath(src_fp)
    dst_fp_str = os.fspath(dst_fp)

    allowed_types = ["replace", "append"]
    if cpy_type not in allowed_types:
        raise ValueError(f"cpy_type 必须是 {allowed_types} 中的一个")

    if cpy_type == "replace" and os.path.exists(dst_fp_str):
        os.remove(dst_fp_str)

    shutil.move(src_fp_str, dst_fp_str)
    return f"成功将 {src_fp_str} 移动到 {dst_fp_str}"


def _copy_file2path(
    src_fp: os.PathLike,
    dst_fp: os.PathLike,
    cpy_type: typing.Literal["replace", "append"] = "replace",
) -> str:
    """复制文件到指定路径。

    Args:
        src_fp: 源文件的路径。
        dst_fp: 目标文件的路径。
        cpy_type: 复制类型，可选值为 "replace" 或 "append"。
            - "replace": 如果目标文件存在，则删除后再复制。
            - "append": 如果目标文件存在，则保留原文件，不会覆盖。

    Returns:
        成功复制的消息。

    Raises:
        ValueError: 如果 `cpy_type` 不是允许的选项之一，则抛出此异常。
    """
    src_fp_str = os.fspath(src_fp)
    dst_fp_str = os.fspath(dst_fp)

    allowed_types = ["replace", "append"]
    if cpy_type not in allowed_types:
        raise ValueError(f"cpy_type 必须是 {allowed_types} 中的一个")

    if cpy_type == "replace" and os.path.exists(dst_fp_str):
        os.remove(dst_fp_str)

    shutil.copy2(src_fp_str, dst_fp_str)

    return f"成功将 {src_fp_str} 复制到 to {dst_fp_str}"
