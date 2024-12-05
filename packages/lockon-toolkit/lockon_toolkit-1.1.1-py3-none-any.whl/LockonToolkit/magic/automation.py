import cv2
import logging
import pandas as np
import subprocess
import mss
import time
from pywinauto import Application
logger = logging.getLogger(__name__)

def search_image(png_fp: str, target_fp: str, bar: float) -> list[tuple[int, int]]:
    """
    在目标图像中搜索模板图像的位置。

    Args:
        png_fp (str): 模板图像的文件路径。
        target_fp (str): 目标图像的文件路径。
        bar (float): 匹配阈值，范围在 0 到 1 之间。

    Returns:
        list[tuple[int, int]]: 匹配位置的列表，每个位置是一个 (x, y) 坐标元组。
    """
    # 读取目标图像和模板图像
    target_img = cv2.imread(target_fp)
    template_img = cv2.imread(png_fp)

    if target_img is None or template_img is None:
        raise "无法读取图像文件，请检查文件路径是否正确。"
        # return []

    # 将图像转换为灰度图像（模板匹配通常在灰度图像上进行）
    target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

    # 执行模板匹配
    result = cv2.matchTemplate(target_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    # logger.debug(f"执行模板匹配完成{png_fp},{target_fp}")

    # 设置阈值
    threshold = bar
    loc = np.where(result >= threshold)

    # 收集匹配位置
    _res = []
    for pt in zip(*loc[::-1]):
        _res.append(pt)

    # logger.debug(f"找到 {len(_res)} 个匹配位置")

    return _res


def restart_app(client_process_name,start_fp,only_shutdown: bool = False, suffix_wait_time: int = 10) -> None:
    """
    重启 CMClient 应用程序。

    Args:
        client_process_name: 需要重启的进程名称
        start_fp: 需要重启的程序的地址
        only_shutdown (bool): 是否仅关闭应用程序而不重新启动，默认为 False。
        suffix_wait_time (int): 重新启动后等待的时间（秒），默认为 10 秒。
    """
    try:
        # 获取当前运行的任务列表
        output = subprocess.check_output(["tasklist"], encoding="gbk")
        logger.debug("获取任务列表成功")

        # 检查 CMClient.exe 是否在运行
        if client_process_name in output:
            logger.debug(f"检测到 {client_process_name} 正在运行")
            try:
                # 关闭 CMClient.exe
                subprocess.run(["taskkill", "/F", "/IM", client_process_name], check=True)
                logger.info(f"成功关闭 {client_process_name}")
            except subprocess.CalledProcessError as e:
                logger.error(f"关闭 {client_process_name} 时发生错误: {e}")
            except Exception as e:
                logger.error(f"未知错误: {e}")
        else:
            logger.debug(f"未检测到 {client_process_name} 正在运行")

        # 如果不只关闭，则重新启动应用程序
        if not only_shutdown:
            logger.debug(f"开始重新启动 {client_process_name}")
            Application(backend="win32").start(
                start_fp
            )
            logger.info(f"{client_process_name} 重新启动成功")
            logger.info(f"等待 {suffix_wait_time} 秒后继续执行")
            time.sleep(suffix_wait_time)

    except Exception as e:
        logger.error(f"重启 {client_process_name} 时发生错误: {e}")

def screenshot_screens() -> list[str]:
    """
    截取多块屏幕的截图。

    Returns:
        list[str]: 包含三张截图文件名的列表。
    """
    png_list = []

    def capture_other_screens(_mon: dict, _monitor_number: int) -> None:
        """
        截取指定屏幕的截图。

        Args:
            _mon (dict): 屏幕信息字典。
            _monitor_number (int): 屏幕编号。
        """
        monitor = {
            "top": _mon["top"],
            "left": _mon["left"],
            "width": _mon["width"],
            "height": _mon["height"],
            "mon": _monitor_number,
        }
        output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

        # 截取屏幕数据
        sct_img = sct.grab(monitor)

        # 保存截图到文件
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        logger.debug(f"已保存屏幕 {_monitor_number} 的截图到 {output}")

        png_list.append(output)

    with mss.mss() as sct:
        # 截取主屏幕的截图
        filename = sct.shot(output="mon-{mon}.png")
        logger.debug(f"已保存主屏幕的截图到 {filename}")
        png_list.append(filename)

        # 截取其他屏幕的截图
        for monitor_number in range(2, 4):
            capture_other_screens(sct.monitors[monitor_number], monitor_number)

    return png_list