import pyautogui

from log import Log
from typing import Optional
from utils.game_utils import GameUtil


class GameLauncher(GameUtil):
    def __init__(self, game_path: str, process_name: str, game_type: str, window_name: str, window_class: Optional[str],
                 log: Optional[Log] = None) -> None:
        super().__init__(game_path, process_name, game_type, window_name, window_class, log)
        self.screen_resolution = pyautogui.size()