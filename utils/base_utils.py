import time
import ctypes
import win32gui
import pyperclip
from log import Log
import pygetwindow as gw
from automation import auto
from utils.time_utils import TimeUtils

log = Log()


class BaseUtils:

    @staticmethod
    def get_window_geometry(window_title):
        window = gw.getWindowsWithTitle(window_title)
        if window:
            win = window[0]
            return win.left, win.top, win.width, win.height
        else:
            raise Exception(f"Window with title '{window_title}' not found.")

    @staticmethod
    # 复制文本到剪切板
    def copy_to_clipboard(text):
        pyperclip.copy(text)
        log.debug(f"已复制到剪切板: {text}")

    @staticmethod
    def paste(text):
        BaseUtils.copy_to_clipboard(text)
        if auto.find_element("./res/phone/basics/home_search1.png", is_global=True):
            auto.press_keys(['ctrl', 'v'])
            TimeUtils.wait_(1)

    @staticmethod
    def get_window_center(window_title):
        """
        通过窗口标题获取窗口中心点坐标.

        Args:
            window_title: 窗口标题，可以是精确的标题或包含标题的字符串.

        Returns:
            Tuple[int, int]: 窗口中心点的 x, y 坐标. 如果窗口未找到，返回 None.
        """
        try:
            window = gw.getWindowsWithTitle(window_title)[0]  # 获取匹配标题的窗口列表，取第一个
            if not window.isActive:  # 如果窗口未激活，则激活它
                window.activate()  # 激活窗口可以确保获取到正确的位置和大小信息，尤其是在多显示器环境下
            center_x = window.left + window.width // 2
            center_y = window.top + window.height // 2
            return center_x, center_y
        except IndexError:
            return None  # 没有找到窗口

    @staticmethod
    def get_window_borders():
        window_title = auto.window_title
        window = gw.getWindowsWithTitle(window_title)
        if window:
            win = window[0]
            left = win.left
            top = win.top
            right = win.left + win.width
            bottom = win.top + win.height
            return left, top, right, bottom
        else:
            raise Exception(f"Window with title '{window_title}' not found.")

    @staticmethod
    def get_window_class_from_title(window_title):
        """通过窗口标题获取窗口类名。"""

        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == window_title:
                ctx['class_name'] = win32gui.GetClassName(hwnd)
                return False  # 停止枚举
            return True

        ctx = {'class_name': None}
        win32gui.EnumWindows(winEnumHandler, ctx)
        return ctx['class_name']

    @staticmethod
    def switch_to_game(window_class, window_name) -> bool:
        """将游戏窗口切换到前台"""
        try:
            hwnd = win32gui.FindWindow(window_class, window_name)
            if hwnd == 0:
                log.debug("切换" + window_name + "至前台窗口时未找到应用")
                return False
            BaseUtils.set_foreground_window_with_retry(hwnd)
            log.info(window_name + "窗口已切换到前台")
            time.sleep(2)
            return True
        except Exception as e:
            log.error(f"激活 {window_name} 窗口时发生错误：{e}")
            return False

    @staticmethod
    def set_foreground_window_with_retry(hwnd):
        """尝试将窗口设置为前台，失败时先最小化再恢复。"""

        def toggle_window_state(hwnd, minimize=False):
            """最小化或恢复窗口。"""
            state = 6 if minimize else 9
            ctypes.windll.user32.ShowWindow(hwnd, state)

        toggle_window_state(hwnd, minimize=False)
        if ctypes.windll.user32.SetForegroundWindow(hwnd) == 0:
            toggle_window_state(hwnd, minimize=True)
            toggle_window_state(hwnd, minimize=False)
            if ctypes.windll.user32.SetForegroundWindow(hwnd) == 0:
                raise Exception("设置窗口前景失败")
