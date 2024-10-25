import os
import time
import psutil
import ctypes
import win32gui
import subprocess
from core.log import Log
from typing import Literal, Tuple, Optional


class GameUtil:
    def __init__(self, game_path: str, process_name: str, game_type: str, window_name: str, window_class: Optional[str],
                 log: Optional[Log] = None) -> None:
        self.game_path = os.path.normpath(game_path)
        self.process_name = process_name
        self.game_type = game_type
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
        """启动"""
        if not os.path.exists(self.game_path):
            self.log_error(f"启动的 {self.window_name} 路径不存在：{self.game_path}")
            return False
        try:
            # 获取游戏文件夹路径
            self.log.debug(f"启动的 {self.window_name} 路径为：{self.game_path}")
            game_folder = os.path.dirname(self.game_path)

            # 尝试使用 subprocess.Popen
            process = subprocess.Popen(self.game_path, cwd=game_folder)
            self.log_info(f"启动 {self.window_name} 成功")
            return True
        except FileNotFoundError:
            self.log_error("cmd 不在用户环境变量中")
        except Exception as e:
            self.log_error(f"启动 {self.window_name} 时发生错误：{e}")
        return False

    def get_resolution(self) -> Optional[Tuple[int, int]]:
        """检查游戏窗口的分辨率"""
        try:
            hwnd = win32gui.FindWindow(self.window_class, self.window_name)
            if hwnd == 0:
                self.log_debug("游戏窗口未找到")
                return None
            _, _, window_width, window_height = win32gui.GetClientRect(hwnd)
            return window_width, window_height
        except IndexError:
            self.log_debug("游戏窗口未找到")
            return None

    @staticmethod
    def terminate_named_process(target_process_name, termination_timeout=10):
        """
        根据进程名终止属于当前用户的进程。

        参数:
        - target_process_name (str): 要终止的进程名。
        - termination_timeout (int, optional): 终止进程前等待的超时时间（秒）。

        返回值:
        - bool: 如果成功终止进程则返回True，否则返回False。
        """
        system_username = os.getlogin()  # 获取当前系统用户名
        # 遍历所有运行中的进程
        for process in psutil.process_iter(attrs=["pid", "name"]):
            # 检查当前进程名是否匹配并属于当前用户
            if target_process_name in process.info["name"]:
                process_username = process.username().split("\\")[-1]  # 从进程所有者中提取用户名
                if system_username == process_username:
                    proc_to_terminate = psutil.Process(process.info["pid"])
                    proc_to_terminate.terminate()  # 尝试终止进程
                    proc_to_terminate.wait(termination_timeout)  # 等待进程终止

    def stop_game(self) -> bool:
        """终止游戏"""
        try:
            # os.system(f'taskkill /f /im {self.process_name}')
            self.terminate_named_process(self.process_name)
            self.log_info(f"游戏终止：{self.process_name}")
            return True
        except Exception as e:
            self.log_error(f"终止游戏时发生错误：{e}")
            return False

    def switch_to_game(self) -> bool:
        """将游戏窗口切换到前台"""
        try:
            hwnd = win32gui.FindWindow(self.window_class, self.window_name)
            if hwnd == 0:
                self.log_debug(self.window_name + "窗口未找到")
                return False
            self.set_foreground_window_with_retry(hwnd)
            self.log_info(self.window_name + "窗口已切换到前台")
            return True
        except Exception as e:
            self.log_error(f"激活 {self.window_name} 窗口时发生错误：{e}")
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
