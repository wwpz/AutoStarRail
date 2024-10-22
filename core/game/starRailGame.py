import pyautogui
from core.log import Log
from typing import Literal, Optional
from utils.starRailGameUtil import StarRailGameUtil

class StarRailGame(StarRailGameUtil):
    def __init__(self, game_path: str, process_name: str, window_name: str, window_class: Optional[str], log: Optional[Log] = None) -> None:
        super().__init__(game_path, process_name, window_name, window_class, log)
