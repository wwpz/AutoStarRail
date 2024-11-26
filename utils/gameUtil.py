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
            self.log_error(f"启动 {self.window_name} 路径不存在：{self.game_path}")
            return False
        try:
            # 获取游戏文件夹路径
            self.log.debug(f"启动 {self.window_name} 路径为：{self.game_path}")
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

    def wait_time(self, timeout, print_interval=5):
        """等待指定时间，并每隔 print_interval 秒打印剩余时间。"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            remaining_time = int(end_time - time.time())  # 更新剩余时间
            if remaining_time % print_interval == 0:
                self.log_debug(f"剩余等待时间: {remaining_time} seconds")
            time.sleep(1)  # 添加一个延迟，以避免快速循环

    def wait_until(condition, timeout, period=1):
        """等待直到条件满足或超时"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if condition():
                return True
            time.sleep(period)
        return False

    def wait_until_retries(self, condition, period=5, retries=2):
        """
        等待直到条件满足或超时，最多重试retries次
        参数:
        condition: 函数，返回布尔值，表示条件是否满足
        timeout: 每次尝试的超时时间，单位为秒
        period: 每次检查条件之间的等待时间，单位为秒，默认为1秒
        retries: 最大重试次数，默认重试3次
        """
        for attempt in range(1, retries + 1):
            self.log.info(f"第 {attempt} 次尝试，共 {retries} 次")
            try:
                if condition():
                    self.log.debug("条件满足，操作成功。")
                    return True
            except Exception as e:
                self.log.debug(f"等待中出现异常，忽略异常: {e}")
            time.sleep(period)
            self.log.debug(f"第 {attempt} 次尝试失败，条件未满足。")

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
                self.log_debug("切换" + self.window_name + "至前台窗口时未找到应用")
                return False
            self.set_foreground_window_with_retry(hwnd)
            self.log_info(self.window_name + "窗口已切换到前台")
            time.sleep(2)
            return True
        except Exception as e:
            self.log_error(f"激活 {self.window_name} 窗口时发生错误：{e}")
            return False

    def check_resolution(self, target_width: int, target_height: int) -> None:
        """
        检查游戏窗口的分辨率是否匹配目标分辨率。

        如果游戏窗口的分辨率与目标分辨率不匹配，则记录错误并抛出异常。
        如果桌面分辨率小于目标分辨率，也会记录错误建议。

        参数:
            target_width (int): 目标分辨率的宽度。
            target_height (int): 目标分辨率的高度。
        """
        resolution = self.get_resolution()
        if not resolution:
            raise Exception("游戏分辨率获取失败")
        window_width, window_height = resolution

        screen_width, screen_height = self.screen_resolution
        if window_width != target_width or window_height != target_height:
            self.log_error(
                f"游戏分辨率: {window_width}x{window_height}，请在游戏设置内切换为 {target_width}x{target_height} 窗口或全屏运行")
            if screen_width < target_width or screen_height < target_height:
                self.log_error(
                    f"桌面分辨率: {screen_width}x{screen_height}，你可能需要更大的显示器或使用 HDMI/VGA 显卡欺骗器")
            raise Exception("游戏分辨率过低")
        else:
            self.log_debug(f"游戏分辨率: {window_width}x{window_height}")

    def check_resolution_ratio(self, target_width: int, target_height: int) -> None:
        """
        检查游戏窗口的分辨率和比例是否符合目标设置。

        如果游戏窗口的分辨率小于目标分辨率或比例不正确，则记录错误并抛出异常。
        如果桌面分辨率不符合最小推荐值，也会记录错误建议。

        参数:
            target_width (int): 目标分辨率的宽度。
            target_height (int): 目标分辨率的高度。
        """
        self.log.info("进入分辨率检测")
        resolution = self.get_resolution()
        if not resolution:
            raise Exception("游戏分辨率获取失败")
        window_width, window_height = resolution

        screen_width, screen_height = self.screen_resolution

        if window_width < target_width or window_height < target_height:
            self.log_error(
                f"游戏分辨率: {window_width}x{window_height} 请在游戏设置内切换为 {target_width}x{target_height} 窗口或全屏运行")
            if screen_width < 1920 or screen_height < 1080:
                self.log_error(
                    f"桌面分辨率: {screen_width}x{screen_height} 你可能需要更大的显示器或使用 HDMI/VGA 显卡欺骗器")
            raise Exception("游戏分辨率过低")
        elif abs(window_width / window_height - (target_width / target_height)) > 0.01:
            self.log_error(
                f"游戏分辨率: {window_width}x{window_height} 请在游戏设置内切换为 {target_width}:{target_height} 比例")
            raise Exception("游戏分辨率比例不正确")
        else:
            if window_width != target_width or window_height != target_height:
                self.log_warning(
                    f"游戏分辨率: {window_width}x{window_height} ≠ {target_width}x{target_height} 可能出现未预期的错误")
                time.sleep(2)
            else:
                self.log_debug(f"游戏分辨率: {window_width}x{window_height}")
            self.log_debug(f"桌面分辨率: {screen_width}x{screen_height}")

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

    def shutdown(self, action: Literal['Exit', 'Loop', 'Shutdown', 'Sleep', 'Hibernate', 'Restart', 'Logoff'], delay: int = 60) -> bool:
        """
        终止游戏并在指定的延迟后执行系统操作：关机、睡眠、休眠、重启、注销。

        参数:
            action: 要执行的系统操作。
            delay: 延迟时间，单位为秒，默认为60秒。

        返回:
            操作成功执行返回True，否则返回False。
        """
        self.stop_game()
        if action not in ["Shutdown", "Sleep", "Hibernate", "Restart", "Logoff"]:
            return True

        self.log_warning(f"将在{delay}秒后开始执行系统操作：{action}")
        time.sleep(delay)  # 暂停指定的秒数

        try:
            if action == 'Shutdown':
                os.system("shutdown /s /t 0")
            elif action == 'Sleep':
                # 必须先关闭休眠，否则下面的指令不会进入睡眠，而是优先休眠
                os.system("powercfg -h off")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                os.system("powercfg -h on")
            elif action == 'Hibernate':
                os.system("shutdown /h")
            elif action == 'Restart':
                os.system("shutdown /r")
            elif action == 'Logoff':
                os.system("shutdown /l")
            self.log_info(f"执行系统操作：{action}")
            return True
        except Exception as e:
            self.log_error(f"执行系统操作时发生错误：{action}, 错误：{e}")
            return False