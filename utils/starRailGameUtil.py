import os
import ctypes
import win32gui
import subprocess
from core.log import Log
from typing import Literal, Tuple, Optional


class StarRailGameUtil:
    def __init__(self, game_path: str, process_name: str, window_name: str, window_class: Optional[str],
                 log: Optional[Log] = None) -> None:
        self.game_path = os.path.normpath(game_path)
        self.process_name = process_name
        self.window_name = window_name
        self.window_class = window_class
        self.log = log

    def log_debug(self, message: str) -> None:
        """记录调试日志，如果log不为None"""
        if self.log is not None:
            self.log.debug(message)

    def log_info(self, message: str) -> None:
        """记录信息日志，如果log不为None"""
        if self.log is not None:
            self.log.info(message)

    def log_error(self, message: str) -> None:
        """记录错误日志，如果log不为None"""
        if self.log is not None:
            self.log.error(message)

    def log_warning(self, message: str) -> None:
        """记录警告日志，如果log不为None"""
        if self.log is not None:
            self.log.warning(message)

    def start_game(self) -> bool:
        """启动游戏"""
        if not os.path.exists(self.game_path):
            self.log_error(f"游戏路径不存在：{self.game_path}")
            return False
        try:
            # 获取游戏文件夹路径
            game_folder = os.path.dirname(self.game_path)

            # 尝试使用 subprocess.Popen
            process = subprocess.Popen(self.game_path, cwd=game_folder)
            self.log_info(f"游戏启动成功：{self.game_path}")
            return True
        except FileNotFoundError:
            self.log_error("cmd 不在用户环境变量中")
        except Exception as e:
            self.log_error(f"启动游戏时发生错误：{e}")
        return False

    def switch_to_game(self) -> bool:
        """将游戏窗口切换到前台"""
        try:
            hwnd = win32gui.FindWindow(self.window_class, self.window_name)
            if hwnd == 0:
                self.log_debug("游戏窗口未找到")
                return False
            self.set_foreground_window_with_retry(hwnd)
            self.log_info("游戏窗口已切换到前台")
            return True
        except Exception as e:
            self.log_error(f"激活游戏窗口时发生错误：{e}")
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
