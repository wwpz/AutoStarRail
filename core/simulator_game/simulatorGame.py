import time
import pyautogui

from core.log import Log
from typing import Optional
from utils.gameUtil import GameUtil


class SimulatorGame(GameUtil):
    def __init__(self, game_path: str, process_name: str, game_type: str, window_name: str, window_class: Optional[str],
                 log: Optional[Log] = None) -> None:
        super().__init__(game_path, process_name, game_type, window_name, window_class, log)
        self.screen_resolution = pyautogui.size()

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
